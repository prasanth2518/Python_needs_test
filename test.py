from copy import deepcopy

payload = {
    "log": "and",
    "rules": [
        {
            "json_path": "$.Claim.Header",
            "lval": "ActualPaidAmount",
            "op": "==",
            "rval": 1
        },
        {
            "json_path": "$.Claim.Header",
            "lval": "BillingZip",
            "op": "==",
            "rval": "NY"
        },
        {
            "log": "or",
            "rules": [
                {
                    "json_path": "$.Propensity.Edits",
                    "lval": "ModelScore",
                    "op": ">",
                    "rval": 0.6
                },
                {
                    "json_path": "$.Claim.Lines",
                    "lval": "LineNumber",
                    "op": "==",
                    "rval": 3
                }
            ]
        },
        {
            "log": "or",
            "rules": [
                {
                    "jaon_path": "Claim.Header",
                    "lval": "DxCode01",
                    "op": "contains",
                    "rval": "ICD"
                },
                {
                    "json_path": "$.Claim.Header",
                    "lval": "DxCode02",
                    "op": "in",
                    "rval": "corpus1"
                },
                {
                    "json_path": "$.Claim.Header",
                    "lval": "DxCode03",
                    "op": "in",
                    "rval": "corpus2"
                },
                {
                    "log": "and",
                    "rules": [
                        {
                            "jaon_path": "Claim.Header1",
                            "lval": "DxCode011",
                            "op": "contains",
                            "rval": "ICD"
                        }
                    ]
                }
            ]
        }
    ]
}


def modifiy_individual_rule(payload, updated_rules=None):
    if "rules" not in payload:
        print(payload)
        raise ("rules not found in input payload")
    if len(payload["rules"]) == 1:
        return payload["rules"]
    modified_rule = deepcopy(payload["rules"])
    updated_rules = updated_rules if updated_rules else []
    if "log" in payload:
        for each_rule in payload['rules']:
            if each_rule != payload["rules"][-1]:
                modified_rule.insert(modified_rule.index(each_rule) + 1, {"log": payload["log"]})
        for _each_mod_rule in modified_rule:
            if "rules" not in _each_mod_rule:
                updated_rules.append(_each_mod_rule)
                continue
            _mod_rule = modifiy_individual_rule(_each_mod_rule)
            updated_rules.append(_mod_rule)
        return modified_rule, updated_rules


modified_rule, updated_rules = modifiy_individual_rule(payload, updated_rules=None)
print([updated_rules])
