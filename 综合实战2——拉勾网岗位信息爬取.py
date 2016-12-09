```
import urllib.request
import urllib.parse
import socket
from multiprocessing.dummy import Pool
import json
import time
import xlsxwriter
#----------------------------------------------------------#
###
###��1����ȡ����IP
###
def getProxies():
    '''
    ���ܣ�����API��ȡԭʼ����IP��
    '''
    url = "http://api.xicidaili.com/free2016.txt"
    i_headers={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 Safari/537.36 SE 2.X MetaSr 1.0"}
    global proxy_addr
    proxy_addr = []
    try:
        req = urllib.request.Request(url,headers = i_headers)
        proxy = urllib.request.urlopen(req).read()
        proxy = proxy.decode('utf-8')
        proxy_addr = proxy.split('\r\n')  #���÷ָ���Ϊ���з�
    except Exception as er:
        print(er)
    return proxy_addr   
def testProxy(curr_ip):
    '''
    ���ܣ����ðٶ���ҳ�������֤����IP����Ч��
    @curr_ip����ǰ����֤��IP
    '''
    socket.setdefaulttimeout(5)  #����ȫ�ֳ�ʱʱ��
    tarURL = "https://www.baidu.com/"  #������ַ
    proxy_ip = []
    try:
        proxy_support = urllib.request.ProxyHandler({"http":curr_ip})
        opener = urllib.request.build_opener(proxy_support)
        opener.addheaders=[("User-Agent","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 Safari/537.36 SE 2.X MetaSr 1.0")]
        urllib.request.install_opener(opener)
        res = urllib.request.urlopen(tarURL).read()
        proxy_ip.append(curr_ip)
        print(len(res))
    except Exception as er:
        print("��֤����IP��"+curr_ip+"��ʱ��������"+er)
    return proxy_ip   
def mulTestProxies(proxies_ip):
    '''
    ���ܣ������������֤���д���IP
    @proxies_ip������IP��
    '''
    pool = Pool(processes=4)  #�����ĸ�����
    proxies_addr = pool.map(testProxy,proxies_ip)
    pool.close()
    pool.join()  #�ȴ����̳��е�worker����ִ�����
    return proxies_addr
#----------------------------------------------------------#
###
###��2����ȡ����
###
def getInfoDict(url,page,pos_words_one,proxy_addr_one):
    '''
    ���ܣ���ȡ��ҳְλ���ݣ����������ֵ�
    @url��Ŀ��URL
    @page����ȡ�ڼ�ҳ
    @pos_words_one�������ؼ��ʣ�������
    @proxy_addr_one��ʹ�õĴ���IP��������
    '''
    global pos_dict
    page = 1
    i_headers=("User-Agent","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 Safari/537.36 SE 2.X MetaSr 1.0")
    proxy = urllib.request.ProxyHandler({"http":proxy_addr_one})
    opener = urllib.request.build_opener(proxy,urllib.request.HTTPHandler)
    opener.addheaders=[i_headers]
    urllib.request.install_opener(opener)
    if page==1:
        tORf = "true"
    else:
        tORf = "false"
    mydata = urllib.parse.urlencode({"first": tORf,           
                                     "pn": page,           #pn�仯ʵ�ַ�ҳ
                                     "kd": pos_words_one } ).encode("utf-8")
    try:
        req = urllib.request.Request(url,mydata)
        data=urllib.request.urlopen(req).read().decode("utf-8","ignore")  #���ô���ip�� 
        pos_dict = json.loads(data)  #��strת��dict
    except urllib.error.URLError  as er:
        if hasattr(er,"code"):
            print("��ȡְλ��Ϣjson����ʱ����URLError���󣬴�����룺")
            print(er.code)
        if hasattr(er,"reason"):
            print("��ȡְλ��Ϣjson����ʱ����URLError���󣬴���ԭ��")
            print(er.reason)
    return pos_dict
def getInfoList(pos_dict): 
    '''
    ���ܣ���getInfoDict()���ص������ֵ�ת��Ϊ�����б�
    @pos_dict��ְλ��Ϣ�����ֵ�
    '''
    pos_list = []  #ְλ��Ϣ�б�   
    jcontent = pos_dict["content"]["positionResult"]["result"]    
    for i in jcontent:        
        one_info = []  #һ��ְλ�������Ϣ      
        one_info.append(i["companyFullName"])        
        one_info.append(i['companySize'])        
        one_info.append(i['positionName'])        
        one_info.append(i['education'])        
        one_info.append(i['financeStage'])        
        one_info.append(i['salary'])        
        one_info.append(i['city'])        
        one_info.append(i['district'])        
        one_info.append(i['positionAdvantage'])        
        one_info.append(i['workYear'])        
        pos_list.append(one_info)
    return pos_list
def getPosInfo(pos_words,city_words,proxy_addr):
    '''
    ���ܣ����ں���getInfoDict()��getInfoList()��ѭ������ÿһҳ��ȡ��������ְλ��Ϣ�б�
    @pos_words��ְλ�ؼ��ʣ������
    @city_words�����Ƴ��йؼ��ʣ������
    @proxy_addr��ʹ�õĴ���IP�أ������
    '''
    posInfo_result = []    
    title = ['��˾ȫ��', '��˾��ģ', 'ְλ����', '�����̶�', '�������', "н��ˮƽ", "����", "����", "����", "��������"]    
    posInfo_result.append(title)  
    for i in range(0,len(city_words)):
        #i = 0
        key_city = urllib.request.quote(city_words[i])
        #ɸѡ�ؼ������ã�gj=Ӧ���ҵ��&xl=��ר&jd=�ɳ���&hy=�ƶ�������&px=new&city=����
        url = "https://www.lagou.com/jobs/positionAjax.json?city="+key_city+"&needAddtionalResult=false"
        for j in range(0,len(pos_words)):
            #j = 0
            page=1
            while page<10:  #ÿ���ؼ�������������ʾ30ҳ���ڴ�ֻ��ȡ10ҳ
                pos_words_one = pos_words[j]
                #k = 1 
                proxy_addr_one = proxy_addr[page]
                #page += 1 
                time.sleep(3)
                pos_info = getInfoDict(url,page,pos_words_one,proxy_addr_one)  #��ȡ��ҳ��Ϣ�б�
                pos_infoList = getInfoList(pos_info)
                posInfo_result += pos_infoList  #�ۼ�����ҳ����Ϣ       
                page += 1   
    return posInfo_result
#----------------------------------------------------------#
###
###(3)�洢����
###
def wXlsConcent(export_path,posInfo_result):
    '''
    ���ܣ������ս��д�뱾��excel�ļ���
    @export_path������·��
    @posInfo_result����ȡ�������б�
    '''
    # ������д����ļ�
    wb1 = xlsxwriter.Workbook(export_path)
    # ����һ��sheet��������
    ws = wb1.add_worksheet()
    try:
        for i in range(0,len(posInfo_result)):
            for j in range(0,len(posInfo_result[i])):
                data = posInfo_result[i][j]
                ws.write(i,j,data)
        wb1.close()
    except Exception as er:
        print('д�롰'+export_path+'���ļ�ʱ���ִ���')
        print(er)
#----------------------------------------------------------#
###
###(4)����main()����
###
def main():
    '''
    ���ܣ���������������غ������������·����F:/spider_ret���µ�positionInfo.xls�ļ�    
    '''
    #---��1����ȡ����IP��
    proxies = getProxies()  #��ȡԭʼ����IP   
    proxy_addr = mulTestProxies(proxies) #���̲߳���ԭʼ����IP
    #---��2����ȡ����
    search_key = ["�����ھ�"]  #����ְλ�ؼ��ʣ��������ö����
    city_word = ["����"]  #������������(�������ö��)
    posInfo_result = getPosInfo(search_key,city_word,proxy_addr) #��ȡְλ��Ϣ
    #---��3���洢����
    export_path = "F:/spider_ret/positionInfo.xls" #���õ���·��
    wXlsConcent(export_path,posInfo_result)  #д�뵽excel��           
if __name__ == "__main__":
    main()