import time
import pymysql
import random
# DB connect
con = pymysql.connect(host="localhost", user="root", password="rhtn1720", charset="utf8", db="senser_db")
cur = con.cursor()

Title = time.strftime("sss%Y%m%d")
sql = "create table if not exists " + Title + " (id INT AUTO_INCREMENT PRIMARY KEY, time VARCHAR(255), cu1 FLOAT(10), cu2 FLOAT(10), cu3 FLOAT(10), pw1 FLOAT(10), pw2 FLOAT(10), pw3 FLOAT(10), total1 FLOAT(10), total2 FLOAT(10), total3 FLOAT(10))"
cur.execute(sql)

total_pw1 = 0
total_pw2 = 0
total_pw3 = 0
    

while True:
    
    try :
    
        dataTime = time.strftime("%H:%M:%S")

        cu1=random.uniform(10,12)
        cu2=random.uniform(10,12)
        cu3=random.uniform(10,12)
        
        PF = 0.97
        dataPw1 = (PF * cu1 * 220 / 1000)
        dataPw2 = (PF * cu2 * 220 / 1000)
        dataPw3 = (PF * cu3 * 220 / 1000)
        
        total_pw1 = total_pw1 +dataPw1
        total_pw2 = total_pw2 +dataPw2
        total_pw3 = total_pw3 +dataPw3

        # DB save
        sql = "INSERT INTO " + Title + " (time, cu1, cu2, cu3, pw1, pw2, pw3 ,total1, total2, total3) value(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" 
        cur.execute(sql, (dataTime, cu1, cu2, cu3, dataPw1, dataPw2, dataPw3, total_pw1, total_pw2, total_pw3))
        con.commit()
        time.sleep(1)
    
    except : 
        pass