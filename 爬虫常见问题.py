# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 13:19:19 2016

@author: whenif
"""
'''
#-------------------------------------------------------------#
'''编码处理'''
import urllib.request
import chardet
data = urllib.request.urlopen("http://www.dangdang.com/").read()
decodeData = data.decode("gbk")
dataEncode = decodeData.encode("utf-8","ignore")
decodeData2 = decodeData.encode("GB2312","ignore")
#查看编码格式
import chardet
chardet.detect(data)
#-------------------------------------------------------------#
'''超时与推迟设置'''
#允许超时
data = urllib.request.urlopen(“http://www.dangdang.com/”,timeout=3).read()
#线程推迟（单位为秒）
import time
time.sleep(3)
#-------------------------------------------------------------#
'''异常处理'''
#（1）可捕获所有异常类型
import urllib.request
import urllib.error
import traceback
import sys
try:
    urllib.request.urlopen("http://blog.csdn.net")
except Exception as er1: 
    print("异常概要：")
    print(er1)
    print("---------------------------")
    errorInfo = sys.exc_info()
    print("异常类型："+str(errorInfo[0]))
    print("异常信息或参数："+str(errorInfo[1]))
    print("调用栈信息的对象："+str(errorInfo[2]))
    print("已从堆栈中“辗转开解”的函数有关的信息："+str(traceback.print_exc()))
#--------------------------------------------------
#（2）捕获URLError
import urllib.request
import urllib.error
try:
    urllib.request.urlopen("http://blog.csdn.net")
except urllib.error.URLError as er2: 
    if hasattr(er2,"code"):
        print("URLError异常代码：")
        print(er2.code)
    if hasattr(er2,"reason"):
        print("URLError异常原因：")
        print(er2.reason)
#--------------------------------------------------
#（3）捕获HTTPError
import urllib.request
import urllib.error
try:
    urllib.request.urlopen("http://blog.csdn.net")        
except urllib.error. HTTPError as er3: 
    print("HTTPError异常概要：")
    print(er3)

#-------------------------------------------------------------#    
'''自动模拟HTTP请求'''

import urllib.request
import urllib.parse
def postData():
    '''1_POST方式登录CSDN'''
    values={}
    values['username'] = "xxx@qq.com" #账号
    values['password']="xxx" #密码
    info = urllib.parse.urlencode(values).encode("utf-8")
    url = "http://passport.csdn.net/account/login"
    req = urllib.request.Request(url,info)
    data = urllib.request.urlopen(req).read()
    return data

def getData():   
    '''2_GET方式搜索简书'''
    keyword = "简书" #搜索关键词
    keyword = urllib.request.quote(keyword)#编码
    url = "http://www.baidu.com/s?wd="+keyword
    req = urllib.request.Request(url)
    data = urllib.request.urlopen(req).read()
    return data   

if __name__=="__main__":
    print(postData())
    print(getData()) 
#-------------------------------------------------------------#
'''浏览器伪装'''
#方法1
import urllib.request
url = "http://blog.csdn.net/"
headers=("User-Agent","Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36") 
opener = urllib.request.build_opener() #自定义opener
opener.addheaders = [headers] #添加客户端信息
#urllib.request.install_opener(opener) #如解除注释，则可以使用方法2
try:
    data = opener.open(url,timeout=10).read()  #打开方法1
    #data=urllib.request.urlopen(url).read()  #打开方法2
except Exception as er:
    print("爬取的时候发生错误，具体如下：")
    print(er)
f = open("F:/spider_ret/csdnTest.html","wb") #创建本地HTML文件
f.write(data) #将首页内容写入文件中
f.close()

#方法2
import urllib.request
url = "http://blog.csdn.net/"
req = urllib.request.Request(url)
req.add_header("User-Agent","Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36") #添加报头客户端信息
try:
    data = urllib.request.urlopen(req).read()
except Exception as er:
    print("爬取的时候发生错误，具体如下：")
    print(er)
f = open("F:/spider_ret/csdnTest2.html","wb") #创建本地HTML文件
f.write(data) #将首页内容写入文件中
f.close()
#-------------------------------------------------------------#
'''代理服务器'''
import urllib.request
def use_proxy(url,proxy_addr,iHeaders,timeoutSec):
    '''
    功能：伪装成浏览器并使用代理IP防屏蔽
    @url：目标URL
    @proxy_addr：代理IP地址
    @iHeaders：浏览器头信息
    @timeoutSec：超时设置（单位：秒）
    '''
    proxy = urllib.request.ProxyHandler({"http":proxy_addr})
    opener = urllib.request.build_opener(proxy,urllib.request.HTTPHandler)
    urllib.request.install_opener(opener)
    try:
        req = urllib.request.Request(url,headers = iHeaders)  #伪装为浏览器并封装request
        data = urllib.request.urlopen(req).read().decode("utf-8","ignore")  
    except Exception as er:
        print("爬取时发生错误，具体如下：")
        print(er)
    return data
    
url = "http://www.baidu.com"
proxy_addr = "125.94.0.253:8080"
iHeaders = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 Safari/537.36 SE 2.X MetaSr 1.0"}
timeoutSec = 10
data = use_proxy(url,proxy_addr,iHeaders,timeoutSec)
print(len(data))

#-------------------------------------------------------------#
'''多线程'''
import urllib
from multiprocessing.dummy import Pool
import time
def getResponse(url):
    '''获取响应信息'''
    try:
        req = urllib.request.Request(url)
        res = urllib.request.urlopen(req)
    except Exception as er:
        print("爬取时发生错误，具体如下：")
        print(er)
    return res
def getURLs():
    '''获取所需爬取的所有URL'''
    urls = []
    for i in range(0, 101,20):#每翻一页其start值增加20
        keyword = "科幻"
        keyword = urllib.request.quote(keyword)
        newpage = "https://movie.douban.com/tag/"+keyword+"?start="+str(i)+"&type=T"
        urls.append(newpage)
    return urls    
def singleTime(urls):
    '''单进程计时'''
    time1 = time.time()
    for i in urls:
        print(i)
        getResponse(i) 
    time2 = time.time()
    return str(time2 - time1)   
def multiTime(urls):
    '''多进程计时'''
    pool = Pool(processes=4) #开启四个进程
    time3 = time.time()
    pool.map(getResponse,urls)
    pool.close()
    pool.join() #等待进程池中的worker进程执行完毕
    time4 = time.time()
    return str(time4 - time3)    
if __name__ == '__main__':
    urls = getURLs()
    singleTimes = singleTime(urls) #单线程计时  
    multiTimes = multiTime(urls) #多线程计时
    print('单线程耗时 : ' + singleTimes + ' s')
    print('多线程耗时 : ' + multiTimes + ' s')
