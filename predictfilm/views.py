# This Python file uses the following encoding: utf-8

# Create your views here.
from django.template import Context
from django.template.loader import get_template
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
import datetime
import os
import xlrd
import operator
from models import Publisher
# import mysql

import urllib
import urllib2
import time
import weiboLogin
from time import sleep
from Diagram import drawDiagram

from django.template import RequestContext
from django.shortcuts import render_to_response

# from BeautifulSoup import *
# import BeautifulSoup
import re
from BeautifulSoup import BeautifulSoup
from parseBigExcel import parse
from filtBoxoffice import filtBoxofficeByMovieSeriNum
from parseBigExcel import filtBigExcelByDictNum

def hello(request):
    return HttpResponse('cleantha')

def clea(request):
    return HttpResponse("clea'\r\n'i love you!!!")

def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)

def cleantha(request):
    cleaTemplate = get_template('cleantha.html')
    c = Context({'name': 'cleantha'})
    html = cleaTemplate.render(c)
    print (os.path.join(os.path.dirname(__file__), '..', 'templates').replace('\\','/'),)
    return HttpResponse(html)

def parseExcel(request):
    fileTemplate = get_template('parsexcel.html')
    filesPath = os.path.join(os.path.dirname(__file__), '..', 'files').replace('\\','/')
    filePath = str(filesPath) + '/movie_view.xls'
    print filePath
    data = xlrd.open_workbook(str(filePath))
    print data.nsheets
    c = Context({'number': data.nsheets})
    html = fileTemplate.render(c)
    return HttpResponse(html)
    # return HttpResponse("excelParse")

def renderresponse(request):
    return render_to_response('parsexcel.html', {'number': 3})

def models(request):
    # p1 = Publisher.objects.create(name='Apress',
    # address='2855 Telegraph Avenue',
    # city='Berkeley', state_province='CA', country='U.S.A.',
    # website='http://www.apress.com/')
    # p2 = Publisher.objects.create(name="O'Reilly",
    # address='10 Fawcett St.', city='Cambridge',
    # state_province='MA', country='U.S.A.',
    # website='http://www.oreilly.com/')
    publisher_list = Publisher.objects.all()
    print publisher_list
    ID_List = [int(publisher.id) for publisher in publisher_list.order_by("name")]
    name_List = [publisher.name for publisher in publisher_list.order_by("name")]
    print ID_List
    print name_List
    print len(name_List)
    return HttpResponse("models!!!")

def deleteModel(request):
    for i in range(11, 18):
        Publisher.objects.filter(id=i).delete()
    # Publisher.objects.filter(id=19).delete()
    # Publisher.objects.filter(id=20).delete()
    return HttpResponse("delete successful")

def diagram(request):
    drawDiagram()
    filesPath = os.path.join(os.path.dirname(__file__), '..', 'templates').replace('\\','/')
    htmlPath = str(filesPath) + "/diagram.html"
    diagramHtml = open(htmlPath).read()
    return HttpResponse(diagramHtml)

def navi(request):
    return render_to_response('navigation.html', {}, RequestContext(request))

def d3Show(request):
    filesPath = os.path.join(os.path.dirname(__file__), '..', 'templates').replace('\\','/')
    # filePath = str(filesPath) + '/modelTemp.html'
    # filePath = str(filesPath) + '/D3Show.html'
    # filePath = str(filesPath) + '/index0.html'

    filePath = str(filesPath) + '/index.html'

    # scriptPath = str(filesPath) + '/media/d3.v3.js'
    # c = Context({'dir': scriptPath})
    #
    # t = get_template('modelTemp.html')
    # return HttpResponse(t.render(c))
    # fp = open(filePath)
    # html = fp.read()
    # fp.close()
    # print "cleantha!!!"

    t = get_template('index.html')
    html = t.render(Context({''}))

    return HttpResponse(html)

def readBigExcel(request):
    # parse()
    filtBoxofficeByMovieSeriNum()
    return HttpResponse('successful!!!')

