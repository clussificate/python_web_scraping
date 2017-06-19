import pandas
data = pandas.read_csv('Dataout.csv',encoding='utf-8')
print(data[data.columns[1:]])