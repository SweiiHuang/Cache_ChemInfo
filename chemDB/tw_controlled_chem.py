import requests

import pymysql
import tabula
import pandas as pd
from sqlalchemy import create_engine

import os
from dotenv import load_dotenv
load_dotenv()



dfs = tabula.read_pdf("tw_controlled.pdf",pages='all',multiple_tables=False)[0]



new_column_names = {'Unnamed: 0':"list1_name", 'Unnamed: 1':"cas_no", 'CAS.':"cn_name", 'Unnamed: 3':"en_name", 'Unnamed: 4':"5",'Unnamed: 5':"6"}
dfs.rename(columns=new_column_names, inplace=True)

controlled_df = dfs.drop(columns=["list1_name","5","6"])

controlled_df = controlled_df.dropna(subset=["cn_name","en_name"]).reset_index(drop=True)


create_engine_content = os.getenv("engine_content")
engine = create_engine(create_engine_content)
controlled_df.to_sql('tw_controlled_chem', engine, if_exists='replace')


