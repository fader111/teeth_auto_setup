# from numpy.random.mtrand import shuffle
import tensorflow as tf
import numpy as np
from tensorflow.keras.layers import Input, Dense, Flatten, Reshape
from tensorflow.keras.models import Model
from tensorflow.python.keras.layers.normalization.batch_normalization import BatchNormalization

# dataset preparation
n = 64
assert n>10
ish = list(range(n))
x_train = np.arange(n).reshape(-1, n)
x_test = np.ones(n).reshape(-1, n)

# print (f"x_train{x_train[:10]}")
y_train = np.arange(n).reshape(-1, n)
# print (f"y_train{y_train[:10]}")

# новый датасет из джа энкодера
ds = [[[17, 134, 8, -22], [28, 107, 7, -17], [38, 86, 7, -15], [48, 67, 8, -12], [59, 53, 7, -9], [69, 42, 8, -6], [80, 35, 7, -3], [90, 31, 7, 0], [100, 30, 8, 1], [110, 31, 8, 3], [120, 35, 9, 6], [131, 42, 8, 8], [141, 53, 8, 11], [152, 67, 8, 15], [162, 86, 8, 16], [172, 107, 9, 22]]]
dsn = np.array(ds)
dsn = dsn.reshape(-1,64)
y_train = dsn[:]
print (f"dsn shape === {dsn.shape} y_train {y_train.shape}")

# model creating
inputs = Input((64,))
x  =    Dense(64, activation='elu')(inputs)
# x  =    BatchNormalization()(x)
x  =    Dense(64, activation='elu')(x)
# x  =    BatchNormalization()(x)
out  =  Dense(64, activation='linear')(x)
# out  = Dense(64, activation='linear')(inputs)

# out = input_
# out = BatchNormalization()(out) # тут не влияет 
model = Model(inputs, out)
model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])
# model.compile(optimizer='adam', loss='MeanSquaredError')
# model.compile(optimizer='adam', loss='mean_absolute_error') # лосс ниже 0.2 вообще не спускается
# model.compile(optimizer='adam')

# model trainng
callbacks = [
    tf.keras.callbacks.EarlyStopping(monitor="loss", min_delta=0.0001, patience=100, verbose=1),
    # tf.keras.callbacks.EarlyStopping(monitor="loss", patience=100, verbose=1),
    # tf.keras.callbacks.ModelCheckpoint(filepath="mymodel_{epoch}", save_best_only=True, monitor="loss", verbose=1),
]

# включение шаффла приводит к полному бардаку
# model.fit(x_train, y_train, batch_size=2, epochs=2000, shuffle=True, callbacks=callbacks) # при epochs<140 иногда ошибается
model.fit(dsn, y_train, batch_size=15, epochs=2040, shuffle=False, callbacks=callbacks) # при epochs<140 иногда ошибается

# model prediction
res = model.predict(dsn)
# res = model.predict(x_test)
# print (f"predicted \n{np.round(res[0])}")


ar = [round(i) for i in res[0]]
# ar = list(np.round(res[0])) # ar[-0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0
# print (f"res_l{res_l}")
val_list = list(y_train[0])

if ar == val_list:
    print (f"\n *OK* списки равны ")
else: 
    print (f"ar {ar} len - {len(ar)}")
    print (f"dsn{val_list} len - {len(val_list)}")
    for i in range(0):#(len(ar)):
        if ar[i]!=val_list[i]:
            print (f"fail {i} ar{ar[i]} dsn{val_list[i]}")

'''
for i, ind in enumerate(ar):
    try:
        if ish[ind] != ar[ind]:
            print (f"missing -> {i}")
    except:
        # print (f'ar {ar}     ish {ish}')    
        print (f"ind   {ind} ish {ish[ind]}")
if ish==ar:
    print ('ok')
'''
# print (f"ish {ish}")
# print (f"ar {ar}")