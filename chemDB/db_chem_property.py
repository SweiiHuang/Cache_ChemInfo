import requests
import pymysql
import os
import time
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


cas_numbers = list_numbers
data_list = []

missing_data = []

for cas_number in cas_numbers:
    url = "https://commonchemistry.cas.org/api/detail?cas_rn=" + cas_number

    try:
        r=requests.get(url)
        r.raise_for_status()  # check if there's a request error
        response = r.json()
    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"Error fetching data for CAS number {cas_number}: {e}")
        missing_data.append(cas_number)
        continue

    data_dict = {}

    experimentalProperties = response.get("experimentalProperties", [])
    for prop in experimentalProperties:
        if prop.get("name") == "Boiling Point":
            boiling_point = prop.get("property", "-")
            data_dict["boiling_point"] = boiling_point
        elif prop.get("name") == "Melting Point":
            melting_point = prop.get("property", "-")
            data_dict["melting_point"] = melting_point
        elif prop.get("name") == "Density":
            density = prop.get("property", "-")
            data_dict["density"] = density

    data_dict["cas_no"] = response.get("rn", "-")
    data_dict["name"] = response.get("name", "-")
    data_dict["image"] = response.get("image", "-")
    data_dict["molecular_formula"] = response.get("molecularFormula", "-")
    data_dict["molecular_mass"] = response.get("molecularMass", "-")

    data_list.append(data_dict)
    time.sleep(1)


if missing_data:
    print(f"CAS numbers that did not return any data: {missing_data}")




try:
    cursor.execute("DROP TABLE IF EXISTS chem_property_list")
    sql = """CREATE TABLE chem_property_list (
    id INT NOT NULL AUTO_INCREMENT,
    name TEXT NOT NULL,
    cas_no VARCHAR(255) NOT NULL,
    image LONGTEXT,
    molecular_formula VARCHAR(255),
    molecular_mass VARCHAR(255),
    boiling_point VARCHAR(255),
    melting_point VARCHAR(255),
    density VARCHAR(255),
    PRIMARY KEY (id)
    )"""
    cursor.execute(sql)

  
    
    for data_dict in data_list:
        sql = "INSERT INTO  chem_property_list(name, cas_no, image, molecular_formula, molecular_mass,boiling_point, melting_point, density) VALUE(%s,%s,%s,%s,%s,%s,%s,%s)"
        if 'molecular_formula' in data_dict:
            molecular_formula = data_dict['molecular_formula']
        else:
            molecular_formula = '-'

        if 'molecular_mass' in data_dict:
            molecular_mass = data_dict['molecular_mass']
        else:
            molecular_mass = '-'

        if 'boiling_point' in data_dict:
            boiling_point = data_dict['boiling_point']
        else:
            boiling_point = '-'

        if 'melting_point' in data_dict:
            melting_point = data_dict['melting_point']
        else:
            melting_point = '-'

        if 'density' in data_dict:
            density = data_dict['density']
        else:
            density = '-'
    
        cursor.execute(sql,(data_dict["name"], data_dict["cas_no"], data_dict["image"], data_dict["molecular_formula"],data_dict["molecular_mass"], boiling_point, melting_point, density))
        conn.commit()
    print(f"Data for {len(data_list)} CAS numbers inserted into chem_property_list table")
except Exception as e:
    print(f"Error creating table and inserting data: {e}")

finally:
    cursor.close()
    conn.close()







