import pandas as pd
import numpy as np

fname = 'jaw_encoder/csv/test1.csv'

# Определить словарь, содержащий данные о сотрудниках

data = {'Name':['Jai', 'Princi', 'Conna', 'Anuj'],
        'Age':[45, 10, 20, 300],
        'Address':['Delhi', 'Kanpur', 'Allahabad', 'Kannauj'],
        'Qualification':['Msc', 'MA', 'MCA', 'Phd'], 
        'Cage':[11,33,66,99]}
  
# Конвертировать словарь в DataFrame
df = pd.DataFrame(data)
  
# выбрать два столбца
# print(df[['Name', 'Qualification']])
# print(df.Name.unique())s
print (f"{df['Cage'].between(20, 45)}")

