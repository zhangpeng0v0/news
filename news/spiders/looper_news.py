import requests, time, uuid, random
from newspaper import fulltext
from lxml import etree
import urllib.request
try:
    from news.filter_data import Filter_Data
    from news.save_data import Save_Data
except:
    import sys
    sys.path.append("/app/crawler/news_project/news/")
    from filter_data import Filter_Data
    from save_data import Save_Data



class Looper_News(object):
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
        self.cookies = {'Cookie': 'eu_cookie=1; _ga=GA1.2.716753130.1558322924; __qca=P0-1424062991-1558322923905; __gads=ID=1477ebfc328ade2f:T=1558322965:S=ALNI_MaqMSrLXw4oP8tpYvkTfPLW8rNP8g; OX_ssn=5819416341; _gid=GA1.2.90982873.1559799919; OX_plg=pm; OX_sd=3; looperSessionDepth=3; eu_cookie=1; cuid=5931835b1dcefbdb0a501558923072349_1562391999845; GED_PLAYLIST_ACTIVITY=W3sidSI6IndpbHciLCJ0c2wiOjE1NTk4MDAyOTIsIm52IjoxLCJ1cHQiOjE1NTk4MDAyOTAsImx0IjoxNTU5ODAwMjkxfSx7InUiOiJVYmRFIiwidHNsIjoxNTU5ODAwMDY3LCJudiI6MSwidXB0IjoxNTU5ODAwMDM0LCJsdCI6MTU1OTgwMDA2NX0seyJ1IjoieHl4NiIsInRzbCI6MTU1OTgwMDA1NiwibnYiOjEsInVwdCI6MTU1OTgwMDAzNCwibHQiOjE1NTk4MDAwNTZ9XQ..; _gat=1'}
        self.key_word = ['news', 'features', 'movies', 'television', 'comics']
        self.downloadPath = '/data/crawler'
        self.picPath = '/looper/picture/'
        self.filter = Filter_Data()
        self.save = Save_Data()


    def run(self):
        pg = 12
        while pg < 24:
            for kw in self.key_word:
                url = 'https://www.looper.com/category/{}/?ajax=1&offset={}'.format(kw, pg)
                self.parsing_news_list_page(url=url)
            pg += 12


    def parsing_news_list_page(self, url):
        res = requests.get(url=url, headers=self.headers, cookies=self.cookies).text
        time.sleep(random.uniform(1, 3))
        html = etree.HTML(res)
        url_list = html.xpath('//h3/a/@href')
        for i in url_list:
            status = self.filter.filter_data(details_url=i)
            if status:
                pass
            else:
                self.parsing_details_page(details_url=i)


    def parsing_details_page(self, details_url):
        res = requests.get(url=details_url, headers=self.headers, cookies=self.cookies).text
        time.sleep(random.uniform(1, 3))
        html = etree.HTML(res)
        source = int(13)
        sourceUrl = details_url
        jobId = time.time()
        title = ''.join(html.xpath('//h1[@class="title-gallery"]/text()'))
        authorName = ''.join(html.xpath('//div[@class="gallery-info"]/a/text()'))
        releaseTime = ''.join(html.xpath('//span[@class="news-timestamp"]/text()'))
        content = self.analysis_news_content(html=res, html_obj=html, newspaper=False)
        img =self.analysis_news_img(html_obj=html)
        if img is None or img == '' or content is None or content == '':
            pass
        else:
            data = {'source': source, 'jobId': int(jobId), 'sourceUrl': sourceUrl, 'title': title, 'authorName':authorName,
                    'releaseTime': releaseTime, 'content': content, 'img': img}
            print('data:\n', data)
            self.save.save_data(data=data, news='looper')



    def analysis_news_content(self, html, html_obj, newspaper=False):
        if newspaper:
            text = fulltext(html).split('\n')
            txt = list(filter(lambda x: x.strip() != '', text))
            content = '<p>'.join(txt)
        else:
            content_list = html_obj.xpath('//div[@id="content"]//p//text()')
            content = '<p>'.join([i.replace("\n", '').strip() for i in content_list]).replace("<p><p>", '<p>')
        return content


    def analysis_news_img(self, html_obj):
        pic_url_list = html_obj.xpath('//div[@id="content"]//img/@src')
        img_id = str(uuid.uuid4()).replace('-','')
        index = 1
        img_list = []
        try:
            for pic_url in pic_url_list[:17]:
                urllib.request.urlretrieve(pic_url, r'%s.jpg' % (self.downloadPath + self.picPath + str(img_id) + "-" + str(index)))
                img_list.append(r'%s.jpg' % (self.picPath + str(img_id) + "-" + str(index)))
                index += 1
            img = ','.join(img_list)
            return img
        except:
            return None



if __name__ == '__main__':
    l = Looper_News()
    l.run()

