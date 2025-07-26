from RAG.TxtReader import txtReader as TxtReader
import os

analystDirectoryPath = '../../Docs/'
searchKeyword = ["예"]

def searchDoc(searchKeyword, analystName):
    directory = analystDirectoryPath + analystName
    for fileName in os.listdir(directory):
        if fileName.endswith('.txt'):
            docContent = TxtReader.read_doc(analystName + "/" + fileName)
            if any(keyword in docContent for keyword in searchKeyword):
                print(f"{fileName}에 키워드가 포함되어 있습니다.")

searchDoc(searchKeyword, analystName = 'Analyst1')