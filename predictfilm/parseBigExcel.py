# This Python file uses the following encoding: utf-8

import xlrd
import pylab
import os

def parse():
    filesPath = os.path.join(os.path.dirname(__file__), '..', 'files').replace('\\','/')
    filePath = str(filesPath) + '/bigMovieData.xls'
    saveFilePath = str(filesPath) + '/movieSearchByDate.txt'

    data = xlrd.open_workbook(str(filePath))
    table = data.sheet_by_index(0)
    nrows = table.nrows
    ncols = table.ncols

    searchDateList = []
    searchDateSimpleList = []
    for rownum in range(0, nrows):
        searchDateList.append(table.row_values(rownum)[5].encode('utf-8'))

    searchDateSimpleList = list(set(searchDateList))
    searchDateSimpleList.sort(key=searchDateList.index)

    movieSearchNumByDateDict = {}

    for date in searchDateSimpleList:
        movieSearchNumByDateDict[date] = []

    for date in searchDateSimpleList:
        for rownum in range(0, nrows):
            try:
                movieNum = int(table.row_values(rownum)[1].encode('utf-8'))
                movieSearchNum = int(table.row_values(rownum)[4].encode('utf-8'))
                if table.row_values(rownum)[5].encode('utf-8') == date:
                    movieSearchNumByDateDict[date].append([movieNum, movieSearchNum])
            except:
                pass

    # file = open(saveFilePath, 'w')
    # for key, value in movieSearchNumByDateDict.items():
    #     file.write(str(key) + '----------------\n')
    #     for innerList in value:
    #         file.write('movieNum--->' + str(innerList[0]) + 'movieSearchNum--->' + str(innerList[1]) + '\n')
    #
    # file.close()
    print 'successful!!!'

    return movieSearchNumByDateDict

def filtBigExcelByDictNum(movieSearchNumByDateDic, movieBoxofficeList):
    filesPath = os.path.join(os.path.dirname(__file__), '..', 'files').replace('\\','/')
    filePath = str(filesPath) + '/filtBigExcelByDictNum.txt'

    filtDateFile = open(filePath, 'w')

    for key, value in movieSearchNumByDateDic.items():
        sameCounter = 0
        for innerlist in value:
            for boxlist in movieBoxofficeList:
                if cmp(int(boxlist[0]), int(innerlist[0])) == 0:
                    sameCounter += 1
                    print str(boxlist[0]) + '--->' + str(innerlist[0]) + '\n'
                    print key

        if sameCounter >= 10:
            filtDateFile.write(str(key) + '\n')

    filtDateFile.close()

    fileDateFile = open(filePath, 'r')

    newMovieSearchNumByDateDict = {}
    for date in fileDateFile.readlines():
        # filtDate = date.split('\n')[0]
        date = date.strip('\n')
        newMovieSearchNumByDateDict[date] = movieSearchNumByDateDic[date]

    for key, value in newMovieSearchNumByDateDict.items():
        print str(key) + '-----------\n'
        for llist in value:
            print str(llist[0]) + '--->' + str(llist[1]) + '\n'

    print len(newMovieSearchNumByDateDict)

    return newMovieSearchNumByDateDict

def generateDiagramByBigExcel(movieSearchList, movieBoxofficeList, date):

    imageFilesPath = os.path.join(os.path.dirname(__file__), '..', 'media').replace('\\','/')

    diagramSearchList = []
    diagramBoxofficeList = []
    for searchlist in movieSearchList:
        for boxlist in movieBoxofficeList:
            if cmp(int(searchlist[0]), int(boxlist[0])) == 0:
                # diagramList.append([searchlist[0], searchlist[1], boxlist[1]])
                diagramSearchList.append([searchlist[0], searchlist[1]])
                diagramBoxofficeList.append([boxlist[0], boxlist[1]])

    searchNumlist = [int(clealist[1]) for clealist in diagramSearchList]
    boxofficelist = [int(clealist[1]) for clealist in diagramBoxofficeList]

    searchMax = max(searchNumlist)
    boxofficeMax = max(boxofficelist)

    ylim = max([searchMax, boxofficeMax])

    # print 'ylim--->' + str(ylim)

    # print diagramSearchList
    # print diagramBoxofficeList
    #
    # print len(diagramSearchList)
    # print len(diagramBoxofficeList)

    print ylim

    print diagramSearchList
    print diagramBoxofficeList

    newMovieSearchList = []
    for searchlist in diagramSearchList:
        newMovieSearchList.append([searchlist[0], searchlist[1]*ylim/searchMax])

    newMovieBoxofficeList = []
    for boxlist in diagramBoxofficeList:
        newMovieBoxofficeList.append([boxlist[0], boxlist[1]*ylim/boxofficeMax])

    print newMovieSearchList
    print newMovieBoxofficeList

    xlim = 0
    if cmp(len(newMovieSearchList), len(newMovieBoxofficeList)) == 0:
        xlim = len(newMovieSearchList)

    print xlim

    figureNum = int(date.replace('/', ''))

    print figureNum

    fig = pylab.figure(figureNum)
    x1 = [item for item in range(0, xlim)]
    y1 = [item[1] for item in newMovieSearchList]
    x2 = [item for item in range(0, xlim)]
    y2 = [item[1] for item in newMovieBoxofficeList]

    print x1
    print x2
    print y1
    print y2

    pylab.plot(x1, y1, color='r', linestyle='-', marker='o')# use pylab to plot x and y
    pylab.plot(x2, y2, color='g', linestyle='-', marker='o')
    pylab.title('movieSearchNum --- movieBoxoffice')# give plot a title
    pylab.xlabel('x axis')# make axis labels
    pylab.ylabel('y axis')
    pylab.xlim(0.0, xlim)# set axis limits
    pylab.ylim(0.0, ylim)
    # pylab.show()# show the plot on the screen
    totalImagePath = str(imageFilesPath) + '/images/' + date.replace('/', '') + '.png'
    print totalImagePath
    fig.savefig(totalImagePath)
