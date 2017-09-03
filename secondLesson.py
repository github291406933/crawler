#
# 将糗事百科爬虫进行模块化封装
#

from urllib import request,error,parse
import http.cookiejar
import re

class QSBK:

    # 构造方法，进行一系列属性的赋值初始化
    def __init__(self):
        # 比如定义一些固定Header，代理之类
        self.user_agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                        r"Chrome/52.0.2743.116 Safari/537.36 "
        self.headers={"user-agent":self.user_agent}

        self.order_url=r"http://www.qiushibaike.com/hot/page/?"#问好?用来之后换页替换用

        self.pageIndex = 1

        return

    # 获取网址链接，循环遍历每一页
    def getPageUrl(self,pageNum):

        url = self.order_url.replace("?",str(pageNum))

        return url


    # 设置必要的Header
    def getHeaders(self):

        return self.headers

    ##
    # 获取网页的html代码
    ##
    def getHtmlCodeFromUrl(self,url):
        headers = self.getHeaders()
        q_request = request.Request(url, headers=headers)
        q_response = request.urlopen(q_request)
        html = q_response.read().decode('utf-8')
        return html


    def parseHtml(self,html):
        # 需要一个正则表达式
        # 从上往下，id,userId,username,gender,age,content,likes,comments
        regular = r'<div.*?qiushi_tag_(.*?)\'>' \
                  r'.*?' \
                  r'<a.*?href.*?/users/(.*?)/' \
                  r'.*?' \
                  r'<h2>(.*?)</h2>' \
                  r'.*?' \
                  r'<div.*?(manIcon|womenIcon)' \
                  r'.*?' \
                  r'>(\d*)</div>' \
                  r'.*?' \
                  r'<div.*?class.*?content.*?' \
                  r'<span>(.*?)</span>' \
                  r'.*?' \
                  r'class.*?stats.*?<span.*?class.*?stats-vote.*?<i.*?class.*?number.*?' \
                  r'>(\d*)</i>' \
                  r'.*?<span.*?class.*?stats-comments.*?' \
                  r'<i.*?class.*?number.*?' \
                  r'>(\d*)</i>' \

        pattern = re.compile(regular,flags=re.S)

        items = pattern.findall(html)

        for item in items:
            # 考虑建一个类model保存起来
            print("")
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            print("id:",item[0])
            print("userId:",item[1])
            print("username:",item[2])
            print("gender:",item[3])
            print("age:",item[4])
            print("likes:",item[6])
            print("comments:",item[7])
            print("content:",item[5])
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

        return items


    # 接下来考虑怎么去控制这些函数
    # 每按一次回车键，加载新的一页html并解析打印数据
    def onLoad(self):
        url = self.getPageUrl(self.pageIndex)
        self.pageIndex+=1#指向下一页

        page = self.getHtmlCodeFromUrl(url)
        #最重要的一步解析html代码动作
        datas = self.parseHtml(page)
        # return datas

    def printHtml(self,datas):

        for item in datas:
            # 考虑建一个类model保存起来
            print("")
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            print("id:",item[0])
            print("userId:",item[1])
            print("username:",item[2])
            print("gender:",item[3])
            print("age:",item[4])
            print("likes:",item[6])
            print("comments:",item[7])
            print("content:",item[5])
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

        return


    # 怎么监听回车键
    def start(self):
        print("开始抓取糗事百科，按回车查看新段子（暂时看不了带图片的段子，请见谅。）")

        while True:
            message = input()

            # 不为Q即继续
            if message.lower() == "q":
                print("抓取结束！")
                exit(1)

            self.onLoad()



qsbk = QSBK()
qsbk.start()
