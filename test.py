K = {

    "rule_name": "new_Str_rule_test",
    "start_date": "2022-01-01",
    "end_date": "2022-04-28",
    "rule_scope": {
        "conceptId": "B45",
        "clientId": "ANTHM"
    },
    "description": "Check if provider exclusion",
    "scope": {
        "type": "custom",
        "sub-scope": "",
        "options": {
            "page_num": ""
        }
    },
    "conditions": [
        {
            "log": "and",
            "conditions": [
                {
                    "json_path": "$.claim_header",
                    "lval": "KEY_CHK_DCN_NBR",
                    "op": "==",
                    "rval": "22011BL3390"
                },
                {
                    "json_path": "$.claim_header",
                    "lval": "PROV_SPCLTY_CD",
                    "op": "==",
                    "rval": "200"
                },
                {
                    "log": "or",
                    "conditions": [
                        {
                            "json_path": "$.claim_header",
                            "lval": "ICD_A_CD",
                            "op": "==",
                            "rval": "J3081"
                        },
                        {
                            "json_path": "$.claim_detail",
                            "lval": "DTL_LINE_NBR",
                            "op": "==",
                            "rval": "01"
                        },
                        {
                            "log": "and",
                            "conditions": [
                                {
                                    "json_path": "$.claim_header",
                                    "lval": "ICD_A_CD",
                                    "op": "==",
                                    "rval": "J3081"
                                },
                                {
                                    "json_path": "$.claim_detail",
                                    "lval": "DTL_LINE_NBR",
                                    "op": "==",
                                    "rval": "01"
                                },

                            ]
                        },

                    ]
                },
                {
                    "json_path": "$.claim_detail",
                    "lval": "provider_num",
                    "op": "==",
                    "rval": "a"
                }
            ]
        }
    ],
    "actions": [
        {
            "json_path": "$.claim_detail",
            "op": "create_attribute",
            "lval": "provider_result",
            "rval": True,
            "action_type": "custom"
        }
    ],
    "solution_id": "testdb1",
    "rule_id": "f1592251-8a3b-42ea-be17-c5c45eaf181d_test_new_str",
    "is_deleted": False,
    "created_ts": "2022-03-11 08:17:17.670570"
}

inp = {
    "ruleset_id": "timber-1_test",
    "above_peer_ratio": 0.9,
    "claim_header": [
        {
            "KEY_CHK_DCN_NBR": "22011BL3390",
            "KEY_CHK_DCN_ITEM_CD": "80",
            "clm_from_dt": "01/06/2022",
            "clm_to_dt": "01/06/2022",
            "PROV_SPCLTY_CD": "200",
            "ICD_A_CD": "J3081",
            "ICD_B_CD": "J301",
            "PROV_TAX_ID": "271620575",
            "BILLG_NPI": "1104157114",
            "BILLG_TXNMY_CD": "207KA0200X",
            "RNDRG_TXNMY_CD": "193400000X",
            "NAT_EA2_RNDR_NPI": "1023095411",
            "PRICNG_ZIP_STATE": "VA",
            "ERROR_CDS": ["NCN", "TRT", "BRT"]}
    ],
    "claim_detail": [
        {
            "DTL_LINE_NBR": "01",
            "Revenue_code": None,
            "HCFA_PT_CD": "11",
            "PROC_MDFR_CD": "95",
            "provider_num": "a",
            "PROC_CD": "99204",
            "MDFR_CD_1": None,
            "MDFR_CD_2": None,
            "MDFR_CD_3": None,
            "KEY_CHK_DCN_NBR": "22011BL3390",
            "KEY_CHK_DCN_ITEM_CD": "80"
        }
    ]
}

from copy import deepcopy
from jsonpath_ng import parse
from xpms_storage.db_handler import DBProvider
from datetime import datetime

RULES_PRIMARY_KEYS = []

LIST_OPERATORS = ["any", "not_any", "any_startswith", "not_any_startswith"]
VALID_OPERATORS = ["==", ">", "<", "!=", ">=", "<=", "contains", "regex", "in", "notin"] + LIST_OPERATORS


def get_modified_filter_obj(filter_obj, payload):
    if RULES_PRIMARY_KEYS:
        for primary_key in RULES_PRIMARY_KEYS:
            if primary_key in payload:
                filter_obj[primary_key] = payload[primary_key]
    return filter_obj


def modifiy_individual_rule(payload, updated_rules=None):
    if "conditions" not in payload:
        print(payload)
        raise Exception("conditions not found in input payload")
    if len(payload["conditions"]) == 1:
        return payload["conditions"][0]
    modified_rule = deepcopy(payload["conditions"])
    updated_rules = updated_rules if updated_rules else []
    if "log" in payload:
        for each_rule in payload["conditions"]:
            if each_rule != payload["conditions"][-1]:
                modified_rule.insert(modified_rule.index(each_rule) + 1, {"log": payload["log"]})
        for _each_mod_rule in modified_rule:
            if "conditions" not in _each_mod_rule:
                updated_rules.append(_each_mod_rule)
                continue
            _mod_rule = modifiy_individual_rule(_each_mod_rule)
            updated_rules.append(_mod_rule)
        return updated_rules