def testcookie(request):
    if 'clea' in request.COOKIES:
        return HttpResponse("you have clea is %s" % request.COOKIES['clea'])
    else:
        response = HttpResponse("you dont have clea")
        response.set_cookie('clea', 'cleantha')
        return response

def showDiagramByDate(request):
    try:
        dateTime = request.GET['date']
        print dateTime

    except:
        pass

    del request.session['datedict']
    del request.session['boxofficelist']

    if not 'datedict' in request.session:
        movieSearchNumByDateDict = parse()
        request.session['datedict'] = movieSearchNumByDateDict
    if not 'boxofficelist' in request.session:
        boxofficelist = filtBoxofficeByMovieSeriNum()
        print boxofficelist
        request.session['boxofficelist'] = boxofficelist

    if not 'newDateDict' in request.session:
        datedict = request.session['datedict']
        boxofficelist = request.session['boxofficelist']
        print len(datedict)
        print len(list(boxofficelist))
        # newDateDict = filtBigExcelByDictNum(datedict, boxofficelist)
        # request.session['newDateDict'] = newDateDict

    # newMovieDict = request.session['newDateDict']
    # datelist = newMovieDict.keys()
    # t = get_template('showDiagramByDate.html')
    # html = t.render(Context({'datelist': datelist}))
    # return HttpResponse(html)
    return HttpResponse('cleantha')

    # request.session['datedict'] = movieSearchNumByDateDict

def readExcelFunc():
    filesPath = os.path.join(os.path.dirname(__file__), '..', 'files').replace('\\','/')
    filePath = str(filesPath) + '/boxoffice.xls'

    data = xlrd.open_workbook(str(filePath))
    table = data.sheet_by_index(0)
    nrows = table.nrows
    movieNameList = []
    for rownum in range(1, nrows):
        movieNameList.append(table.row_values(rownum)[0])

    # for name in movieNameList:
    #     print name + "\n"
    simpleNameList = list(set(movieNameList))
    simpleNameList.sort(key=movieNameList.index)

    nameStrList = map(lambda str: str.encode('utf-8'), simpleNameList)

    return nameStrList
    # return simpleNameList

def readExcel(request):
    simpleNameList = readExcelFunc()

    for name in simpleNameList:
        print name + "\n"
        print type(name)
    print 'there are ' + str(len(simpleNameList)) + 'movies!!!'

    return HttpResponse("done read")

def boxOffice(request):
    fileTemplate = get_template('parsexcel.html')
    filesPath = os.path.join(os.path.dirname(__file__), '..', 'files').replace('\\','/')
    filePath = str(filesPath) + '/boxoffice.xls'
    print filePath
    # xlrd.Book.encoding = 'gbk'

    data = xlrd.open_workbook(str(filePath))
    print data.nsheets
    c = Context({'number': data.nsheets})
    html = fileTemplate.render(c)
    table = data.sheet_by_index(0)

    nrows = table.nrows
    ncols = table.ncols
    colnames = table.row_values(0)
    list = []
    normal_list = []
    for rownum in range(1, nrows):
        row = table.row_values(rownum)
        if row:
            app = {}
            for i in range(len(colnames)):
                app[colnames[i]] = row[i]
            list.append(app)
        normal_list.append(row)
    print list[0]
    # titls = [head for head in head_title]
    # print titls

    # return HttpResponse(html)

    itemList = ['clea', 'cleantha', 'kk']
    cleaList = [1, 2, 3]
    kkList = [3, 2, 1]
    t = get_template('boxoffice.html')
    return HttpResponse(t.render(Context({
        'head_list': colnames,
        'item_list': normal_list,
        'len': len(colnames)
    })))

