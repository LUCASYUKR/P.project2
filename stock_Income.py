"""
product_list = 입/출고 log(있음)
product_status = 현 재고관리(있음)
stock_list = 일일 재고 분석 데이터터(있음)
stock_classifier = 재고 학습용 데이터(있음)
stock_test = 재고 학습 테스트용 데이터(있음)
class_status = 재고 등급 현황 데이

"""

import pymysql
import datetime
import time
import numpy
import DB


operation = input("1. income, 2. locating:")

if operation == "1":

    tableCheck = "select * from product_status"
    try:
        DB.cursor.execute(tableCheck)
        rows = DB.cursor.fetchall()
        table = True
    except:
        table = False
        pass

    if table == False:  # 재고 현황 관리용 데이터 테이블
        tableMake = "create table product_status(idx int not null auto_increment primary key,product int not null, quantity int not null, location varchar(20) , date date not null, time int not null, status int)default character set utf8 collate utf8_general_ci"
        DB.cursor.execute(tableMake)
        result = DB.cursor.fetchall()
        print("table generated : product_status")
    else:
        pass
    """
    +----------+-------------+------+-----+---------+----------------+
| Field    | Type        | Null | Key | Default | Extra          |
+----------+-------------+------+-----+---------+----------------+
| idx      | int         | NO   | PRI | NULL    | auto_increment |
| product  | int         | NO   |     | NULL    |                |
| quantity | int         | NO   |     | NULL    |                |
| location | varchar(20) | YES  |     | NULL    |                |
| date     | date        | NO   |     | NULL    |                |
| time     | int         | NO   |     | NULL    |                |
| status   | int         | YES  |     | NULL    |                |
+----------+-------------+------+-----+---------+----------------+
    """

    tableCheck2 = "select * from product_list"
    try:
        DB.cursor.execute(tableCheck2)
        rows = DB.cursor.fetchall()
        table = True
    except:
        table = False
        pass

    if table == False:  # 재고 확인용 데이터 테이블
        tableMake = "create table product_list(idx int not null auto_increment primary key,product int not null, quantity int not null, date date not null, time int not null, purpose varchar(20) not null)default character set utf8 collate utf8_general_ci"
        DB.cursor.execute(tableMake)
        result = DB.cursor.fetchall()
        print("table generated : product_list")
    else:
        pass
    """
    +----------+-------------+------+-----+---------+----------------+
| Field    | Type        | Null | Key | Default | Extra          |
+----------+-------------+------+-----+---------+----------------+
| idx      | int         | NO   | PRI | NULL    | auto_increment |
| product  | int         | NO   |     | NULL    |                |
| quantity | int         | NO   |     | NULL    |                |
| date     | date        | NO   |     | NULL    |                |
| time     | int         | NO   |     | NULL    |                |
| purpose  | varchar(20) | NO   |     | NULL    |                |
+----------+-------------+------+-----+---------+----------------+
    """
    time = time.strftime("%H%M%S")
    date_time = datetime.datetime.now()

    while True:
        product = input("Product No.:")
        if product == "False":
            break
        quantity = input("quantity:")
        location = input("Location:")
        purpose = "in"
        status = "1"

        input_stock = "insert into product_status (product,quantity,location,date,time,status) values ({},{},'{}',now(),{},{})".format(str(product),str(quantity),str(location),str(date_time),str(status))
        DB.cursor.execute(input_stock)
        DB.db.commit()

        class_check = "select * from class_status where product={}".format(str(product))
        DB.cursor.execute(class_check)
        class_data = DB.cursor.fetchone()
        class_notifier = str(numpy.array(class_data[0][1]))

        print("<Product No.",product," is classified to '",class_notifier,"'Class>")  # 입고 담당자에게 현재 특정 품목이 어느 클래스에 지정되어 있는지 알려주고 있음 -> 해당 구역으로 보관유도

        input_history = "insert into product_list (product,quantity,date,time,purpose) values ({},{},now(),{},'{}')".format(
            str(product), str(quantity), str(time),str(purpose))
        DB.cursor.execute(input_history)
        DB.db.commit()




    print("insert complete")


else:
    product = input("Product No.:")
    location = input("Location:")
    location2 = input("Location changed:")
    quantity = input("Quantity")

    update_stock = "update product_status set product={},location='{}',quantity={} where product = {} and location='{}'".format(str(product),str(location2),str(quantity),str(product),str(location))
    DB.cursor.execute(update_stock)
    DB.db.commit()

    print("data updated")

