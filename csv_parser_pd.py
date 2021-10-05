# конвертер csv файла в массивы для обучения сделано средствами pandas
from copy import Error
import numpy as np
import pandas as pd
import time 
import math

def set_gen_fr_csv_pd(csv_path):
    # читает csv файл
    # выдает датасет - 2 объекта T1 и T2 длина каждого равна количеству уникальных кейсов
    up_teeth_nums = [18, 17, 16, 15, 14, 13, 12, 11, 21, 22, 23, 24, 25, 26, 27, 28] # Jaw_id = 2 верхняя
    dw_teeth_nums = [48, 47, 46, 45, 44, 43, 42, 41, 31, 32, 33, 34, 35, 36, 37, 38] # Jaw_id = 1 нижняя 

    df = pd.read_csv(csv_path, index_col='id')
    # уберем временно из датафрейма все верхние челюсти и оставим только нижние
    df = df[df['Jaw_id']==1]
    # отфильтруем дичь вида inf, конские значения, откуда там взявшиеся, интересно???
    ul = 100
    dl = -100
    df = df.query(' StartT0_0   < @ul & StartT0_0   > @dl &\
                    StartT0_1   < @ul & StartT0_1   > @dl &\
                    StartT0_2   < @ul & StartT0_2   > @dl &\
                    EndT0_0     < @ul & EndT0_0     > @dl &\
                    EndT0_1     < @ul & EndT0_1     > @dl &\
                    EndT0_2     < @ul & EndT0_2     > @dl &\
                    StartT1_0   < @ul & StartT1_0   > @dl &\
                    StartT1_1   < @ul & StartT1_1   > @dl &\
                    StartT1_2   < @ul & StartT1_2   > @dl &\
                    EndT1_0     < @ul & EndT1_0     > @dl &\
                    EndT1_1     < @ul & EndT1_1     > @dl &\
                    EndT1_2     < @ul & EndT1_2     > @dl &\
                    BCPointT0_0 < @ul & BCPointT0_0 > @dl &\
                    BCPointT0_1 < @ul & BCPointT0_1 > @dl &\
                    BCPointT0_2 < @ul & BCPointT0_2 > @dl &\
                    FAPointT0_0 < @ul & FAPointT0_0 > @dl &\
                    FAPointT0_1 < @ul & FAPointT0_1 > @dl &\
                    FAPointT0_2 < @ul & FAPointT0_2 > @dl &\
                    BCPointT1_0 < @ul & BCPointT1_0 > @dl &\
                    BCPointT1_1 < @ul & BCPointT1_1 > @dl &\
                    BCPointT1_2 < @ul & BCPointT1_2 > @dl &\
                    FAPointT1_0 < @ul & FAPointT1_0 > @dl &\
                    FAPointT1_1 < @ul & FAPointT1_1 > @dl &\
                    FAPointT1_2 < @ul & FAPointT1_2 > @dl')
                    
    # список уникальных кейсов
    cases = df.Case_id.unique()
    # print (f"len cases - {len(cases)} type {type(cases)}") # len cases - 2 type <class 'numpy.ndarray'>
    dataset_t0 = [[[0.00001 for j in range(12)] for tooth in range(16)] for k in range(len(cases))]# раньше было заполнено нулями 
    dataset_t1 = [[[0.00001 for j in range(12)] for tooth in range(16)] for k in range(len(cases))] # и тут тоже
    # перебираем по всем уникальным cases
    for k, case in enumerate(cases):
        # перебираем по всем строкам из датафрейма, с одним и тем же Case_Id    
        subdf = df[df['Case_id']==case]
        for i in range(len(subdf)): # перебираем по части датафрейма где все Case_id = case
            # здесь - один row - это один зуб, надо заполнить челюсть значениями зубов
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