def filterBoxOffice(request):
    filesPath = os.path.join(os.path.dirname(__file__), '..', 'files').replace('\\','/')
    filePath = str(filesPath) + '/boxoffice.xls'
    data = xlrd.open_workbook(str(filePath))
    table = data.sheet_by_index(0)
    nrows = table.nrows

    values = []
    for rownum in range(1, nrows):
        row = table.row_values(rownum)
        values.append(row)

    nameList = [value[0].encode('utf-8') for value in values]
    simpleNameList = list(set(nameList))
    simpleNameList.sort(key=nameList.index)

    for value in values:
        print value[0].encode('utf-8')

    for name in simpleNameList:
        print name

    movieDict = {}
    for name in simpleNameList:
        boxofficeList = []
        for value in values:
            if value[0].encode('utf-8') == name:
                print '---------------------'
                boxofficeList.append(value[3])

        print boxofficeList
        maxboxoffice = max([int(boxoffice) for boxoffice in boxofficeList])
        movieDict[name] = maxboxoffice

    for key, value in movieDict.items():
        print str(key) + "--->" + str(value) + "\n"

    saveFile(movieDict, 'totalboxoffice.txt')
    return HttpResponse("cleantha filter")

def boxOfficeFilter(request):
    fileTemplate = get_template('parsexcel.html')
    filesPath = os.path.join(os.path.dirname(__file__), '..', 'files').replace('\\','/')
    filePath = str(filesPath) + '/boxoffice.xls'
    print filePath
    # xlrd.Book.encoding = 'gbk'

    data = xlrd.open_workbook(str(filePath))
    print data.nsheets
    c = Context({'number': data.nsheets})
    html = fileTemplate.render(c)
    table = data.sheet_by_index(0)

    nrows = table.nrows
    ncols = table.ncols
    colnames = table.row_values(0)
    dictlist = []
    normal_list = []
    for rownum in range(1, nrows):
        row = table.row_values(rownum)
        if row:
            app = {}
            for i in range(len(colnames)):
                app[colnames[i]] = row[i]
            dictlist.append(app)
        normal_list.append(row)

    weekboxlist = [dict[colnames[2]] for dict in dictlist]
    nameList = [dict[colnames[0]] for dict in dictlist]
    simpleNameList = list(set(nameList))
    simpleNameList.sort(key=nameList.index)

    simpleMovieList = []
    for name in simpleNameList:
        movielist = []
        for dict in dictlist:
            [movielist.append(dict) for value in dict.values() if value == name]
            # if name in dict.values():
            #     movielist.append(dict)
        # boxoffice = max(map(lambda x: int(x), [dict[colnames[3]] for dict in movielist]))
        boxoffice = max(int(dict[colnames[3]]) for dict in movielist)
        movie = {}
        movie['name'] = name
        movie['boxoffice'] = int(boxoffice)
        simpleMovieList.append(movie)

    sorted_movieList = sorted(simpleMovieList, key=operator.itemgetter('boxoffice'), reverse=True)
    print sorted_movieList

    itemList = ['clea', 'cleantha', 'kk']
    cleaList = [1, 2, 3]
    kkList = [3, 2, 1]
    t = get_template('boxoffice.html')
    return HttpResponse(t.render(Context({
        'head_list': colnames,
        'simple_list': sorted_movieList
    })))

def index(request):
    filesPath = os.path.join(os.path.dirname(__file__), '..', 'templates').replace('\\','/')
    filePath = str(filesPath) + '/cleantha.html'
    file = open(filePath)
    html = file.read()
    file.close()
    return HttpResponse(html)

def sinaRsaSpider(request):
    filesPath = os.path.join(os.path.dirname(__file__), '..', 'files').replace('\\','/')
    filePath = str(filesPath) + '/account.txt'

    WBlogin = weiboLogin.weiboLogin()
    resultList = WBlogin.login(filePath)
    if resultList == 1:
        print 'login successful'
        return HttpResponseRedirect('/spider/')
    else:
        print 'login error!'
        return HttpResponse('ERROR')
    return HttpResponse('SUCCESSFUL')

#这个才是项目中最后用到的爬虫 sinaspider是以前写的 不好使
#使用之前要设置好代理 传入URL 然后就可以拿到微博数了
#simpleSpider为moviespider和weekspider调用
def simpleSpider(url):
    # proxy_support = urllib2.ProxyHandler({'http': 'http://127.0.0.1:8087'})
    # opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
    # urllib2.install_opener(opener)

    request = urllib2.Request(url)
    request.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:5.0)')

    response = urllib2.urlopen(request)
    the_page = response.read()

    cleaSoup = BeautifulSoup(the_page)

    scripts = cleaSoup.findAll('script')

    rp = re.compile(r'W_textc(.*?)span')
    result = rp.findall(str(scripts))

    try:
        newResult = result[-1]
        print newResult
        rp = re.compile(r' (.*?) ')
        clea = rp.findall(newResult)
        print clea
        newClea = map(lambda item: item.replace(',', ''), clea)
        finalResult = int(newClea[0])
        return finalResult
    except IndexError:
        print 'this url is something bad ' + str(url)
        return 1

