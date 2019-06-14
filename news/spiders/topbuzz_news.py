import requests, time, json, uuid, random
from lxml import etree
import urllib.request
import urllib.parse
from newspaper import fulltext
try:
    from news.filter_data import Filter_Data
    from news.save_data import Save_Data
except:
    import sys
    sys.path.append("/app/crawler/news_project/news/")
    from filter_data import Filter_Data
    from save_data import Save_Data



class TopBuzz_News(object):
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.   36'}
        self.cookies = {'cookies': 'odin_tt=25f29c3c11ab624e32ea123b341f8e8ad3b9254cb1bcb00828ea8bbdf642ee3018a6a10f8ce2d4c3bb22af93a7fbcf4f44f76469931ce1241c8907041d196a1c; tt_webid=6675470162378032646; __tea_sdk__user_unique_id=6675470162378032646; __tea_sdk__ssid=f4cef532-3e68-4425-a4fa-8963bda2fdc3; csrf-token=da1ad8433b7acb6730721e47b072bc7ec710c4e3; csrf-secret=QBi0atkMP4iR2oosQVsHoAxAo7LA2Qzm'}
        self.keyword = ['foryou','entertainment','sports','lifestyle','gaming','food','tech','autos']
        self.t = time.time()
        self.downloadPath = '/data/crawler'
        self.picPath = '/topbuzz/picture/'
        self.filter = Filter_Data()
        self.save = Save_Data()



    def run(self):
        for cls in self.keyword:
            print('cls:\t', cls)
            url = 'https://www.topbuzz.com/pgc/feed?content_space=bd&language=en&region=us&user_id=6675470162378032646' \
                  '&channel_name=' + cls + \
                  '&classification=all' \
                  '&max_behot_time=' + str(self.t)
            self.parsing_topBuzz_list_page(list_url=url)


    def parsing_topBuzz_list_page(self, list_url):
        res = requests.get(url=list_url, headers=self.headers, cookies=self.cookies).text
        data = json.loads(res)
        item = data['data']['feed']['items']
        for i in range(len(item)):
            group_id = item[i]['group_id']
            impr_id = item[i]['impr_id']
            user_id = item[i]['author_info']['user_id']
            detail_url = 'https://www.topbuzz.com/a/' \
                         + group_id + \
                         '?app_id=1106' \
                         '&gid=' + group_id + \
                         '&impr_id=' + impr_id + \
                         '&language=en' \
                         '&region=us' \
                         '&user_id=' + user_id + \
                         '&c=sys'
            status = self.filter.filter_data(details_url=detail_url)
            if status:
                print('Data already exists!')
            else:
                self.parsing_details_page(details_url=detail_url)


    def parsing_details_page(self, details_url):
        time.sleep(random.uniform(1, 3))
        res = requests.get(url=details_url, headers=self.headers, cookies=self.cookies).text
        html = etree.HTML(res)
        source = int(1)
        jobId = time.time()
        sourceUrl = details_url
        title = ''.join(html.xpath('//div[@class="title"]/text()'))
        authorName = ''.join(html.xpath('//div[@class="name active"]/text()'))
        releaseTime = ''.join(html.xpath('//div[@class="publishTime"]/text()'))
        content = self.parsing_news_content(res=res, html=html, newspaper=True)
        img = self.download_img(html=html)
        if img is None or img == '' or content is None or content == '':
            pass
        else:
            data = {'source': source, 'jobId': int(jobId), 'sourceUrl': sourceUrl, 'title': title, 'authorName':authorName,
                    'releaseTime': releaseTime, 'content': content, 'img': img}
            print('data:\n', data)
            self.save.save_data(data=data, news='topBuzz')


    def parsing_news_content(self, res, html, newspaper=False):
        try:
            if newspaper:
                text = fulltext(res).split('\n')
                txt = list(filter(lambda x: x.strip() != '', text))
                content = '<p>'.join(txt)
                return content
            else:
                text = html.xpath('//div[@class="editor-container"]//p//text()')
                content = '<p>'.join([i.replace("\n", '').strip() for i in text]).replace("<p><p>", '<p>')
                return content
        except:
            return None


    def download_img(self, html):
        pic_url_list = html.xpath('//main//img//@src')
        img_id = str(uuid.uuid4()).replace('-','')
        index = 1
        img_list = []
        if pic_url_list == []:
            pass
        else:
            try:
                pic_list = [i for i in pic_url_list if 'https' not in i]
                for pic_url in pic_list[:17]:
                    urllib.request.urlretrieve('https:' + pic_url, r'%s.jpg' % (self.downloadPath + self.picPath + str(img_id) + "-" + str(index)))
                    img_list.append(r'%s.jpg' % (self.picPath + str(img_id) + "-" + str(index)))
                    index += 1
                img = ','.join(img_list)
                return img
            except:
                return None



if __name__ == '__main__':
    tb = TopBuzz_News()
    tb.run()

