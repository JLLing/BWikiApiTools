import os
import csv
import json
import time
import requests
from requests_toolbelt import MultipartEncoder

url = ""
cookie = ""
headers = ""
query = {
    "format": "json",
    "token": ""
}

def setConfig():
    with open('config.json', 'r') as f:
        global url, cookie
        config = json.loads(f.read())
        url = config["url"]
        cookie = config["cookie"]
        return True

def getHeaders():
    setConfig()
    headers = { }
    #headers["User-Agent"] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0',
    headers["Cookie"] = cookie
    return headers

def getToken():
    params = {}
    params["action"] = "query"
    params["format"] = "json"
    params["meta"] = "tokens"
    response = json.loads(requests.get(url=url,headers=headers, params=params).text)
    query["token"] = response["query"]["tokens"]["csrftoken"]
    print(query["token"])
    return query["token"]

def checkToken():
    data = query
    data["action"] = "checktoken"
    data["type"] = "csrf"
    return print(requests.post(url=url,headers=headers,data=data).text)

def edit(title, text):
    data = query
    data["action"] = "edit"
    data["title"] = title
    data["text"] = text
    print(data)
    return requests.post(url=url,headers=headers,data=data).text

def templateDataFormatter(title, row):
    data = { }
    data["title"] = row[0]
    data["text"] = "{{" + row[1] + "\n"
    keyNum = len(title)
    for i in range(2, keyNum):
        data["text"] += "|" + title[i] + "=" + row[i] + "\n"
    data["text"] += "}}"
    return data

def updateWithCSV(filename):
    with open(filename)as f:
        f_csv = csv.reader(f)
        f_title = []
        num = 0
        for row in f_csv:
            num += 1
            if num == 1:
                f_title = row
            else:
                data = templateDataFormatter(f_title, row)
                print(edit(data["title"], data["text"]))

def updateWithFolder(rootdir):
    list = os.listdir(rootdir) #列出文件夹下所有的目录与文件
    for i in range(0,len(list)):
        path = os.path.join(rootdir,list[i])
        filetype = os.path.splitext(path);
        if os.path.isfile(path) and (filetype[1] == ".txt"):
            with open(path, 'r', encoding="utf-8") as f:
                data = { }
                data["title"] = os.path.basename(path).replace(".txt", "")
                data["text"] = f.read()
                print(edit(data["title"], data["text"]))

def getPageContent(title):
    data = query
    data["action"] = "visualeditor"
    data["page"] = title
    data["paction"] = "wikitext"
    response = requests.post(url=url,headers=getHeaders(),data=data).text
    return json.loads(response)["visualeditor"]["content"]

def addToCategory(category, title):
    data = query
    data["action"] = "edit"
    data["title"] = title
    data["prependtext"] = "[[分类:" + category + "]]\n"
    return requests.post(url=url,headers=getHeaders(),data=data).text
    
def addToCategoryWithCSV(category, filename):
    with open(filename)as f:
        f_csv = csv.reader(f)
        for title in f_csv:
            print(addToCategory(category, title[0]))
            time.sleep(2)

def clearCache(titles):
    data = query
    data["action"] = "purge"
    data["titles"] = titles
    return requests.post(url=url,headers=getHeaders(),data=data).text

headers = getHeaders()
query = {
    "format": "json",
    "token": getToken()
}
checkToken()



