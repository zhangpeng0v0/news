import urllib.parse
import urllib.request
import time
import pymysql
try:
    from news_project.newsfeeds import NewsFeeds
except:
    from newsfeeds import NewsFeeds



class SaveSqlDb():
    def __init__(self):
        self.post_url = 'http://127.0.0.1:30008/crawler/article/transfer'

    # 数据入库 post请求
    def saveDB(self, data, source):
        try:
            if len(data['content']) > 500:
                data1 = urllib.parse.urlencode({
                    'source': source,
                    'sourceUrl': data['sourceUrl'],
                    'title': data['title'],
                    'authorName': data['authorName'],
                    'releaseTime': data['releaseTime'],
                    'content': data['content'],
                    'img': data['img'],
                    'jobId': data['jobId']
                })
                data2 = data1.encode('utf-8')
                re = urllib.request.urlopen(url= self.post_url, data= data2)
                re.read().decode('utf-8')
            else:
                pass

        except BaseException as e:
            NewsFeeds().point_log(str(NewsFeeds().localTime(time.time())), 'SavePostSql\t', str(e))


    # 测试本地 mysql 入库
    def saveMySql(self, data, tableName=None, host= 'localhost',port= 3306, user= 'root', password='zp920316', db= 'crawler', charset= 'utf8', *args):
        # mysql 入库
        conn = pymysql.Connect(host= host,
                               user= user,
                               password= password,
                               port= port,
                               database= db,
                               charset= charset)
        cursor = conn.cursor()
        try:
            sql = 'insert into news(sourceUrl,title,authorName,releaseTime,content,img) VALUES (%s,%s,%s,%s,%s,%s)'

            cursor.execute(sql, [data['sourceUrl'], data['title'], data['authorName'], data['releaseTime'], data['content'], data['img']])
            conn.commit()

        except BaseException as e:
            NewsFeeds().point_log(str(NewsFeeds().localTime(time.time())),'SaveMySql\t',str(e))




if __name__ == '__main__':
    s=SaveSqlDb()
    data ={'sourceUrl': 'https://www.yahoo.com/gma/capitol-hill-attorney-general-william-barr-set-focus-080258609--abc-news-topstories.html',
           'title': 'On Capitol Hill, Attorney General William Barr set to focus on DOJ funding, priorities as Mueller report looms',
           'authorName': 'Luke Barr',
           'releaseTime': '2019, 4, 9, 8, 2, 58',
           'content': 'On Capitol Hill, Attorney General William Barr set to focus on DOJ funding, priorities as Mueller report looms originally appeared on abcnews.go.com<p>Attorney General William Barr is set to testify in front of the House Appropriations Committee on Tuesday, and though lawmakers may want to press him on special counsel Robert Mueller\'s report on the federal probe of Russian interference in the 2016 presidential election, Barr\'s planning to focus his remarks on his budget priorities for the Justice Department, according to his prepared remarks.<p>His four top priorities are combating violent crime, improving immigration laws, fighting the illegal drug epidemic and protecting the homeland from national security threats, according to the remarks released Monday afternoon.<p>(MORE: Mueller report per Attorney General William Barr: Trump campaign did not conspire with Russia during 2016 election)<p>PHOTO: Attorney General William Barr takes part in the \'2019 Prison Reform Summit\' in the East Room of the White House in Washington, April 1, 2019. (Yuri Gripas/Reuters) More<p>The Justice Department is requesting $29.2 billion from the federal budget for the year ahead, about $2 billion more than was requested last year.<p>In his written statement, Barr praised the committee for the money already given to the Justice Department.<p>(MORE: Attorney General Barr says Mueller report won\'t be shared with White House for review, should be released \'mid-April\')<p>"In FY 2018, the Department prosecuted the greatest number of violent criminals in at least 25 years, thanks to the necessary resources provided by this Committee and Congress," he wrote.<p>Barr also outlined the need to secure the southern border and is requesting funds for more immigration judges. New federal statistics from U.S. Customs and Border Protection show an increase of apprehensions along the border over the past several months.<p>(MORE: Immigration backlog exceeds 700,000 cases and rising)<p>The attorney general\'s testimony on Tuesday comes days after Homeland Security Secretary Kristjen Nielsen resigned.<p>Democrats on the committee are expected to ask Barr about the nearly 400-page Mueller report, which was handed off to the Justice Department last month. Barr has said a redacted version of the report should be released by mid-April, if not sooner.',
           'img': '/topbuzz/picture/TB-0b38ec42-390d-46c3-b55a-c348c09e094e.jpg',
           }
    s.saveMySql(data= data)

