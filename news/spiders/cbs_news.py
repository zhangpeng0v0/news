import requests
from lxml import etree
import uuid, time, random
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



class CBS_News():
    def __init__(self):
        self.headers = {'user-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36'}
        self.cookies = {'cookies' : 'fly_device=desktop; fly_geo={"countryCode": "cn"}; CBS_INTERNAL=0; _cb_ls=1; _cb=DrObeWDJQRFdCPmQx1; optimizelyEndUserId=oeu1556274100628r0.4116041118910556; __gads=ID=d68306632b854d8c:T=1556274103:S=ALNI_MYpAOeaoN_TEKi9ErEphorJuu4FxA; aam_uuid=38178500434044041890375836043549172921; _v__chartbeat3=DSbaGWCHXxS0C6XCeZ; first_page_today=false; cbsnews_ad=%7B%22type%22%3A%22gpt%22%2C%22region%22%3A%22aw%22%2C%22session%22%3A%22a%22%2C%22subSession%22%3A%223%22%7D; AMCVS_10D31225525FF5790A490D4D%40AdobeOrg=1; s_cc=true; OX_plg=pm; fly_vid=1a29bea6-1a13-4100-a305-ffa9b02166d3; pmtimesig=[[1556347239934,0],[1556350240525,3000591],[1556372772902,22532377]]; s_vnum=1558866104445%26vn%3D10; s_invisit=true; s_lv_undefined_s=Less%20than%201%20day; AMCV_10D31225525FF5790A490D4D%40AdobeOrg=1406116232%7CMCMID%7C37954619966530193010387509759393309121%7CMCAAMLH-1557023341%7C11%7CMCAAMB-1557023341%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1556425741s%7CNONE%7CvVersion%7C2.5.0; trc_cookie_storage=taboola%2520global%253Auser-id%3Dbfc0c49d-bde0-4b78-9484-33cd8cb7509f-tuct3bdf4f1; AAMC_cbsi_0=REGION%7C11%7CAMSYNCSOP%7C%7CAMSYNCS%7C; _cb_svref=null; _t_tests=eyJMdFRUYmdVZHBDcHBKIjp7ImNob3NlblZhcmlhbnQiOiJCIiwic3BlY2lmaWNMb2NhdGlvbiI6WyJEZlhyTVYiXX0sImxpZnRfZXhwIjoibSJ9; cbsn_device=desktop; muxData=mux_viewer_id=a3de65c6-88bd-4042-a748-fb385d2ada3d&msn=0.5261598146217972&sid=11df9f3c-9e4d-47e4-9786-2de0583451e8&sst=1556418792060&sex=1556421954813; GED_PLAYLIST_ACTIVITY=W3sidSI6ImdDTUIiLCJ0c2wiOjE1NTY0MjA0NTUsIm52IjoxLCJ1cHQiOjE1NTY0MjAxNDIsImx0IjoxNTU2NDIwNDU1fV0.; s_sq=%5B%5BB%5D%5D; prevPageType=topic_list; prevPageName=cbsnews:/latest/us/5/; s_getNewRepeat=1556420875652-Repeat; s_lv_undefined=1556420875654; utag_main=v_id:016a592a36a1009f5e955a97097003079001807100bd0$_sn:10$_ss:0$_st:1556422675588$vapi_domain:cbsnews.com$dc_visit:10$_pn:38%3Bexp-session$ses_id:1556418538777%3Bexp-session$dc_event:30%3Bexp-session$dc_region:eu-central-1%3Bexp-session; _chartbeat2=.1556274100027.1556420876067.111.atSntCpXEouDM4RkLBcjI23BVm-lP.40; s_ptc=%2Flatest%2Fus%2F5%2F%5E%5E0.00%5E%5E0.01%5E%5E0.28%5E%5E0.52%5E%5E0.63%5E%5E0.44%5E%5E5.08%5E%5E0.01%5E%5E6.59; RT="sl=38&ss=1556418537489&tt=40674&obo=1&sh=1556420880100%3D38%3A1%3A40674%2C1556420718464%3D37%3A1%3A34088%2C1556420455825%3D36%3A1%3A31715%2C1556420142482%3D35%3A1%3A30988%2C1556420128526%3D34%3A1%3A30943&dm=cbsnews.com&si=91b57407-760b-481b-87e3-bcff31d166db&bcn=%2F%2F173e2514.akstat.io%2F&ld=1556420880100&r=https%3A%2F%2Fwww.cbsnews.com%2Flatest%2Fus%2F5%2F&ul=1556420983930"'}
        self.downloadPath = '/data/crawler'
        self.picPath = '/cbs_news/picture/'
        self.filter = Filter_Data()
        self.save = Save_Data()


    def run(self):
        pg = 1
        while pg < 4:
            health = 'https://www.cbsnews.com/latest/health/{}/'.format(pg)
            world = 'https://www.cbsnews.com/latest/world/{}/'.format(pg)
            crime = 'https://www.cbsnews.com/latest/crime/{}/'.format(pg)
            entertainment = 'https://www.cbsnews.com/latest/entertainment/{}/'.format(pg)
            science = 'https://www.cbsnews.com/latest/science/{}/'.format(pg)
            technology = 'https://www.cbsnews.com/latest/technology/{}/'.format(pg)

            cbs.parsing_health_news_list_page(start_url=health)
            cbs.parsing_word_news_list_page(start_url=world)
            cbs.parsing_crime_news_list_page(start_url=crime)
            cbs.parsing_entertainment_news_list_page(start_url=entertainment)
            cbs.parsing_science_news_list_page(start_url=science)
            cbs.parsing_technology_news_list_page(start_url=technology)
            pg += 1


    def parsing_health_news_list_page(self, start_url):
        res = requests.get(start_url, headers=self.headers, cookies=self.cookies).text
        time.sleep(random.uniform(3, 5))
        html = etree.HTML(res)
        list_page_url = html.xpath('//section[@id="component-health"]//div[@class="component__item-wrapper"]//article//a/@href')
        thumbnail_img = html.xpath('//section[@id="component-health"]//div[@class="component__item-wrapper"]//span[@class="img item__thumb item__thumb--crop-0"]//img/@src')
        for i in range(len(list_page_url)):
            data = self.parsing_details_page(details_url = list_page_url[i], thumbnail_img= thumbnail_img[i])
            if data is None :
                pass
            else:
                print('health_data\n', data)
                self.save.save_data(data=data, news='cbs')


    def parsing_word_news_list_page(self, start_url):
        res = requests.get(start_url, headers=self.headers, cookies=self.cookies).text
        time.sleep(random.uniform(3, 5))
        html = etree.HTML(res)
        list_page_url = html.xpath(
            '//section[@id="component-world"]//div[@class="component__item-wrapper"]//article//a/@href')
        thumbnail_img = html.xpath(
            '//section[@id="component-world"]//div[@class="component__item-wrapper"]//span[@class="img item__thumb item__thumb--crop-0"]//img/@src')
        for i in range(len(list_page_url)):
            data = self.parsing_details_page(details_url=list_page_url[i], thumbnail_img=thumbnail_img[i])
            if data is None:
                pass
            else:
                print('word_data\n', data)
                self.save.save_data(data=data, news='cbs')


    def parsing_crime_news_list_page(self, start_url):
        res = requests.get(start_url, headers=self.headers, cookies=self.cookies).text
        time.sleep(random.uniform(3, 5))
        html = etree.HTML(res)
        list_page_url = html.xpath('//section[@id="component-crime"]//div[@class="component__item-wrapper"]//article//a/@href')
        thumbnail_img = html.xpath('//section[@id="component-crime"]//div[@class="component__item-wrapper"]//span[@class="img item__thumb item__thumb--crop-0"]//img/@src')
        for i in range(len(list_page_url)):
            data = self.parsing_details_page(details_url=list_page_url[i], thumbnail_img=thumbnail_img[i])
            if data is None:
                pass
            else:
                print('crime_data\n', data)
                self.save.save_data(data=data, news='cbs')


    def parsing_entertainment_news_list_page(self, start_url):
        res = requests.get(start_url, headers=self.headers, cookies=self.cookies).text
        time.sleep(random.uniform(3, 5))
        html = etree.HTML(res)
        list_page_url = html.xpath(
            '//section[@id="component-entertainment"]//div[@class="component__item-wrapper"]//article//a/@href')
        thumbnail_img = html.xpath(
            '//section[@id="component-entertainment"]//div[@class="component__item-wrapper"]//span[@class="img item__thumb item__thumb--crop-0"]//img/@src')
        for i in range(len(list_page_url)):
            data = self.parsing_details_page(details_url=list_page_url[i], thumbnail_img=thumbnail_img[i])
            if data is None:
                pass
            else:
                print('entertainment_data\n', data)
                self.save.save_data(data=data, news='cbs')


    def parsing_science_news_list_page(self, start_url):
        res = requests.get(start_url, headers=self.headers, cookies=self.cookies).text
        time.sleep(random.uniform(3, 5))
        html = etree.HTML(res)
        list_page_url = html.xpath(
            '//section[@id="component-science"]//div[@class="component__item-wrapper"]//article//a/@href')
        thumbnail_img = html.xpath(
            '//section[@id="component-science"]//div[@class="component__item-wrapper"]//span[@class="img item__thumb item__thumb--crop-0"]//img/@src')
        for i in range(len(list_page_url)):
            data = self.parsing_details_page(details_url=list_page_url[i], thumbnail_img=thumbnail_img[i])
            if data is None:
                pass
            else:
                print('science_data\n', data)
                self.save.save_data(data=data, news='cbs')


    def parsing_technology_news_list_page(self, start_url):
        res = requests.get(start_url, headers=self.headers, cookies=self.cookies).text
        time.sleep(random.uniform(3, 5))
        html = etree.HTML(res)
        list_page_url = html.xpath(
            '//section[@id="component-technology"]//div[@class="component__item-wrapper"]//article//a/@href')
        thumbnail_img = html.xpath(
            '//section[@id="component-technology"]//div[@class="component__item-wrapper"]//span[@class="img item__thumb item__thumb--crop-0"]//img/@src')
        for i in range(len(list_page_url)):
            data = self.parsing_details_page(details_url=list_page_url[i], thumbnail_img=thumbnail_img[i])
            if data is None:
                pass
            else:
                print('technology_data\n', data)
                self.save.save_data(data=data, news='cbs')



    def parsing_details_page(self, details_url, thumbnail_img):
        result = self.filter.filter_data(details_url=details_url)
        if result:
            print('Data already exists!')
        else:
            details_res = requests.get(details_url, headers=self.headers, cookies= self.cookies).text
            time.sleep(random.uniform(1, 3))
            html = etree.HTML(details_res)
            source = int(7)
            sourceUrl = details_url
            jobId = time.time()
            title = ''.join(html.xpath('//h1[@class="content__title"]/text()'))
            text = fulltext(details_res).split('\n')
            txt = list(filter(lambda x: x.strip() != '', text))
            content = '<p>'.join(txt)
            author = html.xpath('//p[@class="content__meta content__meta-byline"]/text()')
            authorName = ''.join([i.replace("/n", '<p>').strip() for i in author])
            releaseTimeList = html.xpath('//p[@class="content__meta content__meta-timestamp"]/time/text()')
            releaseTime = ''.join([i.replace("/n", '<p>').strip() for i in releaseTimeList])
            pic_url_list = html.xpath('//span[@class="img embed__content"]//img/@src')
            img = self.download_pic(pic_url_list=pic_url_list, thumbnail_img=thumbnail_img)
            if img is None or img == '' or content is None or content == '' or title is None or title == '':
                pass
            else:
                return {'source': source,'jobId': int(jobId), 'sourceUrl': sourceUrl, 'title': title, 'authorName': authorName,
                        'releaseTime': releaseTime, 'content': content, 'img': img}


    def download_pic(self, pic_url_list, thumbnail_img):
        try:
            img_id = str(uuid.uuid4()).replace('-','')
            index = 1
            img_list = []
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
    cbs = CBS_News()
    cbs.run()

