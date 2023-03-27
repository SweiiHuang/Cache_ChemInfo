import pymysql
import os
from dotenv import load_dotenv
load_dotenv()

user_name = os.getenv("sql_user")
user_pwd = os.getenv("sql_password")


conn = conn = pymysql.connect(host='localhost', user = user_name, password = user_pwd, database='chemDB')
cursor = conn.cursor()



query = "DROP TABLE IF EXISTS cas_no_list"
cursor.execute(query)
conn.commit()


query = """
CREATE TABLE cas_no_list (
    `index` INT AUTO_INCREMENT PRIMARY KEY,
    cas_no VARCHAR(25) NOT NULL
);
"""
cursor.execute(query)
conn.commit()


query = """ 
SELECT cas_no FROM (
    SELECT DISTINCT cas_no
    FROM tw_toxic_chem
    UNION
    SELECT DISTINCT cas_no
    FROM tw_concerned_chem
    UNION
    SELECT DISTINCT cas_no
    FROM tw_priority_chem
    UNION
    SELECT DISTINCT cas_no
    FROM tw_controlled_chem
) AS t
"""
cursor.execute(query)
results = cursor.fetchall()


for result in results:
    query = "INSERT INTO cas_no_list (cas_no) VALUES (%s)"
    cursor.execute(query, result)
conn.commit()


cursor.close()
conn.close()







