# Eval натренированной 3d модели построение графиков
import os, sys
import numpy as np
# from jaw_gen import *
# import tensorflow as tf 
# from tensorflow.keras.layers import Input, Dense, Flatten, Reshape, Dropout
# from tensorflow.keras.layers import Conv2D, MaxPooling2D, UpSampling2D, BatchNormalization
from tensorflow.keras.models import Model, load_model
# from tensorflow.keras.optimizers import Adam

# import tensorflow.keras.backend as K
# from tensorflow.keras.layers import Lambda
# import cv2

# from tqdm import tqdm
# основное отличие - Landmark_gen больше не генерит картинки. только вектора. 
# и у него теперь есть 3D рисовалка, которая есть независимый метод
from jaw_gen3d_3lm import Landmark_gen 

# готовим данные для подачи на вход энкодера
inst_ =                 Landmark_gen()
data_len =              100
dataset =               []
dataset_spoiled =       []
dataset_vec =           []
dataset_vec_spoiled =   []

n=500 # размер батча векторов для предикта
dense_dim = 192 # размер dense слоя 

for i in range(data_len):
    scale =  9 + np.random.sample()*3     # это для размера 200, диапазон от 14 до 19 для размера 400
    factor = 2.2 + np.random.sample()/4   # это для размера 200, диапазон 2.5 - 2.7 для размера 400 
    # name = f"scale {scale:.4}  factor {factor:.3}"
    name = 'Evaluating 3D Setup ML'
    vec, vec_spoiled = inst_.image_gen(scale=scale, factor=factor, spoiledMDW=True, shiftMDW=True)
    # собираем датасет из векторов 
    dataset_vec.append(vec)
    dataset_vec_spoiled.append(vec_spoiled)

# преобразуем датасет в numpy массив
dataset_vec =           np.array(dataset_vec,           dtype="float32") 
dataset_vec_spoiled =   np.array(dataset_vec_spoiled,   dtype="float32") 
# print (f"dataset_vec_spoiled shape{dataset_vec_spoiled.shape}") # shape(10, 16, 12)
dataset_vec_spoiled =    np.reshape(dataset_vec_spoiled,    (-1, dense_dim))
# print (f"dataset_vec_spoiled shape{dataset_vec_spoiled.shape}") # shape(10, 16, 12)

# подгружаем модель 
m_pth = (os.path.dirname(sys.argv[0]))+'/models3D/'
models = os.listdir(m_pth)

ep = 3400       # модели этой эпохи будут загружены

def model(type_, ep):
    f_path = ''
    try:
        f_path = m_pth + [mdl for mdl in models if f"{type_}{ep}" in mdl][0]
    except:
        print (f"Error, check the model path...")
        sys.exit()
    # assert os.path.exists(f_path)
    return load_model(f_path) 

encoder = model("encoder", ep)
decoder = model("decoder", ep)
# encoder = load_model(models[0][0])
# decoder = load_model(models[0][1])

# предиктим 
encoded_vecs = encoder.predict(dataset_vec_spoiled[:n],  batch_size=n)
decoded_vecs = decoder.predict(encoded_vecs[:n], batch_size=n)

dataset_vec_spoiled =   np.reshape(dataset_vec_spoiled,     (-1, 16, dense_dim//16))
decoded_vecs =          np.reshape(decoded_vecs,            (-1, 16, dense_dim//16))

# формируем картинки из предсказанных векторов
# print (f"decoded_vecs shape{decoded_vecs.shape}")
# print (f"dataset_vec_spoiled[1]{dataset_vec_spoiled[1]}")
# print (f"decoded_vecs[1]{decoded_vecs[1]}")
# for i in range(n):

k=3 # колво графиков больше 20 не надо - не рисует
m=1 # штук на графике
assert n>=m*k
for i in range(k):
    inst_.draw_3d(  
                    # dataset_vec         [i*m:(i+1)*m],  # тренировочные
                    dataset_vec_spoiled [i*m:(i+1)*m],  # входные 
                    decoded_vecs        [i*m:(i+1)*m],  # предиктные 

                    show = True)
# inst_.draw_3d((dataset_vec_spoiled[1], dataset_vec_spoiled[1]), show = True)

