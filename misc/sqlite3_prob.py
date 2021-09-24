import csv, sqlite3, pandas as pd

fpath = 'C:\\Users\\Anton\\Projects\\jaw_encoder\\csv\\test1.csv'
fpath = 'C:\\Users\\Anton\\Projects\\jaw_encoder\\csv\\input (004).csv'

'''
# db_fname = 'sqlite:///data.db'
con = sqlite3.connect(":memory:") # change to 'sqlite:///your_filename.db'
cur = con.cursor()
cur.execute("CREATE TABLE t (Id, CaseId);") # use your column names here

with open(fpath,'r') as fin: # `with` statement available in 2.5+
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [(i[Id], i['CaseId']) for i in dr]

cur.executemany("INSERT INTO t (Id, CaseId) VALUES (?, ?);", to_db)
con.commit()
con.close()
'''
con = sqlite3.connect(":memory:") # change to 'sqlite:///your_filename.db'
df = pd.read_csv(fpath)
df.to_sql("bases", con, if_exists='replace', index=False)
cur = con.cursor()

id =7
up_tees_nums = [18, 17, 16, 15, 14, 13, 12, 11, 21, 22, 23, 24, 25, 26, 27, 28] # Jaw_id = 2
dw_tees_nums = [48, 47, 46, 45, 44, 43, 42, 41, 31, 32, 33, 34, 35, 36, 37, 38] # Jaw_id = 1

# перебираемся по Case_Id - т.е. формируем челюсть Jaw_id = 1- нижняя челюсть. 2- верхняя
for row in cur.execute(f'SELECT * FROM bases WHERE Case_Id = {id} AND Jaw_id = 1 ORDER BY Id'):
    print(row)
    # тут есть затык с зубами и надо подумать что с этим делать. 
    pass