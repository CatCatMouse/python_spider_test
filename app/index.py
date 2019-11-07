import requests, time, os
from bs4 import BeautifulSoup
from urllib import parse
sysType = os.name
nowTime = time.strftime("%Y-%m-%d", time.localtime())
if sysType == 'nt':
    file_path = os.getcwd() + "\\..\\download\\"+nowTime+"\\"
else:
    file_path = os.getcwd() + "/../download/"+nowTime+"/"


# webIp = "119.6.103.213:9080"
# url = "http://" + webIp + "/"

# 获取页面内容
def request_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        # response.encoding = requests.utils.get_encodings_from_content(response.text)
        # response.encoding = 'utf-8'
        return response
    else:
        return False
# 获取内容中的a标签列表
def get_all_a_title(html,title):
    titles = BeautifulSoup(html, 'html.parser')
    return titles.find_all(title)
# 创建文件夹
def make_file(path):
    if False == os.path.exists(path):
        return os.mkdir(path)
    else:
        return False
# 创建文件
# 1
# 2

# 逐层递归爬取页面
def spiders(urlPath, filePath):
    global url
    make_file(filePath)
    content = request_content(urlPath)
    if content:
        content = content.text
    else:
        return False
    a_titles = get_all_a_title(content, 'a')

    if isinstance(a_titles, list):
        for val in a_titles:
            if val.string == '[转到父目录]':
                continue
            # a标签内容
            href = val['href']
            # 判断是否是文件
            isFile = href.rsplit('.', 1)
            # 文件名
            file_dir = val.string
            file_dir = file_dir.replace(' ', '')
            file_dir = file_dir.replace('/', '')
            file_dir = file_dir.replace('\\', '')
            # 为1链接
            print("正在爬取:"+url + parse.unquote(href))
            # > 1 文件
            # 请求内容
            fileContent = request_content(url + href)
            # 获取头信息
            if fileContent:
                content_type = fileContent.headers['content-type']
                if 'text/html' in content_type:
                    if os.name == 'nt':
                        spiders(url + href, filePath + file_dir + "\\")
                    else:
                        spiders(url + href, filePath + file_dir + '/')
                else:
                    if os.path.exists(filePath + file_dir + '.' + isFile[1]):
                        pass
                    else:
                        with open(filePath + file_dir + '.' + isFile[1], "wb") as code:
                            code.write(fileContent.content)
try:
    while True:
        url = input("请输入地址:")
        if 'http' in url:
            pass
        else:
            url = 'http://' + url
        confirm = input("您输入的地址是"+url+"!  yes/no:")
        if 'yes' in confirm:
            break
    print("正在从"+url+"下载"
                    "资源中...")
    spiders(url, file_path)
    print("爬取完成")
except IOError:
    print("下载失败")

