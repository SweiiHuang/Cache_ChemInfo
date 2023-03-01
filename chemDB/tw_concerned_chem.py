import pymysql
import pandas as pd
from sqlalchemy import create_engine

import os
from dotenv import load_dotenv
load_dotenv()

from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from time import sleep



options = Options()
options.edge_executable_path = "/Users/szuwei/Desktop/chemDB/msedgedriver"


driver=webdriver.Edge(options=options)


driver.get("https://flora2.epa.gov.tw/ToxicC/Query/database2.aspx")


driver.find_element(By.ID, "ContentPlaceHolder1_rblToxicCCS_1").click()

sleep(2)

create_engine_content = os.getenv("engine_content")
engine = create_engine(create_engine_content)


tw_concerned_df = pd.read_html(driver.page_source)[2]


new_column_names = {"項次":"item","列管編號":"list_no","英文名稱":"en_name","中文名稱":"cn_name","CAS No.":"cas_no","管制濃度 (w/w%)":"control_conc","管制運作行為分級及運作量(KG)":"grading_volume","具危害性":"hazardous"}


tw_concerned_df.rename(columns=new_column_names, inplace=True)
tw_concerned_df.to_sql('tw_concerned_chem', engine, if_exists='replace')

driver.close()

