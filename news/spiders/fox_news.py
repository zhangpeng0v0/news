from newsapi import NewsApiClient
import time, random, requests, uuid
import urllib.parse
import urllib.request
from lxml import etree
from newspaper import fulltext
try:
    from news.filter_data import Filter_Data
    from news.save_data import Save_Data
except:
    import sys
    sys.path.append("/app/crawler/news_project/news/")
    from filter_data import Filter_Data
    from save_data import Save_Data



class FOX_News(object):
    def __init__(self):
        self.news_api = NewsApiClient(api_key='f04f7a8db32841299d4a7fae723e61b2')
        self.t = time.time()
        self.point_time = time.strftime('%Y-%m-%d', time.localtime(self.t))
        self.keyword = ['us', 'word', 'opinion', 'politics', 'entertainment', 'lifestyle', 'health', 'travel', 'autos']
        self.headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
        self.cookies = {'cookie': '_cb_ls=1; optimizelyEndUserId=oeu1556269407120r0.4256555044820445; cto_lwid=a3569f8e-fd62-48fd-8cf3-52e3a3d49218; _gcl_au=1.1.1392012605.1556269408; ajs_user_id=null; ajs_group_id=null; ajs_anonymous_id=%22cfa5a6d1-cac6-4a48-97ed-e2a25488a94a%22; _ga=GA1.2.353904812.1556269412; _cb=D6-ViRhsUuoBSGama; __gads=ID=0a226a472ca026e8:T=1556269422:S=ALNI_Mb8qEqiRmqgHFem87cBOSEiCTTaJQ; trc_cookie_storage=taboola%2520global%253Auser-id%3Dbfc0c49d-bde0-4b78-9484-33cd8cb7509f-tuct3bdf4f1; _scid=47caae3a-e216-48d9-8cdc-3159238a7671; FXN_flk=1; AMCVS_17FC406C5357BA6E0A490D4D%40AdobeOrg=1; _gid=GA1.2.1114110874.1557801782; s_cc=true; _csrf=qWmVWRGxKfzqXCxI9_yuGfZI; s_sq=%5B%5BB%5D%5D; AKA_A2=A; ak_bmsc=3362DC65CD8C5F6FE2F5F2E24D7DD7FE6876060DED3200004C65DA5C0E141B34~pl9V8ncmx0JI/913nUJgfYoKX6Gte64URfMw4gBpTiaQPEzpKVnyOxRIc/NBeHS9HwdJZ+Fd5cB6oDFLpRNLt93qTu4fSjWuP7e+PZea5EArlAr63c0rHI5P+U7hKycyZfvpMt2MSsmqLqtUqZqavEQxBprGj74WIJ0a5ZnH2vSP1CYH+4ijzZPqw/REPx+WlZ+jHCptyFj7C9pjBHstMpWmr4RW6NTHMwyBsckJbiQr0p+5gPNq/FUjz06HN7q/b4; _cb_svref=null; AMCV_17FC406C5357BA6E0A490D4D%40AdobeOrg=2121618341%7CMCIDTS%7C18031%7CMCMID%7C37985443320715041480395091296536963184%7CMCAAMLH-1557842971%7C7%7CMCAAMB-1558421455%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1557823855s%7CNONE%7CMCAID%7CNONE; s_pers=%20s_ppn%3Dfnc%253Aroot%253Aroot%253Achannel%7C1557806491239%3B%20omtr_lv%3D1557816723185%7C1652424723185%3B%20omtr_lv_s%3DLess%2520than%25201%2520day%7C1557818523185%3B%20s_nr%3D1557816723191-Repeat%7C1560408723191%3B; _chartbeat2=.1556269420027.1557816723254.0000000010000001.CY0VlWCO9QUgDFFbO8QLxoyCPj7ho.2; s_sess=%20omtr_evar17%3DD%253Dc17%3B%20s_ppvl%3Dfnc%25253Aworld%25253Asubsection%25253Aarticle%252C22%252C83%252C5886%252C1920%252C925%252C1920%252C1080%252C1%252CL%3B%20SC_LINKS%3D%3B%20s_ppv%3Dfnc%25253Aworld%25253Asubsection%25253Aarticle%252C63%252C96%252C3550%252C1920%252C969%252C1920%252C1080%252C1%252CL%3B; criteo_write_test=ChUIBBINbXlHb29nbGVSdGJJZBgBIAE; bm_sv=8A6F070ED17B9F85AD022D562A830573~oN82OtrVhgL99OXQYjpsFWPKOuwBoUVwy60qge23Kx9pNN2MIe3/AhQZJZ+na42MjDAIyCRuvDS6csM6csNzVnCY/0Ue7dXJIHzFvEjq/KcL+5X57fiZK5b9W/W3g/hw1kSCvVxA/GNO4h9IlDmY6OElMgVSqN2h9kq42m6z+n0='}
        self.downloadPath = '/data/crawler'
        self.picPath = '/fox_news/picture/'
        self.filter = Filter_Data()
        self.save = Save_Data()



    def run(self):
        self.parsing_fox_news_list()


    def parsing_fox_news_list(self):
        today = self.point_time
        for kw in self.keyword:
            print('keyword:\t', kw)
            news_list = self.news_api.get_everything(q=kw,
                                                    sources='fox-news',
                                                    domains='foxnews.com',
                                                    from_param=today,
                                                    to=today[:-1] + str(int(today[-1]) - 1),
                                                    language='en',
                                                    sort_by='relevancy',
                                                    page_size=100, )
            self.parsing_fox_news_list_url(news_list=news_list)


    def parsing_fox_news_list_url(self, news_list):
        articles = news_list['articles']
        for i in range(len(articles)):
            details_url = articles[i]['url']
            result = self.filter.filter_data(details_url=details_url)
            if result:
                print('Data already exists!')
            else:
                details_res = requests.get(details_url, headers=self.headers, cookies=self.cookies).text
                time.sleep(random.uniform(1, 3))
                html_obj = etree.HTML(details_res)
                source = int(9)
                sourceUrl = details_url
                jobId = time.time()
                author = articles[i]['source']['name']
                authorName = self.parsing_author_name(html_obj=html_obj, name_source=author)
                releaseTime = articles[i]['publishedAt']
                title = articles[i]['title']
                content = self.parsing_news_content(content_html=details_res, html_obj=html_obj, newspaper=True)
                thumbnail_img = articles[i]['urlToImage']
                img = self.download_img(html_obj=html_obj, thumbnail_img=thumbnail_img)
                if img is None or img == '' or content is None or content == '':
                    pass
                else:
                    data = {'source': source, 'jobId': int(jobId), 'sourceUrl': sourceUrl, 'title': title, 'authorName': authorName,
                            'releaseTime': releaseTime, 'content': content, 'img': img}
                    print('data:\n', data)
                    self.save.save_data(data=data, news='fox')


    def parsing_author_name(self, html_obj, name_source):
        authorName = ''.join(html_obj.xpath('//div[@class="author-byline"]//span/span//text()'))
        if authorName == '' or authorName is None:
            return name_source
        else:
            return authorName


    def parsing_news_content(self, content_html=None, html_obj=None, newspaper=False):
        try:
            if newspaper:
                text = fulltext(content_html).split('\n')
                txt = list(filter(lambda x: x.strip() != '', text))
                txt_list = []
                for i in txt:
                    if i.isupper():
                        pass
                    else:
                        txt_list.append(i)
                content = '<p>'.join(txt_list)
            else:
                content_list = html_obj.xpath('//div[@class="article-body"]//p//text()')
                content = '<p>'.join([i.replace("\n", '').strip() for i in content_list]).replace("<p><p>", '<p>')
            return content
        except:
            pass


    def download_img(self, html_obj, thumbnail_img):
        pic_url_list = html_obj.xpath('//div[@class="article-body"]//img/@src')
        img_id = str(uuid.uuid4()).replace('-','')
        index = 1
        img_list = []
        try:
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
            return None



if __name__ == '__main__':
    fox = FOX_News()
    fox.run()

