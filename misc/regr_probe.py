from pylab import *	
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras import optimizers

#Generate dummy data
data = data = linspace(1,2,100).reshape(-1,1)
y = data*5

#Define the model
def baseline_model():
   model = Sequential()
   model.add(Dense(1, activation = 'linear', input_dim = 1))
#    model.add(Dense(1, activation = 'relu', input_dim = 1)) # ничего не предсказывает
#    model.compile(optimizer = 'rmsprop', loss = 'mean_squared_error', metrics = ['accuracy'])
   model.compile(optimizer=optimizers.RMSprop(learning_rate=0.1), loss='mean_squared_error', metrics=['mae'])
   return model


#Use the model
regr = baseline_model()
regr.fit(data,y,epochs =200,batch_size = 32)
plt.plot(data, regr.predict(data), 'r', data,y, 'k.')
plt.show()

