import pymysql
import mysql.connector
import time
class DataBase(object):
    def __init__(self,ip,usr,password_,db_):
        self.db = pymysql.connect(host=ip,user=usr,password=password_,database=db_, port=3307,unix_socket=None, charset='utf8')
        self.cursor = self.db.cursor()

    def exeSql(self,sql):
        try:
            self.cursor.execute(sql)
            # 提交到数据库执行
            self.db.commit()
        except:
            self.db.rollback()
            # 如果发生错误则回滚
        #db.rollback()
    def saveArticle(self,author,title,content):
        time_ = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        sql = """INSERT INTO t_article(author,title, content,channel_id, gmt_create)
                    VALUES ('%s', '%s','%s', 101, '%s')""" % (author,title,content,time_)
        print(sql)
        self.exeSql(sql)
    
    
    """
    函数说明：通过get请求获取网页源码
    参数:
        target -目标地址
    返回值:
        html - 获取道得html
    """

if __name__ == "__main__":  
    #database = DataBase('localhost','root','Z001221z','WangWangChat')
    database = DataBase('localhost','root','amsroot','ams')
    database.saveArticle('ams','test','测试内容文章')
    database.saveArticle('ams','test','testcontent')
   