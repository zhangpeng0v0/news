import requests
import time
import json
import re
import hashlib
try:
    from news_project.newsfeeds import NewsFeeds
except:
    import sys
    sys.path.append('news_project')
    from newsfeeds import NewsFeeds




class TopBuzz():
    def __init__(self):
        # 请求头信息
        self.headers = {
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 8.0.0; MIX 2 MIUI/V10.2.2.0.ODECNXM) NewsArticle/8.4.4'
        }
        self.cookies = {
            'cookies': 'install_id=6672646082571388678; ttreq=1$a9ed7f4ce8fc84fced473d6e25c22226f381c13d; odin_tt=3e76568447d177856560d524c6ef5400407a437cfdd62767a36fb3b2decdeb01d43b9a7978232dc05c57af3c81bd10c277e78619093795e8392c1302c9aa8a75; sid_guard=c8f84a23bcce86b376964aeb42991709%7C1554173959%7C5184000%7CSat%2C+01-Jun-2019+02%3A59%3A19+GMT; uid_tt=2ad7176029f7302e11b7924e6e6566b7120075732cedcd39bc999fa5cbcf07a1; sid_tt=c8f84a23bcce86b376964aeb42991709; sessionid=c8f84a23bcce86b376964aeb42991709',
        }


    # TopBuzz列表页时间戳解析
    def hash_code(self, pwd):
        # 通过模块构造出一个hash对象
        h = hashlib.sha1()
        h.update(pwd.encode())
        # 获得字符串类型的加密后的密文
        return h.hexdigest()


    # TopBuzz解析列表页面
    def sendRequest(self, url):
        try:
            res = requests.post(url=url, headers=self.headers, cookies=self.cookies).text
            data = json.loads(res)
            item = data['data']['items']
            # 分析获取的json
            urlList=[]
            for i in range(len(item)):
                # 数据来源
                sourceUrl = item[i]['article_url']
                urlList.append(sourceUrl)
            return urlList

        except BaseException as e:
            NewsFeeds().point_log(str(NewsFeeds().localTime(time.time())), 'TopBuzzSendRequest\t', str(e))




if __name__ == '__main__':
        tb=TopBuzz()
        # 访问时间
        t = time.time()
        #正则匹配时间戳小数位
        result=re.findall('.\d*',str(t))
        sign=tb.hash_code(result[1][1:])
        timestamp=result[0]

        url = 'https://i16-tb.isnssdk.com/api/844/stream?session_impr_id=0&tab=General&count=20&min_behot_time=1.554174097999E9&loc_mode=7&lac=4314&cid=6439033' \
              '&sign='+sign+ \
              '&timestamp='+timestamp+ \
              '&logo=topbuzz&gender=0&bv_is_auto_play=0&youtube=0&manifest_version_code=844&app_version=8.4.4&iid=6672646082571388678&gaid=54b268f4-52c2-470c-a815-abd1d00acce9&original_channel=gp&channel=gp&fp=TlTrJzK1FYsqFYs5PlU1LMGSL2Xr&device_type=MIX+2&language=en&app_version_minor=8.4.4.01&resolution=2030*1080&openudid=ab50caa43e995042&update_version_code=8440&sys_language=zh&sys_region=cn&os_api=26&tz_name=Asia%2FShanghai&tz_offset=28800&dpi=440&brand=Xiaomi&ac=WIFI&device_id=6672637176796333574&os=android&os_version=8.0.0&version_code=844&hevc_supported=1&device_brand=Xiaomi&device_platform=android&sim_region=cn&region=us&aid=1106&ui_language=en'

        a=tb.sendRequest(url=url)
        print(a)

