from RAG.TxtReader import txtReader as TxtReader
import os

analystDirectoryPath = '../../Docs/'

def searchDoc(searchKeyword, analystName):
    directory = analystDirectoryPath + analystName
    searchedFile = []
    for fileName in os.listdir(directory):
        if fileName.endswith('.txt'):
            docContent = TxtReader.read_doc(analystName + "/" + fileName)
            if any(keyword in docContent for keyword in searchKeyword):
                searchedFile.append(fileName)
    if len(searchedFile) > 0:
        return searchedFile
    else:
        return searchAllDoc(analystName)

def searchAllDoc(analystName):
    directory = analystDirectoryPath + analystName
    searchedFile = []
    for fileName in os.listdir(directory):
        if fileName.endswith('.txt'):
            searchedFile.append(fileName)
    return searchedFile

def makeDoc2Json(searchedFiles: list, analystName):
    directory = analystDirectoryPath + analystName
    result = []
    for fileName in os.listdir(directory):
        for docName in searchedFiles:
            if fileName == docName:
                docContent = TxtReader.read_doc(analystName + "/" + docName)
                result.append({
                    "id": f"{fileName}",
                    "doc": docContent
                })
    return result


# print(searchDoc(["예시"], analystName = 'Analyst1'))
# print(makeDoc2Json(searchDoc(["예시"], analystName = 'Analyst1'), analystName = 'Analyst1'))