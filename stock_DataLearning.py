"""

형성 된 데이터 테이블 활용 학습 및 가중치 생성/최신화( 머신러닝, 다중선형회귀분석 사용)
1. 최신화 = 기존 데이터로 형성한 stock_classifier 데이터 추출 -> 학습 + 테스트 -> 학습된 가중치 최신화
2. 테스트 = 테스트 데이터로 형성한 stock_classifier 데이터 추출 -> 학습 + 테스트 -> 학습된 가중치 저장

"""


import tensorflow as tf
import numpy as np
import pymysql
import DB
tf.compat.v1.disable_eager_execution()


select_query = "select loading,prepare_load,income,term_load,class from stock_classifier"
DB.cursor.execute(select_query)
rows = DB.cursor.fetchall()

idx_query = "select max(idx) from stock_classifier"
DB.cursor.execute(idx_query)
idx = DB.cursor.fetchone()
idx = int(np.array(idx[0]))

x1_data = []
x2_data = []
x3_data = []
x4_data = []
y_data = []
print(rows)
for i in range(0,idx):
    x1_data.append(float(np.array(rows[i][0])))
    x2_data.append(float(np.array(rows[i][1])))
    x3_data.append(float(np.array(rows[i][2])))
    x4_data.append(float(np.array(rows[i][3])))
    y_data.append(float(np.array(rows[i][4])))

print(x1_data)
print(x2_data)
print(x3_data)
print(x4_data)
print(y_data)

select_query_test = "select loading,prepare_load,income,term_load,class from stock_classifier_test"
DB.cursor.execute(select_query_test)
rows_test = DB.cursor.fetchall()

idx_query_test = "select max(idx) from stock_classifier_test"
DB.cursor.execute(idx_query_test)
idx_test = DB.cursor.fetchone()
idx_test = int(np.array(idx_test[0]))

x1_data_test = []
x2_data_test = []
x3_data_test = []
x4_data_test = []
y_data_test = []
print(rows_test)
for i in range(0,idx_test):
    x1_data_test.append(float(np.array(rows_test[i][0])))
    x2_data_test.append(float(np.array(rows_test[i][1])))
    x3_data_test.append(float(np.array(rows_test[i][2])))
    x4_data_test.append(float(np.array(rows_test[i][3])))
    y_data_test.append(float(np.array(rows_test[i][4])))

print(x1_data_test)
print(x2_data_test)
print(x3_data_test)
print(x4_data_test)
print(y_data_test)

tf.random.set_seed(777)

w1 = tf.Variable(tf.random.normal([1]), name="weight1")
w2 = tf.Variable(tf.random.normal([1]),name="weight2")
w3 = tf.Variable(tf.random.normal([1]),name="weight3")
w4 = tf.Variable(tf.random.normal([1]),name="weight4")
b = tf.Variable(tf.random.normal([1]),name="bias")

x1 = tf.compat.v1.placeholder(tf.float32)
x2 = tf.compat.v1.placeholder(tf.float32)
x3 = tf.compat.v1.placeholder(tf.float32)
x4 = tf.compat.v1.placeholder(tf.float32)
Y = tf.compat.v1.placeholder(tf.float32)

hypothesis = x1*w1+x2*w2+x3*w3+x4*w4+b

cost = tf.reduce_mean(tf.square(hypothesis-Y))

optimizer = tf.compat.v1.train.AdamOptimizer(learning_rate=0.01)
train = optimizer.minimize(cost)


sess = tf.compat.v1.Session()
sess.run(tf.compat.v1.global_variables_initializer())

for step in range(10001):
    cost_val, hy_val, _ = sess.run([cost,hypothesis,train],feed_dict={x1:x1_data,x2:x2_data,x3:x3_data,x4:x4_data,Y:y_data})

    if step %100 ==0:
        print("step:",step,"\nCost:",cost_val)
print("w1:",w1,", w2:",w2,", ")

# save_file = "./trained_weight.ckpt"
# saver = tf.compat.v1.train.Saver([w1,w2,w3,w4,b])
# saver.save(sess, save_file)

#step: 10000(13000개 데이터 10000번 회귀분석 = 총 13억회)
#Cost: 0.07228681
