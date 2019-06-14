import urllib.parse
import urllib.request
import time


class Save_Data(object):
    '''
    对数据进行入库，计数
    source：源的索引
    '''
    def __init__(self):
        self.post_url = 'http://127.0.0.1:30008/crawler/article/transfer'
        self.point_time = time.strftime('%Y-%m-%d:%H-%M', time.localtime(time.time()))
        self.counter = 0


    def save_data(self, data, news):
        if data is None or data == {}:
            pass
        else:
            self.counter += 1
            with open('logs/{}_log.txt'.format(news), 'w') as w:
                w.write(str(self.point_time) + '\t' + news + '\t' + str(self.counter) + '\n')
            data1 = urllib.parse.urlencode({
                'source': data['source'],
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