def generateDate():
    # filePath = '/home/cutejumper/Downloads/movie_view.xls'
    # boxFilePath = '/home/cutejumper/Downloads/boxoffice.xls'
    filesPath = os.path.join(os.path.dirname(__file__), '..', 'files').replace('\\','/')
    filePath = str(filesPath) + '/movie_view.xls'
    boxFilePath = str(filesPath) + '/boxoffice.xls'


    data = xlrd.open_workbook(str(filePath))
    table = data.sheet_by_index(2)
    # table = data.sheet_by_index(0)
    nrows = table.nrows
    # print nrows

    boxData = xlrd.open_workbook(str(boxFilePath))
    boxTable = boxData.sheet_by_index(0)
    boxnrows = boxTable.nrows
    boxMovieName = []
    filterName = []
    for rownum in range(1, boxnrows):
        boxMovieName.append(boxTable.row_values(rownum)[0].encode('utf-8'))
        filterName = list(set(boxMovieName))
        filterName.sort(key=boxMovieName.index)

    movieMap = {}
    for rownum in range(1, nrows):
        movieName = table.row_values(rownum)[1].encode('utf-8')
        # movieName = str(table.row_values(rownum)[0].encode('gbk'))
        # print type(movieName)
        if movieName in filterName:
            movieDate = table.row_values(rownum)[9].encode('utf-8')
            movieMap[movieName] = movieDate

    movieDateMap = {}
    # movieDict = [lambda value: value.replace('-', '') for value in movieMap.values()]
    for key, value in movieMap.items():
        # print key + '--->' + value + '\n'
        valueList = str(value).split('-')
        valueIntList = map(lambda value: int(value), valueList)
        # print valueIntList
        dataSum = valueIntList[0]*12 + valueIntList[1]
        newSum = dataSum-4
        year = newSum / 12
        month = newSum % 12
        oldDate = str(year) + '-' + str(month) + '-' + str(valueIntList[2]) + '-0'
        newSum = dataSum+4
        year = newSum / 12
        month = newSum % 12
        newDate = str(year) + '-' + str(month) + '-' + str(valueIntList[2]) + '-0'

        finalDate = oldDate + ':' + newDate

        movieDateMap[key] = finalDate

    return movieDateMap

def getDate(request):
    movieDateMap = generateDate()
    movieNameList = readExcelFunc()
    # for key, value in movieDateMap.items():
    #     print key + '--->' + value

    # print len(movieDateMap)
    for name in movieNameList:
        url = 'http://s.weibo.com/weibo/' + str(name) + '&timescope=custom:' + movieDateMap[str(name)] + '&Refer=g'
        print url

    saveFile(movieDateMap)
    return HttpResponse('Done!!!')

def movieSpider(request):
    movieNameList = readExcelFunc()
    movieDateMap = generateDate()

    proxy_support = urllib2.ProxyHandler({'http': 'http://127.0.0.1:8087'})
    opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
    urllib2.install_opener(opener)

    movieMap = {}
    for movieName in movieNameList:
        url = 'http://s.weibo.com/weibo/' + str(movieName) + '&timescope=custom:' + movieDateMap[str(movieName)] + '&Refer=g'

        finalResult = 0

        requestCounter = 0

        #有时候爬下来是0 要重新爬取但又不能无限制 所以设置一个10次的次数
        while True:
            print 'looping'
            requestCounter += 1
            if requestCounter > 10:
                finalResult = 3
                break

            print movieName
            try:
                finalResult = simpleSpider(url)
            except:
                proxy_support = urllib2.ProxyHandler({'http': 'http://127.0.0.1:8087'})
                opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
                urllib2.install_opener(opener)

            if int(finalResult) != 0:
                break

        print type(finalResult)
        print 'final result' + str(finalResult)

        movieMap[movieName] = finalResult
        sleep(3)

    print movieMap
    saveFile(movieMap)

    return HttpResponse("cleantha love you!!!")

