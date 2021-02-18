"""

입력(가정: 스캔 혹은 손수 타이핑)된 입고 데이터를 학습된 가중치 기준으로 머신러닝 활용 classifying 하여 자동 등급화 반복(class_status에 업데이트)
등급화 된 데이터를 기준으로 해당 클래스의 구역 중 빈 곳을 자동으로 추천함(없을 시, 하나 아래 클래스 구역으로 보관)
품목별 재고확인, 품목, 로케이션 기반 재고변경, 로케이션 기반 재고확인 기능

"""
"""
product_list = 입/출고 log(있음)
product_status = 현 재고관리(있음)
stock_list = 일일 재고 분석 데이터터(있음)
stock_classifier = 재고 학습용 데이터(있음)
stock_test = 재고 학습 테스트용 데이터(있음)
class_status = 재고 등급 현황 데이(있음)

"""
import tensorflow as tf
import numpy as np
import pymysql
import datetime
import DB

tf.compat.v1.disable_eager_execution()

def classifier(loading,prepare_load,income,term_load,product):

    A = "3"
    B = "2"
    C = "1"

    loading = int(loading)
    prepare_load = int(prepare_load)
    income = int(income)
    term_load = int(term_load)
    product = int(product)

    if loading <= 18000:
        loading = C
    elif loading >= 18001 and loading <= 20000:
        loading = B
    elif loading >= 20001:
        loading = A

    if prepare_load <= 35:
        prepare_load = C
    elif prepare_load >= 36 and prepare_load <= 40:
        prepare_load = B
    elif prepare_load >= 41:
        prepare_load = A

    if term_load <= 45:
        term_load = C
    elif term_load >= 46 and term_load <= 50:
        term_load = B
    elif term_load >= 51:
        term_load = A

    if income <= 18000:
        income = C
    elif income >= 18001 and income <= 20000:
        income = B
    elif income >= 20001:
        income = A

    return loading,prepare_load,income,str(term_load),str(product)


choice = input("1. stock management, 2. stock controlling :")

if choice == "1":
    date = datetime.date.today()
    d1 = date.strftime("%Y-%m-%d")

    select_data_inout = "select product, purpose, sum(quantity) from product_list where date='{}' group by purpose,product".format(str(d1))

    DB.cursor.execute(select_data_inout)
    data = DB.cursor.fetchall()

    date_time = [40,40,40,40,50,50,50,50,60,60,60,60]
    for i in range(0,int(len(data)/2)):  # 기존 데이터에서 데이터 추출 및 가공
        loading = np.array(data[i][2])  # 가변적이라 자동설정
        prepare_load = date_time[i]  # 가변적이지 않기 때문에 수동설정
        income = np.array(data[i + 6][2])  # 가변적이라 자동설정
        term_load = date_time[i+6]  # 가변적이지 않기 때문에 수동설정
        product = np.array(data[i][0])

    # product_list에서 입출고 내역 끌어와서 가공 필요, 가공 후 머신러닝으로 넘기고 stock_list에 추가

    loading_cs,prepare_load_cs,income_cs,term_load_cs,product_cs,= classifier(int(loading),int(prepare_load),int(income),int(term_load),int(product))
    x1_data = float(loading_cs)  # machine_learning
    x2_data = float(prepare_load_cs)  # machine_learning
    x3_data = float(income_cs)  # machine_learning
    x4_data = float(term_load_cs)  # machine_learning

    x1 = tf.compat.v1.placeholder(tf.float32)  # machine_learning
    x2 = tf.compat.v1.placeholder(tf.float32)  # machine_learning
    x3 = tf.compat.v1.placeholder(tf.float32)  # machine_learning
    x4 = tf.compat.v1.placeholder(tf.float32)  # machine_learning
    Y = tf.compat.v1.placeholder(tf.float32)  # machine_learning

    w1 = tf.Variable(tf.random.normal([1]), name="weight1")  # machine_learning
    w2 = tf.Variable(tf.random.normal([1]),name="weight2")  # machine_learning
    w3 = tf.Variable(tf.random.normal([1]),name="weight3")  # machine_learning
    w4 = tf.Variable(tf.random.normal([1]),name="weight4")  # machine_learning
    b = tf.Variable(tf.random.normal([1]),name="bias")  # machine_learning

    hypothesis = x1*w1+x2*w2+x3*w3+x4*w4+b  # machine_learning

    save_file = "./trained_weight.ckpt"  # machine_learning

    sess = tf.compat.v1.Session()
    new_saver = tf.compat.v1.train.import_meta_graph("trained_weight.ckpt.meta")  # machine_learning
    saved = new_saver.restore(sess,"trained_weight.ckpt")  # machine_learning

    tf.compat.v1.get_default_graph()  # machine_learning

    prediction = sess.run(hypothesis,feed_dict={x1:x1_data,x2:x2_data,x3:x3_data,x4:x4_data})  # machine_learning

    product_class = []  # machine_learning
    for i in range(1):  # machine_learning
        prediction[i] = float(prediction[i])  # machine_learning
        if prediction[i]>=0 and prediction[i]<1.6:  # machine_learning
            prediction[i] = 1  # machine_learning
        elif prediction[i] >=1.6 and prediction[i]<2.6:  # machine_learning
            prediction[i] = 2  # machine_learning
        elif prediction[i] >=2.6 and prediction[i]<=3.5:  # machine_learning
            prediction[i] = 3  # machine_learning
        product_class.append(int(prediction[i]))  # machine_learning

    writeTableData = "insert into stock_classifier (loading, prepare_load, income, term_load, product, class) values({},{},{},{},{},{})".format(
        str(loading), str(prepare_load), str(income), str(term_load), str(product), str(product_class[0]))
    DB.cursor.execute(writeTableData)
    DB.db.commit()

    class_update = "select product,avg(class) from stock_classifier group by product order by avg(class) desc"  # 이전 클래스 구분 모든 기록을 평균내어 ABC 품목 별 클래스 구분
    DB.cursor.execute(class_update)
    class_data = DB.cursor.fetchall()

    print("product:",product,", class:",product_class[0])

    tableCheck = "select * from class_status"
    try:
        DB.cursor.execute(tableCheck)
        rows = DB.cursor.fetchall()
        table = True
    except:
        table = False
        pass

    if table == False:
        tableMake = "create table class_status(idx int not null auto_increment primary key, product int not null, class varchar(8) not null)"
        DB.cursor.execute(tableMake)
        result = DB.cursor.fetchall()
        print("table generated : class_status")

    class_table_reset = "delete from class_status"
    DB.cursor.execute(class_table_reset)
    DB.db.commit()

    class_A_input = "insert into class_status (product,class) values ({},{})".format(class_data[0][0],"A")
    DB.cursor.execute(class_A_input)
    DB.db.commit()

    class_B_input = "insert into class_status (product,class) values ({},{})".format(class_data[1][0],"B")
    DB.cursor.execute(class_B_input)
    DB.db.commit()

    for i in range(len(class_data)-2):
        class_C_input = "insert into class_status (product,class) values ({},{})".format(class_data[i+2][0],"C")
        DB.cursor.execute(class_C_input)
        DB.db.commit()
    print("class data inserted")


