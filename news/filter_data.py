from bloom_filter import BloomFilter
import urllib.parse
import urllib.request
import json




class Filter_Data(object):
    '''
    对详情页文章摘要和url进行数据库去重，可以修改入库时间长短来选择去重时间范围大小
    '''
    def __init__(self):
        self.filter_url = 'http://console.cc.clipclaps.tv/crawler/log'
        self.have_met = BloomFilter(max_elements=100000, error_rate=0.1)


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


