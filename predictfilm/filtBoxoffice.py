# This Python file uses the following encoding: utf-8
# __author__ = 'cutejumper'

#过滤boxoffice.xls中的数据 取总票房最大的和电影编号作为键值对传出到外部调用处

import xlrd
import os

def filtBoxofficeByMovieSeriNum():
    filesPath = os.path.join(os.path.dirname(__file__), '..', 'files').replace('\\','/')
    boxFilePath = str(filesPath) + '/boxoffice.xls'

    boxData = xlrd.open_workbook(str(boxFilePath))
    boxTable = boxData.sheet_by_index(0)
    boxNrows = boxTable.nrows
    boxNcols = boxTable.ncols

    movieNumList = []
    movieNumSimpleList = []
    movieBoxofficeList = []
    for rownum in range(1, boxNrows):
        try:
            movieNum = int(boxTable.row_values(rownum)[1].encode('utf-8'))
            movieBoxoffice = int(boxTable.row_values(rownum)[3].encode('utf-8'))
            movieNumList.append(movieNum)
            movieBoxofficeList.append([movieNum, movieBoxoffice])
        except:
            print 'exception--->' + str(boxTable.row_values(rownum)[3].encode('utf-8'))

    movieNumSimpleList = list(set(movieNumList))
    movieNumSimpleList.sort(key=movieNumList.index)

    filtBoxofficeList = []
    for movienum in movieNumSimpleList:
        singleMovieBoxofficeList = []
        for blist in movieBoxofficeList:
            if blist[0] == movienum:
                singleMovieBoxofficeList.append(blist[1])

        maxBoxoffice = max(singleMovieBoxofficeList)
        filtBoxofficeList.append([movienum, maxBoxoffice])


    for simpleList in filtBoxofficeList:
        print 'movieNum--->' + str(simpleList[0]) + 'movieBoxoffice--->' + str(simpleList[1])

    print len(filtBoxofficeList)

    return filtBoxofficeList
