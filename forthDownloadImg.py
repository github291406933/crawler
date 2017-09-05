from urllib import request,error,parse
import re
import os

class UserModel:

    def __init__(self,name,age,city):
        self.name = name;
        self.age = age;
        self.city = city

    def getPath(self):
        path = "";
        path += self.city + "/" + self.age + "/" + self.name + "/"
        return path

class Splider:

    def __init__(self):
        self.defaultUrl = u'http://mm.taobao.com/json/request_top_list.htm'
        self.pageIndex = 1;

        self.contentRegular = r''
        self.contentPattern = re.compile(self.contentRegular)

        return

    def getRequest(self):

        url = self.defaultUrl;
        url += "?page="+self.pageIndex

        req = request.Request(url)

        return req

    def getHtml(self):
        req = self.getRequest()
        try:
            res = request.urlopen(req)
            return res.read().decode('utf-8')
        except error.URLError as e:
            if hasattr(e,'reason'):
                print(e.reason)
            else:
                print(e)
            return None

    def getContents(self,html):

        pattern = self.contentPattern
        items = pattern.findall(html)
        if items:
            return items
        return None

    # 保存下载用户头像
    def saveImg(self,fileName,imgUrl):

        res = request.urlopen(imgUrl)
        img = res.read()

        file = open(fileName,'wb+')
        file.write(img)
        file.close()
    # 保存用户信息
    def saveUserInfoToFile(self,fileName,contents):
        file = open(fileName,'w+')
        for item in contents:
            file.write(item)

    # 若fileName不存在则创建
    def mkdir(self,fileName):
        path = str(fileName).strip()
        isExists = os.path.exists(path)
        if not isExists:
            os.mkdir(path)


    #

