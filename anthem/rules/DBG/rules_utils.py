from xpms_storage.db_handler import DBProvider


def get_rules(rules, solution_id):
    db_conn = DBProvider.get_instance(db_name=solution_id)
    all_rules = []
    for _rule in rules:
        all_rules.extend(
            db_conn.find(table='rules', filter_obj={"rule_id": _rule, "solution_id": solution_id, "is_deleted": False}))
    return all_rules


def get_cond_sql_string(cond):
    if "op" not in cond and "log" in cond:
        return cond["log"]
    if isinstance(cond, dict):
        pass
        # cond = Condition(**cond)
    if not cond["operator"] and cond.get('log'):
        return cond.get("log")
    if cond["operator"] in [">", "<", "!=", ">=", "<=", "in", "==", "contains", "notin", "in"]:
        operater = cond["operator"]
        rvalue = cond["rvalue"]
        if cond["operator"] == "==":
            operater = "="
        elif cond["operator"] == "contains":
            operater = "like %"
            rvalue = rvalue + "%"
        elif cond["operator"] in ["in", "notin"]:
            if cond["operator"] == "notin":
                operater = "not in"
            if cond.get("operate_on") == "corpus" and "." in rvalue:
                table_name, col_name = rvalue.rsplit(".", 1)
                rvalue = "(select {} from {} )".format(col_name, table_name)
        if isinstance(rvalue, str):
            query_string = "{} {} '{}'".format(cond["lvalue"], operater, rvalue)
        else:
            query_string = "{} {} {}".format(cond["lvalue"], operater, rvalue)
    else:
        raise Exception("Operator {} is not supported ".format(cond["operator"]))
    return query_string


def get_sql_string(conditions, rule_query_string=""):
    if isinstance(conditions, dict):
        cond_query_string = get_cond_sql_string(conditions)
        rule_query_string = rule_query_string + " " + cond_query_string
    elif isinstance(conditions, list):
        rule_query_string = rule_query_string + "("
        for cond in conditions:
            rule_query_string = get_sql_string(cond, rule_query_string)
        rule_query_string = rule_query_string + ")"
    return rule_query_string


def get_update_queries(rules, output_table=None):
    query_sets = []
    rules_logs = []
    for rule in rules:
        # rule = Rule(r)
        if rule["is_active"]:
            if rule["rule_scope"]:
                rule["conditions"] = [rule["conditions"]]
                for k, v in rule["rule_scope"].items():
                    rule["conditions"].append({"log": "and"})
                    rule["conditions"].append({"lval": k, "rval": v, "op": "==", "json_path": ""})
            cond_str = get_sql_string(rule["conditions"])
            update_str = ""
            if rule["actions"]:
                for act in rule["actions"]:
                    # act_obj = Action(**act)
                    if act["rvalue"] == "rule_id":
                        rvalue = rule["rule_id"]
                    elif act["rvalue"] == "rule_name":
                        rvalue = rule["rule_name"]
                    else:
                        rvalue = act["rvalue"]
                    if isinstance(rvalue, str):
                        upd_query = "{} = '{}'".format(act["lvalue"], rvalue)
                    else:
                        upd_query = "{} = {}".format(act["lvalue"], rvalue)
                    if update_str:
                        update_str = update_str + " , "
                    update_str = update_str + upd_query
            final_update_str = "update " + output_table + " set " + update_str + " where " + cond_str + ";"
            rules_logs.append({"rule_id": rule["rule_id"], "rule_name": rule["rule_name"],
                               "condition_clause": cond_str, "update_clause": update_str})
            query_sets.append({"query": final_update_str, "query_name": rule["rule_name"]})
    return query_sets, rules_logs
