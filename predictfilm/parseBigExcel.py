# This Python file uses the following encoding: utf-8

import xlrd
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

    fileDateFile = open('./filtDate.txt', 'r')

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