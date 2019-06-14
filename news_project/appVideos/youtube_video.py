from pytube import YouTube
from pytube import Playlist
from bloom_filter import BloomFilter
import urllib.parse
import urllib.request
from youtube_user_pool import video_list_pool
import json, time



class Download_YouTuBe_Video():
    def __init__(self):
        self.post_video_url = 'http://127.0.0.1:30008/crawler/video/transfer'
        self.filter_url = 'http://console.cc.clipclaps.tv/crawler/log'
        self.have_met = BloomFilter(max_elements=100000, error_rate=0.1)
        self.downloadPath = '/Users/mr.zhang'
        self.videoPath = '/Desktop/picture/'


    def run(self):
        for author in video_list_pool:
            for video_list in video_list_pool[author]:
                self.parsing_youtube_list_page(video_list, author)



    def parsing_youtube_list_page(self, video_list, author):
        pl = Playlist(video_list)  # 下载用户视频列表
        playlist_url = pl.parse_links()  # 获取 playlist 中的视频网址
        for v in playlist_url:
            video_url = "https://www.youtube.com" + v
            data = self.parsing_details_video(details_url=video_url, author=author)
            print(data)
            self.save_video(data=data)


    def parsing_details_video(self, details_url, author):
        yt = YouTube(url = details_url)
        yt.streams.filter(subtype='mp4').all()
        if int(yt.length) < 360:
            status = self.filter_data(details_url=details_url)
            if status:
                pass
            else:
                jobId = time.time()
                sourceUrl = details_url
                authorName = author
                title = yt.title
                yt.streams.first().download(self.downloadPath + self.videoPath)
                video = '%s.mp4' % (self.videoPath + yt.title)
                return {'jobId': jobId, 'sourceUrl': sourceUrl, 'title': title, 'authorName': authorName, 'video': video}
        else:
            pass


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
            'video': data['video'],
        })
        data2 = data1.encode('utf-8')
        re = urllib.request.urlopen(url=self.post_video_url, data=data2)
        status = re.read().decode('utf-8')
        print('status:\n', status)




if __name__ == '__main__':
    ytb =Download_YouTuBe_Video()
    ytb.run()

