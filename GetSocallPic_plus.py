# -*-coding:utf-8 -*-

import requests, re, time, urllib, os
from lxml import etree
import platform
from multiprocessing.dummy import Pool as ThreatPool

# 该爬虫可以在Linux和Windows上使用


url = 'http://www.socwall.com/wallpapers/page:1/'
baseUrl = 'http://www.socwall.com/'
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
    global quality
    html = requests.get(url).text
    selector = etree.HTML(html)
    imgList = []

    urlPlus = 'http://www.socwall.com/desktop-wallpaper/'
    for it in range(1, 16):
        like = selector.xpath('//*[@id="content"]/ul[1]/li[%d]/div/ul[2]/li[4]/text()' % it)[0]
        img = selector.xpath('//*[@id="content"]/ul[1]/li[%d]/div/a/img/@src' % it)[0]
        if int(like) >= 0:
            imgList.append(baseUrl + img)
    # 要下载高清图片
    if quality == 'high':
        imgListPlus = []
        for iurl in imgList:
            num = re.findall(r'wallpapers/(\d+)-', iurl)[0]
            imgPlus = urlPlus + num + 'wallpaper/'
            imgListPlus.append(imgPlus)
        return imgListPlus   # 返回高清网网址
    return imgList


# 获取图片 增加判断操作系统类型：：Linux OR Windows

def saveImg(imgUrl, currentPage):
    global file_n
    global quality
    file_n = 'SOCALL\\'  # windows
    file_linux = r'socwall/'  # linux
    print '操作系统：', platform.system()
    if platform.system() == 'Linux':
        file_n = file_linux
    if not os.path.exists(file_n):
        os.mkdir(file_n)
    # co = 0
    start = currentPage
    print '品质-quality:', quality
    for each in imgUrl:
        if quality == 'high':
            html2 = requests.get(each).text
            selector = etree.HTML(html2)
            img2 = selector.xpath('//*[@id="content"]/div/div[3]/a/img/@src')[0]
            each = baseUrl + img2

        print '开始下载' + each
        # urllib.urlretrieve(each,file_n+'\\Socall%s.jpg'%co)
        # with closing(requests.get(self.url(), stream=True)) as response:
        #     chunk_size = 1024  # 单次请求最大值
        #     content_size = int(response.headers['content-length'])  # 内容体总大小
        #     progress = ProgressBar(self.file_name(), total=content_size,
        #                             unit="KB", chunk_size=chunk_size, run_status="正在下载", fin_status="下载完成")
        pic = requests.get(each)
        num = re.findall(r'wallpapers/(\d+.+\d).', each)[0]
        print num
        fn = file_n + r'soc%spic%s.jpg' % (start, num)
        # co += 1
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
        print "起始页面:", eachPage
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
    global quality
    global decision
    decision = str(raw_input('你想要下载高清品质【1920×1080】还是普通品质【290X260】?yes/no:'))
    print 'decision:', decision
    if decision.lower() == 'yes' or decision.lower() == 'y':
        quality = 'high'
    else:
        quality = 'low'

    getImgUrl(url)
    print '下载完毕'
    print r'文件下载至->',file_n
    print '-----let me say it again-----版权->刘贺贺-------切勿商用-----否则后果自负-----'
    time.sleep(1)
