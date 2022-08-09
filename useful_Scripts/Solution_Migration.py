"""
Import Modules
"""
import requests
from xpms_storage.db_handler import DBProvider
import json
from cryptography.fernet import Fernet
import os
from xpms_file_storage.file_handler import XpmsResource, LocalResource

""" STEP:1 --->    Add solution name in solutions collection of adminDB """

# Connecting to Admin Database
db = DBProvider.get_instance(db_name="cognitive-platform_admin")

soln = {"is_elasticsearch": False, "updated_ts": "2021-08-26T06:44:25.214143", "is_nifi_enabled": False,
        "solution_type": "automation", "created_ts": "2021-08-26T06:44:25.214143", "description": "",
        "solution_id": "claimsol9", "is_deleted": False, "hocr_type": "XPMS", "solution_name": "DNA_SOLUTION"}
db.insert(table="solutions", rows=[soln])
user_data = db.find(table="users", filter_obj={"userName": "nurse_se"}, multi_select=False)
user_data['solutions'].append({"id": "claimsol7", "name": "DNA_SOLUTION"})
db.update(table="users", filter_obj={"userName": "nurse_se"}, update_obj=user_data)

print("sol_db_usr_config_Added")

""" STEP:2 --->    Solution Creation intilaization """

payload = {
    "data": {
        "configuration": None,
        "is_elasticsearch": False,
        "git_cred_details": {
            "url_type": "https",
            "user_name": "srcccpcogplatpr",
            "password": "!@992LetmE",
            "git_repo_url": "https://bitbucket.anthem.com/scm/~ag82357/cognitive-platform-claimsol2.git",
            "branch": "refs/heads/sit"
        }
    },
    "solution_id": "claimsol7"
}
# posting request for intilize the solution creation
url = "https://mq-proxy-cognitive-platform-sit.apps.ent-ocp4-np1-har.antmdc.internal.das/solution/create"
requests.post(url, data=json.dumps(payload), verify=False)

print("Solution_Creation intilization Done")

""" STEP:3 --->    Git Repo Configure to the solution """

# api_url = "https://mq-proxy-cognitive-platform-perf.apps.ent-ocp4-np2-har.antmdc.internal.das/add_git_credentials"
api_url = "https://mq-proxy-cognitive-platform-sit.apps.ent-ocp4-np1-har.antmdc.internal.das/add_git_credentials"
headers = {'Content-Type': 'application/json'}
solution_id = "claimsol7"
git_cred_details = {
    "url_type": "https",
    "user_name": "srcccpcogplatpr",
    "password": "!@992LetmE",
    "git_repo_url": "https://bitbucket.anthem.com/scm/~ag82357/cognitive-platform-claimsol2.git",
    "branch": "refs/heads/sit"
}


def hash_git_password(git_cred_details):
    text_password = str(git_cred_details["password"])
    key = Fernet.generate_key()
    fernet_object = Fernet(key)
    encrypted_password = fernet_object.encrypt(text_password.encode())
    git_cred_details.update({"password": encrypted_password.decode(), "hash_key": key.decode()})


hash_git_password(git_cred_details)

# db = DBProvider.get_instance(db_name="system")
# db.update(table="pm_solution",filter_obj={"solution_id":solution_id},update_obj={"git_cred_details":git_cred_details,"is_git_enabled":True})
payload = {"data": git_cred_details, "solution_id": solution_id}
a = requests.post(api_url, data=json.dumps(payload), headers=headers, verify=False)
print(a)

""" STEP:4 --->    Import Normal functions """

