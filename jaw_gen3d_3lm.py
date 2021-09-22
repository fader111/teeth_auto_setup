# новый генератор с 3-мя лендмарками 

import cv2
import numpy as np

import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

# класс который генерит картинки размерностью с искривлениями зубов или без.
# основное отличие - генерятся не картинки с зубами, а данные в виде 
# [[метка][координаты точки начала, длина вектора]]
# вектора в этой версии 3-х мерные, поэтому без opencv в этот раз

np.random.seed() # устанавливает режим случайных чисел без повторений от запуска к запуску

class Landmark_gen():
    ''' creates pictures with MDW, BCP, FAP landmarks '''

    def __init__(self, dim=(200, 200, 200)):
        self.dim = dim

    def image_gen(  self, 
                    name='_', 
                    scale=1, 
                    factor=2.6, 
                    spoiledMDW = False,    # вводит хаотичный наклон и смещение зубов имитируя T1 для лендмарка MDW
                    shiftXMDW = False,     # add random shift for whole tooth for X axis для лендмарка MDW
                    shiftYMDW = False,     # add random shift for whole tooth for Y axis для лендмарка MDW

                ):
        # возвращает 2 вектора - ровных и кореженных зубов 
        # все делаем под разрешение 200x200 
        self.name= name
        self.back = np.zeros(self.dim)            # картинка с ровными зубами
        self.back_spoiled = np.zeros(self.dim)     # картинка с корявыми зубами
        self.factor = factor
        self.out_vector = []                        # вектор лендмарков [x,y,len_x, len_y]
        self.out_vector_spoiled = []                # то же, но искривленные зубы
        center = (self.dim[0]//2, self.dim[1]//2, self.dim[2]//2) # центральная точка на графике
        
        # Генерим Medial Distal Width Line лендмарк
        # строим дугу. так чтобы на основе ее точек можно было зубья подровнять
        # сначала на плоскости, потом по мере добавим изменения координат по оси z
        for i in range(-8, 8): # от зуба к зубу
            
            #### Формируем лендмарк Medial Distal Width line MDW #### 
            
            # в вектор добавляются 3 значения - координаты начальной точки x,y,z,
            # + 3 значения проекций отрезка на оси, всего 6 значений
            # остальные лендмарки просто будут добавляться в хвост.
            
            # строим точки графика 
            z_lev = center[2]         # уровень на котором будет плоскость "окклюзии" в координате z
            # первая точка зуба
            point_mdw = [int(i*scale)+center[0], int(self.duga(i)) + center[1], z_lev] 
            # вторая
            point2_mdw = [int((i+1-0.2)*scale +
                          center[0]), int(self.duga(i+1-0.2)) + center[1], z_lev]
            
            # строим линии по дуге - ровные зубы
            # cv2.line(self.back, point_mdw, point2_mdw, 1, 2)
            # добавляем координаты точек в выдачу
            len_x = point2_mdw[0] - point_mdw[0]
            len_y = point2_mdw[1] - point_mdw[1]
            len_z = 0
            # это теперь будем добавлять в самом конце
            # self.out_vector.append([point_mdw[0], point_mdw[1], point_mdw[2], len_x, len_y, len_z])

            # шатаем зубы если задано шатать и выдаем на картинку back_spoiled
            if spoiledMDW: 
                if i in [-8, -7, -6, 5, 6, 7 ]: # портим моляры 
                    point_mdw[0]+= int((np.random.sample()-1)*i)

                if i in [-5, -4, -3, -2, 1, 2, 3, 4]: # премоляры и резцы
                    point_mdw[1]+= int((np.random.sample()-1)*i*2)

                if i in [-1, 0]: # передние резцы
                    point_mdw[1]+= int((np.random.sample()-1)*4)
            
            if shiftXMDW:
                case_shift_x_ = int((np.random.sample()-1)*5)
                point_mdw[0] += case_shift_x_
                point2_mdw[0] += case_shift_x_
            
            if shiftYMDW:
                case_shift_y_ = int((np.random.sample()-1)*5)
                point_mdw[1] += case_shift_y_
                point2_mdw[1] += case_shift_y_
            
            # для второго вектора делаем покореженные значения. или те-же если корежить не надо
            len_x = point2_mdw[0] - point_mdw[0]
            len_y = point2_mdw[1] - point_mdw[1]
            # добавляем координаты точек в выдачу
            self.out_vector_spoiled.append([point_mdw[0], point_mdw[1], point_mdw[2], len_x, len_y, len_z])
        
            #### Формируем лендмарк Buccal Cusp Points BCP ####

            # в вектор добавляем 3 значения - координаты точки
            # он повторяет точки  MDW с небольшим сдвигом вниз по z и вверх по х
            point_bcp = [int(i*scale)+center[0] - 5, int(self.duga(i)) + center[1], z_lev-5] 
            self.out_vector.append([point_bcp[0], point_bcp[1], point_bcp[2])


        return self.out_vector, self.out_vector_spoiled  


    def duga(self, x):
        ''' returns arc function'''
        return abs(x)**self.factor - self.dim[0] * 0.35

    # @staticmethod
    def draw_pic_fr_vec(self, vec):
        # это осталось из версии 2D возможно придется удалить
        # get landmarks and Draw pictures
        # vec это вектор лендмарка длиной 16, vec[i] = [x,y, x_len, y_len]
        self.pred_pict = np.zeros(self.dim)   
        for i in range(len(vec)):
            x,y, x_len, y_len = vec[i]
            cv2.line(self.pred_pict, (int(x), int(y)), 
                (int(x+x_len), int(y+y_len)), 1, 2)
        
        return self.pred_pict
    
    def draw_3d(self, *args,  show=False):
        # draw 3d pictures in matplotlib
        colors = ['b','r','g']
        titls = ["Train", "T1", "Predicted T2"]
        # mpl.rcParams['legend.fontsize'] = 10
        # n = min([x.shape[0] for x in args]) # сколько столбцов нарисуем
        n = min([len(x) for x in args]) # сколько столбцов нарисуем
        fig = plt.figure(figsize=(3*n, 3*len(args)))
        fig.canvas.set_window_title('AutoSetup ML')

        for j in range(n):
            for i in range(len(args)):
                ax = plt.subplot(len(args), n, i*n + j + 1, title = f'{titls[i]} {j}', projection='3d')
                q= args[i][j] # промежуточная ня чтобы проверить что там челюсть а не труля-ля ля
                for t in q: # 16 зубов * [x,z,z, len_x, len_y, len_z]
                    ax.plot(
                    [t[0],t[0]+t[3]], 
                    [t[1],t[1]+t[4]], 
                    [t[2],t[2]+t[5]], 
                    # label='норм', title=f"{i,j}", color = colors[i])
                    label='норм', color = colors[i])
                
                # ax.title.set_text('My')
                ax.set_xlim(0,     200)
                ax.set_ylim(0,     200)
                ax.set_zlim(96,    104)
                ax.view_init(90, 90)

        plt.show() if show == True else None


if __name__ == "__main__":
    ex = Landmark_gen() 
    # генерируем разные картинки
    m1 = []
    m2 = []
    for i in range(4):  
        scale =  9 + np.random.sample()*3    # 9,3 это для размера 200, для размера 400 - диапазон от 14 до 19 
        factor = 2.2 + np.random.sample()/4   # 2.2, 4 - это для размера 200, для размера 400 - диапазон 2.5 - 2.7  
        name = f"scale {scale:.4}  factor {factor:.3}"
        vec = ex.image_gen(scale=scale, factor=factor, name=name, spoiled=True, shiftX=True, shiftY=True)
        m1.append(vec[0])
        m2.append(vec[1])
        # print (f"vec shape{vec[0][0]}")
        # print (f"vec[0][0]{vec[0][0]}")
    ex.draw_3d(m1, m2, show=True)


