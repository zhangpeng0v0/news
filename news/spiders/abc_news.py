from newsapi import NewsApiClient
import time, requests, random, uuid
from lxml import etree
import urllib.parse
import urllib.request
from newspaper import fulltext
try:
    from news.filter_data import Filter_Data
    from news.save_data import Save_Data
except:
    import sys
    sys.path.append("/app/crawler/news_project/news/")
    from filter_data import Filter_Data
    from save_data import Save_Data



class ABC_News(object):
    def __init__(self):
        self.news_api = NewsApiClient(api_key='e7d5104fc5c74e259dbe2427b68257fb')
        self.key_word = ['U.S.','Lifestyle', 'Technology', 'Entertainment', 'Sports', 'Health']
        self.t = time.time()
        self.point_time = time.strftime('%Y-%m-%d', time.localtime(self.t))
        self.headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36'}
        self.cookies = {'cookie': 'cookieMonster=1; _cb_ls=1; SWID=522fc1e1-4ffd-4802-86fa-d7475f8dca57; optimizelyEndUserId=oeu1557122779744r0.05588715173473946; s_vi=[CS]v1|2E67E7728507B2CE-4000011580009D3A[CE]; __gads=ID=b52dc242d5ad893e:T=1557122797:S=ALNI_MaWnnuLLKP88qrPEsPEVuViaoGlJg; UNID=0df479d5-1639-4404-b6a8-36d731a7876d; UNID=0df479d5-1639-4404-b6a8-36d731a7876d; _cb=Dz5K21B0CX5JDkjMG; _v__chartbeat3=DbUUrKDDGTaEDqauaQ; _cb_svref=null; AkamaiAnalytics_BrowserSessionId=4d41ba72-5ab2-8f33-46aa-f5748aca9647; HTML_VisitIntervalStartTime=1557125661015; s_sess=%20s_cc%3Dtrue%3B%20s_sq%3D%3B; adnum=3undefined; _chartbeat2=.1557122809880.1557125676423.1.DoKBmGC2OW5QDWek5PEERi8oZtYZ.12; HTML_BitRateBucketCsv=0,19083,16715,0,0,0,0,0; HTML_VisitValueCookie=1|1|1|0|35798|35826|0|0|0|0|0|0|NaN; s_pers=%20s_fid%3D22C0AF24132A0778-001FDBB2DA7591AD%7C1620284117936%3B%20s_c20%3D1557125717941%7C1651733717941%3B%20s_c20_s%3DFirst%2520Visit%7C1557127517941%3B; HTML_isPlayingCount=2; GED_PLAYLIST_ACTIVITY=W3sidSI6IlhYU0wiLCJ0c2wiOjE1NTcxMjU3MzgsIm52IjowLCJ1cHQiOjE1NTcxMjU1NDQsImx0IjoxNTU3MTI1NjM3fSx7InUiOiIzbnlXIiwidHNsIjoxNTU3MTI1NzM3LCJudiI6MCwidXB0IjoxNTU3MTI1NTU2LCJsdCI6MTU1NzEyNTYyM30seyJ1IjoiWG81TSIsInRzbCI6MTU1NzEyNTczNywibnYiOjEsInVwdCI6MTU1NzEyNTU4NSwibHQiOjE1NTcxMjU3MzV9XQ..; HTML_VisitCountCookie=1'}
        self.downloadPath = '/data/crawler'
        self.picPath = '/abc_news/picture/'
        self.filter = Filter_Data()
        self.save = Save_Data()


    def run(self):
        self.parsing_abc_news_list()


    def parsing_abc_news_list(self):
        today = self.point_time
        for kw in self.key_word:
            print('keyword:\t', kw)
            news_list = self.news_api.get_everything(q = kw,
                                                  sources = 'abc-news',
                                                  domains = 'abcnews.go.com',
                                                  from_param = today,
                                                  to = today[:-1]+str(int(today[-1])-1),
                                                  language = 'en',
                                                  sort_by = 'relevancy',
                                                  page_size = 100,)
            self.parsing_news_list_url(news_list=news_list)


    def parsing_news_list_url(self, news_list):
        articles = news_list['articles']
        for i in range(len(articles)):
            details_url = articles[i]['url']
            result = self.filter.filter_data(details_url=details_url)
            if result :
                print('Data already exists!')
            else:
                time.sleep(random.uniform(1, 3))
                details_res = requests.get(details_url, headers=self.headers, cookies=self.cookies).text
                html_obj = etree.HTML(details_res)
                source = int(2)
                sourceUrl = details_url
                jobId = time.time()
                authorName = articles[i]['source']['name']
                releaseTime = articles[i]['publishedAt']
                title_source = articles[i]['title']
                title = self.parsing_news_title(html_obj=html_obj, title_source=title_source)
                content = self.parsing_news_content(content_html=details_res, html_obj=html_obj, newspaper=True)
                thumbnail_img = articles[i]['urlToImage']
                img = self.download_img(html_obj=html_obj, thumbnail_img=thumbnail_img)
                if img is None or img == '' or content is None or content == '':
                    pass
                else:
                    data = {'source': source, 'jobId': int(jobId), 'sourceUrl': sourceUrl, 'title': title, 'authorName': authorName,
                            'releaseTime': releaseTime, 'content': content, 'img': img}
                    print('data:\n', data)
                    self.save.save_data(data=data, news='abc')


    def parsing_news_title(self, html_obj, title_source):
        title = ''.join(html_obj.xpath('//header[@class="article-header"]//h1/text()'))
        if title == '' or title is None:
            return title_source
        else:
            return title


    def parsing_news_content(self, content_html=None, html_obj=None, newspaper=False):
        if newspaper:
            text = fulltext(content_html).split('\n')
            txt = list(filter(lambda x: x.strip() != '', text))
            content = '<p>'.join(txt)
        else:
            content_list = html_obj.xpath('//div[@id="news-content"]//p/text()')
            content = '<p>'.join([i.replace("\n", '').strip() for i in content_list]).replace("<p><p>", '<p>')
        return content


    def download_img(self, html_obj, thumbnail_img):
        try:
            pic_url_list = html_obj.xpath('//figure//div//picture//img/@src')
            img_id = str(uuid.uuid4()).replace('-','')
            index = 1
            img_list = []
            if pic_url_list == []:
                urllib.request.urlretrieve(thumbnail_img, r'%s.jpg' % (self.downloadPath + self.picPath + str(img_id) + "-" + str(index)))
                img = r'%s.jpg' % (self.picPath + str(img_id) + "-" + str(index))
                return img
            else:
                for pic_url in pic_url_list[:17]:
                    urllib.request.urlretrieve(pic_url, r'%s.jpg' % (self.downloadPath + self.picPath + str(img_id) + "-" + str(index)))
                    img_list.append(r'%s.jpg' % (self.picPath + str(img_id) + "-" + str(index)))
                    index += 1
                img = ','.join(img_list)
                return img
        except:
            pass



if __name__ == '__main__':
    abc = ABC_News()
    abc.run()
