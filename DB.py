import pymysql


db = pymysql.connect(host="localhost",
                     port=3306,
                     user="javauser",
                     passwd="1234",
                     db="javadb",
                     charset="utf8")
cursor = db.cursor()