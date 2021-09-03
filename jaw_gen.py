import cv2
import numpy as np

red = (0, 0, 255)
white = (255, 255, 255)

# print(f" cv2 ver. {cv2.__version__}, np ver. {np.__version__}")
np.random.seed() # устанавливает режим случайных чисел без повторений от запуска к запуску

class Landmark_gen():
    ''' creates pictures with incistor edges landmarks '''

    def __init__(self, number=100, dim=(200, 200), x_axes=(-10, 10), y_axes=(-200, 10)):
        self.number = number
        self.dim = dim
        self.x_axes = x_axes
        self.y_axes = y_axes

    def image_gen(  self, 
                    name='_', 
                    scale1=1, 
                    factor=2.6, 
                    shift_x=0, 
                    shift_y=0, 
                    spoiled = False,    # вводит хаотичный наклон и смещение зубов имитируя T1
                    shiftX = False,     # add random shift for whole tooth for X axis
                    shiftY = False,     # add random shift for whole tooth for Y axis
                    show=False):
        # встроить сюда еще смещение 
        # все делаем под разрешение 200x200 
        self.back = np.zeros((200, 200))            # картинка с ровными зубами
        self.back_spoiled = np.zeros((200,200))     # картинка с корявыми зубами
        self.factor = factor
        center = (100, 100)

        # оси координат по центру
        if 1:
            cv2.line(self.back, (0, center[1]), (200, center[1]), 0.4, 1)
            cv2.line(self.back, (center[0], 0), (center[0], 200), 0.4, 1)
            cv2.line(self.back_spoiled, (0, center[1]), (200, center[1]), 0.4, 1)
            cv2.line(self.back_spoiled, (center[0], 0), (center[0], 200), 0.4, 1)

        # строим дугу. так чтобы на основе ее точек можно было зубья подровнять
        for i in range(-8, 8):
            # строим точки графика
            # первая точка зуба
            point_ = [int(i*scale1)+center[0], int(self.duga(i)) + center[1]]
            # вторая
            point2_ = [int((i+1-0.2)*scale1 +
                          center[0]), int(self.duga(i+1-0.2)) + center[1]]
            
            # строим линии по дуге - ровные зубы
            cv2.line(self.back, point_, point2_, 1, 2)

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
            cv2.line(self.back_spoiled, point_, point2_, 1, 2)
            
            # cv2.circle(self.back, point_, 1, 0.2, 1)
        # print (f"self.back shape {self.back.shape}")

        if show: # shows picture. beware using in batсh processing
            self.back = cv2.resize(self.back, self.dim)  # увеличиваем только для показа
            self.back_spoiled = cv2.resize(self.back_spoiled, self.dim)  # увеличиваем только для показа
            img_for_show = np.hstack((self.back, self.back_spoiled))
            cv2.imshow(name, img_for_show)
            k = cv2.waitKey()

        return self.back, self.back_spoiled  

    def duga(self, x):
        ''' returns arc function'''
        return abs(x)**self.factor - 200 * 0.35


if __name__ == "__main__":
    ex = Landmark_gen(dim=(400, 400)) 
    # генерируем разные картинки
    for i in range(30):  
        scale =  9 + np.random.sample()*3    # 9,3 это для размера 200, для размера 400 - диапазон от 14 до 19 
        factor = 2.2 + np.random.sample()/4   # 2.2, 4 - это для размера 200, для размера 400 - диапазон 2.5 - 2.7  
        name = f"scale {scale:.4}  factor {factor:.3}"
        ex.image_gen(show=True, scale1=scale, factor=factor, name=name, spoiled=True, shiftX=True, shift_y=True)
        # print(scale, factor)
