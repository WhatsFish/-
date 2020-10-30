# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 20:43:12 2020

@author: User
"""
from bs4 import BeautifulSoup

import urllib3


raw_urls = ["http://stic.sz.gov.cn/zxbs/kjtj/index.html", \
            "http://stic.sz.gov.cn/zxbs/kjtj/index_2.html", \
            "http://stic.sz.gov.cn/zxbs/kjtj/index_3.html", \
            "http://stic.sz.gov.cn/zxbs/kjtj/index_4.html"]
all_money = [[], [], [], [], [], [], []]
all_acc_money = [[], [], [], [], [], [], []]
all_rate = [[], [], [], [], [], [], []]
dic = {"全行业产值" : 0, "1. 电子与信息行业" : 1, "2. 生物、医药行业" : 2, "其中" : 1, \
       "3. 先进制造行业" : 3, "4. 新能源行业" : 4, "5. 新材料行业" : 5,"6. 其他高技术行业" : 6, \
           "4. 新能源、新材料行业" : 4, "5. 其他高技术行业" : 6}

http = urllib3.PoolManager()

url_strs = []
# 从主页面中读取78个子页面链接，存到url_strs中
for raw in raw_urls:
    r = http.request('GET',raw)
    html_doc = r.data.decode()
    soup = BeautifulSoup(html_doc, "html.parser", from_encoding="utf-8")
    links = soup.find_all('a')
    urls = soup.find_all(name='div',attrs={"class":"item"})
    for url in urls:
        url_strs.append(url.a['href'])

# 循环每个子页面   
cn = 1
for url_sub in url_strs :
    print(url_sub + " " + str(cn))
    cn = cn + 1
    if url_sub == "http://stic.sz.gov.cn/zxbs/kjtj/content/post_2908299.html":
        continue
    if url_sub == "http://stic.sz.gov.cn/zxbs/kjtj/content/post_2908315.html":
        break;
    r = http.request('GET', url_sub)
    html_doc = r.data.decode()
    soup = BeautifulSoup(html_doc, "html.parser", from_encoding="utf-8")
    trs = soup.find_all('tr')
    print(len(trs))
    # 循环每一行
    for i in range(len(trs)):
        if i == 0:
            continue
        tr = trs[i]
        tds = tr.find_all('td')
        cur = 0 #记录到哪一行了
        cnt = 0 #记录到哪一列
        # 循环每一列
        for j in range(len(tds)):
            td = tds[j]
            if len(td.find_all('p')) == 1:
                cell = td.p.string
                if cell == None:
                    cell = "0"
                else:
                    cell = cell.strip()
            else:
                cell = td.string
                if cell == None:
                    cell = "0"
                else:
                    cell = cell.strip()
            # 跟据第一列判断之后数据填放位置
            if j == 0:
                cur = dic[cell]
            else:
                if cell == "1. 电子与信息行业":
                    continue;
                #print("hhh")
                if cnt == 0:
                    all_money[cur].append(cell)
                elif cnt == 1:
                    all_acc_money[cur].append(cell)
                elif cnt == 2:
                    all_rate[cur].append(cell)
                cnt = cnt + 1
        
        
        
        
        
        
        
        
        