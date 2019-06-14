import requests, time, uuid, random, re, json
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



class Associated_Press_News(object):
    def __init__(self):
        self.headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36'}
        self.cookies = {'cookie': '_cb_ls=1; _cb=ChGdwsejPcBwqK1A; _ga=GA1.2.1067424464.1556266698; __gads=ID=b2804ef9280ce726:T=1556266708:S=ALNI_MbsZp6KMsLTd9MAhzM98UpWqF4sEQ; __qca=P0-112096547-1556266838413; trc_cookie_storage=taboola%2520global%253Auser-id%3Dbfc0c49d-bde0-4b78-9484-33cd8cb7509f-tuct3bdf4f1; GED_PLAYLIST_ACTIVITY=W3sidSI6Ilp4Q0YiLCJ0c2wiOjE1NTY2MTc5NjcsIm52IjowLCJ1cHQiOjE1NTY2MTc5NjAsImx0IjoxNTU2NjE3OTYwfV0.; _gid=GA1.2.1304411157.1557027854; _cb_svref=null; OptanonConsent=landingPath=NotLandingPage&datestamp=Sun+May+05+2019+11%3A44%3A56+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=4.1.0&EU=false&groups=0_140011%3A1%2C1%3A1%2C0_140010%3A1%2C2%3A1%2C3%3A1%2C4%3A1%2C0_140046%3A1%2C0_140042%3A1%2C0_140038%3A1%2C0_140034%3A1%2C0_140055%3A1%2C0_140051%3A1%2C0_140047%3A1%2C0_140043%3A1%2C0_140039%3A1%2C0_140035%3A1%2C0_140031%3A1%2C0_140052%3A1%2C0_140048%3A1%2C0_140044%3A1%2C0_140040%3A1%2C0_140036%3A1%2C0_140032%3A1%2C0_140053%3A1%2C0_140049%3A1%2C0_140045%3A1%2C0_140041%3A1%2C0_140037%3A1%2C0_140033%3A1%2C0_140054%3A1%2C0_140050%3A1%2C101%3A1%2C102%3A1%2C103%3A1%2C104%3A1%2C105%3A1%2C106%3A1%2C107%3A1%2C108%3A1%2C109%3A1%2C110%3A1%2C111%3A1%2C112%3A1%2C113%3A1%2C114%3A1%2C115%3A1%2C116%3A1%2C117%3A1%2C118%3A1%2C119%3A1%2C120%3A1%2C121%3A1%2C122%3A1%2C123%3A1%2C124%3A1%2C125%3A1%2C126%3A1%2C127%3A1%2C128%3A1%2C129%3A1%2C130%3A1%2C131%3A1%2C132%3A1%2C133%3A1%2C134%3A1%2C135%3A1%2C136%3A1%2C137%3A1%2C138%3A1%2C139%3A1%2C140%3A1%2C141%3A1%2C142%3A1%2C143%3A1%2C144%3A1%2C145%3A1%2C146%3A1%2C147%3A1%2C148%3A1%2C149%3A1%2C150%3A1%2C151%3A1%2C152%3A1%2C153%3A1%2C154%3A1%2C155%3A1&AwaitingReconsent=false; _tb_sess_r=; _tb_t_ppg=https%3A//apnews.com/245117b7dafd4790ba3d51db06cf345a; _gat=1; _chartbeat2=.1556266696382.1557028669628.1111100001.Vfd8vwJvnJujXq7Dq7JmkgXZfl.4'}
        self.downloadPath = '/data/crawler'
        self.picPath = '/ap_news/picture/'
        self.filter = Filter_Data()
        self.save = Save_Data()



    def run(self):
        news_dic = {
            'top' : 'https://apnews.com/apf-topnews',
            'sport' : 'https://apnews.com/apf-sports',
            'entertainment' : 'https://apnews.com/apf-entertainment',
            'travel' : 'https://apnews.com/apf-Travel',
            'technology' : 'https://apnews.com/apf-technology',
            'lifestyle' : 'https://apnews.com/apf-lifestyle',
            'business' : 'https://apnews.com/apf-business',
            'usNews' : 'https://apnews.com/apf-usnews',
            'health' : 'https://apnews.com/apf-Health',
            'science' : 'https://apnews.com/apf-science',
            'intlNews' : 'https://apnews.com/apf-intlnews',
            'politics' : 'https://apnews.com/apf-politics',
        }
        for url in news_dic:
            print('newsUlr:\n', url)
            try:
                ap.parsing_news_list_page(news_start_url=news_dic[url])
            except:
                pass


    def parsing_news_list_page(self, news_start_url):
        list_page_html = requests.get(url=news_start_url, headers=self.headers, cookies=self.cookies).text
        time.sleep(random.uniform(2, 5))
        list_html_obj = etree.HTML(list_page_html)
        list_page_url = list_html_obj.xpath('//a[@class="headline"]/@href')
        list_url = ['https://apnews.com' + i for i in list_page_url if 'https://apnews.com' not in i]
        for details_url in list_url:
            result=self.filter.filter_data(details_url=details_url)
            if result:
                print('Data already exists!')
            else:
                self.parsing_details_page(details_url=details_url)


    def parsing_details_page(self, details_url):
        details_html = requests.get(url=details_url, headers = self.headers, cookies = self.cookies).text
        time.sleep(random.uniform(1, 3))
        html_obj = etree.HTML(details_html)
        source = int(4)
        sourceUrl = details_url
        jobId = time.time()
        title = ''.join(html_obj.xpath('//div[@class="headline"]//h1/text()'))
        authorName = ''.join(html_obj.xpath('//span[@class="byline"]/text()'))
        releaseTime = ''.join(html_obj.xpath('//span[@class="Timestamp"]/@data-source'))
        content = self.parsing_news_content(content_html =details_html)
        img_urls = html_obj.xpath('//a[@class="LeadFeature LeadFeature_gallery"]/@href')
        if img_urls == [] or img_urls is None:
            pass
        else:
            img = self.download_picture(html=details_html)
            if img is None or img == '':
                pass
            else:
                data = {'source': source, 'jobId': int(jobId), 'sourceUrl': sourceUrl, 'title': title, 'authorName': authorName,
                        'releaseTime': releaseTime, 'content': content, 'img': img}
                print('data:\n', data)
                self.save.save_data(data=data, news='ap')


    def parsing_news_content(self, content_html):
        text = fulltext(content_html).split('\n')
        txt = list(filter(lambda x: x.strip() != '', text))
        content = '<p>'.join(txt)
        return content


    def download_picture(self, html):
        try:
            url_list = self.analysis_pic_url(html=html)
            img_id = str(uuid.uuid4()).replace('-','')
            index = 1
            img_list = []
            for pic_url in url_list[:17]:
                urllib.request.urlretrieve(pic_url, r'%s.jpg' % (self.downloadPath + self.picPath + str(img_id) + "-" + str(index)))
                img_list.append(r'%s.jpg' % (self.picPath + str(img_id) + "-" + str(index)))
                index += 1
            img = ','.join(img_list)
            return img
        except:
            pass


    def analysis_pic_url(self,  html):
        html_script = r'<script>(.*?)</script>'
        script = re.findall(html_script, html, re.S | re.M)
        mediumIds_rule = r'mediumIds(.*?)]'
        rule = re.compile(mediumIds_rule)
        result = rule.findall(script[0])[0][3:]
        result = "[" + result + "]"
        js = json.loads(result)
        url_list = []
        for i in js:
            url = 'https://storage.googleapis.com/afs-prod/media/' + i + '/' + '600.jpeg'
            url_list.append(url)
        return url_list



if __name__ == '__main__':
    ap =Associated_Press_News()
    ap.run()