def adjustDate(datetime):
    if int(datetime[0]) == 0:
        date = int(datetime)
        month = date / 100
        day = date % 100
        dateStr = '2013-' + str(month) + '-' + str(day) + '-0'
        return dateStr
    else:
        date = int(datetime)
        month = date / 100
        day = date % 100
        dateStr = '2012-' + str(month) + '-' + str(day) + '-0'
        return dateStr

def parseWeekExcel():
    # boxFilePath = '/home/cutejumper/Downloads/boxoffice.xls'
    filesPath = os.path.join(os.path.dirname(__file__), '..', 'files').replace('\\','/')
    boxFilePath = str(filesPath) + '/boxoffice.xls'

    boxData = xlrd.open_workbook(str(boxFilePath))
    boxTable = boxData.sheet_by_index(0)
    boxnrows = boxTable.nrows

    movieDateDict = {}
    for rownum in range(1, boxnrows):
        movieName = boxTable.row_values(rownum)[0].encode('utf-8')
        movieStartDateSum = (boxTable.row_values(rownum)[6].encode('utf-8'))
        movieEndDateSum = (boxTable.row_values(rownum)[7].encode('utf-8'))
        movieStartDate = adjustDate(movieStartDateSum)
        movieEndDate = adjustDate(movieEndDateSum)

        if movieName in movieDateDict.keys():
            movieDateDict[movieName].append([movieStartDate, movieEndDate])
        else:
            movieDateDict[movieName] = [[movieStartDate, movieEndDate]]

    return movieDateDict

def weekBoxOffice(request):
    filesPath = os.path.join(os.path.dirname(__file__), '..', 'files').replace('\\','/')
    boxFilePath = str(filesPath) + '/boxoffice.xls'

    boxData = xlrd.open_workbook(str(boxFilePath))
    boxTable = boxData.sheet_by_index(0)
    boxnrows = boxTable.nrows

    movieDateDict = {}
    for rownum in range(1, boxnrows):
        movieName = boxTable.row_values(rownum)[0].encode('utf-8')
        movieStartDateSum = (boxTable.row_values(rownum)[6].encode('utf-8'))
        movieEndDateSum = (boxTable.row_values(rownum)[7].encode('utf-8'))
        movieBoxoffice = int(boxTable.row_values(rownum)[2])
        movieStartDate = adjustDate(movieStartDateSum)
        movieEndDate = adjustDate(movieEndDateSum)

        #和weekspider一样将电影名称和开始上映时间组合成为键
        movieTip = str(movieName) + ':' + str(movieStartDate)
        movieDateDict[movieTip] = movieBoxoffice

    saveFile(movieDateDict, 'weekboxoffice.txt')

    return HttpResponse("clea clea clea")

def weekSpider(request):
    proxy_support = urllib2.ProxyHandler({'http': 'http://127.0.0.1:8087'})
    opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
    urllib2.install_opener(opener)

    movieDateDict = parseWeekExcel()
    movieMap = {}

    for key, value in movieDateDict.items():
        for date in value:
            url = 'http://s.weibo.com/weibo/' + str(key) + '&timescope=custom:' + str(date[0]) + ':' + str(date[1]) + '&Refer=g'

            finalResult = 0

            requestCounter = 0

            while True:
                print 'looping'
                requestCounter += 1
                if requestCounter > 10:
                    finalResult = 3
                    break

                print key
                try:
                    finalResult = simpleSpider(url)
                except:
                    proxy_support = urllib2.ProxyHandler({'http': 'http://127.0.0.1:8087'})
                    opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
                    urllib2.install_opener(opener)

                if int(finalResult) != 0:
                    break

            print type(finalResult)
            print 'final result' + str(finalResult)

            #将电影名称和放映开始的日期作为一个标签
            movieTip = str(key) + ':' + str(date[0])

            movieMap[movieTip] = finalResult
            sleep(3)

    saveFile(movieMap, 'weekSearchNum.txt')
    return HttpResponse("cleantha love love love you!!!")


