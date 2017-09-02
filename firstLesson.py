from urllib import request, parse, error
import re
import http.cookiejar

# 目的url,?代表页数
orderUrl = "http://www.qiushibaike.com/hot/page/?"
# 默认第一页
pageNum = 1


# 设置必要的Header
def getHeaders():
    headers = {}
    # headers['Host'] = r"www.qiushibaike.com"
    # 很多网站都需要设置这样的header，以证明是浏览器发起的请求
    headers[
        'User-Agent'] = r"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                        r"Chrome/52.0.2743.116 Safari/537.36 "

    return headers


##
# 获取网页的html代码
##
def getHtmlCodeFromUrl(url):
    q_request = request.Request(orderUrl, headers=getHeaders())
    q_response = request.urlopen(q_request)
    html = q_response.read().decode('utf-8')
    return html


def parseHtml(html):

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
              # r'.*?' \
              # r'<a.*?href="/user/(.*?)"' \
              # r'.*?' \
              # r'<h2>(.*?)</h2>' \
              # r'.*?' \
              # r'</a>.*?' \
              # r'(manIcon|womenIcon)' \
              # r'.*>(\d)' \
              # r'.*?' \
              # r'class.*?content.*?' \
              # r'<span>(.+?)</span>'

    pattern = re.compile(regular,flags=re.S)

    items = pattern.findall(html)
    print(len(items))
    for item in items:
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

# 先尝试将整个网页抓取下来
q_orderUrl = orderUrl.replace(r"?", str(pageNum))

# 打印看下替换的正不正确
# print(q_orderUrl)

page = getHtmlCodeFromUrl(q_orderUrl)

#print(page)
print("抓到网页数据")

parseHtml(page)
