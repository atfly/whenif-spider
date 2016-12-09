# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 13:19:19 2016

@author: whenif
"""
'''������������������ȡ'''
import urllib
import re
import xlsxwriter
import MySQLdb
#-----------------(1)�洢��excel��txt-------------------------#
def gxls_concent(target_url,pat):
    '''
    ���ܣ���ȡ����
    @target_url����ȡĿ����ַ
    @pat�����ݹ���ģʽ
    '''
    data = urllib.request.urlopen(target_url).read()
    ret_concent = re.compile(pat).findall(str(data,'utf-8'))
    return ret_concent
def wxls_concent(ret_xls,ret_concent):
    '''
    ���ܣ������ս��д��douban.xls��
    @ret_xls�����ս���洢excel���·��
    @ret_concent����ȡ���ݽ���б�
    '''
    # ������д����ļ�
    wb1 = xlsxwriter.Workbook(ret_xls)
    # ����һ��sheet��������
    ws = wb1.add_worksheet()
    try:
        for i in range(len(ret_concent)):
            data = ret_concent[i]
            ws.write(i,0,data)
        wb1.close()
    except Exception as er:
        print('д�롰'+ret_xls+'���ļ�ʱ���ִ���')
        print(er)    
def wtxt_concent(ret_txt,ret_concent):
    '''
    ���ܣ������ս��д��douban.txt��
    @ret_xls�����ս���洢excel���·��
    @ret_concent����ȡ���ݽ���б�
    '''
    fh = open(ret_txt,"wb")
    try:
        for i in range(len(ret_concent)):
            data = ret_concent[i]
            data = data+"\r\n"
            data = data.encode()
            fh.write(data)
    except Exception as er:
        print('д�롰'+ret_txt+'���ļ�ʱ���ִ���')
        print(er)  
    fh.close()
def mainXlsTxt():
    '''
    ���ܣ������ݴ洢��excel����
    '''
    target_url = 'https://read.douban.com/provider/all'  # ��ȡĿ����ַ
    pat = '<div class="name">(.*?)</div>' # ��ȡģʽ
    ret_xls = "F:/spider_ret/douban.xls"   # excel�ļ�·��
    ret_txt = "F:/spider_ret/douban.txt"   # txt�ļ�·��
    ret_concent = gxls_concent(target_url,pat) # ��ȡ����
    wxls_concent(ret_xls,ret_concent) # д��excel��
    wtxt_concent(ret_txt,ret_concent) # д��txt�ļ�  
#---------------------END(1)--------------------------------#
#-------------------(2)�洢��MySQL---------------------------#
def db_con():
    '''
    ���ܣ�����MySQL���ݿ�
    '''
    con = MySQLdb.connect(
        host='localhost',  # port
        user='root',       # usr_name
        passwd='xxxx',     # passname
        db='urllib_data',  # db_name
        charset='utf8',
        local_infile = 1
        )
    return con   
def exeSQL(sql):
    '''
    ���ܣ����ݿ��ѯ���� 
    @sql������SQL���
    '''
    print("exeSQL: " + sql)
    #�������ݿ�
    con = db_con()
    con.query(sql)   
def gdb_concent(target_url,pat):
    '''
    ���ܣ�ת����ȡ����Ϊ�������ݿ��ʽ:[[value_1],[value_2],...,[value_n]]
    @target_url����ȡĿ����ַ
    @pat�����ݹ���ģʽ
    '''
    tmp_concent = gxls_concent(target_url,pat)
    ret_concent = []   
    for i in range(len(tmp_concent)):
        ret_concent.append([tmp_concent[i]])
    return ret_concent
def wdb_concent(tbl_name,ret_concent):
    '''
    ���ܣ�����ȡ���д��MySQL���ݿ���
    @tbl_name�����ݱ���
    @ret_concent����ȡ���ݽ���б�
    '''
    exeSQL("drop table if exists " + tbl_name)
    exeSQL("create table " + tbl_name + "(pro_name VARCHAR(100));")
    insert_sql = "insert into " + tbl_name + " values(%s);"
    con = db_con()
    cursor = con.cursor()
    try:
        cursor.executemany(insert_sql,ret_concent)
    except Exception as er:
        print('ִ��MySQL��"' + str(insert_sql) + '"ʱ����')        
        print(er)
    finally:
        cursor.close()        
        con.commit() 
        con.close()
def mainDb():
    '''
    ���ܣ������ݴ洢��MySQL���ݿ���
    '''
    target_url = 'https://read.douban.com/provider/all'  # ��ȡĿ����ַ
    pat = '<div class="name">(.*?)</div>' # ��ȡģʽ
    tbl_name = "provider" # ���ݱ���
    # ��ȡ����
    ret_concent = gdb_concent(target_url,pat)
    # д��MySQL���ݿ�
    wdb_concent(tbl_name,ret_concent)  
#---------------------END(2)--------------------------------#
if __name__ == '__main__':
    mainXlsTxt()
    mainDb()