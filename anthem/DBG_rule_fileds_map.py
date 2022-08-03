from xpms_storage.db_handler import DBProvider
import pandas as pd
import json

error_list = []
copied_list = []
procesed_list = []

map_Df = pd.read_excel("Query_Builder_technical_criteria_names_to_business_field_names.xlsx",engine='openpyxl')
print(len(map_Df))

map_Df = map_Df.drop_duplicates(subset = ["Technical Criteria Names"])
print(len(map_Df))

map_df_dict = map_Df.to_dict(orient = 'records')
name_list = map_Df["Technical Criteria Names"].to_list()

db_Conn = DBProvider.get_instance(db_name="claimsol12")
response = db_Conn.find(table="rules_fields",filter_obj={"is_active":True})
fields = response[0]["fields"]["query_fields"]
print(len(fields))

for filed in fields:
    if filed["name"] not in name_list:
        error_list.append(filed)
    else:
        if filed["name"] in procesed_list:
            copied_list.append(filed["name"])
        filed["name"] =  map_Df[map_Df["Technical Criteria Names"] == filed["name"]]["Business Field Names"].to_list()[0]
        procesed_list.append(filed["name"])

print(error_list)
print(copied_list)
print(response)

df = pd.DataFrame(response[0]["fields"]["query_fields"])
print(len(df))

df = df.drop_duplicates(subset=["name","field_type","type"])
print(len(df))

