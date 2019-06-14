import requests
import json, time
try:
    from news_project.newsfeeds import NewsFeeds
except:
    from newsfeeds import NewsFeeds



class NewsBreak():
    def __init__(self):
        self.data = {
            "clientInfo": {
                "deviceInfo": {
                    "model": "MIX 2",
                    "device": "chiron",
                    "androidVersion": "8.0.0",
                    "screenWidth": 1080,
                    "screenHeight": 2030
                },
                "userInfo": {
                    "mac": "02:00:00:00:00:00",
                    "language": "zh",
                    "country": "CN",
                    "serviceProvider": "WIFI"
                }
            }
        }
        self.headers = {
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 8.0.0; MIX 2 MIUI/V10.2.2.0.ODECNXM)',
        }
        self.cookies = {
            'JSESSIONID': 'bV9kSkqHnHWIWsl6YJ6Vuw',
        }

    # 解析Post请求，获取docid
    def parsingPost(self, url):
        try:

            res = requests.post(url= url, headers=self.headers, data= self.data, cookies= self.cookies).text
            data = json.loads(res)
            result = data['result']
            docList = []
            for i in result:
                try:
                    docList.append(i['docid'])
                except:
                    pass
            return ','.join(i for i in docList)

        except BaseException as e:
            NewsFeeds().point_log(str(NewsFeeds().localTime(time.time())), 'NewsBreakPost', str(e))

    # 解析Get请求
    def parsingGet(self, url):
        try:
            res = requests.get(url, headers=self.headers, cookies=self.cookies).text
            data = json.loads(res)
            result = data["documents"]
            urlList=[]
            for i in range(len(result)):
                sourceUrl = result[i]['url']
                urlList.append(sourceUrl)
            return urlList
        except BaseException as e:
            NewsFeeds().point_log(str(NewsFeeds().localTime(time.time())), 'NewsBreakGet\t', str(e))





if __name__ == '__main__':


    post_url='http://api.particlenews.com/Website/channel/news-list-for-best-channel?cstart=0&infinite=true&refresh=1&epoch=5&distribution=newsbreak&platform=1&cv=4.7.3&cend=10&appid=newsbreak&weather=true&fields=docid&fields=date&fields=image&fields=image_urls&fields=like&fields=source&fields=title&fields=url&fields=comment_count&fields=fb_share_total&fields=coach_mark_text&fields=up&fields=down&fields=summary&fields=favicon_id&fields=dominant_image&fields=contextMeta&fields=video_urls&fields=viewType&push_refresh=0&modularize=true&ts=2019-04-07+18%3A14%3A01+%2B0800&version=020025&net=wifi'

    nb=NewsBreak()
    docId=nb.parsingPost(url=post_url)
    get_url = 'http://api.particlenews.com/Website/contents/content?related_docs=false&cv=4.7.3' \
              '&docid=' + docId + \
              '&appid=newsbreak&bottom_channels=false&distribution=newsbreak&platform=1&version=020025&net=wifi'
    u=nb.parsingGet(url=get_url)
    print(u)