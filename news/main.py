try:
    from news.spiders.abc_news import ABC_News
    from news.spiders.ap_news import Associated_Press_News
    from news.spiders.bbc_news import BBC_News
    from news.spiders.buzzfeed_news import Buzz_Feed_News
    from news.spiders.cbs_news import CBS_News
    from news.spiders.fox_news import FOX_News
    from news.spiders.huffpost_news import HuffPost_News
    from news.spiders.looper_news import Looper_News
    from news.spiders.matador_network import Matador_Network
    from news.spiders.medium_news import Medium_News
    from news.spiders.nypost_news import New_York_Post_news
    from news.spiders.smart_news import Smart_News
    from news.spiders.topbuzz_news import TopBuzz_News
    from news.spiders.techcrunch import Techcrunch_News
except:
    import sys
    sys.path.append("/app/crawler/news_project/news/")
    from spiders.abc_news import ABC_News
    from spiders.ap_news import Associated_Press_News
    from spiders.bbc_news import BBC_News
    from spiders.buzzfeed_news import Buzz_Feed_News
    from spiders.cbs_news import CBS_News
    from spiders.fox_news import FOX_News
    from spiders.huffpost_news import HuffPost_News
    from spiders.looper_news import Looper_News
    from spiders.matador_network import Matador_Network
    from spiders.medium_news import Medium_News
    from spiders.nypost import New_York_Post_news
    from spiders.smart_news import Smart_News
    from spiders.topbuzz_news import TopBuzz_News
    from spiders.techcrunch import Techcrunch_News


import threading, multiprocessing


class Main():
    def __init__(self):
        '''
        开启三个进程，每个进程开启多个线程；
        根据脚本数量来添加或删减进程和线程
        '''
        pass

    def multi(self):
        p1 = multiprocessing.Process(target=self.thread_1()).start()
        p2 = multiprocessing.Process(target=self.thread_2()).start()
        p3 = multiprocessing.Process(target=self.thread_3()).start()
        p1.join()
        p2.join()
        p3.join()


    def thread_1(self):
        t1 = threading.Thread(target=ABC_News().run()).start()
        t2 = threading.Thread(target=Associated_Press_News().run()).start()
        t3 = threading.Thread(target=BBC_News().run()).start()
        t4 = threading.Thread(target=Buzz_Feed_News().run()).start()
        t5 = threading.Thread(target=Techcrunch_News().run()).start()
        t1.join()
        t2.join()
        t3.join()
        t4.join()
        t5.join()

    def thread_2(self):
        h1 = threading.Thread(target=CBS_News().run()).start()
        h2 = threading.Thread(target=FOX_News().run()).start()
        h3 = threading.Thread(target=HuffPost_News().run()).start()
        h4 = threading.Thread(target=Looper_News().run()).start()
        h1.join()
        h2.join()
        h3.join()
        h4.join()

    def thread_3(self):
        r1 = threading.Thread(target=Matador_Network().run()).start()
        r2 = threading.Thread(target=Medium_News().run()).start()
        r3 = threading.Thread(target=New_York_Post_news().run()).start()
        r4 = threading.Thread(target=Smart_News().run()).start()
        r5 = threading.Thread(target=TopBuzz_News().run()).start()
        r1.join()
        r2.join()
        r3.join()
        r4.join()
        r5.join()


if __name__ == '__main__':
    m = Main()
    m.multi()
