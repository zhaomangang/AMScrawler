#Author:Mason_Zhao
from bs4 import BeautifulSoup
import re 
import requests
from database import *
import time
class downloader(object):
    def __init__(self):
        self.target = 'https://blog.csdn.net/'#'http://yynews.cnnb.com.cn/' #目标网址
        self.data = DataBase('localhost','root','amsroot','ams')
        self.cou = 0
    """
    函数说明：通过get请求获取网页源码
    参数:
        target -目标地址
    返回值:
        html - 获取道得html
    """
    def getHtml(self,target):
        req = requests.get(target) #获取对象
        req.encoding = "utf-8" #设置编码格式
        html = req.text #获得网页源代码
        return html

    """
    函数说明：获取网页中为a且href中包含str的标签的herf
    参数:
        html -网页源码
        str -href中要包含的内容
    返回值:
        list_div_a -满足条件的a标签
    """
    def getaAndstr(self,html,str,count):
        soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
        list_div_a = []
        index = 0
        for x in soup.find_all('a',href = re.compile(str)):
            link = x.get('href')
            index+=1
            if(index>=count):
                break
            try:
                list_div_a.index(link)
            except:
                print(link)
                list_div_a.append(link)
        return list_div_a

         
    """
    函数说明：写入指定的本地文件
    参数:
        path -文件路径
        contect -要写入的内容
    返回值:
        status -是否成功写入
    """
    def writeToFile(self,path,contect):
        if(contect!=None):
            filewrite =  open(path,'ab+')
            filewrite.write(("""<html><head><meta charset = "utf-8"></head>""").encode())
            #print('+++++++++++++++++++++++++++++++++++')
           # print(contect)
            filewrite.write(contect.encode())
            filewrite.write(('</html>').encode())
            filewrite.close()
    """"
    函数说明：保存文章文字（仅p标签内容）
    参数:
        path    -文件路径 例如："/home/code/amsCrawer/article/name.txt"
        ontect  -文章内容 
    返回值:
        无
    """
    def writeToFileTxt(self,path,contect):
        if(contect!=None):
            print(path)
            self.cou+=1
            print(self.cou)
            filewrite =  open(path,'wb')
            filewrite.write(contect.encode())
            filewrite.close()

    """
    函数说明：获取文章信息及正文内容针对CSDN
    参数:
        url -文章地址
    返回值:
        dic_article -文章信息
    """
    def getArticleInfoCSDN(self,url):
        html = self.getHtml(url)
        print(url)
        dic_article = {'Title':'','Time':'','Name':'','Content':'','Image':''}
        soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
        title = soup.find('h1',attrs={"class":"title-article"})
        if(title!=None):
            dic_article['Title'] = title.string
            time = soup.find('span',attrs={"class":"time"})
            if(time!=None):
                dic_article['Time'] = time.string
            name = soup.find('a',attrs={"class":"follow-nickName"})
            if(name!=None):
                dic_article['Name'] = name.string
            #class="markdown_views prism-atom-one-light" id="content_views">attrs={"id":"content_view"}
            content = ''
            temp = soup.find('div',{'class':'markdown_views prism-atom-one-dark'})        ###(id = 'content_view') #attrs={"class":"markdown_views prism-atom-one-light"})
            if(temp==None):
                temp = soup.find('div',{'class':'markdown_views prism-atom-one-light'}) 
                #print(temp) 
            if(temp == None):
                soup.find('div',{'class':'markdown_views prism-tomorrow-night'})    #markdown_views prism-tomorrow-night
                #print(temp) 
            if(temp == None):
                soup.find('div',{'class':'markdown_views prism-Dracula'})  
                #print(temp) 
            if(temp == None):
                soup.find('div',{'class':'markdown_views prism-github-gist'})
                #print(temp) 
            if(temp == None):
                soup.find('div',{'class':'markdown_views prism-kimbie.light'})
                #print(temp) 
            if(temp == None):
                soup.find('div',{'class':'markdown_views prism-tomorrow-night-eighties'})
                #print(temp) 
            if(temp == None):
                soup.find('div',{'class':'markdown_views prism-atelier-sulphurpool-light'})
                #print(temp) 
            if(temp!=None):
                #print(temp)
                filename = '/home/code/amsCrawer/article/'+dic_article['Title'].strip()+'.html'
                self.writeToFile(filename,temp)
                #self.data.saveArticle(dic_article['Name'],dic_article['Title'],temp)
                print("-----------------------------------------")
                for x in temp.find_all('p'):
                    if(x.string!=None):
                        content += x.string
            if(content!=None):
                dic_article['Contect'] = content
                filename = '/home/code/amsCrawer/article/'+dic_article['Title'].strip()+'.txt'
                self.writeToFile(filename,content)
                #database.saveArticle('ams','test','测试内容文章')
                #self.data.saveArticle(dic_article['Name'],dic_article['Title'],content)
                #print(dic_article['Title'])#+dic_article['Time']+dic_article['Name'] = name)
                #print(dic_article['Time'])
                #print(dic_article['Contect'])
        return dic_article
    """
    函数说明：获取文章信息及正文内容针对哔哩哔哩
    参数:
        url -文章地址
    返回值:
        dic_article -文章信息
    """
    def getArticleInfoBILIBILI(self,url):
        html = self.getHtml(url)
        #print(url)
        dic_article = {'Title':'','Time':'','Name':'','Content':'','Image':''}
        soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
        title = soup.find('h1',attrs={"class":"title"})
        if(title!=None):
            #print(title)
            dic_article['Title'] = title.string
            name = soup.find('a',attrs={"class":"category-link"})
            if(name!=None):
                dic_article['Name'] = name.string
            #class="markdown_views prism-atom-one-light" id="content_views">attrs={"id":"content_view"}
            content = ''
            temp = soup.find('div',{'class':'article-holder'})        ###(id = 'content_view') #attrs={"class":"markdown_views prism-atom-one-light"})
            if(temp!=None):
                print(temp)
                filename = '/home/code/amsCrawer/article/'+dic_article['Title'].strip()+'.html'
                self.writeToFile(filename,temp)
                #self.data.saveArticle(dic_article['Name'],dic_article['Title'],temp)
               # print("-----------------------------------------")
                for x in temp.find_all('p'):
                    if(x.string!=None):
                        content += x.string
            if(content!=None):
                dic_article['Contect'] = content
                filename = '/home/code/amsCrawer/article/'+dic_article['Title'].strip()+'.txt'
                self.writeToFileTxt(filename,content)
                #database.saveArticle('ams','test','测试内容文章')
                #self.data.saveArticle(dic_article['Name'],dic_article['Title'],content)
        return dic_article

    """
    函数说明：获取文章信息及正文内容针对新浪新闻
    参数:
        url -文章地址
    返回值:
        dic_article -文章信息
    """
    def getArticleInfoSINA(self,url):
        html = self.getHtml(url)
        #print(url)
        dic_article = {'Title':'','Time':'','Name':'','Content':'','Image':''}
        soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
        title = soup.find('h1',attrs={"class":"main-title"})
        if(title!=None):
            #print(title)
            dic_article['Title'] = title.string
            name = soup.find('a',attrs={"class":"source"})
            if(name!=None):
                dic_article['Name'] = name.string
            #class="markdown_views prism-atom-one-light" id="content_views">attrs={"id":"content_view"}
            content = ''
            temp = soup.find('div',{'class':'article'})        ###(id = 'content_view') #attrs={"class":"markdown_views prism-atom-one-light"})
            if(temp!=None):
                #print(temp)
                filename = '/home/code/amsCrawer/article/'+dic_article['Title'].strip()+'.html'
                self.writeToFile(filename,temp)
                #self.data.saveArticle(dic_article['Name'],dic_article['Title'],temp)
               # print("-----------------------------------------")
                for x in temp.find_all('p'):
                    if(x.string!=None):
                        content += x.string
            if(content!=None):
                dic_article['Contect'] = content
                filename = '/home/code/amsCrawer/article/'+dic_article['Title'].strip()+'.txt'
                self.writeToFileTxt(filename,content)
                #database.saveArticle('ams','test','测试内容文章')
                #self.data.saveArticle(dic_article['Name'],dic_article['Title'],content)
        return dic_article

    """
    函数说明：获取a标签中相关内容针对CSDN
    参数:
        list_div_a -a标签列表
    返回值:
        list_article -文章列表
    """
    def getArticleList(self,list_div_a,type):
        #dic_temp = {'Title':'','time':'','name':'','content':''}
        list_article = []
        for x in list_div_a:
            #print(x)
            if(type =='CSDN'):
                list_article.append(self.getArticleInfoCSDN(x))
            if(type=='SINA'):
                print('sina')
                list_article.append(self.getArticleInfoSINA(x))
            if(type=='BILIBILI'):
                if(-1==x.find('https:')):
                    x = 'https:' + x
                list_article.append(self.getArticleInfoBILIBILI(x))
    """
    函数说明：爬取CSDN文章
    参数:
        count   -爬取数目
    返回值:
        list_article -文章列表
    """
    def getArticleCSDN(self,count):
        main_page = self.getHtml('https://blog.csdn.net/')
        a_list = self.getaAndstr(main_page,'article',1000)
        self.getArticleList(a_list,'CSDN')
    
    """
    函数说明：爬取CSDN文章
    参数:
        count   -爬取数目
    返回值:
        list_article -文章列表
    """
    def getArticleSINA(self,count):
        main_page = self.getHtml('http://sports.sina.com.cn/')
        a_list = self.getaAndstr(main_page,'doc',count)
        self.getArticleList(a_list,'SINA')

    """
    函数说明：爬取BILINBILI文章
    参数:
        count   -爬取数目
    返回值:
        list_article -文章列表
    """
    def getArticleBILINILI(self,count):
        main_page = self.getHtml('https://www.bilibili.com/read/home?spm_id_from=333.851.b_7072696d617279467269656e64736869704c696e6b.1')    
        a_list = self.getaAndstr(main_page,'read/cv',100000)
        self.getArticleList(a_list,'BILIBILI')
        for x in a_list:
            print(x)
        #print(main_page)


    """
    函数说明:获取翻页地址
    Parameters:
        xiayiye - 下一页地址(string)
    Returns:
        fanye - 当前页面的翻页地址(list)
    """
    


if __name__ == "__main__":  
    begin = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    dl = downloader()
    dl.getArticleBILINILI(1000)
    end = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    print('开始时间: ')
    print(begin)
    print('结束时间：')
    print(end)