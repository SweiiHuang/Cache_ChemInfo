import pymysql
import pandas as pd
from sqlalchemy import create_engine

import os
from dotenv import load_dotenv
load_dotenv()

#tw_toxic_Chem
tw_toxic_df = pd.read_html("https://flora2.epa.gov.tw/ToxicC/Query/database2.aspx")[0]

#修改dataframe欄位名稱
new_column_names = {"項次":"item","列管編號":"list_no","英文名稱":"en_name","中文名稱":"cn_name","CAS No.":"cas_no","管制濃度(w/w%)":"control_conc","分級運作量(KG)":"grading_volume","毒性分類":"toxic_class"}

#("inplace"modifies the DataFrame directly, without creating a copy of the DataFrame.)
tw_toxic_df.rename(columns=new_column_names, inplace=True)


#assign()方法用於創建一個新的欄位，
#str.split()方法的pat參數使用正規表達式[,，]，表示使用逗號或comma來進行拆分
#explode()方法將每個值轉換為一個新行
#使用reset_index()方法重置索引。這樣就可以將一個欄位中的多個值拆分成多行，而不是增加新的欄位。
df = tw_toxic_df.assign(cas_no=tw_toxic_df["cas_no"].str.split('[,，]')).explode("cas_no").reset_index(drop=True)


create_engine_content = os.getenv("engine_content")
engine = create_engine(create_engine_content)
df.to_sql('tw_toxic_chem', engine, if_exists='replace')