else:
    tableCheck = "select * from product_status"
    try:
        DB.cursor.execute(tableCheck)
        rows = DB.cursor.fetchall()
        table = True
    except:
        table = False
        pass

    if table == False:
        tableMake = "create table product_status(idx int not null auto_increment primary key,product int not null, quantity int not null, location varchar(20) , date date not null, time int not null, status int)default character set utf8 collate utf8_general_ci"
        DB.cursor.execute(tableMake)
        result = DB.cursor.fetchall()
        print("table generated : product_status")

    operation = input("1. product stock status, 2. change stock 3. location status:")

    if operation == "1":
        print("to stop process, input'stop' in 'Product No.'")
        while True:
            product_number = input("Product No.:")
            if product_number == "stop":
                exit()
            select_data = "select sum(stock) from product_status where product={} and status=1".format(str(product_number))
            DB.cursor.execute(select_data)
            product_data = DB.cursor.fetchall()
            products = []
            products.append(int(np.array(product_data[0])))
            print("Product:",product_number,"Stock:",products[0])

    if operation == "2":
        print("to stop process, input'stop' in 'Product No.'")
        while True:
            product_number = input("Product No.:")
            if product_number == "stop":
                exit()
            location = input("Location:")
            change = input("Change:")

            check_data = "select stock from product_status where product={} and location='{}'".format(str(product_number),str(location))
            DB.cursor.execute(check_data)
            result = DB.cursor.fetchall()
            products = []
            try:
                products.append(int(np.array(result[0])))
            except:
                print("The data is not correct")
                pass

            else:
                update_data = "update product_status set stock={} where location='{}'".format(str(change), str(location))
                DB.cursor.execute(update_data)
                DB.db.commit()
                print("update completed")

    if operation == "3":
        location = input("Location:")
        select_data = "select product,quantity,status from product_status where location='{}' and status=1".format(str(location))
        DB.cursor.execute(select_data)
        result = DB.cursor.fetchall()
        
        product = []
        product.append(int(np.array(result[0][0])))
        quantity = []
        quantity.append(int(np.array(result[0][1])))
        status = []
        status.append(int(np.array(result[0][2])))

        print("Location:",str(location),"Product:",str(product[0]),", Quantity:",str(quantity[0]),", Status:",str(status[0]))




