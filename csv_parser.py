import csv
import numpy as np
import sqlite3 
import pandas as pd

def set_gen(csv_path):
    # читает csv файл
    # выдает датасет - 2 объекта T1 и T2 длина каждого равна количеству уникальных кейсов
    con = sqlite3.connect(":memory:") # change to 'sqlite:///your_filename.db'
    df = pd.read_csv(csv_path)
    df.to_sql("bases", con, if_exists='replace', index=False)
    cur = con.cursor()

    up_teeth_nums = [18, 17, 16, 15, 14, 13, 12, 11, 21, 22, 23, 24, 25, 26, 27, 28] # Jaw_id = 2
    dw_teeth_nums = [48, 47, 46, 45, 44, 43, 42, 41, 31, 32, 33, 34, 35, 36, 37, 38] # Jaw_id = 1
    cases = []    
    # узнаем какие Case_id есть в файле и фиксим их в cases
    # возможно это надо будет оптимизировать, написав более хитрый запрос к базе
    for row in cur.execute(f'SELECT Case_Id FROM bases '):
        cases.append(row[0])
    cases_set = set(cases) # тут лежат номера кейсов их файла
    # print (f"cs {cases_set}")

    # перебираемся по Case_Id - т.е. формируем челюсть Jaw_id = 1- нижняя челюсть. 2- верхняя
    for CaseId in cases_set:
        # тут на каждом шаге мы формируем 1 челюсть - нижнюю. (или 2 позже)
        # upper_jaw = [[] for i in range(16)]
        lower_jaw_t0 = [[None for j in range(12)] for i in range(16)]
        lower_jaw_t1 = [[None for j in range(12)] for i in range(16)]
        for row in cur.execute(f'SELECT * FROM bases WHERE Case_Id = {CaseId} AND Jaw_id = 1 ORDER BY Id'):
            # здесь - один row - это один зуб, надо заполнить челюсть значениями зубов
            # print(row) (42, 3, 1, 47, -25.357, 32.1696, 0.29188, -26.4387, 40.1274, -0.1345 ........ 
            # есть массив dw_tees_nums с номерами зубов. и есть челюсть lower_jaw c нулевыми списками вместо зубов. 
            # теперь берем номер зуба из row и ставим этот зуб по индексу из dw_teeth в lower_jaw. 
            # Те зубы которые есть в кейсе, вставятся в челюсть, остальные останутся списками с нулями (None).
            # и это нужно так для конвертации в np
            # номер зуба в row - 4-й по счету, имеет индекс 3. Начиная с 4-го индекса идут значения лендмарков.
            ind = dw_teeth_nums.index(row[3])
            lower_jaw_t0[ind] = row[4:10] + row[16:22] # получается микс списков и туплей, но роде для np это пох
            lower_jaw_t1[ind] = row[10:16] + row[22:28] 
        # print (f"{lower_jaw_t0} len{len(lower_jaw_t0)}")
        # print (f"\n\n")
        # print (f"{lower_jaw_t1} len{len(lower_jaw_t1)}")
        # print (f"caseId{CaseId}") 
    return lower_jaw_t0, lower_jaw_t1
