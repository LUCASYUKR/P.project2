"""

머신러닝 가중치 최신화 혹은 테스트 데이터 생성 및 훈련
1. 최신화 = stock_list 데이터 추출 -> def classifier -> stock_classifier 테이블로 입력 + test 데이터 난수로 형성
2. 테스트 = stock_list 데이터 기준에 맞게 난수로 형성 -> def classifier -> stock_classifier 테이블로 입력 + test 데이터 난수로 형성

"""

import random
import pymysql
import numpy
import csv
import DB


def classifier(loading,prepare_load,income,term_load,product):
    classfier = ""
    A = "3"
    B = "2"
    C = "1"

    A_class = "3"
    B_class = "2"
    C_class = "1"

    loading = int(loading)
    prepare_load = int(prepare_load)
    income = int(income)
    term_load = int(term_load)
    product = int(product)

    loading_dataCheck = "select product,sum(loading) from stock_list group by product order by sum(loading) desc;"
    DB.cursor.execute(loading_dataCheck)
    loadingLevel = DB.cursor.fetchall()
    loading_list = []
    for i in range(len(loadingLevel)):
        loading_list.append(numpy.array(int(loadingLevel[i][0])))

    if product == int(loading_list[0]):
        loading = A
    elif product == int(loading_list[1]):
        loading = B
    else:
        loading = C

    if prepare_load <= 35:  # 개별 설정 (준비 시간이 길 수록 A 클래스)
        prepare_load = C
    elif prepare_load >= 36 and prepare_load <= 40:
        prepare_load = B
    elif prepare_load >= 41:
        prepare_load = A

    if term_load <= 45:  # 개별 설정 ( 출고간격이 짧을 수록 A 클래스)
        term_load = A
    elif term_load >= 46 and term_load <= 50:
        term_load = B
    elif term_load >= 51:
        term_load = C

    income_dataCheck = "select product,sum(income) from stock_list group by product order by sum(income) desc;"
    DB.cursor.execute(income_dataCheck)
    incomeLevel = DB.cursor.fetchall()
    income_list = []
    for i in range(len(incomeLevel)):
        income_list.append(numpy.array(int(incomeLevel[i][0])))

    if product == int(income_list[0]):
        income = A
    elif product == int(income_list[1]):
        income = B
    else:
        income = C

    classCal = int(loading) + int(prepare_load) + int(term_load) + int(income)
    if classCal <= 6:  # 최대 기준 CCBB or CCCA
        classfier = C_class
    elif classCal >= 7 and classCal <= 9:  # 3점 터울
        classfier = B_class
    elif classCal >= 10:  # 3점 터울
        classfier = A_class

    return loading,prepare_load,income,str(term_load),str(product),classfier


testCheck = input("1.make test data, 2.input stock list data:")