def get_modified_rules(_rule_json):
    conditions = _rule_json["conditions"][0]
    updated_rules = modifiy_individual_rule(conditions)
    if not isinstance(updated_rules, list):
        updated_rules = [updated_rules]
    _rule_json["conditions"] = updated_rules
    return _rule_json


def get_json_path_Val(json_path, inp):
    jsonpath_expression = parse(json_path)
    jsonpath_match = jsonpath_expression.find(inp)
    matched_list = jsonpath_match[0].value
    return matched_list


def get_result(_json_val, operator, lval, rval, json_path, matches=None):
    if operator not in VALID_OPERATORS:
        raise Exception(f"{operator}  is not a valid operator")
    json_value = deepcopy(_json_val)
    if not isinstance(_json_val, list):
        _json_val = [_json_val]
    result = None
    for json_val in _json_val:
        if operator == "==":
            result = json_val[lval] == rval
        elif operator == "!=":
            result = json_val[lval] != rval
        elif operator == "in":
            result = json_val[lval] in rval
        elif operator == "notin":
            result = json_val[lval] not in rval
        elif operator == ">":
            result = json_val[lval] > rval
        elif operator == ">=":
            result = json_val[lval] >= rval
        elif operator == "<":
            result = json_val[lval] < rval
        elif operator == "<=":
            result = json_val[lval] <= rval
        elif operator in LIST_OPERATORS:
            if not isinstance(json_val[lval], list):
                json_val[lval] = [json_val[lval]]

            if operator == "startswith":
                result = True if [True for _each_item in json_val[lval] for each_item in rval if
                                  _each_item.startswith(each_item)] else False
            elif operator == "notstartswith":
                result = False if [True for _each_item in json_val[lval] for each_item in rval if
                                   _each_item.startswith(each_item)] else True

            elif operator == "any":
                result = True if [True for _each_item in json_val[lval] if
                                  _each_item in rval] else False

            elif operator == "notany":
                result = False if [True for _each_item in json_val[lval] if
                                   _each_item in rval] else True

        if result:
            if isinstance(json_value, list):
                if matches:
                    if json_path in matches and json_val not in matches[json_path]:
                        matches[json_path].extend([json_val])
                        return result, matches
                return result, {json_path: [json_val]}
            return result, {json_path: json_val}

        elif not result and json_val == _json_val[-1]:
            return result, {}
        else:
            continue


def exec_Cond(conditon, inp, solution_id, matches=None):
    if "json_path" not in conditon:
        raise Exception("json_path is not found")
    json_val = get_json_path_Val(conditon["json_path"], inp)
    if not conditon.get("op"):
        raise Exception("operator not found")
    if "operate_on" in conditon and conditon["operate_on"]:
        db_conn = DBProvider.get_instance(db_name=solution_id)
        filter_obj = {"corpus_name": conditon["rval"], "corpus_type": "corpus"}
        filter_obj = get_modified_filter_obj(filter_obj, inp)
        corpus_data = db_conn.find(table="rules_corpus", filter_obj=filter_obj,
                                   multi_select=False)
        if not corpus_data:
            raise Exception("no corpous data found for {} ".format(conditon["rval"]))
        return get_result(json_val, conditon["op"], conditon["lval"], conditon["rval"],
                          conditon["json_path"], matches=matches)
    return get_result(json_val, conditon["op"], conditon["lval"], conditon["rval"],
                      conditon["json_path"], matches=matches)


def create_Conditional_str(conditions, solution_id, main_cond_Str=None, matches=None):
    matches = matches if matches else {}
    main_cond_Str = main_cond_Str if main_cond_Str else ""
    for cond in conditions:
        cond_str = ""
        if isinstance(cond, dict):
            if "log" in cond:
                cond_str = cond_str + " " + cond["log"]
            else:
                result, _matches = exec_Cond(cond, inp, solution_id, matches=matches)
                matches.update(_matches)
                cond_str = cond_str + " " + str(result)
            main_cond_Str = main_cond_Str + cond_str

        elif isinstance(cond, list):
            main_cond_Str = main_cond_Str + " " + "("
            main_cond_Str, matches = create_Conditional_str(cond, solution_id, main_cond_Str=main_cond_Str,
                                                            matches=matches)
            main_cond_Str = main_cond_Str + " " + ")"

    return main_cond_Str, matches


st1 = datetime.utcnow()
_rule_json = get_modified_rules(K)
print((datetime.utcnow() - st1).total_seconds())
solution_id = "testdb1"

st = datetime.utcnow()
print(create_Conditional_str(_rule_json["conditions"], solution_id))

print((datetime.utcnow() - st).total_seconds())
l = [1, 2, 3, 4, 5, 6]

m = [22, 0, 7, 8, 9]
# sw
# result = True if [True for _each_item in l for each_item in m if
#                                   _each_item.startswith(each_item)] else False
# nsw
# result = False if [True for _each_item in l for each_item in m if
#                                    _each_item.startswith(each_item)] else True

# any
result = True if [True for _each_item in l if
                  _each_item in m] else False
print(result)

