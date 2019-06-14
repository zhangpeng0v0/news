import requests, time, uuid, random
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



class Smart_News():
    def __init__(self):
        self.headers={'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
        self.downloadPath = '/data/crawler'
        self.picPath = '/smartNews/picture/'
        self.filter = Filter_Data()
        self.save = Save_Data()



    def run(self):
        index = 1
        while index < 3:
            url_dic = { 'news' : 'https://www.smithsonianmag.com/category/smart-news/?no-ist%252F=938&page={}'.format(index),
                        'history' : 'https://www.smithsonianmag.com/category/history/?page={}'.format(index),
                        'science' : 'https://www.smithsonianmag.com/category/science-nature/?page={}'.format(index),
                        'innovation' : 'https://www.smithsonianmag.com/category/innovation/?page={}'.format(index),
                        'arts_culture' : 'https://www.smithsonianmag.com/category/arts-culture/?page={}'.format(index),
                        'travel' : 'https://www.smithsonianmag.com/category/travel/?page={}'.format(index),
                        'smithsonian' : 'https://www.smithsonianmag.com/category/smithsonian-institution/?page={}'.format(index),
                    }
            for kw in url_dic:
                print('keyword:\t', kw)
                self.parsing_smart_news_list_page(url_dic[kw])
            index += 1


    def parsing_smart_news_list_page(self, list_url):
        time.sleep(random.uniform(5, 10))
        list_res = requests.get(url=list_url, headers=self.headers).text
        html = etree.HTML(list_res)
        thumbnail_img_list = html.xpath('//main[@class="main"]//img//@src')
        details_url_list = html.xpath('//h3[@class="headline"]//a/@href')
        for i in range(len(details_url_list)):
            result = self.filter.filter_data(details_url='https://www.smithsonianmag.com' + details_url_list[i])
            if result:
                print('Data already exists!')
            else:
                data = self.parsing_details_page(details_url='https://www.smithsonianmag.com' + details_url_list[i], thumbnail_img=thumbnail_img_list[i])
                if data is None or data=='':
                    pass
                else:
                    print('data:\n', data)
                    self.save.save_data(data=data, news='smart')


    def parsing_details_page(self, details_url, thumbnail_img):
        time.sleep(random.uniform(3, 5))
        details_res = requests.get(url=details_url, headers=self.headers).text
        details_html = etree.HTML(details_res)
        source = int(5)
        sourceUrl = details_url
        jobId = time.time()
        title = ''.join(details_html.xpath('//h1[@class="headline"]/text()'))
        if title is None or title == '':
            pass
        else:
            text = fulltext(details_res).split('\n')
            txt = list(filter(lambda x: x.strip() != '', text))
            content = '<p>'.join(txt)
            author = details_html.xpath('//a[@class="author-name"]/text()')
            authorName = ''.join([i.replace("/n", '<p>').strip() for i in author])
            releaseTimeList = details_html.xpath('//time[@class="pub-date"]/text()')
            releaseTime = ''.join([i.replace("/n", '<p>').strip() for i in releaseTimeList])
            img = self.analysis_filter_img_url(html=details_html, thumbnail_img=thumbnail_img)
            if img is None or img == '' or content is None or content == '':
                pass
            else:
                return {'source': source, 'jobId': int(jobId), 'sourceUrl': sourceUrl, 'title': title, 'authorName': authorName,
                        'releaseTime': releaseTime, 'content': content, 'img': img}


    def analysis_filter_img_url(self, html, thumbnail_img):
        href_list = html.xpath('//main[@class="main"]//img//@src')
        pic_url_list = [i for i in href_list if 'filer' in i and 'png' not in i]
        img = self.download_img(pic_url_list=pic_url_list)
        if img == '' or img is None:
            img = self.download_img(pic_url_list=[thumbnail_img])
            return img
        else:
            return img


    def download_img(self, pic_url_list):
        img_id = str(uuid.uuid4()).replace('-','')
        index = 1
        img_list = []
        try:
            for pic_url in pic_url_list[:17]:
                if '220x130' in pic_url or '60x60' in pic_url:
                    pass
                else:
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
    sm = Smart_News()
    sm.run()