manifest_func = [
    {
        "function_name": "DCN_CM_generate_mdl_input",
        "function_file_path": "DNA_CM/DCN_CM_generate_mdl_input.py"
    },
    {
        "function_name": "dna_check_for_medrecs",
        "function_file_path": "DNA_CM/dna_check_for_medrecs.py"
    },
    {
        "function_name": "dna_cm_post_process",
        "function_file_path": "DNA_CM/dna_cm_post_process.py"
    },
    {
        "function_name": "dna_cm_prepare_input",
        "function_file_path": "DNA_CM/dna_cm_prepare_input.py"
    },
    {
        "function_name": "dna_cm_validate",
        "function_file_path": "DNA_CM/dna_cm_validate.py"
    },
    {
        "function_name": "get_eligible_policies",
        "function_file_path": "DNA_CM/get_eligible_policies.py"
    },
    {
        "function_name": "save_auth_dna",
        "function_file_path": "DNA_CM/save_auth_dna.py",
        "function_config_path": "config/save_auth_dna.json"
    },
    {
        "function_name": "prepare_smartum_v3_payload",
        "function_file_path": "DNA_CM/prepare_smartum_v3_payload.py"
    },
    {
        "function_name": "prepare_umidal_payload",
        "function_file_path": "DNA_CM/prepare_umidal_payload.py"
    },
    {
        "function_name": "dna_claims_prepare_input",
        "function_file_path": "DNA_Claims/dna_claims_prepare_input.py"
    },
    {
        "function_name": "dna_generate_model_input",
        "function_file_path": "DNA_Claims/dna_generate_model_input.py"
    },
    {
        "function_name": "dna_post_process",
        "function_file_path": "DNA_Claims/dna_post_process.py"
    },
    {
        "function_name": "DNA_Validate_claim",
        "function_file_path": "DNA_Claims/DNA_Validate_claim.py"
    },
    {
        "function_name": "get_dna_claims_eligible_policies",
        "function_file_path": "DNA_Claims/get_dna_claims_eligible_policies.py"
    },
    {
        "function_name": "save_claim_dna",
        "function_file_path": "DNA_Claims/save_claim_dna.py"
    },
    {
        "function_name": "dna_consolidate_results",
        "function_file_path": "common_functions/dna_consolidate_results.py"
    },
    {
        "function_name": "prepare_payload",
        "function_file_path": "common_functions/prepare_payload.py"
    },
    {
        "function_name": "route_response",
        "function_file_path": "common_functions/route_response.py"
    },
    {
        "function_name": "prepare_nextgen_payload",
        "function_file_path": "common_functions/prepare_nextgen_payload.py"
    },
    {
        "function_name": "remove_model_metadata",
        "function_file_path": "common_functions/remove_model_metadata.py"
    },
    {
        "function_name": "tf_validate",
        "function_file_path": "Timely_filing/tf_validate.py"
    },
    {
        "function_name": "save_tf",
        "function_file_path": "Timely_filing/save_tf.py",
        "function_config_path": "config/save_tf.json"
    },
    {
        "function_name": "tf_prepare_input",
        "function_file_path": "Timely_filing/tf_prepare_input.py"
    },
    {
        "function_name": "tf_create_filesystem_payload",
        "function_file_path": "Timely_filing/tf_create_filesystem_payload.py"
    },
    {
        "function_name": "tf_generate_model_input",
        "function_file_path": "Timely_filing/tf_generate_model_input.py"
    },

    {
        "function_name": "tf_post_process",
        "function_file_path": "Timely_filing/tf_post_process.py"
    },
    {
        "function_name": "pre_process_save_claim_dna",
        "function_file_path": "DNA_Claims/pre_process_save_claim_dna.py"
    },
    {
        "function_name": "gna_cm_validate",
        "function_file_path": "GNA/gna_cm_validate.py"
    },
    {
        "function_name": "gna_cm_prepare_input",
        "function_file_path": "GNA/gna_cm_prepare_input.py"
    },
    {
        "function_name": "gna_get_eligible_policies",
        "function_file_path": "GNA/gna_get_eligible_policies.py"
    },
    {
        "function_name": "gna_DCN_CM_generate_mdl_input",
        "function_file_path": "GNA/gna_DCN_CM_generate_mdl_input.py"
    },
    {
        "function_name": "gna_cm_post_process",
        "function_file_path": "GNA/gna_cm_post_process.py"
    },
    {
        "function_name": "gna_check_for_medrecs",
        "function_file_path": "GNA/gna_check_for_medrecs.py"
    },
    {
        "function_name": "save_auth_gna",
        "function_file_path": "GNA/save_auth_gna.py",
        "function_config_path": "config/save_auth_gna.json"
    },
    {
        "function_name": "gna_check_for_medrecs",
        "function_file_path": "GNA/gna_check_for_medrecs.py"
    },
]
url = "https://mq-proxy-cognitive-platform.apps.ent-ocp4-prod-ric.antmdc.internal.das/import_git_function"
payload = {"data": {}, "solution_id": "claimsol7", "solution_group": "sync"}
for func in manifest_func:
    print(func["function_name"])
    data = {"function_name": func["function_name"], "function_path": func["function_file_path"],
            "category": "NLP", "solution_id": "claimsol7"}
    payload["data"] = data
    resp = requests.post(url, json.dumps(payload), verify=False)
    print(resp.text)
    # print(func, "import posted")
print("all done")

""" STEP:5 --->    Import Model functions """

