import uuid, time, random
from newspaper import Article
from newspaper import fulltext
from io import BytesIO
from PIL import Image
import requests
from bloom_filter import BloomFilter
import validators
import urllib.request



class NewsFeeds():
    def __init__(self):
        self.have_met = BloomFilter(max_elements= 100000, error_rate= 0.1)
        self.random_time = random.uniform(0,1)



    # 时间
    def localTime(self, t):
        # 断点时间
        point_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t))
        return point_time


    # 日志的输出函数
    def point_log(self, time, area, status):
        with open('log.txt', 'a') as w:
            w.write(time + '\t' + area + '\t' + status + '\n')


    # 获取图片尺寸，按要求下载
    def getPicSize(self, picUrls, downloadPath, picPath):
        img_id = uuid.uuid4()
        index = 1
        imgList = []
        # 利用 Validators.url 判断解析出来的url是否是正确的
        href_list = [href for href in picUrls  if validators.url(href) == True]
        for url in href_list:
            req = requests.get(url)
            im = Image.open(BytesIO(req.content))
            pic_path = '%s.jpg' % (picPath + str(img_id) + '-' + str(index))
            if im.size[0] > 50 and im.size[1]>50:
                urllib.request.urlretrieve(url,r'%s.jpg' % (downloadPath+picPath+str(img_id)+"-"+str(index)))
                imgList.append(pic_path)
                index += 1
        img = ','.join(imgList)
        return img


    # 新闻详情页解析
    def parsingUrl(self, url, downloadPath, picPath):
        time.sleep(self.random_time)
        try:
            # 源链接
            sourceUrl = url
            # 利用newspaper进行解析
            article = Article(url)
            article.download()
            # html页面
            html = article.html
            article.parse()
            # jobId
            jobId = time.time()
            # 标题
            title = article.title
            # 作者
            authorName = article.authors[0]
            # 发布时间
            releaseTime = article.publish_date
            # 文本内容
            text = fulltext(html).split('\n')
            txt = list(filter(lambda x: x.strip() != '', text))
            content = '<p>'.join(txt)
            # 多图
            picUrls = article.images
            img = self.getPicSize(picUrls, downloadPath, picPath)
            if img is None or img == '':
                pass

            return {'jobId': int(jobId), 'sourceUrl': sourceUrl, 'title': title, 'authorName': authorName,
                     'releaseTime': releaseTime, 'content': content, 'img': img}

        except BaseException as e:
            self.point_log(str(self.localTime(time.time())), 'NewsFeedsParsingUrl\t', str(e))



if __name__ == '__main__':

    url = 'https://www.cbsnews.com/news/john-havlicek-boston-celtics-star-has-died-at-79-cause-of-death-unknown-2019-04-26/'
    path = '/Users/mr.zhang'
    picPath = '/Desktop/picture/'
    n = NewsFeeds()
    data = n.parsingUrl(url=url, downloadPath=path, picPath=picPath)
    print('analysis_data\t', data)
