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
                    spoiled = False, # вводит хаотичный наклон и смещение зубов имитируя T1
                    show=False):
        # встроить сюда еще смещение 
        # все делаем под разрешение 200x200 потом ресайз
        self.back = np.zeros((200, 200))
        self.factor = factor
        center = (100, 100)

        # оси координат по центру
        cv2.line(self.back, (0, center[1]), (200, center[1]), 0.4, 1)
        cv2.line(self.back, (center[0], 0), (center[0], 200), 0.4, 1)

        # строим дугу. так чтобы на основе ее точек можно было зубья подровнять
        for i in range(-8, 8):
            # строим точки графика
            # первая точка зуба
            point_ = [int(i*scale1)+center[0], int(self.duga(i)) + center[1]]
            # вторая
            point2_ = [int((i+1-0.2)*scale1 +
                          center[0]), int(self.duga(i+1-0.2)) + center[1]]
            
            if spoiled: # шатаем зубы если задано шатать
                
                if i in [-8, -7, -6, 5, 6, 7 ]: # портим моляры 
                    point_[0]+= int((np.random.sample()-1)*i)

                if i in [-5, -4, -3, -2, 1, 2, 3, 4]: # премоляры и резцы
                    point_[1]+= int((np.random.sample()-1)*i*2)

                if i in [-1, 0]: # передние резцы
                    point_[1]+= int((np.random.sample()-1)*4)

            # cv2.circle(self.back, point_, 1, 0.2, 1)

            # строим линии между точками - они же лендмарки
            cv2.line(self.back, point_, point2_, 1, 2)
        # print (f"self.back shape {self.back.shape}")

        if show: # shows picture. beware using in batсh processing
            self.back = cv2.resize(self.back, self.dim)  # увеличиваем только для показа
            cv2.imshow(name, self.back)
            k = cv2.waitKey()

        return self.back  

    def duga(self, x):
        ''' returns arc function'''
        return abs(x)**self.factor - 200*0.35


if __name__ == "__main__":
    ex = Landmark_gen(dim=(400, 400)) 
    # генерируем разные картинки
    for i in range(30):  
        scale =  9 + np.random.sample()*3     # это для размера 200, диапазон от 14 до 19 для размера 400
        factor = 2.2 + np.random.sample()/4   # это для размера 200, диапазон 2.5 - 2.7 для размера 400 
        name = f"scale {scale:.4}  factor {factor:.3}"
        ex.image_gen(show=True, scale1=scale, factor=factor, name=name, spoiled=True)
        # print(scale, factor)