solution_id = "claimsol2"
ml_functions = ['tf_model', 'GNA_Model', 'AttachmentClassification', 'DNA_V2_TOC_SURFACING']
for func in ml_functions:
    url = "https://mq-proxy-cognitive-platform.apps.ent-ocp4-prod-ric.antmdc.internal.das/api/faas/export"
    payload = {"data": {"function": {"name": func}}, "solution_id": solution_id}
    a = requests.post(url=url, data=json.dumps(payload), verify=False)
    response = json.loads(a.text)
    path = response["result"]["metadata"]["export_path"]
    presigned_url = "https://mq-proxy-cognitive-platform.apps.ent-ocp4-prod-ric.antmdc.internal.das/presignedurl/get/"
    presigned_payload = {"file_path": path, "solution_id": solution_id}
    b = requests.post(url=presigned_url, data=json.dumps(presigned_payload), verify=False)
    response_pre = json.loads(b.text)
    presigned_path = response_pre["metadata"]["presigned_url_get"]
    folder_path = "/export_files/"
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
    file_name = folder_path + func + ".zip"
    file_data = requests.get(url=presigned_path, verify=False)
    with open(file_name, 'wb') as fd:
        fd.write(file_data.content)
    local_res = LocalResource(fullpath=file_name)
    source_path = solution_id + file_name
    source_res = XpmsResource.get(key=source_path)
    local_res.copy(source_res)
    # import_url = "https://mq-proxy-cognitive-platform-perf.apps.ent-ocp4-np2-har.antmdc.internal.das/faas/import"
    import_url = "https://mq-proxy-cognitive-platform.apps.ent-ocp4-prod-ric.antmdc.internal.das/faas/import"
    # import_payload = {"data": {"import_path": source_res.urn.replace("\\", "/")}, "solution_id": solution_id}
    import_payload = {"data": {"import_path": source_res.urn.replace("\\", "/")}, "solution_id": "claimsol7"}
    requests.post(url=import_url, data=json.dumps(import_payload), verify=False)
    print(func, "posted")

from xpms_storage.db_handler import DBProvider

db = DBProvider.get_instance(db_name="system")
dag_ver = db.find(table="dag_task_version_bundle", filter_obj={})
dag_task = db.find(table="dag_tasks", filter_obj={})
to_be_deleted = []
task_present_name = []
multiple_dag_ver = []
not_present = []
all_v = [t['task_id'] for t in dag_ver]
all_t = [t['task_id'] for t in dag_task]
missed_v = [t for t in all_t if t not in all_v]
missed_t = [t for t in all_v if t not in all_t]
for d in dag_ver:
    all_tasks = [t for t in dag_task if t['name'] == d['name']]
    if len(all_tasks) > 1:
        to_be_deleted.extend([t for t in dag_task if t['name'] == d['name'] and d['task_id'] != t['task_id']])
    if d['name'] in task_present_name:
        multiple_dag_ver.append(d['name'])
    else:
        task_present_name.append(d['name'])
task_present_name = []
multiple_dag_task = []
for d in dag_task:
    if d['name'] in task_present_name:
        multiple_dag_task.append(d['name'])
    else:
        task_present_name.append(d['name'])

print(multiple_dag_ver)
print(task_present_name)
print(multiple_dag_task)


from xpms_file_storage.file_handler import XpmsResource, LocalResource

coll_list = ["V2_Policy_config", "dna_proc_medicarepolicy", "medicare_policy_config", "tf_config"]


def minio_to_local(minio_paths):
    '''
    :DEF: Store Minio files into local
    :param minio_paths:  list of minio paths
    :return: local paths of stored minio files
    '''
    local_file_paths = []
    for each_path in minio_paths:
        source = XpmsResource.get(urn=each_path)
        if source.exists():
            path = "/tmp/" + str(source.filename)
            local_path = LocalResource(fullpath=path)
            source.copy(local_path)
            print("{} is downloded successfully".format(each_path))
            local_file_paths.append(path)
        else:
            print("{} is not found in minio".format(each_path))
    print(local_file_paths)
    db = DBProvider.get_instance(db_name="claimsol3")
    for coll in coll_list:
        with open("/tmp/" + coll + ".json", encoding='utf-8-sig') as r:
            d = json.load(r)
            db.insert(table=coll, rows=d)

    return local_file_paths


minio_paths = ['minio://anthemecp/claimsol2/dna/V2_Policy_config.json',
               "minio://anthemecp/claimsol2/dna/dna_proc_medicarepolicy.json",
               "minio://anthemecp/claimsol2/dna/medicare_policy_config.json"],
"minio://anthemecp/claimsol2/dna/tf_config.json"
minio_to_local(minio_paths)
