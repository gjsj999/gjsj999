import urllib.request
import ssl
import re
import json
import sys

home_file = r'../../../README.md'
url_list_file = r'../../../url_list.txt'
baned_list_file = r'../../../baned_list.txt'
check_url = 'https://check.uomg.com/api/urlsec/wall?token=fc74d511ff2c7606304f22a423b2fe19&domain='

def check_baned(url, retry=0):
    if retry == 4 : 
        return -1
    print("检测是否被墙："+url)
    api = check_url + url
    print("API: " + api)
    req = urllib.request.Request(api)
    context = ssl._create_unverified_context()
    f = urllib.request.urlopen(req,context=context)
    resp = json.loads(f.read().decode('utf-8')) 
    code = resp['code']
    print("检测返回："+str(code)+", "+ resp['msg'])
    if code == '-1':
        print("API 出错，重试")
        return check_baned(url,retry + 1)
    return code
      

def current_url():
    match_reg = re.compile(r'[(](.*?)[)]', re.S)  #最小匹配
    with open(home_file, "r", encoding="utf-8") as f:
        for line in f:
            urls = re.findall(match_reg, line)
            if len(urls) > 0 :
                url = urls[0]
                return url
    return ""   

def record_baned_url(str):
    with open(baned_list_file,"a") as file:
        file.write(str+"\n")

def check_and_pick():
    result_url = ""
    content = ""
    with open(url_list_file, "r", encoding="utf-8") as f:
        for url in f:
            url = url.replace("\n","")
            if result_url == "" :
                if len(url) > 0:
                    code = check_baned(url)
                    if(code == 200 or code == '200'):
                        result_url = url
                        content += url
                    else:
                        print("发现不可用url，做记录："+url)
                        record_baned_url(url)
                else:
                    content += url
            else:
                content += url
    with open(url_list_file,"w",encoding="utf-8") as f:
        f.write(content)
    return result_url

def replaceHomeUrl(old_url,new_url):
    file_data = ""
    with open(home_file, "r", encoding="utf-8") as f:
        for line in f:
            if old_url in line:
                line = line.replace(old_url,new_url)
            file_data += line
    with open(home_file,"w",encoding="utf-8") as f:
        f.write(file_data)

# steps   -----------
#获取当前url
curr = current_url()
if len(curr) <= 0:
    print("没有查找到当前的url")
    #终止
    sys.exit()

print("检测url: " + curr)
#检测是否被墙
code = check_baned(curr)

if code == 200 or code == '200' :
    print("一切正常")
    sys.exit()

print("被墙了，做记录")
record_baned_url(curr)
print("读取备用列表")
new_url = check_and_pick()
if len(new_url) > 0 :
    print("替换为新的可用域名, 老域名：" + curr + ", 新域名："+new_url)
    replaceHomeUrl(curr,new_url)
    print("替换完成，进行提交")
else:
    print("错误：当前的被墙了，也没找到新的可用的，需要买新域名了")
