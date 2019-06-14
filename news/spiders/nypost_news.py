import requests, uuid, time, random
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


class New_York_Post_news(object):
    def __init__(self):
        self.headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
        self.cookies = {'cookie': 'optimizelyEndUserId=oeu1555918735298r0.6812295616493853; _ga=GA1.2.501461025.1557229334; __pnahc=0; __tbc=%7Bjzx%7DbOREsfUR6SMcRp5niCu4XyJqGIm9xLbU2svbGCB3e5Y-ZlpcwIXRF_gOx5ssrGMlRCzVeeO-JA50xgthIobqDMJS2og0GbDQCa7bPklPxk1yFokaLXVHvRa0s4J7s817Uqt8s09tJ4GcmUzNoGeVhA; __pat=-14400000; __gads=ID=b83698edc796f48a:T=1557229341:S=ALNI_MZYuxiKvMlIMXV92xfTw1XB6ms7EA; __qca=P0-643878854-1557229359497; _gid=GA1.2.1904385410.1557829332; _ncg_g_id_=9d6dce3e-2d15-45b6-a948-9dbb7fa69171; OX_plg=pm; _ncg_id_=16a959d5d8b-5c91174d-2719-4974-99d8-33e86e4219c2; _pc_morningReportRan=true; _sp_ses.3725=*; _parsely_session={%22sid%22:3%2C%22surl%22:%22https://nypost.com/%22%2C%22sref%22:%22%22%2C%22sts%22:1557886391506%2C%22slts%22:1557829347024}; _parsely_visitor={%22id%22:%2236e3895b-5884-4e1e-b290-0b0a1e631850%22%2C%22session_count%22:3%2C%22last_session_ts%22:1557886391506}; AMP_TOKEN=%24NOT_FOUND; bounceClientVisit2045v=N4IgNgDiBcIBYBcEQM4FIDMBBNAmAYnvgHYCeEA9iggHQDGFAtkcQKYDu6BIANCAE4wQZStXpMQAXyA; _ncg_sp_ses.64db=*; _gat=1; __idcontext=eyJjb29raWVJRCI6IlpORUtKQzRVUEwzNUhUUTI2QkNJVUIySDZZVUFOTjI1V0E0VzI1WERQSU9RPT09PSIsImRldmljZUlEIjoiWk5FS0pDNFVPVFU1NzVaQTVZSU1LVlNHUlVFU0pOM0JWNEdTWVJHNUM0WEE9PT09IiwiaXYiOiJQR1ZMV1NQWTc2R0pGMkhISUJCVEpBTEc0UT09PT09PSIsInYiOjF9; __pvi=%7B%22id%22%3A%22v-2019-05-15-11-28-33-472-TCTTCzJ3MeatqGej-a5838d1dc51fc02369a5c570d5bb61d6%22%2C%22domain%22%3A%22.nypost.com%22%2C%22time%22%3A1557891488612%7D; __adblocker=false; xbc=%7Bjzx%7DCTyXA66nwH4u0LSnMj_hrMtwYTk54JF59dLs5o_wp3snMXNdvj2Yy6TBtbRxyGxf14_VW1q5TLlW6vo43sH4bt1xlU681XmGmmXaT-SetcMReVqnxTFjI2gW-7RAeJAQFo8mvk88JA2ghePCorbhbWMs02tfzF_-k1Krwk0Vz5I_4BWDD33FM1fohQjjcgYaPM-1rt-sKsCEnjEZlCFDpqiFO54mgbKUB-kFVcHhi-_WjEFJazS2Vtn_ZZJHi-y44g16CXbGiqpHfoDR9DPafHAts-4n-G65fMRtwt9Ml8JaS73yz78cdU_g515IoAaF5TiHkpwV8OOumbfwBrkq2AU3h3dtbnjKZd070tIlyyZdFCbfpjqxaxax2jiN0PitRuCioMt8p4TO3fxq6ok4tA; _ncg_sp_id.64db=d08b0f08-4e58-40a9-8cd3-63efa5ae79b6.1557229345.5.1557891492.1557886389.183b444b-a79a-4498-bd82-c06c607b176e; _sp_id.3725=b96eefdc3adfd036.1557229358.3.1557891502.1557831911'}
        self.downloadPath = '/data/crawler'
        self.picPath = '/nypost/picture/'
        self.filter = Filter_Data()
        self.save = Save_Data()



    def run(self):
        pg = 1
        while pg < 3:
            url_dic = { "news" :'https://nypost.com/news/page/{}/'.format(pg),
                        "metro" : 'https://nypost.com/metro/page/{}/'.format(pg),
                        "pagesix" : 'https://pagesix.com/page/{}/'.format(pg),
                        "basketball" : 'https://nypost.com/basketball/page/{}/'.format(pg),
                        "baseball" : 'https://nypost.com/baseball/page/{}/'.format(pg),
                        "football" : 'https://nypost.com/football/page/{}/'.format(pg),
                        "college" : 'https://nypost.com/college/page/{}/'.format(pg),
                        "hockey" : 'https://nypost.com/hockey/page/{}/'.format(pg),
                        "business" : 'https://nypost.com/business/page/{}/'.format(pg),
                        "opinion" : 'https://nypost.com/opinion/page/{}/'.format(pg),
                        "entertainment" : 'https://nypost.com/entertainment/page/{}/'.format(pg),
                        "fashion" : 'https://nypost.com/fashion/page/{}/'.format(pg),
                        "living" : 'https://nypost.com/living/page/{}/'.format(pg),
                        "tech" : 'https://nypost.com/tech/page/{}/'.format(pg),
                    }
            for kw in url_dic:
                print('keyword:\t', kw)
                self.parsing_list_page_url(list_url=url_dic[kw])
            pg += 1


    def parsing_list_page_url(self, list_url):
        res = requests.get(url=list_url, headers = self.headers, cookies = self.cookies).text
        html = etree.HTML(res)
        time.sleep(random.uniform(2, 5))
        details_urls_list = html.xpath('//h3[@class="entry-heading"]//a/@href')
        title_list =html.xpath('//h3[@class="entry-heading"]//a/text()')
        releaseTime_list = html.xpath('//div[@class="entry-meta"]//p//text()')
        for i in range(len(details_urls_list)):
            sourceUrl = details_urls_list[i]
            title = title_list[i]
            releaseTime = releaseTime_list[i]
            source_headers = {'sourceUrl':sourceUrl, 'title':title, 'releaseTime':releaseTime}
            self.parsing_details_page_url(source_headers=source_headers, )


    def parsing_details_page_url(self, source_headers):
        status = self.filter.filter_data(details_url=source_headers['sourceUrl'])
        if status:
            print('Data already exists!')
        else:
            res = requests.get(url=source_headers['sourceUrl'], headers=self.headers, cookies=self.cookies).text
            html = etree.HTML(res)
            time.sleep(random.uniform(1, 3))
            source = int(10)
            sourceUrl = source_headers['sourceUrl']
            jobId = time.time()
            title = source_headers['title']
            releaseTime = source_headers['releaseTime']
            authorName = ''.join(html.xpath('//p[@class="byline"]//a/text()'))
            content = self.parsing_news_content(content_html=res, html_obj=html,newspaper=True)
            img = self.download_img(html_obj=html)
            if img is None or img == '' or content is None or content == '':
                pass
            else:
                data = {'source': source, 'jobId': int(jobId), 'sourceUrl': sourceUrl, 'title': title, 'authorName': authorName,
                        'releaseTime': releaseTime, 'content': content, 'img': img}
                print('data:\n', data)
                self.save.save_data(data=data, news='nowYorkPost')



    def parsing_news_content(self, content_html=None, html_obj=None, newspaper=False):
        if newspaper:
            text = fulltext(content_html).split('\n')
            txt = list(filter(lambda x: x.strip() != '', text))
            content = '<p>'.join(txt)
        else:
            content_list = html_obj.xpath('//div[@id="news-content"]//p/text()')
            content = '<p>'.join([i.replace("\n", '').strip() for i in content_list]).replace("<p><p>", '<p>')
        return content


    def download_img(self, html_obj):
        pic_list_1 = html_obj.xpath('//div[@class="featured-image"]/img/@src')
        pic_list_2 = html_obj.xpath('//div[@class="article-header"]//img/@data-srcset')
        pic_url_list = pic_list_1 + pic_list_2
        img_id = str(uuid.uuid4()).replace('-','')
        index = 1
        img_list = []
        if pic_url_list == []:
            return None
        else:
            for pic_url in pic_url_list[:17]:
                urllib.request.urlretrieve(pic_url, r'%s.jpg' % (self.downloadPath + self.picPath + str(img_id) + "-" + str(index)))
                img_list.append(r'%s.jpg' % (self.picPath + str(img_id) + "-" + str(index)))
                index += 1
            img = ','.join(img_list)
            return img



if __name__ == '__main__':
    ny = New_York_Post_news()
    ny.run()
