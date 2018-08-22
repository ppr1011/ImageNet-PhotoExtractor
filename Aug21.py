import urllib3
import re
import os
import datetime
import random

baseUrl = "http://www.image-net.org"
user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0  "
headers = {"User-Agent" : user_agent}
def search(objectName,http):
    global baseUrl,headers
    searchUrl = baseUrl + "/search?q=" + objectName
    print (searchUrl)    
    imgUrls=[]
    imgUrlList = []
    try:
        content = http.request('GET', searchUrl, headers=headers).data
        pattern = r'search_result" border-style="none"><tr><td>.*</table>'
        searchResult = re.findall(pattern,str(content))
        searchResult = searchResult[0]
        imgUrls = re.findall(r'<img src="([^"]*)"',searchResult)        
        for imgUrl in imgUrls:
            imgUrl = baseUrl+imgUrl
            imgUrlList.append(imgUrl)
    except:
        print("error")

    return imgUrlList

def mkdir(dirPath):
    dirPath = dirPath.strip()
    if(not os.path.exists(dirPath)):
        os.makedirs(dirPath)
    


def download(imgUrlList,dirPath,http):
    global headers
    print("Path:"+dirPath+",Downloading")
    for imgUrl in imgUrlList:
        randomNum=random.randint(0,100)
        nowTime=datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        uniqueNum=str(nowTime)+str(randomNum);        
        fileName = uniqueNum + ".jpg"
        content = http.request('GET', str(imgUrl),headers=headers).data
        with open(dirPath + "/" +fileName,'wb') as imageFile:
            imageFile.write(content);
    print("All done!")
    
if __name__ == "__main__": 
    http = urllib3.PoolManager(100)
    while True:
       objectName = input("Search For:")
       dirPath = "imagefiles/" + objectName
       urls = search(objectName,http)
       if (len(urls) > 0) :
           mkdir(dirPath)
       download(urls,dirPath,http)
