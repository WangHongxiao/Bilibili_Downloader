import os
import requests
import time
import json


headers = {
      'referer': 'http://www.bilibili.com/',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0'
    }

def downloadFile(name, url): #url下载模块
    r = requests.get(url, stream=True, headers=headers)
    print("\nDownload Startd")
    dt_start = time.time()#下载时间开始计时
    length = float(r.headers['content-length'])
    print("VideoFileSize:" + str(length/ 1024 / 1024) +"m\n")
    f = open(name, 'wb')
    count = 0
    count_tmp = 0
    time1 = time.time()
    for chunk in r.iter_content(chunk_size = 512):
        if chunk:
            f.write(chunk)
            count += len(chunk)
            if time.time() - time1 > 1.0:
                p = count / length * 100
                speed = (count - count_tmp) / 1024 / 1024 / 1
                count_tmp = count
                print("文件下载进度" +  ': ' + formatFloat(p) + '%' + ' Speed: ' + formatFloat(speed) + 'M/S Time remaining:' + str((length-count)/1024/1024/speed) + "s")
                time1 = time.time()
    f.close()
    dt_end = time.time()#下载时间计时结束
    dt_c= dt_end - dt_start#下载时间计算
    print("\n下载完成")
    print('\ntime cost '+ str(dt_c)+ 's')
    print('avg speed: ' + str(count/dt_c/ 1024 / 1024) + 'm/s\n')
    
def formatFloat(num):
    return '{:.2f}'.format(num)

def jxurl(burl):
    global upinfo_dic,videoinfo_dic,downinfo
    r = requests.get(burl)
    r.encoding = 'utf-8'
    source = r.text
    source = source.split('<script>window.__playinfo__=')[1]
    source = source.split('</script>')[0]
    downinfo_dic = json.loads(source)
    downinfo = downinfo_dic['data']['dash']

    videoinfo = r.text
    videoinfo = videoinfo.split('window.__INITIAL_STATE__=')[1] 
    videoinfo = videoinfo.split(';(function()')[0]
    videoinfo_dic = json.loads(videoinfo)

    upinfo_dic = videoinfo_dic['upData']
    videoinfo_dic = videoinfo_dic['videoData']
burl = input("请输入B站播放页Url 多p视频如果只需下载单个请参照?p=1指定p下载：");
jxurl(burl)

print("您输入了视频\n%s\nAvid:%s \nBid:%s\nUpName:%s\n共%sP" %(videoinfo_dic['title'],videoinfo_dic['aid'],videoinfo_dic['bvid'],upinfo_dic['name'],videoinfo_dic['videos']))
if(videoinfo_dic['videos'] > 1):
    if("?p=" in burl):
        for i in range(1,videoinfo_dic['videos']):
            jxurl("https://www.bilibili.com/video/" + videoinfo_dic['bvid'] + "?p=" +str(i))
            print("\n第%sP视频文件开始下载\n" %(str(i)))
            downloadFile(videoinfo_dic['title']+"_p" + str(i) + ".mp4",downinfo['video'][0]['base_url'])
            print("\n第%sP音频文件开始下载\n" %(str(i)))
            downloadFile(videoinfo_dic['title']+"_p" + str(i) + ".mp3",downinfo['audio'][0]['base_url'])
    else:
        jxurl(burl)
        print("\n视频文件开始下载\n" )
        downloadFile(videoinfo_dic['title']+".mp4",downinfo['video'][0]['base_url'])
        print("\n音频文件开始下载\n")
        downloadFile(videoinfo_dic['title']+".mp3",downinfo['audio'][0]['base_url'])
else:
    print ("开始下载")
    jxurl(burl)
    print("\n视频文件开始下载\n")
    downloadFile(videoinfo_dic['title']+".mp4",downinfo['video'][0]['base_url'])
    print("\n音频文件开始下载\n")
    downloadFile(videoinfo_dic['title']+".mp3",downinfo['audio'][0]['base_url'])
input("任意键退出");
