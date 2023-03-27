import requests
import pymysql
import os
import time
import json
from time import sleep
from zeep import Client
from dotenv import load_dotenv
load_dotenv()

user_name = os.getenv("sql_user")
user_pwd = os.getenv("sql_password")

conn = pymysql.connect(host='localhost', user = user_name, password = user_pwd, database='chemDB')
cursor = conn.cursor()


query = """ 
SELECT cas_no FROM cas_no_list 
"""

cursor.execute(query)
results = cursor.fetchall()



list_numbers = [result[0] for result in results]



cursor.close()
conn.close()


wsdl = "https://ec.europa.eu/taxation_customs/dds2/ecics/cs/services/chemical-substance?wsdl"
client = Client(wsdl=wsdl)


cas_numbers = list_numbers # a list of CAS numbers
responses = []
for i in range(0, len(cas_numbers), 10):
    sub_list = cas_numbers[i:i+10]
    for cas_number in sub_list:
        try:
            response = client.service.chemicalSubstanceForWs(casNumber=cas_number)
            if len(response.result) > 0:
                for res in response.result:
                    response_dict = {
                        'cus_number': res.cus_number,
                        'cas_rn': res.cas_rn,
                        'cn_code': res.cn_code,
                        'ec_number': res.ec_number,
                        'un_number': res.un_number,
                    }
                    for name in res.names.name:
                        if name.lang_code == 'EN':
                            response_dict['name'] = name.description
                            break
                    else:
                        response_dict['name'] = ''

                    responses.append(response_dict)
        except Exception as e:
            print(f'An error occurred for cas number {cas_number}: {e}')
            pass
    time.sleep(1)


conn = pymysql.connect(host='localhost', user=user_name, password= user_pwd, database='chemDB')
cursor = conn.cursor()


cursor.execute("DROP TABLE IF EXISTS chem_id_list")
sql = """CREATE TABLE chem_id_list (
    id INT NOT NULL AUTO_INCREMENT,
    name TEXT NOT NULL,
    cus_number VARCHAR(255) NOT NULL,
    cas_rn VARCHAR(255) NOT NULL,
    cn_code VARCHAR(255),
    ec_number VARCHAR(255),
    un_number VARCHAR(255),
    PRIMARY KEY (id)
    )"""
cursor.execute(sql)


for response_dict in responses:
    sql = "INSERT INTO chem_id_list (name, cus_number, cas_rn, cn_code, ec_number, un_number) VALUES (%s,%s, %s, %s, %s, %s)"
    cursor.execute(sql, (response_dict["name"],response_dict["cus_number"], response_dict["cas_rn"], response_dict["cn_code"], response_dict["ec_number"], response_dict["un_number"]))


conn.commit()
conn.close()