def saveFile(saveData, filename):
    filesPath = os.path.join(os.path.dirname(__file__), '..', 'files').replace('\\','/')
    # filePath = str(filesPath) + '/movieSearchNum.txt'
    filePath = str(filesPath) + '/' + str(filename)

    fileHandler = open(filePath, 'w')
    for key, value in dict(saveData).items():
        fileHandler.writelines(str(key) + '-' + str(value) + '\n')

    fileHandler.close()

def sinaSpider(request):
    movieName = '泰囧'
    url = 'http://s.weibo.com/weibo/' + movieName + '&timescope=custom:2012-11-30-0:2013-04-05-0&Refer=g'

    proxy_support = urllib2.ProxyHandler({'http': 'http://127.0.0.1:8087'})
    opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
    urllib2.install_opener(opener)

    try:
        print 'searchNum=' + str(simpleSpider(url))
    except:
        proxy_support = urllib2.ProxyHandler({'http': 'http://127.0.0.1:8087'})
        opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
        urllib2.install_opener(opener)

    #设置代理 防止新浪封IP
    # proxy_support = urllib2.ProxyHandler({'http': 'http://127.0.0.1:8087'})
    # opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
    # urllib2.install_opener(opener)
    #
    try:
        request = urllib2.Request(url)
        request.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:5.0)')
    #
        response = urllib2.urlopen(request)
        the_page = response.read()
    except:
        pass
    #
    # cleaSoup = BeautifulSoup(the_page)
    #
    # scripts = cleaSoup.findAll('script')

    # print scripts

    #why!!!!
    # # rp = re.compile(r'span class=\"W_textc\"(.*?)span')
    # rp = re.compile(r'W_textc(.*?)span')
    # result = rp.findall(str(scripts))
    # rp = re.compile(r' (.*?) ')

    # rp = re.compile(r'W_textc(.*?)span')
    # result = rp.findall(str(scripts))
    # print result
    # rp = re.compile(r' (.*?) ')
    # itemlist = rp.findall(str(result))
    # print itemlist
    # newItemList = map(lambda x: x.replace(',', ''), itemlist)
    # print newItemList
    # rp = re.compile(r'\b(?:\d)+')
    # for item in newItemList:
    #     match = rp.match(str(item))
    #     if match:
    #         print str(item) + '   cleantha'

    return HttpResponse(the_page)

    # url = 'http://weibo.sina.com'

    # request = urllib2.Request(url='http://weibo.sina.com')
    # %25E6%25B3%25B0%25E5%259B%25A7
    # request = urllib2.Request(url='http://s.weibo.com/weibo/王小土予&timescope=custom:2012-11-30-0:2013-04-05-0&Refer=g')
    # req.headers
    # print the_page
    # print type(the_page)
    # print cleaSoup.title
    # print cleaSoup.findAll(text=re.compile(r"^\u627e\u5230"))
    # siteUrls=soup.findAll('span',attrs={'class':'g'})
    # print cleaSoup.findAll('span', attrs={'class': 'W_textc'})
    # urls_pat=re.compile(r'<span class="g">(.*?)</span>')
    # print cleaSoup.findAll(re.compile(r'<span class=\"W_textc\">(.)<\/span>'))

    # new_page = str(scripts).replace('script', 'div')
    # cleaSoup = BeautifulSoup(new_page)
    # cleaSoup.findAll(re.compile(r'span class=\"W_textc\"(.*?)'))

    # scriptList = list(str(scripts).split('script'))
    # for para in scriptList:
    #     print para + '!!!'

    # user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    # values = {'name': 'WHY',
    #           'location': 'SDU',
    #           'language': 'Python'}

    # headers = {'User-Agent': user_agent}
    # data = urllib.urlencode(values)
    # req = urllib2.Request(url, headers)
    # response = urllib2.urlopen(req)
    # the_page = response.read()