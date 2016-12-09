# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 13:19:19 2016

@author: whenif
"""
'''
#-------------------------------------------------------------#
'''���봦��'''
import urllib.request
import chardet
data = urllib.request.urlopen("http://www.dangdang.com/").read()
decodeData = data.decode("gbk")
dataEncode = decodeData.encode("utf-8","ignore")
decodeData2 = decodeData.encode("GB2312","ignore")
#�鿴�����ʽ
import chardet
chardet.detect(data)
#-------------------------------------------------------------#
'''��ʱ���Ƴ�����'''
#����ʱ
data = urllib.request.urlopen(��http://www.dangdang.com/��,timeout=3).read()
#�߳��Ƴ٣���λΪ�룩
import time
time.sleep(3)
#-------------------------------------------------------------#
'''�쳣����'''
#��1���ɲ��������쳣����
import urllib.request
import urllib.error
import traceback
import sys
try:
    urllib.request.urlopen("http://blog.csdn.net")
except Exception as er1: 
    print("�쳣��Ҫ��")
    print(er1)
    print("---------------------------")
    errorInfo = sys.exc_info()
    print("�쳣���ͣ�"+str(errorInfo[0]))
    print("�쳣��Ϣ�������"+str(errorInfo[1]))
    print("����ջ��Ϣ�Ķ���"+str(errorInfo[2]))
    print("�ѴӶ�ջ�С�շת���⡱�ĺ����йص���Ϣ��"+str(traceback.print_exc()))
#--------------------------------------------------
#��2������URLError
import urllib.request
import urllib.error
try:
    urllib.request.urlopen("http://blog.csdn.net")
except urllib.error.URLError as er2: 
    if hasattr(er2,"code"):
        print("URLError�쳣���룺")
        print(er2.code)
    if hasattr(er2,"reason"):
        print("URLError�쳣ԭ��")
        print(er2.reason)
#--------------------------------------------------
#��3������HTTPError
import urllib.request
import urllib.error
try:
    urllib.request.urlopen("http://blog.csdn.net")        
except urllib.error. HTTPError as er3: 
    print("HTTPError�쳣��Ҫ��")
    print(er3)

#-------------------------------------------------------------#    
'''�Զ�ģ��HTTP����'''

import urllib.request
import urllib.parse
def postData():
    '''1_POST��ʽ��¼CSDN'''
    values={}
    values['username'] = "xxx@qq.com" #�˺�
    values['password']="xxx" #����
    info = urllib.parse.urlencode(values).encode("utf-8")
    url = "http://passport.csdn.net/account/login"
    req = urllib.request.Request(url,info)
    data = urllib.request.urlopen(req).read()
    return data

def getData():   
    '''2_GET��ʽ��������'''
    keyword = "����" #�����ؼ���
    keyword = urllib.request.quote(keyword)#����
    url = "http://www.baidu.com/s?wd="+keyword
    req = urllib.request.Request(url)
    data = urllib.request.urlopen(req).read()
    return data   

if __name__=="__main__":
    print(postData())
    print(getData()) 
#-------------------------------------------------------------#
'''�����αװ'''
#����1
import urllib.request
url = "http://blog.csdn.net/"
headers=("User-Agent","Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36") 
opener = urllib.request.build_opener() #�Զ���opener
opener.addheaders = [headers] #��ӿͻ�����Ϣ
#urllib.request.install_opener(opener) #����ע�ͣ������ʹ�÷���2
try:
    data = opener.open(url,timeout=10).read()  #�򿪷���1
    #data=urllib.request.urlopen(url).read()  #�򿪷���2
except Exception as er:
    print("��ȡ��ʱ�������󣬾������£�")
    print(er)
f = open("F:/spider_ret/csdnTest.html","wb") #��������HTML�ļ�
f.write(data) #����ҳ����д���ļ���
f.close()

#����2
import urllib.request
url = "http://blog.csdn.net/"
req = urllib.request.Request(url)
req.add_header("User-Agent","Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36") #��ӱ�ͷ�ͻ�����Ϣ
try:
    data = urllib.request.urlopen(req).read()
except Exception as er:
    print("��ȡ��ʱ�������󣬾������£�")
    print(er)
f = open("F:/spider_ret/csdnTest2.html","wb") #��������HTML�ļ�
f.write(data) #����ҳ����д���ļ���
f.close()
#-------------------------------------------------------------#
'''���������'''
import urllib.request
def use_proxy(url,proxy_addr,iHeaders,timeoutSec):
    '''
    ���ܣ�αװ���������ʹ�ô���IP������
    @url��Ŀ��URL
    @proxy_addr������IP��ַ
    @iHeaders�������ͷ��Ϣ
    @timeoutSec����ʱ���ã���λ���룩
    '''
    proxy = urllib.request.ProxyHandler({"http":proxy_addr})
    opener = urllib.request.build_opener(proxy,urllib.request.HTTPHandler)
    urllib.request.install_opener(opener)
    try:
        req = urllib.request.Request(url,headers = iHeaders)  #αװΪ���������װrequest
        data = urllib.request.urlopen(req).read().decode("utf-8","ignore")  
    except Exception as er:
        print("��ȡʱ�������󣬾������£�")
        print(er)
    return data
    
url = "http://www.baidu.com"
proxy_addr = "125.94.0.253:8080"
iHeaders = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 Safari/537.36 SE 2.X MetaSr 1.0"}
timeoutSec = 10
data = use_proxy(url,proxy_addr,iHeaders,timeoutSec)
print(len(data))

#-------------------------------------------------------------#
'''���߳�'''
import urllib
from multiprocessing.dummy import Pool
import time
def getResponse(url):
    '''��ȡ��Ӧ��Ϣ'''
    try:
        req = urllib.request.Request(url)
        res = urllib.request.urlopen(req)
    except Exception as er:
        print("��ȡʱ�������󣬾������£�")
        print(er)
    return res
def getURLs():
    '''��ȡ������ȡ������URL'''
    urls = []
    for i in range(0, 101,20):#ÿ��һҳ��startֵ����20
        keyword = "�ƻ�"
        keyword = urllib.request.quote(keyword)
        newpage = "https://movie.douban.com/tag/"+keyword+"?start="+str(i)+"&type=T"
        urls.append(newpage)
    return urls    
def singleTime(urls):
    '''�����̼�ʱ'''
    time1 = time.time()
    for i in urls:
        print(i)
        getResponse(i) 
    time2 = time.time()
    return str(time2 - time1)   
def multiTime(urls):
    '''����̼�ʱ'''
    pool = Pool(processes=4) #�����ĸ�����
    time3 = time.time()
    pool.map(getResponse,urls)
    pool.close()
    pool.join() #�ȴ����̳��е�worker����ִ�����
    time4 = time.time()
    return str(time4 - time3)    
if __name__ == '__main__':
    urls = getURLs()
    singleTimes = singleTime(urls) #���̼߳�ʱ  
    multiTimes = multiTime(urls) #���̼߳�ʱ
    print('���̺߳�ʱ : ' + singleTimes + ' s')
    print('���̺߳�ʱ : ' + multiTimes + ' s')
