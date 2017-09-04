from urllib import request, error, parse
import re
import http.cookiejar

class Tool:

    # 去除Img标签
    removeImg = re.compile(r'<img.*?>| {7}')

    # 去除a标签，超链接
    removeAddr = re.compile(r'<a.*?>|</a>')

    # 把换行的标签换为\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    # 将表格制表<td>替换为\t
    replaceTD= re.compile('<td>')
    # 把段落开头换为\n加空两格
    replacePara = re.compile('<p.*?>')
    # 将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')

    # 将其余标签剔除
    removeExtraTag = re.compile('<.*?>')

    def __init__(self):
        return

    def cleanContent(self,content):

        content = re.sub(self.removeImg,"",content)
        content = re.sub(self.removeAddr,"",content)
        content = re.sub(self.removeExtraTag,"",content)

        return content

class BDTB:
    def __init__(self):
        self.orderUrl = r"https://tieba.baidu.com/p/3138733512"  # 百度某张帖子
        self.userAgent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                         r"Chrome/52.0.2743.116 Safari/537.36 "
        self.seeLz = 1;  # 默认看楼主
        self.pageIndex = 1;  # 默认第一页

        # 解析标题的正则表达式
        self.parseTitleRegular = r'class.*?core_title_txt.*?' \
                                 r'>(.*?)<'
        self.titlePattern = re.compile(self.parseTitleRegular,re.S)


        # 解析总页数的正则表达式
        self.parseTotalPageNumRegular = r'class.*?l_reply_num.*?<span.*?</span>.*?<span.*?' \
                                        r'>(\d*)<'
        self.totalPageNumPattern = re.compile(self.parseTotalPageNumRegular)

        # 解析每一层的内容
        self.parseFloorContentRegular = r'<div.*?post_content.*?>(.*?)</div>'
        self.floorContentPattern = re.compile(self.parseFloorContentRegular,re.S)

    def getHeaders(self):
        headers = {'user-agent': self.userAgent}

        return headers

    def getUrlReuqeust(self):
        # 参数
        datas = {"see_lz": self.seeLz, "pn": self.pageIndex}
        data = parse.urlencode(datas)
        data = data.encode('utf-8')
        bdRequest = request.Request(url=self.orderUrl, data=data, headers=self.getHeaders(),method='GET')

        return bdRequest

    def getPageHtml(self):

        bdRequest = self.getUrlReuqeust()

        try:
            bdResopnse = request.urlopen(bdRequest)
            return bdResopnse.read().decode('utf-8')
        except error.URLError as e:
            if hasattr(e, "reason"):
                print(e.reason)
                return None

    # 获取到标题
    def getTitle(self,page):

        pattern = self.titlePattern

        result = pattern.search(page)

        if result:
            return result.group(1)
        else:
            return None

    # 获取帖子的页数
    def getPageTotalNum(self,page):

        pattern = self.totalPageNumPattern

        result = pattern.search(page)

        if result:
            return result.group(1)

        return None

    # 获取每一层楼的内容
    def getContent(self,page):

        pattern = self.floorContentPattern

        items = pattern.findall(page)

        if items:
            return items;

        return None

    def parsePageHtml(self, html):

        # 暂时只打印内容
        title = self.getTitle(html)
        print("title:",title)

        totalPageNum = self.getPageTotalNum(html)
        print("totalPageNum:",totalPageNum)

        items = self.getContent(html)
        print("content====================")
        for item in items:
            print(Tool().cleanContent(item))

    def start(self):
        print("按回车键开始抓取内容(输入q结束抓取)：")

        while True:

            message = input()

            if message.lower() != 'q':
                html = self.getPageHtml()  # 获取网页的内容
                print("开始解析")
                self.parsePageHtml(html)    # 进行解析网页
                # 差个打印功能
            else:
                print("抓取结束！")
                exit(1)

            self.pageIndex+=1


bd = BDTB()
bd.start()