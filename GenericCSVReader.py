def main(): #Example
    distanceList = readCSVFile("distances3.csv")
    newDistanceList = searchDataList(distanceList, Travel_Mode = ('cycle','car', 'walk')) # search anything with travel mode 'cycle' or 'car'
    newDistanceList = searchDataList(newDistanceList, Source_State = 'NSW') # search within the new subset if anything's source is 'WA'
    newDistanceList = [i for i in newDistanceList if float(i['Distance']) < 100.0] # search within the new new subset that it has a distance of < 100.0
    concisePrint(newDistanceList, 'Source', 'Travel_Mode', 'Destination', 'Distance', 'Time') #print the attributes specified

def concisePrint(dataList = [], *attributes):
    for data in dataList:
        print({k: v for k, v in data.items() if k in attributes})

def searchDataList(dataList = [], **keywords):
    newDataList = []
    for data in dataList:
        for kw in keywords:
            if (kw in data) and (data[kw] in keywords[kw]):
                newDataList.append(data)
                break

    return newDataList

def readCSVFile(path):
    dataList = []

    f = open(path,'r')
    read_data = f.read()
    lineList = read_data.split("\n")

    dataClassification = lineList[0].split(",") #Use the first line as the attributes
    del lineList[0]

    for line in lineList:
        dataDict = {}
        tmpList = line.split(",")
        for i, data in enumerate(tmpList):
            try:
                dataDict[dataClassification[i]] = str(data)
            except (IndexError):
                pass

        dataList.append(dataDict)

    return dataList

if __name__ == "__main__":
    main()
