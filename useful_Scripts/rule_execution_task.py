from copy import deepcopy

from xpms_lib_dag import utils
from xpms_lib_dag.constants import ExecType, Status, _globals, NotAvailableException
from xpms_lib_dag.tasks.task import Task
from xpms_rules.triggers.execute_ruleset import ExecuteRuleset
from xpms_rules.triggers.execute_rulesets import ExecuteRulesets
from xpms_common.mq_endpoint import MQMessage
from xpms_lib_dag.utils import serialize_content


class RuleExecutionTask(Task):

    def __init__(self, **kwargs):
        super(RuleExecutionTask, self).__init__(**kwargs)
        self.exec_type = ExecType.ASYNC.value

    def on_complete(self, outputs):
        self.status = Status.PROCESSED.value
        self.end_ts = utils.get_timestamp()
        for output in outputs:
            if isinstance(output, dict) and "_exception_" in output:
                if output["_type_"] == "xpms_lib_dag.constants.NotAvailableException":
                    self.status = Status.YIELDED.value
                else:
                    self.status = Status.FAILED.value
                    break
        self.outputs = outputs

    def preapre_req_msg(self, inputs, trigger, caching=False):
        mq_message = MQMessage()
        mq_message.message_type = "api"
        mq_message._from = "mqproxy"
        mq_message.solution_id = getattr(self, "solution_id")
        mq_message.trigger = trigger
        mq_message.request_id = self.config["context"]["request_id"]
        mq_message.data = inputs
        mq_message.data["request_type"] = self.config["service_name"]
        mq_message.state.update({
            "instance_id": self.instance_id,
            "execution_id": getattr(self, "execution_id"),
            "caching": caching})
        msg_dict = mq_message.to_json()
        return msg_dict

    def run(self, inputs, caching=False):
        response = {}
        trigger = self.config["trigger"]
        msg_dict = self.preapre_req_msg(inputs, trigger, caching=caching)
        context = self.config["context"]
        if trigger == "execute_ruleset":
            response = ExecuteRuleset(context, msg_dict).run()
        elif trigger == "execute_rulesets":
            response = ExecuteRulesets(context, msg_dict).run()
        return self, serialize_content([response])[0]

    def setup(self, mapped_inputs, caching=False):
        # creating mapped input object{ prev_task:prev_task_output}
        for k in list(mapped_inputs.keys()):
            mapped_inputs[k] = mapped_inputs[k][-1]

        if self.status == Status.PROCESSED.value or self.status == Status.FAILED.value:
            return

        # in case previous task is an exception, if all tasks are expected return None, else skip and remove the task input.
        for k in list(mapped_inputs.keys()):
            if (isinstance(mapped_inputs[k], dict) and "_exception_" in mapped_inputs[k]) or isinstance(
                    mapped_inputs[k], NotAvailableException):
                if self.config.get("dependencies", "any") == "any":
                    mapped_inputs.pop(k)
                else:
                    return

        if self.config.get("conditions"):
            eval_globals = deepcopy(_globals)
            for key, value in self.config["conditions"].items():
                condition_inputs = mapped_inputs.get(key, None)
                if condition_inputs is None:
                    continue
                eval_globals.update({"inputs": condition_inputs})
                eval_result = eval(value, eval_globals)
                if type(eval_result) == bool and not eval_result:
                    if self.config.get("dependencies", "any") == "any":
                        mapped_inputs.pop(key, None)
                    else:
                        return

        if not mapped_inputs:
            return

        if self.status == Status.PENDING.value:
            self.status = Status.PROCESSING.value
            self.start_ts = utils.get_timestamp()
            self.inputs = list(mapped_inputs.values())

            return self, list(mapped_inputs.values())

        elif self.status == Status.YIELDED.value:
            return self, [mapped_inputs[self.instance_id]]
