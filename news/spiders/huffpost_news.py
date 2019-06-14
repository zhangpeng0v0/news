import requests, time, uuid, random
from lxml import etree
from newspaper import fulltext
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



class HuffPost_News():
    def __init__(self):
        self.headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36'}
        self.cookies = {'cookie': 'BX=cj1ovi5ee464n&b=3&s=nk; rxx=aflhe5fyk20.1j3ho4gz&v=1; _fbp=fb.1.1558321313127.2047077689; GUC=AQEBAQFc42Vdw0If_QRY&s=AQAAAB6nBWF3&g=XOIY0w; trc_cookie_storage=taboola%2520global%253Auser-id%3Dbfc0c49d-bde0-4b78-9484-33cd8cb7509f-tuct3bdf4f1; _tb_sess_r=https%3A//www.huffpost.com/topic/nsfw%3Fpage%3D1; GED_PLAYLIST_ACTIVITY=W3sidSI6Im9TTWYiLCJ0c2wiOjE1NTgzNDA3MTMsIm52IjoxLCJ1cHQiOjE1NTgzNDA3MDYsImx0IjoxNTU4MzQwNzEzfSx7InUiOiIxSmhlIiwidHNsIjoxNTU4MzQwNjQ5LCJudiI6MSwidXB0IjoxNTU4MzQwNjM5LCJsdCI6MTU1ODM0MDY0OX1d; _tb_t_ppg=https%3A//www.huffpost.com/entry/nobuyoshi-araki-museum-of-sex_n_5a7c8c38e4b0c6726e10b29d'}
        self.downloadPath = '/data/crawler'
        self.picPath = '/huffpost/picture/'
        self.filter = Filter_Data()
        self.save = Save_Data()


    def run(self):
        pg = 1
        while pg < 11:
            start_url = 'https://www.huffpost.com/topic/nsfw?page={}'.format(pg)
            self.parsing_huffpost_news_list(list_url = start_url)
            pg += 1


    def parsing_huffpost_news_list(self, list_url):
        res = requests.get(url=list_url, headers=self.headers, cookies=self.cookies).text
        time.sleep(random.uniform(3, 5))
        html = etree.HTML(res)
        news_list_url = html.xpath('//div[@class="card__content"]/a/@href')
        for details_url in news_list_url:
            try:
                self.parsing_details_page_url(details_url=details_url)
            except:
                pass


    def parsing_details_page_url(self, details_url):
        status = self.filter.filter_data(details_url=details_url)
        if status:
            print('Data already exists!')
        else:
            res = requests.get(url=details_url, headers=self.headers, cookies=self.cookies).text
            time.sleep(random.uniform(1, 3))
            html = etree.HTML(res)
            source = int(12)
            jobId = time.time()
            sourceUrl = details_url
            title = ''.join(html.xpath('//h1[@class="headline__title"]//text()'))
            authorName = self.analysis_author_name(html=html)
            releaseTime = self.analysis_release_time(html=html).replace("\n", '').strip()
            content = self.analysis_new_content(res=res, html=html, newspaper=False)
            img_list = self.analysis_download_img(html=html)
            img = self.download_pic(img_url_list=img_list)
            if img == '' or img is None or content == '' or content is None:
                pass
            else:
                data = {'source': source, 'jobId': int(jobId), 'sourceUrl': sourceUrl, 'title': title, 'authorName': authorName,
                        'releaseTime': releaseTime, 'content': content, 'img': img}
                print('data:\n', data)
                self.save.save_data(data=data, news='huffpost')



    def analysis_author_name(self, html):
        authorName = ''.join(html.xpath('//div[@class="author-list"]/span/text()'))
        if authorName =='' or authorName is None:
            authorName = ''.join(html.xpath('//div[@class="author-card__name"]//text()'))
            return authorName
        else:
            return authorName



    def analysis_release_time(self, html):
        releaseTime_1 = ''.join(html.xpath('//div[@class="timestamp timestamp--has-modified-date"]//text()'))
        if releaseTime_1 =='' or releaseTime_1 is None:
            releaseTime_2 = ''.join(html.xpath('//div[@class="timestamp"]//text()'))
            if releaseTime_2 == '' or releaseTime_2 is None:
                releaseTime_3 = ''.join(html.xpath('//div[@class="timestamp timestamp--contributor timestamp--has-modified-date"]//text()'))
                return releaseTime_3
            else:
                return releaseTime_2
        else:
            return releaseTime_1


    def analysis_new_content(self, res, html, newspaper=False):
        if newspaper:
            text = fulltext(res).split('\n')
            txt = list(filter(lambda x: x.strip() != '', text))
            content = '<p>'.join(txt)
            return content
        else:
            text = html.xpath('//div[@class="content-list-component yr-content-list-text text"]//p//text()')
            content = '<p>'.join([i.replace("\n", '').strip() for i in text]).replace("<p><p>", '<p>').replace("<p>,<p>", ' ')
            return content


    def download_pic(self, img_url_list):
        img_id = str(uuid.uuid4()).replace('-', '')
        index = 1
        img_list = []
        pic_url_list_1 = [i for i in img_url_list if '.svg' not in i]
        pic_url_list = [j for j in pic_url_list_1 if 'ops=100_100' not in j]
        miss_pic = 'https://img.huffingtonpost.com/asset/default-missing-image.jpg?cache=jio2vozgty&ops=scalefit_970_noupscale'
        if pic_url_list == [] or miss_pic in pic_url_list:
            return None
        else:
            if len(pic_url_list) < 18:
                pic_list = pic_url_list
            else:
                pic_list = pic_url_list[:17]
            for pic_url in pic_list:
                urllib.request.urlretrieve(pic_url, r'%s.jpg' % (self.downloadPath + self.picPath + str(img_id) + "-" + str(index)))
                img_list.append(r'%s.jpg' % (self.picPath + str(img_id) + "-" + str(index)))
                index += 1
            img = ','.join(img_list)
            return img


    def analysis_download_img(self, html):
        pic_url_list1 = html.xpath('//div[@class="listicle__slide-content"]/img/@src')
        if pic_url_list1 == []:
            pic_url_list2 = html.xpath('//div[@class="entry__body js-entry-body"]//img/@src')
            if pic_url_list2 == []:
                pic_url_list3 = html.xpath('//div[@class="collection-item image"]//img/@src')
                return pic_url_list3
            else:
                return pic_url_list2
        else:
            return pic_url_list1



if __name__ == '__main__':
    rt = HuffPost_News()
    rt.run()
    