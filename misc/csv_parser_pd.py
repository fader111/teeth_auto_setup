# конвертер сым файла в массивы для обучения сделано средствами pandas
# import csv
import numpy as np
import sqlite3 
import pandas as pd
import time 

def set_gen_fr_csv_pd(csv_path):
    # читает csv файл
    # выдает датасет - 2 объекта T1 и T2 длина каждого равна количеству уникальных кейсов
    up_teeth_nums = [18, 17, 16, 15, 14, 13, 12, 11, 21, 22, 23, 24, 25, 26, 27, 28] # Jaw_id = 2 верхняя
    dw_teeth_nums = [48, 47, 46, 45, 44, 43, 42, 41, 31, 32, 33, 34, 35, 36, 37, 38] # Jaw_id = 1 нижняя 

    df = pd.read_csv(csv_path, index_col='id')
    # уберем временно из датафрейма все верхние челюсти и оставим только нижние
    df = df[df['Jaw_id']==1]
    # список уникальных кейсов
    cases = df.Case_id.unique()
    print (f"len cases - {len(cases)} type {type(cases)}") # len cases - 2 type <class 'numpy.ndarray'>
    # ts = time.time()
    dataset_t0 = [[[0.00001 for j in range(12)] for tooth in range(16)] for k in range(len(cases))]# раньше было заполнено нулями 
    dataset_t1 = [[[0.00001 for j in range(12)] for tooth in range(16)] for k in range(len(cases))] # и тут тоже
    # перебираем по всем уникальным cases
    for k, case in enumerate(cases):
        # перебираем по всем строкам из датафрейма, с одним и тем же Case_Id    
        subdf = df[df['Case_id']==case]
        for i in range(len(subdf)): # перебираем по части датафрейма где все Case_id = case
            # здесь - один row - это один зуб, надо заполнить челюсть значениями зубов
            # print(row) (42, 3, 1, 47, -25.357, 32.1696, 0.29188, -26.4387, 40.1274, -0.1345 ........ 
            row = subdf.iloc[i].tolist() # [7.0, 1.0, 36.0, 19.8454, 23.327, -1.1470 ... 982, -1.87889, 24.06, 27.2699, -3.97232, 0.0]
            tooth_id = int(row[2])&255 # 36 к примеру
            num_in_jaw = dw_teeth_nums.index(tooth_id)
            dataset_t0[k][num_in_jaw] = row[3:9] + row[15:21]
            dataset_t1[k][num_in_jaw] = row[9:15] + row[21:27]

           

    dataset_t0 = np.array(dataset_t0) # конверт их в numpy
    dataset_t1 = np.array(dataset_t1) 

    return dataset_t0, dataset_t1


if __name__ == "__main__":
    # fpath = 'C:\\Users\\Anton\\Projects\\jaw_encoder\\csv\\input_004.csv'
    fpath = 'C:\\Users\\Anton\\Projects\\jaw_encoder\\csv\\input.csv' 
    t0, t1 = set_gen_fr_csv_pd(fpath)
    print (f"t0 {t0[:3]} shape {t0.shape} len {len(t0)}") # shape(?, 16, 12)