if testCheck=="1":

    tableCheck = "select * from stock_classifier"
    try:
        DB.cursor.execute(tableCheck)
        rows = DB.cursor.fetchall()
        table = True
    except:
        table = False
        pass

    if table == False:  # 학습 데이터 테이블
        tableMake = "create table stock_classifier(idx int not null auto_increment primary key,loading int not null, prepare_load int not null, income int not null, term_load int not null,product int not null, class int not null)default character set utf8 collate utf8_general_ci"
        DB.cursor.execute(tableMake)
        result = DB.cursor.fetchall()
        print("table generated : stock_classifier")
    else:
        pass

    tableCheck2 = "select * from stock_classifier_test"
    try:
        DB.cursor.execute(tableCheck2)
        rows = DB.cursor.fetchall()
        table = True
    except:
        table = False
        pass

    if table == False:  # 테스트 데이터 테이블
        tableMake2 = "create table stock_classifier_test(idx int not null auto_increment primary key,loading int not null, prepare_load int not null, income int not null, term_load int not null,product int not null, class int not null)default character set utf8 collate utf8_general_ci"
        DB.cursor.execute(tableMake2)
        result = DB.cursor.fetchall()
        print("table generated : stock_classifier_test")
    else:
        pass

    tableCheck3 = "select * from stock_list"
    try:
        DB.cursor.execute(tableCheck3)
        rows = DB.cursor.fetchall()
        table = True
    except:
        table = False
        pass

    if table == False:  # 입출고 이력 테이블(기존 데이터가 없어서 여기서 난수로 생성)
        tableMake3 = "create table stock_list(idx int not null auto_increment primary key,loading int not null, prepare_load int not null, income int not null, term_load int not null,product int not null)default character set utf8 collate utf8_general_ci"
        DB.cursor.execute(tableMake3)
        result = DB.cursor.fetchall()
        print("table generated : stock_list")
    else:
        pass

    """

    # 기존 데이터 사용 알고리즘
    idx_query = "select max(idx) from stock_list"
    cursor.execute(idx_query)
    idx = cursor.fetchone()
    idx = int(np.array(idx_test[0]))


    selectStockData = "select loading,prepare_load,income,term_load,product from stock_list
    cursr.execute(selectStockData)
    datas = cursor.fetchall()

    for i in range(0,idx):
        x1_data = float(np.array(datas_test[i][0]))
        x2_data = float(np.array(datas_test[i][1]))
        x3_data = float(np.array(datas_test[i][2]))
        x4_data = float(np.array(datas_test[i][3]))
        x5_data = float(np.array(datas_test[i][4]))
        loading, prepare_load, income, term_load, product, classfier = classifier(x1_data, x2_data, x3_data, x4_data,x5_data)  # classifying
        writeTableData = "insert into stock_classifier (loading, prepare_load, income, term_load, product, class) values({},{},{},{},{},{})".format(loading,prepare_load,income,term_load,product,classfier)
        cursor.execute(writeTableData)
        db.commit()
    print("learning data inserted)

        """
    ################################################ 테스트용이며, 기준 데이터가 있을 시 아래 난수형성은 제거, 위 알고리즘 사용
    for i in range(1,1001):
        loading = random.randint(0,3000)  # 1일 입고 총합
        prepare_load = random.randint(0,60)  # 1일 평균
        income = random.randint(0,3000)  # 1일 출고 총합
        term_load = random.randint(0,60)  # 1일 평균
        product_int = random.randint(1,3)  # 품목은 3개로 가정
        product = str(product_int)

        writeStockData = "insert into stock_list (loading, prepare_load, income, term_load, product) values({},{},{},{},{})".format(
            loading, prepare_load, income, term_load, product)
        DB.cursor.execute(writeStockData)
        DB.db.commit()

        loading, prepare_load, income, term_load, product, classfier = classifier(loading, prepare_load, income,
                                                                                 term_load, product)
        writeTableData = "insert into stock_classifier (loading, prepare_load, income, term_load, product, class) values({},{},{},{},{},{})".format(loading,prepare_load,income,term_load,product,classfier)
        DB.cursor.execute(writeTableData)
        DB.db.commit()
    print("stock data inserted")
    print("class data inserted")
    ################################################ 테스트용이며, 기준 데이터가 있을 시 아래 난수형성은 제거, 위 알고리즘 사용

    ################################################ 테스트용이며, 훈련 데이터랑 별도
    for i in range(1,31):
        loading2 = random.randint(0, 3000)  # 1일 입고 총합
        prepare_load2 = random.randint(0, 60)  # 1일 평균
        income2 = random.randint(0, 3000)  # 1일 출고 총합
        term_load2 = random.randint(0, 60)  # 1일 평균
        product_int2 = random.randint(1, 3)  # 품목은 3개로 가정
        product2 = str(product_int2)
        #
        loading2, prepare_load2, income2, term_load2, product2, classfier2 = classifier(loading2, prepare_load2, income2,
                                                                                  term_load2, product2)

        writeTableData2 = "insert into stock_classifier_test (loading, prepare_load, income, term_load, product, class) values({},{},{},{},{},{})".format(loading2,prepare_load2,income2,term_load2,product2,classfier2)
        DB.cursor.execute(writeTableData2)
        DB.db.commit()
    print("test data inserted")
    ################################################ 테스트용이며, 훈련 데이터랑 별도

else:

    method_choice = input("1.manual 2.CSV file upload:")
    if method_choice == "1":
        loading_raw = []
        while True:
            print("insert product i/o data, to stop process input 'stop' at fist section")
            loading = input("출고수량(1일기준):")
            if loading == "stop":
                exit()
            prepare_load = input("출고준비시간(1일평균):")
            income = input("입고수량(1일기준):")
            term_load = input("출고간격(1일평균):")
            product = input("재고넘버:")
    else:
        input_path = input("file path(csv):")
        f = open(input_path)
        csvReader = csv.reader(f)
        for data in csvReader:
            writeStockData = "insert into stock_list (loading, prepare_load, income, term_load, product) values({},{},{},{},{})".format(
                data[0], data[1], data[2], data[3], data[4])
            DB.cursor.execute(writeStockData)
            DB.db.commit()
