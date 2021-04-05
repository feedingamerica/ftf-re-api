import json
import psycopg2
import MySQLdb
import mysql.connector


try:
    conn=mysql.connector.connect(host='localhost', database='API', user='XueyangLi', password='Wozhixihuanni48')
    #cursor.execute(table)
    if conn.is_connected():
        db_Info = conn.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = conn.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
except Error as e:
    print("Error while connecting to MySQL", e)
print('\n')
def query_db(query, one=False):
    cur = conn.cursor()
    cur.execute(query)
    r = [dict((cur.description[i][0], value) \
               for i, value in enumerate(row)) for row in cur.fetchall()]
    #cur.connection.close()
    return (r[0] if r else None) if one else r

ID=input('Please enter the report ID: ')
query='SELECT * FROM addin_ohio WHERE ID='+ID+';'
my_query = query_db(query)

query2='SELECT * FROM addin_mid_ohio_foodbank WHERE ID='+ID+';'
my_query2 = query_db(query2)

big_num='SELECT * FROM big_numbers WHERE ID='+ID+';'
big_query=query_db(big_num)

service='SELECT * FROM services WHERE ID='+ID+';'
ser_query=query_db(service)

families='SELECT * FROM families WHERE ID='+ID+';'
fam_query=query_db(families)

new_families='SELECT * FROM new_families WHERE ID='+ID+';'
newF_query=query_db(new_families)

geographic_origin='SELECT * FROM geographic_origin WHERE ID='+ID+';'
geographic_origin_query=query_db(geographic_origin)

family_members='SELECT * FROM family_members WHERE ID='+ID+';'
family_members_query=query_db(family_members)

trends='SELECT * FROM trends WHERE ID='+ID+';'
trends_query=query_db(trends)

json_output1 = json.dumps(my_query)
json_output2 = json.dumps(my_query2)
json_outputBIG=json.dumps(big_query) 
json_outputSER= json.dumps(ser_query) 
json_fam=json.dumps(fam_query)
json_newF=json.dumps(newF_query)
json_geo=json.dumps(geographic_origin_query)
json_faMem=json.dumps(family_members_query)
json_tren=json.dumps(trends_query) 
result='addin_ohio: \n'+json_output1+'\n'+'addin_mid_ohio_foodbank: \n'+json_output2+'\n'+'big_numbers: \n'+json_outputBIG+'\n'+'services: \n'+json_outputSER
result=result+'families: \n'+json_fam+'\n'+'new_families: \n'+json_newF+'\n'+'geographic_origin: \n'+json_geo+'\n'
result=result+'family_members: \n'+json_faMem+'\n'+'trends: \n'+json_tren
print("data: \n"+result)
