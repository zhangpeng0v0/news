import requests, time, uuid, random, re
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



class Medium_News():
    def __init__(self):
        self.headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
        self.cookies = {'cookie': '__cfduid=d6ba6448200002747444269a19593dbdd1555908016; __cfruid=985eba5fa2a449247bfd0598c1c1c5ec968a9416-1558490711; _ga=GA1.2.1064338879.1558490714; _gid=GA1.2.136804405.1558490714; lightstep_guid/medium-web=8f0cd65b0ef4abdb; lightstep_session_id=fcac5cf910466bc4; pr=1; tz=-480; uid=3314454e53ae; sid=1:4N4F93p0H1gPvFCIGldZUdIdQeFiifNF6stzqPFyBikCsGpjcmnIyu/NNWwIVVTx; xsrf=89TsRPcZaZKu; lightstep_guid/lite-web=7d9b16045b97b840; _parsely_session={%22sid%22:3%2C%22surl%22:%22https://medium.com/%22%2C%22sref%22:%22%22%2C%22sts%22:1558512703778%2C%22slts%22:1558503751909}; _parsely_visitor={%22id%22:%22pid=092447ecfa41ad2c2f2833a4997f1d2f%22%2C%22session_count%22:3%2C%22last_session_ts%22:1558512703778}; sz=1905'}
        self.downloadPath = '/data/crawler'
        self.picPath = '/huffpost/picture/'
        self.filter = Filter_Data()
        self.save = Save_Data()


    def run(self):
        news_dict = {
            'topic':'https://medium.com/topic/editors-picks',
            'technology':'https://medium.com/topic/technology',
            'startups':'https://medium.com/topic/startups',
            'self':'https://medium.com/topic/self',
            'politics':'https://medium.com/topic/politics',
            'health':'https://medium.com/topic/health',
            'design':'https://medium.com/topic/design',
            'art':'https://medium.com/topic/art',
            'beauty':'https://medium.com/topic/beauty',
            'humor':'https://medium.com/topic/humor',
            'fiction':'https://medium.com/topic/fiction',
            'media':'https://medium.com/topic/social-media',
            'crime':'https://medium.com/topic/true-crime',
            # 'comics':'https://medium.com/topic/comics',
        }
        for i in news_dict:
            self.parsing_medium_topic_list_page(url=news_dict[i])

        news_list = {
            'elemental':'https://medium.com/elemental-by-medium',
            'heated':'https://heated.medium.com/',
            'human':'https://medium.com/human-parts',
        }
        for j in news_list:
            self.parsing_medium_other_list_page(url=news_list[j])


    def parsing_medium_topic_list_page(self, url):
        html = requests.get(url=url, headers=self.headers, cookies=self.cookies).text
        time.sleep(random.uniform(3 ,5))
        html_script = r'<script>(.*?)</script>'
        script = re.findall(html_script, html, re.S | re.M)
        mediumUrl_rule = r'"mediumUrl":"(.*?)"'
        rule = re.compile(mediumUrl_rule)
        result = rule.findall(script[4])
        for i in result:
            details_url = i.replace(r'\u002F', '/')
            self.parsing_details_page(details_url=details_url)



    def parsing_medium_other_list_page(self, url):
        res = requests.get(url=url, headers=self.headers, cookies=self.cookies).text
        html = etree.HTML(res)
        list_page_urls = html.xpath('//div[@class="u-lineHeightBase postItem"]/a/@href')
        for details_url in list_page_urls:
            self.parsing_details_page(details_url=details_url)


    def parsing_details_page(self, details_url):
        status = self.filter.filter_data(details_url=details_url)
        if status:
            print('Data already exists!')
        else:
            res = requests.get(url=details_url, headers=self.headers, cookies=self.cookies).text
            time.sleep(random.uniform(1, 3))
            html = etree.HTML(res)
            source = int(8)
            jobId = time.time()
            sourceUrl = details_url
            title =''.join(html.xpath('//div[@class="section-content"]//h1//text()'))
            if title == '' or title is None:
                pass
            else:
                authorName = ''.join(html.xpath('//div[@class="u-paddingBottom3"]/a/text()'))
                releaseTime = ''.join(html.xpath('//time/text()'))
                content = self.analysis_news_content(html=res, obj=html, newspaper=False)
                img = self.analysis_news_img(obj=html)
                if img is None or img == '' or content is None or content == '':
                    pass
                else:
                    data = {'source': source,'jobId': int(jobId), 'sourceUrl': sourceUrl, 'title': title, 'authorName': authorName,
                            'releaseTime': releaseTime, 'content': content, 'img': img}
                    print('data:\n', data)
                    self.save.save_data(data=data, news='medium')


    def analysis_news_content(self, html, obj, newspaper=True):
        if newspaper:
            text = fulltext(html).split('\n')
            txt = list(filter(lambda x: x.strip() != '', text))
            content = '<p>'.join(txt)
            return content
        else:
            content_list= obj.xpath('//div[@class="section-content"]//text()')[7:]
            content = '<p>'.join([i.replace("\n", '').strip() for i in content_list]).replace("<p><p>", '<p>')
            return content


    def analysis_news_img(self, obj):
        try:
            pic_url_list = obj.xpath('//img[@class="progressiveMedia-image js-progressiveMedia-image"]/@data-src')
            img_id = str(uuid.uuid4()).replace('-', '')
            index = 1
            img_list = []
            if pic_url_list == []:
                return None
            else:
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
    m = Medium_News()
    m.run()
