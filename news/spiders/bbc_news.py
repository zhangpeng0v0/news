from newsapi import NewsApiClient
from newspaper import fulltext
import requests, time, uuid, random
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


class BBC_News():
    def __init__(self):
        self.news_api = NewsApiClient(api_key = 'cb7a4ae15a98429890aeedb9a7b460a0')
        self.headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36'}
        self.cookies = {'cookie': 'ckns_orb_fig_cache={%22ad%22:1%2C%22ap%22:4%2C%22ck%22:0%2C%22eu%22:0%2C%22uk%22:0}; ckns_sa_labels_persist={}; ckns_sscid=7f5aa895-8a47-4928-8632-ae8118032bcb; _cb_ls=1; _cb=CF1-z-CgoNtbBVcmNK; ckns_eds=INS-vt29-666188954:923108334-1556503556; ckns_settings-nonce=FwTiPYjnehKUtBu4zb7oIJ4j; amlbcookie=01; ckns_mvt=8c10379c-2f9b-44e6-a88b-97b0315adccb; ckns_account_experiments=j%3A%7B%22accxp_marketing_opt_in_2%22%3A%22control%22%7D; AWSELB=0FC55D47187ECE9190E70C0A017AC69A844CA844E9727B10D1C45E9E505E11A5757E62A62559CE5ECC76BE5C0D98ACC5FFDFADB0DF8505DDE5C427CC6C744FDB90DA13BB15F2555DE48D9361FEFE0FBEA45595E8C7; ckns_stateless=1; ckns_nonce=nzFw9J2FPDEn17WnPYS0LnRO; ckns_id=eyJhYiI6Im8xOCIsImVwIjp0cnVlLCJldiI6ZmFsc2UsInBzIjoicHVmZjhMV3pjSUlfckQ3RlkwaVo1V0dsM3czbFdBWDQ0TmVXNktKYjdDMCIsInNlcy1leHAiOjE1NTY1MTgzOTIwMDAsImp3dC1leHAiOjE2MTk1ODk0OTIwMDAsInRrbi1leHAiOjE1NTY1MjExMzEwMDAsInJ0a24tZXhwIjoxNjE5NTg5NDkyMDAwfQ; ckns_atkn=eyJ0eXAiOiJKV1QiLCJ6aXAiOiJOT05FIiwiYWxnIjoiSFMyNTYifQ.eyJzdWIiOiIzY2RiOWVkOC01ZjdmLTRlZWEtODYxNS1jMzZmMTdhZjZkMzEiLCJjdHMiOiJPQVVUSDJfU1RBVEVMRVNTX0dSQU5UIiwiYXV0aF9sZXZlbCI6MiwiYXVkaXRUcmFja2luZ0lkIjoiNmJmNjBhOTAtMzdiZS00MjE2LWIyOWQtNWI4NDFmZjA2Y2RmLTM2MTkxOTY1MCIsImlzcyI6Imh0dHBzOi8vYWNjZXNzLmFwaS5iYmMuY29tL2JiY2lkdjUvb2F1dGgyIiwidG9rZW5OYW1lIjoiYWNjZXNzX3Rva2VuIiwidG9rZW5fdHlwZSI6IkJlYXJlciIsImF1dGhHcmFudElkIjoidlhTaHVESDJRc3BOTTItZ0d3ek4yYlBJczRRIiwiYXVkIjoiQWNjb3VudCIsIm5iZiI6MTU1NjUxNzUzMSwiZ3JhbnRfdHlwZSI6InJlZnJlc2hfdG9rZW4iLCJzY29wZSI6WyJleHBsaWNpdCIsImltcGxpY2l0IiwicGlpIiwidWlkIiwib3BlbmlkIl0sImF1dGhfdGltZSI6MTU1NjUxNzQ5MSwicmVhbG0iOiIvIiwiZXhwIjoxNTU2NTI0NzMxLCJpYXQiOjE1NTY1MTc1MzEsImV4cGlyZXNfaW4iOjcyMDAsImp0aSI6IkZXcExhak13bmYxdUJyRWMtY0xaNnlpTUE1cyJ9.OhaC7wNmB_bALESjcJH8JjKcGRa-WaGkcZGWS0rhAtg; ckns_idtkn=eyJ0eXAiOiJKV1QiLCJraWQiOiJIa2d0WDBJd3RDOStSVGQvOWdYdFN0bk9VaU09IiwiYWxnIjoiUlMyNTYifQ.eyJhdF9oYXNoIjoiNGFfU2tJMWtQaVVZbks2VGlNSm9BdyIsInN1YiI6IjNjZGI5ZWQ4LTVmN2YtNGVlYS04NjE1LWMzNmYxN2FmNmQzMSIsImFiIjoibzE4IiwiYXVkaXRUcmFja2luZ0lkIjoiNmJmNjBhOTAtMzdiZS00MjE2LWIyOWQtNWI4NDFmZjA2Y2RmLTM2MTkxOTY1MSIsImlzcyI6Imh0dHBzOi8vYWNjZXNzLmFwaS5iYmMuY29tL2JiY2lkdjUvb2F1dGgyIiwidG9rZW5OYW1lIjoiaWRfdG9rZW4iLCJhdWQiOiJBY2NvdW50IiwiYWNyIjoiMCIsImF6cCI6IkFjY291bnQiLCJhdXRoX3RpbWUiOjE1NTY1MTc0OTEsInJlYWxtIjoiLyIsImV4cCI6MTU1NjUyMTEzMSwidG9rZW5UeXBlIjoiSldUVG9rZW4iLCJpYXQiOjE1NTY1MTc1MzF9.LqYjXmcfMMVfB3UupPV8oqez0gojKu-9anW-73WVKXOS5deEbwwYMrTr8JQy85WhwzlZNA5e8eqLPWJ_lAgfjCiw60zdYMxM_x_ZYaHtpPtAXf0SCOD8FlTBKnRZYDqKNkj8F22ctDqPUqrRrN-tDVTqrVMYW38sHqBeXalUGkw-2C24UBlE4DFcDqeqjn0pOFbwuFyQpgwrwp1y6UyUvF3WhuB6GVIkkKNUgYbWpnHTmP9OD8DNM_MH9TLDaC9SoRE5py51CpkZ78Y4rnQUAHeHibjbOwLKQkadVGhFzxr4vzxwJlRj_nrCySmrplgDJ7a9P_raVKfL4JH6UeA1_A; atuserid=%7B%22name%22%3A%22atuserid%22%2C%22val%22%3A%222a12b799-e590-476f-9b23-800e48e162f4%22%2C%22options%22%3A%7B%22end%22%3A%222020-05-30T05%3A59%3A40.931Z%22%2C%22path%22%3A%22%2F%22%7D%7D; _chartbeat2=.1556007561538.1556517584378.1000001.BzGCuqD5hQB-BMGlTiNhxZyCFMP2O.1; _cb_svref=https%3A%2F%2Fwww.bbc.com%2Fnews; ckps_id_ptrt=https%3A%2F%2Fwww.bbc.co.uk%2Fprogrammes%2Fw172wy08d8yw9mq; ecos.dt=1556517629804'}
        self.t = time.time()
        self.point_time = time.strftime('%Y-%m-%d', time.localtime(self.t))
        self.keyword = ['News', 'Health', 'Science', 'Entertainment', 'Technology']
        self.downloadPath = '/data/crawler'
        self.picPath = '/bbc_news/picture/'
        self.filter = Filter_Data()
        self.save = Save_Data()


    def run(self):
        bbc.parsing_bbc_news_list()


    def parsing_bbc_news_list(self):
        today = self.point_time
        for kw in self.keyword:
            print('keyword:\n', kw)
            news_list = self.news_api.get_everything(q = kw,
                                                    sources = 'bbc-news',
                                                    domains = 'bbc.co.uk',
                                                    from_param = today,
                                                    to = today[:-1] + str(int(today[-1]) - 1),
                                                    language = 'en',
                                                    sort_by = 'relevancy',
                                                    page_size = 100)
            self.parsing_news_list_url(news_list=news_list)


    def parsing_news_list_url(self, news_list):
        articles = news_list['articles']
        for i in range(len(articles)):
            details_url = articles[i]['url']
            if 'www.bbc.co.uk' in details_url:
                result = self.filter.filter_data(details_url=details_url)
                if result:
                    print('Data already exists!')
                else:
                    details_res = requests.get(details_url, headers=self.headers, cookies=self.cookies).text
                    time.sleep(random.uniform(1, 5))
                    html_obj = etree.HTML(details_res)
                    source = int(6)
                    sourceUrl = details_url
                    jobId = time.time()
                    authorName = articles[i]['source']['name']
                    releaseTime = articles[i]['publishedAt']
                    title_source = articles[i]['title']
                    title = self.parsing_news_title(html= html_obj, title_source=title_source)
                    thumbnail_img = articles[i]['urlToImage']
                    img = self.download_img(html=html_obj, thumbnail_img=thumbnail_img)
                    content = self.parsing_news_content(content_html=details_res)
                    if content == 'Sign in to the BBC, or Register' or content is None or img is None or img == '':
                        pass
                    else:
                        data = {'source': source, 'jobId': int(jobId), 'sourceUrl': sourceUrl, 'title': title, 'authorName': authorName,
                                'releaseTime': releaseTime, 'content': content, 'img': img}
                        print('data:\n', data)
                        self.save.save_data(data=data, news='bbc')


    def parsing_news_title(self, html, title_source):
        title =''.join(html.xpath('//h1[@class="story-body__h1"]/text()'))
        if title == '' or title is None:
            return title_source
        else:
            return title


    def parsing_news_content(self, content_html):
        text = fulltext(content_html).split('\n')
        txt = list(filter(lambda x: x.strip() != '', text))
        content = '<p>'.join(txt)
        return content


    def download_img(self, html, thumbnail_img):
        try:
            pic_list_1 = html.xpath('//span[@class="image-and-copyright-container"]/img/@src')
            pic_list_2 = html.xpath('//div[@class="js-delayed-image-load"]/@data-src')
            pic_list_3 = [i for i in pic_list_2 if '320' in i]
            pic_list = pic_list_1 + pic_list_3
            img_id = str(uuid.uuid4()).replace('-', '')
            index = 1
            img_list = []
            pic_url_list = [i for i in pic_list if 'png' not in i]
            if pic_url_list == []:
                urllib.request.urlretrieve(thumbnail_img, r'%s.jpg' % (self.downloadPath + self.picPath + str(img_id) + "-" + str(index)))
                img = r'%s.jpg' % (self.picPath + str(img_id) + "-" + str(index))
                return img
            else:
                for pic_url in pic_url_list:
                    if '320' in pic_url:
                        url = pic_url.replace("320", '660')
                        urllib.request.urlretrieve(url, r'%s.jpg' % (self.downloadPath + self.picPath + str(img_id) + "-" + str(index)))
                        img_list.append(r'%s.jpg' % (self.picPath + str(img_id) + "-" + str(index)))
                        index += 1
                    else:
                        urllib.request.urlretrieve(pic_url, r'%s.jpg' % (self.downloadPath + self.picPath + str(img_id) + "-" + str(index)))
                        img_list.append(r'%s.jpg' % (self.picPath + str(img_id) + "-" + str(index)))
                        index += 1
                img = ','.join(img_list)
                return img
        except:
            return None



if __name__ == '__main__':
    bbc = BBC_News()
    bbc.run()

