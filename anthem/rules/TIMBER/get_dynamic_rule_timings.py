import datetime

from xpms_storage.db_handler import DBProvider

db = DBProvider.get_instance(db_name="claimsol3")
exec_ids_lst = []
for task_id in ["e303a1cb-f143-4bcb-9a22-ca04b9d7c747"]:
    # data = db.find(table="dag_task_executions",filter_obj={"task_id":"cffbede2-6e93-4b5a-9a0c-b1595d44421d"},columns = {"include":["task_id","execution_id"]},sort = [{"key": "update_ts", "order": "dsc"}],limit=10)
    data = db.find(table="dag_task_executions", filter_obj={"task_id": task_id},
                   columns={"include": ["task_id", "execution_id"]}, sort=[{"key": "update_ts", "order": "dsc"}],
                   limit=10)
    exec_list = [exec_Data["execution_id"] for exec_Data in data]
    lst_mean_time = []
    for exec_id in exec_list:
        sort = [{"key": "start_ts", "order": "dsc"}]
        res = db.find(table="dag_task_instances", filter_obj={"execution_id": exec_id, "name": "Invoke Rule Dynamic"},
                      sort=sort)

        t1_d = datetime.datetime.strptime(res[0]["end_ts"], '%Y-%m-%d %H:%M:%S.%f')
        t2_d = datetime.datetime.strptime(res[0]["start_ts"], '%Y-%m-%d %H:%M:%S.%f')
        lst_mean_time.append((t1_d - t2_d).total_seconds())
        print(f"total_time for {exec_id}  {(t1_d - t2_d).total_seconds()}")

    print(f"mean_time {task_id} --> {sum(lst_mean_time) / 10}")
