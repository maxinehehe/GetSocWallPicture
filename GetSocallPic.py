# -*-coding:utf-8 -*-

import requests, re, time, urllib, os
from lxml import etree
import platform
from multiprocessing.dummy import Pool as ThreatPool

# 该爬虫可以在Linux和Windows上使用


url = 'http://www.socwall.com/wallpapers/page:1/'

# 幻夜


def changePage(url):
    list = []
    global start
    print '----------------Hi,Guy,这是一个socwall图片下载脚本----------------'
    print '------------------版权->刘贺贺-------切勿商用-----否则后果自负-----'
    start_up = int(raw_input('从多少页开始？(共702页):'))
    start = start_up
    total_page = int(raw_input('下载至多少页？( ?? ω ?? )15/page（request:>start_up）:'))
    if start_up > total_page:
        print '\n警告：起始页不能小于终止页！'
        exit()
    for i in range(start_up, total_page + 1):
        page = re.sub('page:\d+', 'page:%s' % i, url)
        list.append(page)
    return list
# 通过

# 获取合格（赞大于等于0）

def getAvalue(url):
    html = requests.get(url).text
    selector = etree.HTML(html)
    imgList = []
    for it in range(1, 16):
        like = selector.xpath('//*[@id="content"]/ul[1]/li[%d]/div/ul[2]/li[4]/text()' % it)[0]
        img = selector.xpath('//*[@id="content"]/ul[1]/li[%d]/div/a/img/@src' % it)[0]
        if int(like) >= 0:
            imgList.append('http://www.socwall.com/'+img)
    return imgList

# 获取图片 增加判断操作系统类型：：Linux OR Windows

def saveImg(imgUrl, currentPage):
    global file_n
    file_n = 'SOCALL\\'  # windows
    file_linux = r'socwall/'  # linux
    print platform.system()
    if platform.system() == 'Linux':
        file_n = file_linux
    if not os.path.exists(file_n):
        os.mkdir(file_n)
    co = 0
    start = currentPage
    for each in imgUrl:
        print '开始下载' + each
        # urllib.urlretrieve(each,file_n+'\\Socall%s.jpg'%co)
        pic = requests.get(each)
        fn = file_n + r'soc%spic%s.jpg' % (start, co)
        co += 1
        # fn_copy = file_n+'\\NR%spic%s' % (start, co)
        if not os.path.exists(fn):
            fp = open(fn, 'wb')
            fp.write(pic.content)
            fp.close()
            print '已下载'
        else:
            print '提示：该图片已经存在了,将跳过它'
            continue


# 获取图片网址
def getImgUrl(pages):
    pages = changePage(url)  # 要获取页数数
    # print "pages:", pages
    for eachPage in pages:
        print "eachpage:", eachPage
        currentPage = re.findall(r"page:(\d+)/", eachPage)  # ['5']
        currentPage = currentPage[0]
        imgUrl = getAvalue(eachPage)  # 获取图片列表
        saveImg(imgUrl, currentPage)

if __name__ == '__main__':
    # pool = ThreatPool(4)
    # pages = changePage(url)
    # pool.map(getImgUrl, pages)
    # pool.close()
    # pool.join()
    global file_n
    getImgUrl(url)
    print '下载完毕'
    print r'文件下载至->',file_n
    print '-----let me say it again-----版权->刘贺贺-------切勿商用-----否则后果自负-----'
    time.sleep(1)
