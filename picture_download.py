import requests
import re
import tkinter as tk
import os
from tkinter.filedialog import askdirectory

def getHTMLPage(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, timeout = 10, headers=headers)
        r.encoding = 'utf-8'
        #r.encoding = r.apparent_encoding
        #print(r.encoding)
        #print(r.text)
        return r.text
    except:
        return ''

def getPicsUrl(html, list):
    #print('getPicsUrl begin')
    #list = []
    rURL = re.compile(r'\"thumbURL\":\"https.*?\"')
    for i in rURL.findall(html):
        list.append(((i.split(':', maxsplit=1))[-1]).split('"')[1])
    #print('getPicsUrl end')

def getPic(url):
    #print('getPic begin')
    try:
        r = requests.get(url)
        r.encoding = 'utf-8'
        return r.content
    except:
        return ''
    #print('getPic end')

def savePics(list, path):
    global count
    global picNum
    for i in list:
        if count > 0:
            try:
                pic = getPic(i)
                with open(path+'%d.jpg' % (picNum-count+1), 'wb') as f:
                    f.write(pic)
                    f.close()
                    #print('\r当前进度：{:.2f}%'.format(100*count/picNum), end = '') #print()的end控制结尾字符，默认是\n
            except:
                continue
            count -= 1
            print('\r当前进度：%.2f%%' % (100 * (picNum-count) / picNum), end='')  # print()的end控制结尾字符，默认是\n
            downloadRate.config(text='当前进度：%.2f%%' % (100*(picNum-count)/picNum))
            #root.update_idletasks() #只刷新界面，不处理用户请求，此时拖动窗口等操作是无效的
            root.update()           #刷新用户的所有请求


def path_choose():
    path = askdirectory()
    path_tmp.set(path)

def hit():
    try:
        global picNum
        global count

        #path = 'D:/Pics/'
        path = path_tmp.get()
        path = path + '/'
        url = 'https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&sf=1&fmq=&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&fm=index&pos=history&word='
        if not os.path.exists(path):
            os.mkdir(path)

        pics = pics_input.get()
        picNum = num_input.get()
        picNum = int(picNum)
        depth = picNum // 30 + 1  # 搜寻的页面数
        count = picNum  # 计数---百分比和图片命名
        list = []

        for i in range(depth):
            if i == 0:
                html = getHTMLPage(url + pics)
            else:
                urlNext = 'https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=' + pics + '&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=&z=&ic=&word=' + pics + '&s=&se=&tab=&width=&height=&face=&istype=&qc=&nc=&fr=&pn=' + str(
                    i * 30)  # +'&rn=30&gsm=&1497266879881='
                html = getHTMLPage(urlNext)
            getPicsUrl(html, list)
            savePics(list, path)
            list = []
    except:
        pass



root = tk.Tk()
root.title('图片下载工具')
root.geometry('700x400')
root.resizable(width = False, height = False) #界面大小固定

pics_label = tk.Label(root, text = '请输入图片查询关键词:', font = ('Arial',12), width = 30, height = 2)
pics_label.place(x=10,y=20)
pics_input = tk.Entry(root, show = None)
pics_input.place(x = 350, y = 35)

num_label = tk.Label(root, text = '请输入要下载的数量:', font = ('Arial',12), width = 30, height = 2)
num_label.place(x=10,y=100)
num_input = tk.Entry(root, show = None)
num_input.place(x = 350, y = 112)

path_tmp = tk.StringVar()
path_label = tk.Label(root, text = '请选择存储位置:', font = ('Arial',12), width = 30, height = 2)
path_label.place(x=10, y=180)
#path_text = tk.Text(root, width = 20, height = 2)
#path_text.place(x=350,y=189)
tk.Entry(root, textvariable = path_tmp, show = None).place(x=350,y=189)
path_button = tk.Button(root, text = '...', width = 3, height = 1, command = path_choose)
path_button.place(x=540, y=182)

b = tk.Button(root, text = '下载', width = 30, height = 3, command = hit)
b.place(x = 50, y = 270)

downloadRate = tk.Label(root, text = '当前进度：', width = 30, height = 3)
downloadRate.place(x=330,y=270)

#copy_right = tk.Label(root, text = 'by 冰冻', width = 10, height = 3)
#copy_right.place(x=600, y=350)

picNum = 0
count = 0

root.mainloop()

