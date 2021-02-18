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


print(datetime.date.today())
print(time.strftime("%H%M%S"))


print(type(int(time.strftime("%H%M%S"))))


operation = input("1. load, 2. locating:")

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
        purpose = "out"

        output_stock = "select quantity from product_status where product={} and location='{}'".format(str(product),str(location))
        DB.cursor.execute(output_stock)
        quantity_status = DB.cursor.fetchone()
        Q_S = int(numpy.array(quantity_status[0]))
        if Q_S == 0:
            status = "0"
        else:
            status = "1"

        quantity_output = Q_S-int(quantity)

        output_stock = "update product_status set quantity={},status={} where product={} and location='{}'".format(str(quantity_output),str(status),str(product),str(location))
        DB.cursor.execute(output_stock)
        DB.db.commit()

        output_history = "insert into product_list (product,quantity,date,time,purpose) values ({},{},now(),{},'{}')".format(
            str(product), str(quantity), str(date_time),str(purpose))
        DB.cursor.execute(output_history)
        DB.db.commit()

        print("data updated")




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