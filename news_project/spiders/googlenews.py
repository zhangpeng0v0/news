from newsapi import NewsApiClient
from bs4 import BeautifulSoup as soup
import urllib.request
import ssl
import time
try:
    from news_project.newsfeeds import NewsFeeds
except:
    import sys
    sys.path.append('news_project')
    from newsfeeds import NewsFeeds


class GoogleNews():
    def __init__(self):
        self.news_api = NewsApiClient(api_key='cb7a4ae15a98429890aeedb9a7b460a0')
        self.key_word = ['Latest','World','U.S.','Business', 'Technology', 'Entertainment', 'Sports', 'Science', 'Health']
        self.t = time.time()
        self.point_time = time.strftime('%Y-%m-%d', time.localtime(self.t))
        self.google_crawler = 1


    def googleNews(self):

        if self.google_crawler == 1:
            # 从google新闻中获取热门新闻
            news_url = "https://news.google.com/news/rss"
            ssl._create_default_https_context = ssl._create_unverified_context
            Client = urllib.request.urlopen(news_url)
            xml_page = Client.read()
            Client.close()
            soup_page = soup(xml_page, "xml")
            news_list = soup_page.findAll("item")
            return news_list

        elif self.google_crawler == 2:
            # 返回 google-news 指定日期和分类的资讯
            today = self.point_time
            url_list = []
            for kw in self.key_word:
                all_articles = self.news_api.get_everything(q = kw,
                                                      sources = 'google-news',
                                                      domains = 'news.google.com',
                                                      from_param = today,
                                                      to = today[:-1]+str(int(today[-1])-1),
                                                      language = 'en',
                                                      sort_by = 'relevancy',
                                                      page_size = 100,)
                articles = all_articles['articles']
                for i in range(len(articles)):
                    url = articles[i]['url']
                    url_list.append(url)
            return url_list

        else:
            # 返回google-news的头条新闻
            top_headlines = self.news_api.get_top_headlines(
                                                        sources = 'google-news',
                                                        language='en',
                                                        page_size = 100,
                                                       )

            articles = top_headlines['articles']
            url_list=[]
            for i in range(len(articles)):
                url = articles[i]['url']
                url_list.append(url)
            return url_list







if __name__ == '__main__':
    g = GoogleNews()
    t = g.t
    today = g.point_time
    t2 = g.point_time
    print(today)
    print()


