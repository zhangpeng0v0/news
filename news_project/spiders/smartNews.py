import requests
import json


class SmartNews():
    def __init__(self):
        self.headers = {'User-Agent': 'SmartNews 5.4.3 (Android 8.0.0; zh_CN; MIX 2 Build/OPR1.170623.027)'}
        self.data = {
                    'Accept-Encoding':'gzip',
                    'Content-Length':'397',
                    'Content-Type':'application/x-www-form-urlencoded',
                    'Host':'www.smartnews.be',
                    'Connection':'keep-alive',
                    'deviceToken':'gw73n3ddMfRttJlu-YVFdw',
                    'timestamp':'1556004832',
                    'version':'20140105.1.android',
                    'edition':'en_ALL',
                    'timezone':'Asia/Shanghai',
                    'locale':'zh_cn',
                    'language':'zh',
                    'country':'cn',
                    'useUnifiedChannels':'true',
                    'channelIdentifiers':'cr_en_all_sports,cr_en_all_entertainment,cr_en_all_world,cr_en_all_business,cr_en_all_technology,cr_en_all_science,cr_en_all_lifestyle,cr_en_all_twitter',
                    'since':'1555916243956',
                    }
        self.url = 'http://www.smartnews.be/api/v2/refresh'
        self.detailUrl='http://sf-proxy.smartnews.com/https%3A%2F%2Fthriveglobal.com%2Fstories%2Fwhy-vision-and-mission-really-do-matter%2F?etag=4e420c3234fdf77326f69071250655fa'


    def smartNews(self):
        res = requests.post(url = self.url, headers = self.headers, data = self.data).text
        data = json.loads(res)
        items = data["items"]
        blocks = []
        for i in items:
            blocks += i['blocks']
        links = []
        for j in blocks:
            links += j['links']
        url_list = []
        for u in links:
            url_list.append(u['url'])
        return url_list


if __name__ == '__main__':
    sm = SmartNews()
    sm.smartNews()





