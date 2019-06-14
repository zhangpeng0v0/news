import time, requests, random, uuid, json
from lxml import etree
from newspaper import fulltext
from PIL import Image
from io import BytesIO
try:
    from news.filter_data import Filter_Data
    from news.save_data import Save_Data
except:
    import sys
    sys.path.append("/app/crawler/news_project/news/")
    from filter_data import Filter_Data
    from save_data import Save_Data



class UPROXX_News():
    def __init__(self):
        self.headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
        self.cookies = {'cookie': '_ga=GA1.2.1916480018.1557387143; _omappvp=NXTUG1O09XwizTEVPHY0CDatCFaa7zmyENXMZ3yBzNBfpRrUJyJSjzawWbNOtmCk3a0M6l51v1hv01nhoAdHqIQLyxntcGlZ; __gads=ID=967d7ff68a5a2656:T=1557387149:S=ALNI_MZFY5Q_tfI8WS1_30SK817ySI14RQ; _cb_ls=1; _cb=BvCRDMN1EZ-CKUJwA; _scid=12f16568-c9b2-4331-9513-626f26e7aac6; _fbp=fb.1.1558321180103.1335358405; __qca=P0-305115545-1558321179420; _chartbeat2=.1558321174581.1558322228287.1.w0ijvCb8zgbDJfkouB1YhL9BM0Wu2.15; _sctr=1|1559059200000; _gid=GA1.2.676333276.1559707655; _cmpQcif3pcsupported=1; _parsely_visitor={%22id%22:%22f94909f1-8e1d-499d-8590-04e058a8acdf%22%2C%22session_count%22:4%2C%22last_session_ts%22:1559707963140}; _parsely_slot_click={%22url%22:%22https://uproxx.com/dimemag/demarcus-cousins-warriors-game-2-nba-finals-passing-analysis-videos/%22%2C%22x%22:1163%2C%22y%22:0%2C%22xpath%22:%22//*[@id=%5C%22menu-item-1560569%5C%22]/a[1]%22%2C%22href%22:%22https://uproxx.com/news%22}; _threds=1; _thredb=uproxx.76a113a16f1e45e5bf36b23bf05e76a6.1558321178020.1559712981550.1559713181162.30.6; _gat_auPassiveTagger=1; _gat=1'}
        self.downloadPath = '/data/crawler'
        self.picPath = '/uproxx/picture/'
        self.filter = Filter_Data()
        self.save = Save_Data()


    def run(self):
        pg = 1
        while pg <10:
            start_url = 'https://uproxx.com/wp-json/wovenis/v1/home/{}?offset=34'.format(1)
            self.parsing_news_list_page(url=start_url)
            pg += 1


    def parsing_news_list_page(self, url):
        res = requests.get(url=url, headers=self.headers, cookies=self.cookies).text
        time.sleep(random.uniform(1, 3))
        js = json.loads(res)
        html = js['html']
        html_obj = etree.HTML(html)
        url_list = html_obj.xpath('//h2/a/@href')
        for i in url_list:
            status = self.filter.filter_data(details_url=i)
            if status:
                print('Data already exists!')
            else:
                try:
                    self.parsing_details_page(details_url=i)
                except:
                    pass


    def parsing_details_page(self, details_url):
        res = requests.get(url=details_url, headers=self.headers, cookies=self.cookies).text
        time.sleep(random.uniform(1, 2))
        html = etree.HTML(res)
        source = int(13)
        jobId = time.time()
        sourceUrl = details_url
        title = ''.join(html.xpath('//div[@class="post-top"]//h1//text()'))
        authorName = html.xpath('//span[@class="authorname"]//text()')[0]
        releaseTime = html.xpath('//span[@class="published-date uproxx-the-date"]//text()')[0]
        content = self.analysis_news_content(html=res)
        img = self.analysis_news_img(html_obj=html)
        if img is None or img == '' or content is None or content == '':
            pass
        else:
            data = {'source': source, 'jobId': int(jobId), 'sourceUrl': sourceUrl, 'title': title,
                    'authorName': authorName,
                    'releaseTime': releaseTime, 'content': content, 'img': img}
            print('data:\n', data)
            self.save.save_data(data=data, news='UPROXX')



    def analysis_news_content(self, html):
        text = fulltext(html).split('\n')
        txt = list(filter(lambda x: x.strip() != '', text))
        content = '<p>'.join(txt)
        return content


    def analysis_news_img(self, html_obj):
        pic_url_list =html_obj.xpath('//div[@class="ug_page"]//img/@src')
        img_id = str(uuid.uuid4()).replace('-', '')
        index = 1
        img_list = []
        if pic_url_list == []:
            return None
        else:
            try:
                for pic_url in pic_url_list[:17]:
                    response = requests.get(pic_url)
                    image = Image.open(BytesIO(response.content))
                    image.save(r'%s.jpg' % (self.downloadPath + self.picPath + str(img_id) + "-" + str(index)))
                    img_list.append(r'%s.jpg' % (self.picPath + str(img_id) + "-" + str(index)))
                    index += 1
                img = ','.join(img_list)
                return img
            except:
                return None



if __name__ == '__main__':
    up = UPROXX_News()
    up.run()

