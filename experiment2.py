
# coding: utf-8
import re
import pymysql
import re
import csv
import codecs
import sys 
import networkx as nx
import matplotlib.pyplot as plt
# reload(sys)
# sys.setdefaultencoding('utf8')
import networkx as nx
G=nx.Graph()

def generate_only_nodes():
    conn = pymysql.connect(host='localhost',port = 3306,user='root',passwd='root',db ='nationalnet',charset='utf8')
    cur = conn.cursor()
    sql_str="select name from optical_fibre where PAR_ZONE='0CF3663A-EB41-4DF9-9061-D27EDA049BFD-00020' limit 2,300"
    cur.execute(sql_str)

    rows = cur.fetchall()
    # csvfile = file(u'D:\\repo\\nationalnet_data\\csv1.csv', 'wb')
    # csvfile.write(codecs.BOM_UTF8)
    # writer=csv.writer(csvfile)
    data=[]
    for r in rows:
        s=re.split(u'\\(|～|\\)',r[0])
        if len(s)<3:
            continue
        data.append((s[1],s[2]))
        print(s[1],s[2])
    # writer.writerows(data)
    # csvfile.close()

def draw_network():
    conn = pymysql.connect(host='localhost',port = 3306,user='root',passwd='root',db ='nationalnet',charset='utf8')
    cur = conn.cursor()
    sql_str="select name from optical_fibre where PAR_ZONE='0CF3663A-EB41-4DF9-9061-D27EDA049BFD-00020' limit 2,300"
    cur.execute(sql_str)

    rows = cur.fetchall()
    #csvfile = file(u'D:\\repo\\nationalnet_data\\csv1.csv', 'wb')
    #csvfile.write(codecs.BOM_UTF8)
    #writer=csv.writer(csvfile)
    data=[]
    for r in rows:
        s=re.split(u'\(|～|\\)',r[0])
        if len(s)<3:
            continue
        data.append((s[1],s[2]))
        print(s[1],s[2])

    G=nx.Graph()
    for e in data:
        G.add_edge(*e)
    
    for k in nx.degree(G):
        print(k,nx.degree(G)[k])
    nx.draw_random(G,node_shape = 'o',node_size=10) #画出图G
    plt.show()
    
class TestAll(object):
    def __init__(self):
        pass

    def test_generate_only_nodes(self):
        generate_only_nodes()
        
    def test_draw_network(self):
        draw_network()
myTest=TestAll()
myTest.test_draw_network()



