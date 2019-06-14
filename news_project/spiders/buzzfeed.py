import requests
from lxml import etree
import time, json
try:
    from news_project.newsfeeds import NewsFeeds
except:
    from newsfeeds import NewsFeeds



class BuzzFeed():
    def __init__(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        }
        self.cookies = {
            'cookie': '_ga=GA1.2.980887030.1554094864; __qca=P0-370898470-1554094864412; permutive-id=4b0388f5-cd06-48fb-bc43-3bd5b284a15f; __gads=ID=7ed4ac47516d0c08:T=1554094874:S=ALNI_Mb5hT5yTksr6ehByJBrLYY7lWInBA; _fbp=fb.1.1554094878563.234463870; ads_amazon_tam=on; ads_amazon_tam_version=1; ads_ad_lightning=on; ads_ad_lightning_version=1; ads_prebid=on; ads_prebid_version=1; ADSGROUP-699-outbrain-redux=control; ADSGROUP-699-outbrain-redux_version=2; ad_exchange_vox_concert=inline; ad_exchange_vox_concert_version=3; ads_scroll_subscription=on; ads_scroll_subscription_version=1; advertise_international=on; advertise_international_version=1; moat_dfp_native_video_tracking=on; moat_dfp_native_video_tracking_version=1; ADSGROUP-442-permutive=on; ADSGROUP-442-permutive_version=1; non_us_ad_lookahead_adjustments=on; non_us_ad_lookahead_adjustments_version=1; ads_adrizer=on; ads_adrizer_version=1; ADSGROUP-1015_awareness_billboard=billboard; ADSGROUP-1015_awareness_billboard_version=1; _cmpQcif3pcsupported=1; _gid=GA1.2.1718839625.1554714335; ads_inline_density_bfnews=density-250; ads_inline_density_bfnews_version=2; bfn_recirc_popup=control; bfn_recirc_popup_version=1; ad_display_card_sticky=control; ad_display_card_sticky_version=2; bfn_newsletter_popup=on; bfn_newsletter_popup_version=1; bfn_support_text=role; bfn_support_text_version=1; bf_nb_pp_dismissed=true; _pdfps=%5B7684%2C13160%2C13164%2C13730%2C10915%2C12448%2C12449%2C12882%2C13675%2C12244%2C14140%2C14192%2C10222%2C10788%2C10216%2C13098%2C13162%2C13276%2C13319%2C14110%2C14144%2C%2212244-15-22969%22%2C%2212244-15-22970%22%2C%2213458-15-22969%22%2C%2213458-15-22970%22%2C%2213459-15-22969%22%2C%2213459-15-22970%22%2C%2213524-2-294%22%2C%2214140-2-6723%22%2C%2214147-2-292%22%2C%2214351-15-22835%22%5D; _gat=1; sailthru_pageviews=12; permutive-session=%7B%22session_id%22%3A%22c440b2b2-d5b2-47da-a80a-a915417b28f6%22%2C%22last_updated%22%3A%222019-04-08T09%3A19%3A31.428Z%22%7D; sailthru_content=4aabfd73798a801ca4c9a396b30365ca5e49765b4283840f5c8259960590061f65292542d9dc5ee7cb5545f027fdd2b1f044956926b209e90497a64953e290f7; sailthru_visitor=6e0b676a-cfc5-4a77-bd49-98f70afc486f'
        }


    def parsingNewsUrl(self):
        try:
            pg = 1
            urls_news = []
            while pg < 6:
                new_url = 'https://www.buzzfeednews.com/us/feed/home?page=' + str(pg) + '&flexpro_enabled=1'
                res = requests.get(url=new_url, headers=self.headers, cookies=self.cookies).text
                html = etree.HTML(res)
                url_list = html.xpath('//div[@class="news-feed grid-layout-main"]//article/a/@href')
                urls_news += url_list
                pg += 1
            return urls_news
        except BaseException as e:
            NewsFeeds().point_log(str(NewsFeeds().localTime(time.time())), 'BuzzFeedParsingNewsUrl]\t', str(e))

    def parsingTopUrl(self):
        try:
            pg = 1
            urls_tops = []
            while pg <6:
                top_url = 'https://www.buzzfeed.com/site-component/v1/en-us/morebuzz?page='+str(pg)+'&page_size=15&image_crop=wide'
                res = requests.get(url=top_url, headers=self.headers, cookies=self.cookies).text
                data = json.loads(res)
                results = data['results']
                for i in range(len(results)):
                    res_url = results[i]['url']
                    if res_url is None or res_url == '':
                        pass
                    urls_tops.append(res_url)
                pg += 1
            return urls_tops
        except BaseException as e:
            NewsFeeds().point_log(str(NewsFeeds().localTime(time.time())), 'BuzzFeedParsingTopUrl]\t', str(e))

    def parsingHome(self):
        try:
            pg = 1
            urls_homes = []
            while pg < 6:
                home_url = 'https://www.buzzfeed.com/us/feedpage/feed/home?page='+str(pg)+'&page_name=home'
                res = requests.get(url=home_url, headers=self.headers, cookies=self.cookies).text
                html = etree.HTML(res)
                urls_list = html.xpath('//a[@class="js-card__link link-gray"]/@href')
                urls_homes += urls_list
                pg += 1
            return urls_homes
        except BaseException as e:
            NewsFeeds().point_log(str(NewsFeeds().localTime(time.time())), 'BuzzFeedParsingHomeUrl]\t', str(e))

    def parsingQuizzes(self):
        try:
            pg = 1
            urls_quizzes = []
            while pg < 6:
                quizzes_url = 'https://www.buzzfeed.com/us/feedpage/feed/quizzes?page='+str(pg)+'&page_name=quizzes'
                res = requests.get(url=quizzes_url, headers=self.headers, cookies=self.cookies).text
                html = etree.HTML(res)
                urls_list = html.xpath('//a[@class="js-card__link link-gray"]/@href')
                urls_quizzes += urls_list
                pg += 1
            return urls_quizzes
        except BaseException as e:
            NewsFeeds().point_log(str(NewsFeeds().localTime(time.time())), 'BuzzFeedParsingQuizzesUrl]\t', str(e))

    def parsingShopping(self):
        try:
            pg = 1
            urls_shopping = []
            while pg < 6:
                shopping_url = 'https://www.buzzfeed.com/us/feedpage/feed/shopping?page='+str(pg)+'&page_name=shopping'
                res = requests.get(url=shopping_url, headers=self.headers, cookies=self.cookies).text
                html = etree.HTML(res)
                urls_list = html.xpath('//a[@class="js-card__link link-gray"]/@href')
                urls_shopping += urls_list
                pg += 1
            return urls_shopping
        except BaseException as e:
            NewsFeeds().point_log(str(NewsFeeds().localTime(time.time())), 'BuzzFeedParsingShoppingUrl]\t', str(e))





if __name__ == '__main__':

    bz = BuzzFeed()
    # a=bz.parsingShopping()
    # bz.parsingNewsUrl()
    # a=bz.parsingTopUrl()
    a = bz.parsingHome()
    print(a)