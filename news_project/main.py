import time,re
from bloom_filter import BloomFilter
try:
    from news_project.newsfeeds import NewsFeeds
    from news_project.saveSqldb import SaveSqlDb
    from news_project.spiders.topbuzz import TopBuzz
    from news_project.spiders.newsbreak import NewsBreak
    from news_project.spiders.buzzfeed import BuzzFeed
    from news_project.spiders.googlenews import GoogleNews
    from news_project.spiders.smartNews import SmartNews
except:
    from newsfeeds import NewsFeeds
    from saveSqldb import SaveSqlDb
    from spiders.topbuzz import TopBuzz
    from spiders.newsbreak import NewsBreak
    from spiders.buzzfeed import BuzzFeed
    from spiders.googlenews import GoogleNews
    from spiders.smartNews import SmartNews



class Main():
    def __init__(self):
        self.have_met = BloomFilter(max_elements= 100000, error_rate= 0.1)
        self.t = time.time()
        self.point_time = time.strftime('%Y-%m-%d', time.localtime(self.t))
        self.post_DB = True


    def mainTopBuzz(self):
        n = NewsFeeds()
        s = SaveSqlDb()
        tb=TopBuzz()

        # 访问时间
        t = time.time()
        #正则匹配时间戳小数位
        result=re.findall('.\d*',str(t))
        sign=tb.hash_code(result[1][1:])
        timestamp=result[0]
        url_tb = 'https://i16-tb.isnssdk.com/api/844/stream?session_impr_id=0&tab=General&count=20&min_behot_time=1.554174097999E9&loc_mode=7&lac=4314&cid=6439033' \
              '&sign='+sign+ \
              '&timestamp='+timestamp+ \
              '&logo=topbuzz&gender=0&bv_is_auto_play=0&youtube=0&manifest_version_code=844&app_version=8.4.4&iid=6672646082571388678&gaid=54b268f4-52c2-470c-a815-abd1d00acce9&original_channel=gp&channel=gp&fp=TlTrJzK1FYsqFYs5PlU1LMGSL2Xr&device_type=MIX+2&language=en&app_version_minor=8.4.4.01&resolution=2030*1080&openudid=ab50caa43e995042&update_version_code=8440&sys_language=zh&sys_region=cn&os_api=26&tz_name=Asia%2FShanghai&tz_offset=28800&dpi=440&brand=Xiaomi&ac=WIFI&device_id=6672637176796333574&os=android&os_version=8.0.0&version_code=844&hevc_supported=1&device_brand=Xiaomi&device_platform=android&sim_region=cn&region=us&aid=1106&ui_language=en'
        news_list = tb.sendRequest(url= url_tb)
        path = '/data/crawler'
        pic_path = '/topbuzz/picture/'
        number = 1
        for url in news_list:
            if url not in self.have_met:
                self.have_met.add(url)
                data=n.parsingUrl(url= url, downloadPath= path, picPath= pic_path)
                if data is None:
                    pass
                else:
                    print('TB_detail_url\t', url)
                    print('TB_number\t', number)
                    number += 1
                    if data['releaseTime'] is None or data['releaseTime'] == '':
                        data['releaseTime'] = str(self.point_time)
                    if self.post_DB:
                        s.saveDB(data= data, source= 1)
                    else:
                        s.saveMySql(data = data)
            else:
                pass


    def mainNewsBreak(self):
        n = NewsFeeds()
        s = SaveSqlDb()
        nb = NewsBreak()
        url_nb = 'http://api.particlenews.com/Website/channel/news-list-for-best-channel?cstart=0&infinite=true&refresh=1&epoch=5&distribution=newsbreak&platform=1&cv=4.7.3&cend=10&appid=newsbreak&weather=true&fields=docid&fields=date&fields=image&fields=image_urls&fields=like&fields=source&fields=title&fields=url&fields=comment_count&fields=fb_share_total&fields=coach_mark_text&fields=up&fields=down&fields=summary&fields=favicon_id&fields=dominant_image&fields=contextMeta&fields=video_urls&fields=viewType&push_refresh=0&modularize=true&ts=2019-04-07+18%3A14%3A01+%2B0800&version=020025&net=wifi'
        docId = nb.parsingPost(url= url_nb)
        get_url = 'http://api.particlenews.com/Website/contents/content?related_docs=false&cv=4.7.3' \
                  '&docid=' + docId + \
                  '&appid=newsbreak&bottom_channels=false&distribution=newsbreak&platform=1&version=020025&net=wifi'
        news_list = nb.parsingGet(url= get_url)
        path = '/data/crawler'
        pic_path = '/newsbreak/picture/'
        number = 1
        for url in news_list:
            if url not in self.have_met:
                self.have_met.add(url)
                data=n.parsingUrl(url= url, downloadPath= path, picPath= pic_path)
                if data is None:
                    pass
                else:
                    print('NB_detail_url\t', url)
                    print('NB_number\t', number)
                    number += 1
                    if data['releaseTime'] is None or data['releaseTime'] == '':
                        data['releaseTime'] = str(self.point_time)
                    if self.post_DB:
                        s.saveDB(data= data, source= 2)
                    else:
                        s.saveMySql(data= data)
            else:
                pass


    def mainBuzzFeed(self):
        n = NewsFeeds()
        s = SaveSqlDb()
        bf =BuzzFeed()
        top_urls = bf.parsingTopUrl()
        news_urls = bf.parsingNewsUrl()
        urls_list = top_urls+news_urls
        path = '/data/crawler'
        pic_path = '/buzzfeed/picture/'
        number = 1
        for url in urls_list:
            if url not in self.have_met:
                self.have_met.add(url)
                data = n.parsingUrl(url= url, downloadPath= path, picPath= pic_path)
                if data is None:
                    pass
                else:
                    print('BF_detail_url\t', url)
                    print('BF_number\t', number)
                    number += 1
                    if data['releaseTime'] is None or data['releaseTime'] == '':
                        data['releaseTime'] = str(self.point_time)
                    if self.post_DB:
                        s.saveDB(data= data,source= 3)
                    else:
                        s.saveMySql(data= data)
            else:
                pass


    def mainGoogleNews(self):
        n = NewsFeeds()
        s = SaveSqlDb()
        gn = GoogleNews()
        news_list = gn.googleNews()
        path = '/data/crawler'
        pic_path = '/googleNews/picture/'
        number = 1
        for new in news_list:
            url = new.link.text
            if url not in self.have_met:
                data = n.parsingUrl(url= url, downloadPath= path, picPath= pic_path)
                if data is None:
                    pass
                else:
                    print('GN_detail_url\t', url)
                    print('GN_number\t', number)
                    number += 1
                    if data['releaseTime'] is None or data['releaseTime'] == '':
                        data['releaseTime'] = str(self.point_time)
                    if self.post_DB:
                        s.saveDB(data= data, source= 4)
                    else:
                        s.saveMySql(data= data)
            else:
                pass


    def mainSmartNews(self):
        n = NewsFeeds()
        s = SaveSqlDb()
        sm = SmartNews()
        news_list = sm.smartNews()
        path = '/data/crawler'
        pic_path = '/smartNews/picture/'
        number = 1
        for new in news_list:
            if new not in self.have_met:
                self.have_met.add(new)
                data = n.parsingUrl(url= new, downloadPath= path, picPath= pic_path)
                if data is None:
                    pass
                else:
                    print('SM_detail_url\t', new)
                    print('SM_number\t', number)
                    number += 1
                    if data['releaseTime'] is None or data['releaseTime'] == '':
                        data['releaseTime'] = str(self.point_time)
                    if self.post_DB:
                        s.saveDB(data = data, source = 5)
                    else:
                        s.saveMySql(data = data)
            else:
                pass





if __name__ == '__main__':
    m = Main()
    # m.mainTopBuzz()
    # m.mainNewsBreak()
    # m.mainBuzzFeed()
    # m.mainGoogleNews()
    m.mainSmartNews()

