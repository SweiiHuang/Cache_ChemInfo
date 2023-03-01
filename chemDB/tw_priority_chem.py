import requests

import pymysql
import tabula
import pandas as pd
from sqlalchemy import create_engine

import os
from dotenv import load_dotenv
load_dotenv()

df = pd.read_excel('tw_priority.ods', engine='odf')
# print(df.columns)

new_column_names = {'附錄一、對於未滿18歲及妊娠或分娩後未滿1年女性勞工具危害性之化學品名單':"1", 'Unnamed: 1':"2", 'Unnamed: 2':"cas_no",'Unnamed: 3':"en_name", 'Unnamed: 4':"cn_name", 'Unnamed: 5':"remark"
}
df.rename(columns=new_column_names, inplace=True)

#刪除欄位1&2，並刪除"cas_no"值为 NaN的row
dfs = df.drop(columns=["1","2"]).dropna(subset=["cas_no"])
#'!='過濾出'cas_no'不等於 'CAS No.'值並重置index
dfs = dfs[dfs['cas_no'] != 'CAS No.'].reset_index(drop=True)




create_engine_content = os.getenv("engine_content")
engine = create_engine(create_engine_content)
dfs.to_sql('tw_priority_chem', engine, if_exists='replace')
