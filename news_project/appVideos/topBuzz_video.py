import requests
from lxml import etree
import time ,json, uuid, re
import urllib.request
import urllib.parse
import hashlib ,random
from bloom_filter import BloomFilter



class TopBuzzVideo():
    def __init__(self):
        self.headers = {'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 8.0.0; MIX 2 MIUI/V10.2.2.0.ODECNXM) NewsArticle/8.4.4'}
        self.cookies = {'cookies': 'install_id=6672646082571388678; ttreq=1$a9ed7f4ce8fc84fced473d6e25c22226f381c13d; odin_tt=3e76568447d177856560d524c6ef5400407a437cfdd62767a36fb3b2decdeb01d43b9a7978232dc05c57af3c81bd10c277e78619093795e8392c1302c9aa8a75; sid_guard=c8f84a23bcce86b376964aeb42991709%7C1554173959%7C5184000%7CSat%2C+01-Jun-2019+02%3A59%3A19+GMT; uid_tt=2ad7176029f7302e11b7924e6e6566b7120075732cedcd39bc999fa5cbcf07a1; sid_tt=c8f84a23bcce86b376964aeb42991709; sessionid=c8f84a23bcce86b376964aeb42991709'}
        self.headers_details = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}
        self.cookies_details = {'Cookie': 'tt_webid=6683297640216282629; __tea_sdk__user_unique_id=6683297640216282629; __tea_sdk__ssid=40d2e59e-696c-4a93-ace8-e1479b10aeef; csrf-token=61575f8b568b577d9d06c777d103ae53e6c10723; csrf-secret=6qDUsFL6WZ1aG2soaPw7PpmCtnxCv7fw'}
        self.post_video_url = 'http://127.0.0.1:30008/crawler/video/transfer'
        self.filter_url = 'http://console.cc.clipclaps.tv/crawler/log'
        self.have_met = BloomFilter(max_elements=100000, error_rate=0.1)


    def run(self):
        number = 0
        while number < 5:
            t = time.time()
            result = re.findall('.\d*', str(t))   # 正则匹配时间戳小数位
            sign = tb.hash_code(result[1][1:])    # 对时间戳进行解密
            timestamp = result[0]
            start_url = 'https://i16-tb.isnssdk.com/api/844/stream?session_impr_id=0&tab=General&count=20&min_behot_time=1.554174097999E9&loc_mode=7&lac=4314&cid=6439033' \
                  '&sign=' + sign + \
                  '&timestamp=' + timestamp + \
                  '&logo=topbuzz&gender=0&bv_is_auto_play=0&youtube=0&manifest_version_code=844&app_version=8.4.4&iid=6672646082571388678&gaid=54b268f4-52c2-470c-a815-abd1d00acce9&original_channel=gp&channel=gp&fp=TlTrJzK1FYsqFYs5PlU1LMGSL2Xr&device_type=MIX+2&language=en&app_version_minor=8.4.4.01&resolution=2030*1080&openudid=ab50caa43e995042&update_version_code=8440&sys_language=zh&sys_region=cn&os_api=26&tz_name=Asia%2FShanghai&tz_offset=28800&dpi=440&brand=Xiaomi&ac=WIFI&device_id=6672637176796333574&os=android&os_version=8.0.0&version_code=844&hevc_supported=1&device_brand=Xiaomi&device_platform=android&sim_region=cn&region=us&aid=1106&ui_language=en'
            tb.analysis_topBuzz(start_url=start_url)
            number += 1
            time.sleep(random.uniform(60, 70))    # 每隔 1min 进行一次访问


    def hash_code(self, pwd):
        # 通过模块构造出一个hash对象
        h = hashlib.sha1()
        h.update(pwd.encode())
        # 获得字符串类型的加密后的密文
        return h.hexdigest()


    def analysis_topBuzz(self, start_url):
        try:
            res = requests.post(url=start_url, headers=self.headers, cookies=self.cookies).text
            time.sleep(random.uniform(1, 3))
            data = json.loads(res)
            item = data['data']['items']
            # 分析列表页，获得详情页url
            for i in range(len(item)):
                cls = item[i]['article_class']
                if cls == 'Video':
                    duration = item[i]['video']['duration']
                    if duration < 360:
                        share_url = item[i]['share_url']
                        video_url = item[i]['video']['url_list'][0]['urls'][0]
                        data = self.parsing_details_url(details_url=share_url, video_url=video_url)
                        print('analysis_topBuzz_data:\n', data)
                        self.save_video(data = data)
                    else:
                        pass
        except:
            pass


    def parsing_details_url(self, details_url=None, video_url=None):
        status = self.filter_data(details_url=details_url)
        if status:
            print('Data already exists!')
        else:
            time.sleep(random.uniform(0, 3))
            result = requests.get(url=details_url, headers=self.headers_details, cookies=self.cookies_details).text
            html = etree.HTML(result)
            # 调度任务
            jobId = time.time()
            # 文章标题
            title = html.xpath('//div[@class="title"]/text()')[0]
            # 作者
            authorName = ' '.join(html.xpath('//div[@class="name active"]/text()'))
            if authorName == '':
                authorName = ' '.join(html.xpath('//div[@class="name"]/text()'))
            # 文章发布时间
            releaseTime = ' '.join(html.xpath('//div[@class="publishTime"]/text()'))
            # 视频
            video = self.download_video(videoUrl=video_url)

            return {'jobId': jobId, 'sourceUrl': details_url, 'title': title, 'authorName': authorName,
                    'releaseTime': releaseTime, 'video': video}


    def download_video(self, videoUrl):
        videoId = str(uuid.uuid4()).replace('-','')
        downloadPath = '/data/crawler'
        videoPath = '/topbuzz/video/'
        urllib.request.urlretrieve(videoUrl, r'%s.mp4' % (downloadPath + videoPath + str(videoId)))
        video = '%s.mp4' % (videoPath + str(videoId))
        return video


    def filter_data(self, details_url):
        data1 = urllib.parse.urlencode({
                'type': int(4),
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


    def save_video(self, data):
        data1 = urllib.parse.urlencode({
            'source': 1,
            'sourceUrl': data['sourceUrl'],
            'title': data['title'],
            'authorName': data['authorName'],
            'releaseTime': data['releaseTime'],
            'video': data['video'],
        })
        data2 = data1.encode('utf-8')
        re = urllib.request.urlopen(url=self.post_video_url, data=data2)
        status = re.read().decode('utf-8')
        print('status:\n', status)


if __name__ == '__main__':
    tb = TopBuzzVideo()
    try:
        tb.run()
    except BaseException as e:
        print('run_error:\n', e)

