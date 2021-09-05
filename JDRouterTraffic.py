import json
import requests
import datetime
import time

uploadcount=0
downloadcount=0
loginUrl = 'http://192.168.68.1/api/login'
loginData = {'password':'XXXXXXXXXX'} # XXXXXXXXXX在登录时发送的包里获得
Headers = {
    'Accept':'application/json, text/plain, */*',
    }
dumpJsonData = json.dumps(loginData)
print(f"dumpJsonData = {dumpJsonData}")
res = requests.post(loginUrl, data=dumpJsonData, headers=Headers, allow_redirects=True)
print(f"statusCode = {res.status_code}, res text = {res.text}") #responseTime = {datetime.datetime.now()}, 
token=json.loads(res.text)
token=token['data']['token']

postUrl = 'http://192.168.68.1/api/api_wrapper'
#payloadData数据
payloadData = {"payload":[
    #{"method":"idc.get_all"},
    {"method":"wan.ipstat.get_realspeed"}],
        "version":"1.0.0",
        "action":"call"}

# Header
payloadHeader = {
    #'Accept':'application/json, text/plain, */*',
    #'Accept-Encoding': 'gzip, deflate',
    #'Accept-Language':'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    #'Connection':'keep-alive',
    #'Content-Type':'application/json;charset=UTF-8',
    #'Host': '192.168.68.1',
    #'Origin':'http://192.168.68.1',
    #'Referer':'http://192.168.68.1',
    'User-Agent':"Mozilla/5.0(Windows NT 10.0; Win64; x64)AppleWebKit/537.36(KHTML, like Gecko)Chrome/88.0.4324.190 Safari/537.36",
    #'X-Token': token,
    'Cookie': 'd2admin-1.5.6-uuid=; d2admin-1.5.6-token='+token
}
print(token)
r = requests.post(postUrl,data=json.dumps(payloadData),headers=payloadHeader)
dumpJsonData = json.dumps(payloadData)
print(f"dumpJsonData = {dumpJsonData}")
while(1):
    res = requests.post(postUrl, data=dumpJsonData, headers=payloadHeader, allow_redirects=True)
    #print(f"responseTime = {datetime.datetime.now()}, statusCode = {res.status_code}, res text = {res.text}")
    total=json.loads(res.text)
    totalupload=total['result'][0]['data']['total']['upload']
    totaldownload=total['result'][0]['data']['total']['download']
    downloadspeed=total['result'][0]['data']['total']['download_speed']
    uploadspeed=total['result'][0]['data']['total']['upload_speed']
    uploadcount+=uploadspeed
    downloadcount+=downloadspeed
    print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}    总传输量")
    print(f"upload={uploadspeed/8:.2f}KB/S      {uploadcount/8192:.2f}MB\ndownload={downloadspeed/8:.2f}KB/S      {downloadcount/8192:.2f}MB\n")
    time.sleep(2.1)#2.1ms是因为路由器随机延迟发送数据包