# not any
result = False if [True for _each_item in l if
                   _each_item in m] else True

print(result)
from xpms_common.redis_handler import RedisHandler
from xpms_storage.db_handler import DBProvider

cache_handle = RedisHandler()
#
# # for i in range(10):
# #     cache_key = "claimsol3_timnber_rules_test{}_ruleset".format(str(i))
# #     cache_handle.set(cache_key, [{"rule":"rule"+str(i)}])
# #     print("claimsol3_timnber_rules_test{}_ruleset".format(str(i)))
#
# for i in range(10):
#     cache_key = "claimsol3_timnber_rules_test{}_ruleset".format(str(i))
#     result = cache_handle.get_json_value(key=cache_key)
#     # print(result)
#
# # res = cache_handle.get_matching_keys(key_starts_with='claimsol3_timnber_rules_*')
# # print(res)
# some_list = [1, 2, 3, 4, 5, 6]
# for item in some_list:
#     if item < 4:
#         some_list.remove(item)
# print (some_list)
#
# some_numbers = [5, 4, 3, 2, 1]
# some_numbers.sort()
# print(some_numbers)

import datetime

db = DBProvider.get_instance(db_name="testdb1")
exec_ids_lst = []
# for task_id in ["cffbede2-6e93-4b5a-9a0c-b1595d44421d","3700326d-f47a-49ce-a426-6140d1530519"]:
# for task_id in ["87864f83-2555-48bf-9962-06eb539ea3f7"]:
for task_id in ["3700326d-f47a-49ce-a426-6140d1530519"]:
    # data = db.find(table="dag_task_executions",filter_obj={"task_id":"cffbede2-6e93-4b5a-9a0c-b1595d44421d"},columns = {"include":["task_id","execution_id"]},sort = [{"key": "update_ts", "order": "dsc"}],limit=10)
    data = db.find(table="dag_task_executions", filter_obj={"task_id": task_id},
                   columns={"include": ["task_id", "execution_id"]}, sort=[{"key": "update_ts", "order": "dsc"}],
                   limit=10)

    exec_list = [exec_Data["execution_id"] for exec_Data in data]

    lst_mean_time = []
    for exec_id in exec_list:

        sort = [{"key": "start_ts", "order": "dsc"}]
        if task_id in ["cffbede2-6e93-4b5a-9a0c-b1595d44421d"]:
            res = db.find(table="dag_task_instances", filter_obj={"execution_id": exec_id, "name": "Invoke Rule Task"},
                          sort=sort)
        else:
            res = db.find(table="dag_task_instances",
                          filter_obj={"execution_id": exec_id, "name": "Invoke Rule Task DAG"},
                          sort=sort)
        # res = db.find(table="dag_task_instances", filter_obj={"execution_id": exec_id},
        #               sort=sort)
        print("last", res[0]["end_ts"])
        print("first", res[0]["start_ts"])
        t2_d = datetime.datetime.strptime(res[0]["end_ts"], '%Y-%m-%d %H:%M:%S.%f')
        t1_d = datetime.datetime.strptime(res[0]["start_ts"], '%Y-%m-%d %H:%M:%S.%f')
        # t1_d = datetime.datetime.strptime(res[0]["end_ts"], '%Y-%m-%d %H:%M:%S.%f')
        # try:
        #     t2_d = datetime.datetime.strptime(res[-1]["start_ts"], '%Y-%m-%d %H:%M:%S.%f')

        lst_mean_time.append((t2_d - t1_d).total_seconds())
        print(f"total_time for {exec_id}  {(t2_d - t1_d).total_seconds()}")

    print(f"mean_time {task_id} --> {sum(lst_mean_time) / 10}")


def delete_cache(solution_id, remove_ruleset_cache=None, remove_corpous_cache=None, cache_keys=None):
    cache_handle = RedisHandler()
    if remove_ruleset_cache:
        cache_str = f"{solution_id}_rules_*"
        cache_keys = cache_handle.get_matching_keys(key_starts_with=cache_str)
    if remove_corpous_cache:
        cache_str = f"{solution_id}_corpus_*"
        cache_keys = cache_handle.get_matching_keys(key_starts_with=cache_str)
    cache_handle.delete_keys(cache_keys)
    return True


# delete_cache("testdb1",remove_ruleset_cache=True)

from bounded_pool_executor import BoundedProcessPoolExecutor
from time import sleep
from random import randint


def do_job(num):
    sleep_sec = randint(1, 10)
    print('value: %d, sleep: %d sec.' % (num, sleep_sec))
    sleep(sleep_sec)


# with BoundedProcessPoolExecutor(max_workers=5) as worker:
#     for num in range(10000):
#         print('#%d Worker initialization' % num)
#         worker.submit(do_job, num)

# Str='is2 thi1s babu3'
# str_lst  = [ i.replace(j,"") for i in Str.split()  for j in "123456789" if j in i]
# new_list = []
# for i in str_lst:
#     if i.lower() == "this":
#         new_list.insert(0,i)
#     elif i.lower() == "is":
#         new_list.insert(1,i)
#     elif i.lower() == "babu":
#         new_list.insert(2,i)
# print(" ".join(new_list))


