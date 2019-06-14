import requests, time, uuid, json, random
from lxml import etree
from bloom_filter import BloomFilter
import urllib.request
import urllib.parse


class CNN_News(object):
    def __init__(self):
        self.headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
        self.cookies = {'cookie': 'tryThing00=1098; tryThing01=5838; tryThing02=0552; optimizelyEndUserId=oeu1556099053513r0.5843061130621663; s_fid=4A92F5E10FC9F2AB-176246D5FD4ACB26; gig_hasGmid=ver2; s_vi=[CS]v1|2E60197B8507E3C9-40000113A004AC13[CE]; __gads=ID=5243df9823110dbb:T=1556099830:S=ALNI_MbcB64SpCOjLKHMNlWpA0cU3jln6A; bfp_sn_rf_8b2087b102c9e3e5ffed1c1478ed8b78=Direct; bfp_sn_rt_8b2087b102c9e3e5ffed1c1478ed8b78=1556099832385; _fbp=fb.1.1556099850902.815265183; ajs_user_id=null; ajs_group_id=null; ajs_anonymous_id=%22abac316b-5aa7-403d-9230-f90f4f625c5f%22; _cb_ls=1; ug=5cc02ff00e7dc50a3f9cca0013c765a0; __qca=P0-689587383-1556590653464; _cb=BmyPaDKxXHCDf5t7; ugs=1; s_cc=true; s_ppv=100; countryCode=US; bounceClientVisit340v=N4IgNgDiBcIBYBcEQM4FIDMBBNAmAYnvgMYB2pApihAIakD2YAdGaS-QLZEgA0IATjBAgAvkA; _cb_svref=null; dmxRegion=false; s_sq=%5B%5BB%5D%5D; GED_PLAYLIST_ACTIVITY=W3sidSI6InA1UU4iLCJ0c2wiOjE1NTc3MTMxMzQsIm52IjoxLCJ1cHQiOjE1NTc3MTMwNzUsImx0IjoxNTU3NzEzMTMyfV0.; OptanonConsent=landingPath=NotLandingPage&datestamp=Mon+May+13+2019+10%3A05%3A38+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=4.4.0&EU=false&groups=1%3A1%2C2%3A1%2C3%3A1%2C4%3A1%2C0_37248%3A1%2C0_37215%3A1%2C0_37244%3A1%2C0_37211%3A1%2C0_37240%3A1%2C0_37207%3A1%2C0_37236%3A1%2C0_37203%3A1%2C0_37198%3A1%2C0_37231%3A1%2C0_37227%3A1%2C0_37223%3A1%2C0_37219%3A1%2C0_37216%3A1%2C0_37249%3A1%2C0_37212%3A1%2C0_37245%3A1%2C0_37208%3A1%2C0_37241%3A1%2C0_37204%3A1%2C0_37237%3A1%2C0_37232%3A1%2C0_37199%3A1%2C0_37228%3A1%2C0_37224%3A1%2C0_37220%3A1%2C0_37217%3A1%2C0_37246%3A1%2C0_37213%3A1%2C0_37242%3A1%2C0_37209%3A1%2C0_37238%3A1%2C0_37205%3A1%2C0_37234%3A1%2C0_37200%3A1%2C0_37233%3A1%2C0_37196%3A1%2C0_37229%3A1%2C0_37225%3A1%2C0_37221%3A1%2C0_37250%3A1%2C0_37214%3A1%2C0_37210%3A1%2C0_37243%3A1%2C0_37206%3A1%2C0_37239%3A1%2C0_37202%3A1%2C0_37235%3A1%2C0_37201%3A1%2C0_37230%3A1%2C0_37197%3A1%2C0_37226%3A1%2C0_37222%3A1%2C0_37218%3A1%2C8%3A1%2C101%3A1%2C102%3A1%2C103%3A1%2C104%3A1%2C105%3A1%2C106%3A1%2C107%3A1%2C108%3A1%2C109%3A1%2C110%3A1%2C111%3A1%2C112%3A1%2C113%3A1%2C114%3A1%2C115%3A1%2C116%3A1%2C117%3A1%2C118%3A1%2C119%3A1%2C120%3A1%2C121%3A1%2C122%3A1%2C123%3A1%2C124%3A1%2C125%3A1%2C126%3A1%2C127%3A1%2C128%3A1%2C129%3A1%2C130%3A1%2C131%3A1%2C133%3A1%2C134%3A1%2C135%3A1%2C136%3A1%2C137%3A1&AwaitingReconsent=false; _chartbeat2=.1557484090990.1557713169225.1001.S1zafCOkPc4t2pQ-D9by5sD3_rnb.3'}
        self.post_url = 'http://127.0.0.1:30008/crawler/article/transfer'
        self.filter_url = 'http://console.cc.clipclaps.tv/crawler/log'
        self.have_met = BloomFilter(max_elements=100000, error_rate=0.1)
        self.downloadPath = '/data/crawler'
        self.picPath = '/cnn_news/picture/'



    def run(self):
        news_dic ={ 'us':'https://cnnespanol.cnn.com/seccion/estados-unidos/',
                    'word':'https://cnnespanol.cnn.com/seccion/mundo/',
                    'entertainment':'https://cnnespanol.cnn.com/seccion/entretenimiento/',
                    'sport':'https://cnnespanol.cnn.com/seccion/deportes/',
                    'technology':'https://cnnespanol.cnn.com/seccion/tecnologia/',
                    'travel':'https://cnnespanol.cnn.com/seccion/viajes-y-turismo/',
                    'health':'https://cnnespanol.cnn.com/seccion/salud/' }

        for kw in news_dic:
            print('KeyWord:\n', kw)
            try:
                self.parsing_cnn_news_list(start_url=news_dic[kw])
            except :
                pass



    def parsing_cnn_news_list(self, start_url):
        time.sleep(random.uniform(1, 3))
        list_res = requests.get(url=start_url, headers=self.headers, cookies=self.cookies).text
        html = etree.HTML(list_res)
        thumbnail_img_list = html.xpath('//img[@class="image"]/@src')
        details_url_list = html.xpath('//h2[@class="news__title"]//a/@href')
        index = 1
        for i in range(len(details_url_list)):
            self.parsing_details_urls(details_url=details_url_list[i], thumbnail_img=thumbnail_img_list[i+index])
            index += 1


    def parsing_details_urls(self, details_url, thumbnail_img):
        result = self.filter_data(details_url=details_url)
        if result:
            print('Data already exists!')
        else:
            time.sleep(random.uniform(3, 5))
            details_res = requests.get(url=details_url, headers=self.headers, cookies=self.cookies).text
            html = etree.HTML(details_res)
            sourceUrl = details_url
            jobId = time.time()
            title = self.parsing_article_title(html=html)
            content = self.parsing_article_content(html=html)
            img = self.download_img(html=html, thumbnail_img=thumbnail_img)
            releaseTime = self.parsing_details_release_time(html=html)
            authorName = self.parsing_details_author_name(html=html)
            if img is None or img == '' or content is None or content == '':
                pass
            else:
                data = {'jobId': int(jobId), 'sourceUrl': sourceUrl, 'title': title, 'authorName': authorName,
                        'releaseTime': releaseTime, 'content': content, 'img': img}
                print('data:\n', data)
                self.save_data(data=data)


    def parsing_details_release_time(self, html):
        release = html.xpath('//time[@class="storyfull__time"]//text()')
        releaseTime = ''.join([i.replace("/n", '').strip() for i in release])
        if releaseTime == '' or releaseTime is None:
            releaseTime = ''.join(html.xpath('//time[@class="news__date"]/@datetime'))
        return releaseTime


    def parsing_details_author_name(self, html):
        author = html.xpath('//p[@class="storyfull__authors"]/a/@title')
        authorName = ''.join([i.replace("/n", '').strip() for i in author])
        if authorName == '' or authorName is None:
            authorName = ''.join(html.xpath('//span[@itemprop="author"]//span[@itemprop="name"]/text()')[0])
        return authorName


    def parsing_article_title(self, html):
        title = ''.join(html.xpath('//h1[@class="storyfull__title"]//text()'))
        if title == '' or title is None:
            title = ''.join(html.xpath('//h1[@class="news__title"]//text()')).strip()
        return title


    def parsing_article_content(self, html):
        content_list = html.xpath('//div[@class="news__excerpt"]//p//text()')
        content = '<p>'.join([i.replace("\n", '').strip() for i in content_list]).replace("<p><p>", '<p>')
        if content == '' or content is None:
            content_list = html.xpath('//div[@class="storyfull__body"]//p/text()')
            content = '<p>'.join([i.replace("\n", '').strip() for i in content_list]).replace("<p><p>", '<p>')
        return content


    def download_img(self, html, thumbnail_img):
        img_id = str(uuid.uuid4()).replace('-','')
        index = 1
        img_list = []
        pic_url_list = html.xpath('//div[@class="storyfull__body"]//img/@src')
        if pic_url_list == []:
            urllib.request.urlretrieve(thumbnail_img, r'%s.jpg' % (self.downloadPath + self.picPath + str(img_id) + "-" + str(index)))
            img = r'%s.jpg' % (self.picPath + str(img_id) + "-" + str(index))
            return img
        else:
            for pic_url in pic_url_list:
                if '.gif' in pic_url:
                    pass
                else:
                    urllib.request.urlretrieve(pic_url, r'%s.jpg' % (self.downloadPath + self.picPath + str(img_id) + "-" + str(index)))
                    img_list.append(r'%s.jpg' % (self.picPath + str(img_id) + "-" + str(index)))
                    index += 1
            img = ','.join(img_list)
            return img



    def filter_data(self, details_url):
        data1 = urllib.parse.urlencode({
            'type': int(5),
            'days': int(3),
        })
        data2 = data1.encode('utf-8')
        re = urllib.request.urlopen(url=self.filter_url, data=data2)
        status = re.read().decode('utf-8')
        result = json.loads(status)
        data = result['data']
        for kw in data:
            self.have_met.add(data[kw])
        if details_url in self.have_met:
            return True
        else:
            return False


    def save_data(self, data):
        data1 = urllib.parse.urlencode({
            'source': 6,
            'jobId': data['jobId'],
            'sourceUrl': data['sourceUrl'],
            'title': data['title'],
            'authorName': data['authorName'],
            'releaseTime': data['releaseTime'],
            'content': data['content'],
            'img': data['img'],
        })
        data2 = data1.encode('utf-8')
        re = urllib.request.urlopen(url=self.post_url, data=data2)
        status = re.read().decode('utf-8')
        print('status:\n', status)



if __name__ == '__main__':
    cnn = CNN_News()
    cnn.run()
