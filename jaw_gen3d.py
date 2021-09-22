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
    ''' creates pictures with MDW and others landmarks '''

    def __init__(self, dim=(200, 200, 200)):
        self.dim = dim

    def image_gen(  self, 
                    name='_', 
                    scale=1, 
                    factor=2.6, 
                    spoiled = False,    # вводит хаотичный наклон и смещение зубов имитируя T1
                    shiftX = False,     # add random shift for whole tooth for X axis
                    shiftY = False,     # add random shift for whole tooth for Y axis
                ):
        # 
        # все делаем под разрешение 200x200 
        self.name= name
        self.back = np.zeros(self.dim)            # картинка с ровными зубами
        self.back_spoiled = np.zeros(self.dim)     # картинка с корявыми зубами
        self.factor = factor
        self.out_vector = []                        # вектор лендмарков [x,y,len_x, len_y]
        self.out_vector_spoiled = []                # то же, но искривленные зубы
        center = (self.dim[0]//2, self.dim[1]//2, self.dim[2]//2) # центральная точка на графике
        
        # строим дугу. так чтобы на основе ее точек можно было зубья подровнять
        # сначала на плоскости, потом по мере добавим изменения координат по оси z
        for i in range(-8, 8):
            # строим точки графика
            # первая точка зуба
            z_lev = center[2]         # уровень на котором будет плоскость "окклюзии" в координате z
            point_ = [int(i*scale)+center[0], int(self.duga(i)) + center[1], z_lev] 
            # вторая
            point2_ = [int((i+1-0.2)*scale +
                          center[0]), int(self.duga(i+1-0.2)) + center[1], z_lev]
            
            # строим линии по дуге - ровные зубы
            # cv2.line(self.back, point_, point2_, 1, 2)
            # добавляем координаты точек в выдачу
            len_x = point2_[0] - point_[0]
            len_y = point2_[1] - point_[1]
            len_z = 0
            self.out_vector.append([point_[0], point_[1], point_[2], len_x, len_y, len_z])

            # шатаем зубы если задано шатать и выдаем на картинку back_spoiled
            if spoiled: 
                if i in [-8, -7, -6, 5, 6, 7 ]: # портим моляры 
                    point_[0]+= int((np.random.sample()-1)*i)

                if i in [-5, -4, -3, -2, 1, 2, 3, 4]: # премоляры и резцы
                    point_[1]+= int((np.random.sample()-1)*i*2)

                if i in [-1, 0]: # передние резцы
                    point_[1]+= int((np.random.sample()-1)*4)
            
            if shiftX:
                case_shift_x_ = int((np.random.sample()-1)*5)
                point_[0] += case_shift_x_
                point2_[0] += case_shift_x_
            
            if shiftY:
                case_shift_y_ = int((np.random.sample()-1)*5)
                point_[1] += case_shift_y_
                point2_[1] += case_shift_y_
            
            # для второй картинки сторим покореженные зубы. или те-же если корежить не надо
            # cv2.line(self.back_spoiled, point_, point2_, 1, 2)
            len_x = point2_[0] - point_[0]
            len_y = point2_[1] - point_[1]
            # добавляем координаты точек в выдачу
            self.out_vector_spoiled.append([point_[0], point_[1], point_[2], len_x, len_y, len_z])
            
            # cv2.circle(self.back, point_, 1, 0.2, 1)
        # print (f"self.back shape {self.back.shape}")
        # выключил тут рисование - рисовать будет другими средствами

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
        # !!! переделать чтобы рисовал любое количество субплотов. 
        # draw 3d pictures in matplotlib
        # vec = [vec_norm, vec_spoiled]
        colors = ['b','g','r']
        # mpl.rcParams['legend.fontsize'] = 10
        # plt.subplot(1,1,1)
        n = min([x.shape[0] for x in args]) # сколько столбцов нарисуем
        # fig = plt.figure(num=self.name, figsize=plt.figaspect(0.5))
        plt.figure(figsize=(2*n, 2*len(args)))
        for j in range(n):
            for i in range(len(args)):
                ax = plt.subplot(len(args), n, i*n + j + 1)
                # q здесь оказывается одномерным массивом
                # а в оригинале каждым аргументом из args является набор картинок. 
                q= args[i][j] # промежуточная ня чтобы проверить что там челюсть а не труля-ля ля
                for t in q: # 16 зубов * [x,z,z, len_x, len_y, len_z]
                    ax.plot(
                    [t[0],t[0]+t[3]], 
                    [t[1],t[1]+t[4]], 
                    [t[2],t[2]+t[5]], 
                    label='норм', color = colors[i])
                
                ax.set_xlim(0,     200)
                ax.set_ylim(0,     200)
                ax.set_zlim(96,    104)
                
        # fig.suptitle('MDWidth')
        # рисуем дугу из отрезков mdw 
        '''
        for i, t in enumerate(vec[0]): # 16 зубов * [x,z,z, len_x, len_y, len_z]
            ax1.plot3D(
                [t[0],t[0]+t[3]], 
                [t[1],t[1]+t[4]], 
                [t[2],t[2]+t[5]], 
                label='норм', color = 'r')
        
        # теперь то же для кореженных зубов
        for i, t in enumerate(vec[1]): # 16 зубов * [x,z,z, len_x, len_y, len_z]
            ax2.plot(
                [t[0],t[0]+t[3]], 
                [t[1],t[1]+t[4]], 
                [t[2],t[2]+t[5]], 
                # label='корежен', color = '#505050')
                label='корежен', color = 'g')
        # fig.legend()
        # вставить надписи для графиков
        '''
        # ax1.view_init(90, 90)
        # ax2.view_init(90, 90)
        plt.show() if show == True else None


if __name__ == "__main__":
    ex = Landmark_gen() 
    # генерируем разные картинки
    for i in range(1):  
        scale =  9 + np.random.sample()*3    # 9,3 это для размера 200, для размера 400 - диапазон от 14 до 19 
        factor = 2.2 + np.random.sample()/4   # 2.2, 4 - это для размера 200, для размера 400 - диапазон 2.5 - 2.7  
        name = f"scale {scale:.4}  factor {factor:.3}"
        vec = ex.image_gen(scale=scale, factor=factor, name=name, spoiled=True, shiftX=True, shiftY=True)
        # print (f"vec shape{vec[0][0]}")
        ex.draw_3d(vec, show=True)


