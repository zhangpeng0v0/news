import requests, json, time, random, uuid
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



class Matador_Network(object):
    def __init__(self):
        self.headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
        self.cookies = {'cookie': '_ga=GA1.2.1006188425.1558506407; __auc=c07ed86116ade38958b6f215c90; __gads=ID=ebab27bbe751d3d9:T=1558506409:S=ALNI_MbKANVLVZlZmub7wcHXVdRq__9uAQ; _fbp=fb.1.1558506413908.2064431331; cache-primed=1; mn-push-status=8; EU=(null); _gid=GA1.2.549309516.1558921947; __asc=2b5b28f116af808ea5c6cf504f0'}
        self.downloadPath = '/data/crawler'
        self.picPath = '/matador_network/picture/'
        self.filter = Filter_Data()
        self.save = Save_Data()



    def run(self):
        pg = 8
        while pg < 68 :
            start_url = 'https://matadornetwork.com/wp-content/plugins/matadornetwork/mn-ajax.php?component=post&action=get_posts&' \
                        'offset={}' \
                        '&posts_per_page=20&grid=small&post__not_in%5B%5D=546093&post__not_in%5B%5D=%20546069&post__not_in%5B%5D=%20545872&post__not_in%5B%5D=%20497520&post__not_in%5B%5D=%20501737&post__not_in%5B%5D=%20486578&post__not_in%5B%5D=%20342847&home=1&_=1558941893778'.format(pg)
            self.parsing_matador_network_list_page(list_url=start_url)
            pg += 20


    def parsing_matador_network_list_page(self, list_url):
        res = requests.get(url=list_url, headers=self.headers, cookies=self.cookies).text
        time.sleep(random.uniform(3, 5))
        js = json.loads(res)
        html = js['html']
        html_obj = etree.HTML(html)
        urls_list = html_obj.xpath('//a[@class="article__image-wrapper"]/@href')
        for details_url in urls_list:
            status = self.filter.filter_data(details_url=details_url)
            if status:
                print('Data already exists!')
            else:
                data = self.parsing_details_page_url(details_url=details_url)
                print('data:\t', data)
                self.save.save_data(data=data, news='matador')


    def parsing_details_page_url(self, details_url):
        res = requests.get(url=details_url, headers=self.headers, cookies=self.cookies).text
        html = etree.HTML(res)
        time.sleep(random.uniform(1, 3))
        source = int(11)
        sourceUrl = details_url
        jobId = time.time()
        title = ''.join(html.xpath('//div[@class="container"]//h1/text()'))
        releaseTime = ''.join(html.xpath('//div[@class="post-info-date"]/text()'))
        authorName = ''.join(html.xpath('//a[@class="post-info-author"]/text()'))
        content = self.analysis_news_content(content_html=res, html_obj=html, newspaper=True)
        img = self.analysis_content_img(html_obj=html)
        if img is None or img == '' or content is None or content == '':
            pass
        else:
            return {'source': source, 'jobId': int(jobId), 'sourceUrl': sourceUrl, 'title': title, 'authorName': authorName,
                    'releaseTime': releaseTime, 'content': content, 'img': img}


    def analysis_news_content(self, content_html=None, html_obj=None, newspaper=True):
        if newspaper:
            text = fulltext(content_html).split('\n')
            txt = list(filter(lambda x: x.strip() != '', text))
            content = '<p>'.join(txt)
        else:
            content_list = html_obj.xpath('//div[@class="post-content"]//text()')
            content = '<p>'.join([i.replace("\n", '').strip() for i in content_list]).replace("<p><p>", '<p>')
        return content


    def analysis_content_img(self, html_obj):
        pic_url_list = html_obj.xpath('//div[@class="container"]//img/@src')
        pic_set = [i for i in pic_url_list if '.png' not in i]
        img_id = str(uuid.uuid4()).replace('-', '')
        index = 1
        img_list = []
        if pic_set == []:
            return None
        else:
            for pic_url in pic_set:
                response = requests.get(pic_url)
                image = Image.open(BytesIO(response.content))
                image.save(r'%s.jpg' % (self.downloadPath + self.picPath + str(img_id) + "-" + str(index)))
                img_list.append(r'%s.jpg' % (self.picPath + str(img_id) + "-" + str(index)))
                index += 1
            img = ','.join(img_list)
            return img



if __name__ == '__main__':
    m = Matador_Network()
    m.run()
