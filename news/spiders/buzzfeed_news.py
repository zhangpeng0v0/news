import requests, time, json, uuid, random
from lxml import etree
import urllib.request
import urllib.parse
try:
    from news.filter_data import Filter_Data
    from news.save_data import Save_Data
except:
    import sys
    sys.path.append("/app/crawler/news_project/news/")
    from filter_data import Filter_Data
    from save_data import Save_Data


class Buzz_Feed_News():
    def __init__(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36'
        }
        self.cookies = {
            'cookie': '_ga=GA1.2.2006098489.1555559856; _fbp=fb.1.1555559860721.1190642659; __qca=P0-464700868-1555559857580; permutive-id=35526ebd-337f-4b00-bf5b-10a6610a85a5; __gads=ID=2cb4be529258fba6:T=1555559912:S=ALNI_MawMBKcEjsbSC3roAOVcCQm5lCB2A; _pdfps=%5B7684%2C13160%2C13164%2C13319%2C13730%2C14474%2C10166%2C12448%2C12449%2C12882%2C13097%2C13214%2C13217%2C13276%2C13278%2C13834%2C14353%2C10748%2C10788%2C13102%2C13144%2C13145%2C13146%2C13147%2C13150%2C13151%2C13157%2C13163%2C13169%2C13667%2C14437%2C14458%2C10224%2C10915%2C13153%2C13675%2C14142%2C13064%2C13216%2C13279%2C14431%2C14432%2C10749%2C10789%2C10906%2C10916%2C10917%2C11655%2C12233%2C12244%2C12679%2C12985%2C13099%2C13101%2C13148%2C13244%2C13741%2C13742%2C14143%2C14479%2C14872%2C15077%2C15128%2C15139%2C10222%2C13100%2C10216%2C%2212244-15-22969%22%2C%2212244-15-22970%22%2C%2212679-5-118997US%22%2C%2212985-5-118497US%22%2C%2213244-5-325997US%22%2C%2213245-5-325997US%22%2C%2213246-5-325997US%22%2C%2213458-15-22969%22%2C%2213458-15-22970%22%2C%2213459-15-22969%22%2C%2213459-15-22970%22%2C%2214229-5-318346US%22%2C%2214351-15-22835%22%2C%2214479-5-325547US%22%2C%2214872-15-22835%22%2C%2214872-15-22814%22%2C%2215063-5-318346US%22%2C%2215063-5-325346US%22%5D; permutive-session=%7B%22session_id%22%3A%2215c3b65a-580a-47aa-ab95-b44076421376%22%2C%22last_updated%22%3A%222019-04-27T02%3A27%3A38.962Z%22%7D; _cmpQcif3pcsupported=1; _gid=GA1.2.13310005.1557196067; _gat=1; sailthru_pageviews=4; sailthru_content=cbe347ea3dd8f028b2a79dd2124b2609d73dc57549ee138bd1d9dedee18e797c3cde4668fc0929097a33767e5b408948300e3683df34cf01dce50805bbb1306ce0bce460f7e70fed288b52d84bd9816499693f0167a253c9d1ba851de3a9d8e9dd7ae6730eff39df6f3b2fee47cae2908e3260668e0361ea9bd2ebb68e2a0591e9ec864cd274cc1d8b3a98016c2bcf1d874e57a78b55d2f981aeb6d2c79bfecc9d43236330abbff1afd96b7ffa626bb4936065bb0196c7181b628021dea483cf13a2f044347925f429d5fbc7008162c9cd736b79ca68d62341101204bca0cca1ff22ee54be7fa316d48db768db05dda4f044956926b209e90497a64953e290f7; sailthru_visitor=a057d87e-b51c-4f1e-9167-d146c2a3a7bc'
        }
        self.downloadPath = '/data/crawler'
        self.picPath = '/buzzfeed/picture/'
        self.filter = Filter_Data()
        self.save = Save_Data()


    def run(self):
        page = 1
        while page < 3:
            news_list_url = 'https://www.buzzfeednews.com/site-component/v1/en-us/trending-on-buzzfeednews?page={}&page_size=10'.format(page)
            self.parsing_buzzFeed_news_list(news_list_url = news_list_url)
            time.sleep(random.uniform(60, 70))
            page += 1


    def parsing_buzzFeed_news_list(self, news_list_url):
        res = requests.get(url=news_list_url, headers=self.headers, cookies=self.cookies).text
        item = json.loads(res)
        results = item['results']
        for i in range(len(results)):
            jobId = time.time()
            source = int(3)
            sourceUrl = results[i]['url']
            filter_data = self.filter.filter_data(details_url=sourceUrl)
            if filter_data:
                print('Data already exists!')
            else:
                title = results[i]['name']
                releaseTime = results[i]['created_at']
                thumbnail_img = results[i]['image']
                article = self.parsing_details_url(details_url=sourceUrl, thumbnail_img=thumbnail_img)
                if article == '' or article is None:
                    pass
                else:
                    data = {'source': source, 'jobId': int(jobId), 'sourceUrl': sourceUrl, 'title': title, 'authorName': article['authorName'], 'releaseTime': releaseTime, 'content': article['content'], 'img': article['img']}
                    print('data:\n', data)
                    self.save.save_data(data=data, news='buzzfeed')


    def parsing_details_url(self, details_url, thumbnail_img):
        time.sleep(random.uniform(2, 5))
        html = requests.get(url=details_url, headers=self.headers, cookies=self.cookies).text
        html_obj = etree.HTML(html)
        authorName =''.join(html_obj.xpath('//span[@class="news-byline-full__name xs-block link-initial--text-black"]/text()'))
        content_list = html_obj.xpath('//div[@data-module="article-wrapper"]//p//text()')
        content = '<p>'.join([i.replace("\n", '').strip() for i in content_list]).replace("<p><p>", '<p>')
        if content == '' or content is None:
            pass
        else:
            img = self.download_img(html=html_obj,thumbnail_img=thumbnail_img)
            if img == '' or img is None :
                return None
            else:
                article = {'authorName':authorName, 'content':content, 'img':img}
                return article


    def download_img(self, html, thumbnail_img):
        pic_list_1 = html.xpath('//figure//img/@data-src')
        pic_list_2 = html.xpath('//picture//img/@src')
        pic_list_3 = [i for i in pic_list_1 if i not in pic_list_2]
        pic_url_list = pic_list_2 + pic_list_3
        img_id = str(uuid.uuid4()).replace('-', '')
        index = 1
        img_list = []
        if pic_url_list == []:
            urllib.request.urlretrieve(thumbnail_img, r'%s.jpg' % (self.downloadPath + self.picPath + str(img_id) + "-" + str(index)))
            img = r'%s.jpg' % (self.picPath + str(img_id) + "-" + str(index))
            return img
        else:
            for pic_url in pic_url_list[:17]:
                urllib.request.urlretrieve(pic_url, r'%s.jpg' % (
                            self.downloadPath + self.picPath + str(img_id) + "-" + str(index)))
                img_list.append(r'%s.jpg' % (self.picPath + str(img_id) + "-" + str(index)))
                index += 1
            img = ','.join(img_list)
            return img



if __name__ == '__main__':
    bf = Buzz_Feed_News()
    bf.run()
