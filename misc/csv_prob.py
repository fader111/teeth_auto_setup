import csv
import numpy as np
import sqlite3, pandas as pd

fpath = 'C:\\Users\\Anton\\Projects\\jaw_encoder\\csv\\input (004).csv'
fpath = 'C:\\Users\\Anton\\Projects\\jaw_encoder\\csv\\test1.csv'
reader = None
with open(fpath, newline='') as csvfile:
    # reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    reader = csv.reader(csvfile)
    for i, row in enumerate(reader):
        
        # print (f"{row}") if ('id' or 'Tooth') in row else None
        # print (f"{row}") if False else None
        # print(', '.join(row))
        if i>3:
            break


# TODO сделать надо так чтобы из файла csv все попало в выходную структуру класса

class CsvParser:
    # берет файл csv и конвертит его 
    # формат выходных данных: out_vector см ниже
    # формат входных данныХ: 
    '''
    id,Case_id,Jaw_id,Tooth,

    StartT0_0,StartT0_1,StartT0_2,   EndT0_0,EndT0_1,EndT0_2,
    StartT1_0,StartT1_1,StartT1_2,   EndT1_0,EndT1_1,EndT1_2,

    BCPointT0_0,BCPointT0_1,BCPointT0_2,
    FAPointT0_0,FAPointT0_1,FAPointT0_2,

    BCPointT1_0,BCPointT1_1,BCPointT1_2,
    FAPointT1_0,FAPointT1_1,FAPointT1_2,

    LastFrameNumber'
    '''
    def __init__(self, csv_f= None):
        fpath = 'C:\\Users\\Anton\\Projects\\jaw_encoder\\csv\\input (004).csv'
        if csv_f == None:
            csv_f = fpath
        
        self.out_vector = [] # вектор лендмарков - сначала mdw xyz, длины mdw x,y,z, потом точки bcp и fap
        self.out_vector_spoiled = []                # то же, но искривленные зубы
        # инициируем все точки лендмарков 
        point_mdw_t1, point2_mdw_t1, len_x_t1, len_y_t1, len_z_t1, \
            point_bcp_t1, point_fap_t1 =        [0,0,0], [0,0,0], 0,0,0, [0,0,0], [0,0,0]
        # то же для точек T2
        point_mdw_s_t2, point2_mdw_s_t2, len_x_s_t2, len_y_s_t2, len_z_s_t2, \
            point_bcp_s_t2, point_fap_s_t2 =    [0,0,0], [0,0,0], 0,0,0, [0,0,0], [0,0,0]
        
        reader = None
        with open(fpath, newline='') as csvfile:
            # reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            self.reader = csv.reader(csvfile)
        # print (f"reader{reader}") # возвращает объект 
        
    def set_gen_OLD(self):
        # выдает 2 списка челюстей T1 и T2     
        self.dataset_t1, self.dataset_t2 = [np.array([]) for i in [0,1]] 
        # гребем по строкам файла csv
        for ind, row in enumerate(reader):
            if ('id' or 'Case_id') in row: # пропуск первой строчки, CAseId просто для страховки, одного Id достаточно
                continue
            # начинаем набивать данными точки - и тут проблема. в файле много челюстей \
            # а уменя генератор выдает 2 объекта для одной челюсти. 
            # Q - КАк быть?
            # A - сделать 2 метода, один будет выдавать 2 объекта одной челючти, 
            #       а другой все кейсы. в каком формате - надо подумать. 
            # Q - В каком формате этот второй метод будет выдавать объекты?
            # A - в таком чтоб было удобно встроить в существующий алгоритм:
            #       в цикле по числу кейсов делать dataset_vec.append(vec)
            # пусть на выходе у него будут 2 массива - T1 и T2
            # далее в каждой строке массив с чиселками в виде строк. мляя
            
        return None # self.dataset_t1, self.dataset_t2    

    def set_gen(self):
        # выдает датасет - 2 объекта T1 и T2
        con = sqlite3.connect(":memory:") # change to 'sqlite:///your_filename.db'
        df = pd.read_csv(fpath)
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
            print (f"{lower_jaw_t0} len{len(lower_jaw_t0)}")
            # print (f"\n\n")
            print (f"{lower_jaw_t1} len{len(lower_jaw_t1)}")
            # print (f"caseId{CaseId}") 
        return lower_jaw_t0, lower_jaw_t1


    def image_gen(self):
        # возвращает 2 файла - T1 и T2
        
        return self.out_vector, self.out_vector_spoiled

# print (f"reader {next(reader)}")

a= CsvParser()
a.set_gen()
