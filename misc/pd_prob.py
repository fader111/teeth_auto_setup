
import pandas as pd
import numpy as np

df = pd.DataFrame({"name": ['Alfred', 'Batman', 'Catwoman'],
                   "toy": [np.nan, 'Batmobile', 'Bullwhip'],
                   "born": [pd.NaT, pd.Timestamp("1940-04-25"),
                            pd.NaT]})

df

# df.dropna()

# Выбор тех строк, чье значение столбца присутствует в списке, с помощью метода isin() информационного кадра.
# Код № 1: Выбор всех строк в данном кадре данных, в которых «Поток» присутствует в списке опций, с использованием базового метода.
record = {
  'Name': ['Ankit', 'Amit', 'Aishwarya', 'Priyanka', 'Priya', 'Shaurya'],
  'Age': [21, 19, 20, 18, 17, 21],
  'Stream': ['Math', 'Commerce', 'Science', 'Math', 'Math', 'Science'],
  'Percentage': [88, 92, 95, 70, 65, 78]}
  
dataframe = pd.DataFrame(record, columns = ['Name', 'Age', 'Stream', 'Percentage'])
# print("Given Dataframe :\n", dataframe) 
# Given Dataframe :
#          Name  Age    Stream  Percentage
# 0      Ankit   21      Math          88
# 1       Amit   19  Commerce          92
# 2  Aishwarya   20   Science          95
# 3   Priyanka   18      Math          70
# 4      Priya   17      Math          65
# 5    Shaurya   21   Science          78

options = ['Math', 'Commerce']

# выбор строк на основе условия
rslt_df = dataframe[dataframe['Stream'].isin(options)]
# print('\nResult dataframe :\n', rslt_df)

# Result dataframe :
#         Name  Age    Stream  Percentage
# 0     Ankit   21      Math          88
# 1      Amit   19  Commerce          92
# 3  Priyanka   18      Math          70
# 4     Priya   17      Math          65


# создание фрейма данных из CSV-файла
# data = pd.read_csv("jaw_encoder/csv/nba.csv", index_col ="Name")
# print (f"data\n{data}")  
# извлечение строки методом loc
# first = data.loc["Avery Bradley"]
# second = data.loc["R.J. Hunter"]

# print(first, "\n\n\n", second)
csv_path = 'C:\\Users\\Anton\\Projects\\jaw_encoder\\csv\\test1.csv' 
df = pd.read_csv(csv_path, index_col='id')
for i in [1]:#df.index-1:
  subdf = df[df['Case_id']==7]
  print (f"{subdf}")
  # print (f"{df[df['Case_id']==7].iloc[i].tolist()}")
len(df)



