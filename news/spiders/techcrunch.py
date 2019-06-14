import time, random, requests, uuid, json
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



class Techcrunch_News(object):
    def __init__(self):
        self.headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
        self.cookies = {'cookie': 'rxx=293dmvskaws.1i9frk99&v=1; _ga=GA1.2.893461412.1556504122; _fbp=fb.1.1556504132562.1028440015; __pnahc=0; __pat=-25200000; OTH=v=1&d=eyJraWQiOiIwMTY0MGY5MDNhMjRlMWMxZjA5N2ViZGEyZDA5YjE5NmM5ZGUzZWQ5IiwiYWxnIjoiUlMyNTYifQ.eyJjdSI6eyJndWlkIjoiUDJCVVRPR0RVT0VGVERUV0pNTFdKNFlFSDQiLCJzaWQiOiJEYTNsbjdKbG11MmwifX0.HoiBv5OlQvNY2x6q-LJBN-VzgCErT7GTCnODqLLQ8foasqTVUCPVXvwHFniFc7CwCf0n7lmSgfrSycQNevIFSJHZ7M-S9SRQH4FMtu91qykbuvAzAOQZRw_iz_warZWFJtpIys0EVH4Gn9wYqaqLXv-5lO39fuPsqJx9z7X6luQ; BX=e7bndb9eccnhl&b=4&d=lrdDlyNpYELw7nQr45ylAA--&s=8v&i=_g5gVQJJ34nc.9WZ3JGN; GUC=AQEAAQJc0SBdu0IgxgTZ&s=AQAAAJQ2Kk5V&g=XM_RDg; __tbc=%7Bjzx%7DjGAToaZMxJYLoS7N4KRjDaxHalABoj31MSFHkZP0UNxHLBrPMu6clUAaZwsaHnUnQQaMDnEIRO1fDpAMrkMVflCNhUFWsFFB8n1hsUBhKEKL38bZEAUprS1G6wPj4GNM4bchi9l7YPvr6or9wrNMLmWzw2hPXY5j7UVUWDOUH_U; __pcvc={}; _parsely_session={%22sid%22:6%2C%22surl%22:%22https://techcrunch.com/2019/05/04/uber-is-facing-australian-class-action-suit-alleging-unlawful-conduct/%22%2C%22sref%22:%22%22%2C%22sts%22:1558071232131%2C%22slts%22:1557885616789}; _parsely_visitor={%22id%22:%22pid=092447ecfa41ad2c2f2833a4997f1d2f%22%2C%22session_count%22:6%2C%22last_session_ts%22:1558071232131}; cmp=t=1558071232&j=0; _gid=GA1.2.1358424281.1558071235; _gat=1; __adblocker=false; xbc=%7Bjzx%7DYW6Rlvft6bPCfQyJ3DedvFReFNeSWzD34uqjUgyftdmRMMeJaQrGxlc0RnHslaNJuW923ovrMyh3fAAIY_x7R_Da15zP9YopEn3Om90NI0T5GRkVz40I1R8zV8ZQB68kBF2YuF_JsLshS1YKLFcyLSN12KbxNP4vrnBqkqtIO2yaJ5LoTRrcAPA64ePs4VtlokVTqGlotnhRSiMBSeplyP6M0a5Lj5rCIn1GIetfFxi-gIZuaMlkdAHSSmrqD1nfLBrQXcHSWrDRR0PGzzVvFjSVEXhIbldyChWDeAkkgN0hgI8KXA304yID8T-gx9UZiwWN897EFpRv3ZNtbg5IqW5GixrDYN1X7y_FdQGe5c4Tlz-figdB5Mbe5Qj2godX23QAk9Y6PbNudCC8Em1tgOzteL0CnIShQ--XvwA9qsvEZSWlAxrGfFmStXYiVaTRc1BM1DSemqPeEIoI_XtXT1h-FOYTaDZfqgflEl3Qb8MlWCowztRcnRznul-OxLIUMkPAraljlm83Bs9Z0ZZTeULOzew-rPTbrZfnXeQjr8OJtrUbNexMaJib654rgmNL7kXPxNmVdB1ZWX5IXEgmiW4XKjZACr0RxZbzXhXFfEN9gPbI7xVJJD8kfmfWoGW_0O6MebIrRbW8xxFPLY90Mw; __pvi=%7B%22id%22%3A%22v-2019-05-17-13-33-55-875-qtmTHL61BOYny2co-1510a80d282f15b71b1e5f4d8bc358ee%22%2C%22domain%22%3A%22.techcrunch.com%22%2C%22time%22%3A1558072171993%7D'}
        self.downloadPath = '/data/crawler'
        self.picPath = '/techcrunch/picture/'
        self.filter = Filter_Data()
        self.save = Save_Data()


    def run(self):
        pg = 1
        while pg < 3:
            start_url = 'https://techcrunch.com/wp-json/tc/v1/magazine?page={}&_embed=true'.format(pg)
            self.parsing_tc_news_list_url(list_url=start_url)
            pg += 1


    def parsing_tc_news_list_url(self, list_url):
        res =requests.get(url=list_url, headers=self.headers, cookies=self.cookies).text
        time.sleep(random.uniform(1, 3))
        article = json.loads(res)
        for i in range(len(article)):
            sourceUrl = article[i]["link"]
            status = self.filter.filter_data(details_url=sourceUrl)
            if status:
                pass
            else:
                releaseTime = article[i]["date_gmt"]
                header_info = {'sourceUrl':sourceUrl, 'releaseTime':releaseTime}
                self.parsing_details_page(header_info=header_info)


    def parsing_details_page(self, header_info):
        jobId = time.time()
        source = int(14)
        sourceUrl = header_info['sourceUrl']
        releaseTime = header_info['releaseTime']
        res = requests.get(url=sourceUrl, headers=self.headers, cookies=self.cookies).text
        time.sleep(random.uniform(1, 3))
        html = etree.HTML(res)
        title = ''.join(html.xpath('//h1[@class="article__title"]/text()'))
        authorName = ''.join(html.xpath('//div[@class="article__byline"]/a/text()')).strip()
        content = self.parsing_news_content(content_html=res)
        img = self.download_img(html_obj=html)
        if img is None or img == '' or content is None or content == '':
            pass
        else:
            data = {'source': source, 'jobId': int(jobId), 'sourceUrl': sourceUrl, 'title': title, 'authorName': authorName,
                    'releaseTime': releaseTime, 'content': content, 'img': img}
            print('data:\n', data)
            self.save.save_data(data=data, news='techcrunch')


    def parsing_news_content(self, content_html=None):
        text = fulltext(content_html).split('\n')
        txt = list(filter(lambda x: x.strip() != '', text))
        content = '<p>'.join(txt)
        return content


    def download_img(self, html_obj,):
        pic_url_list = html_obj.xpath('//article[@class="article-container article--post "]//img/@src')
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
    tc = Techcrunch_News()
    tc.run()

