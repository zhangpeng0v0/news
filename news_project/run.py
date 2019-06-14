import time, random
try:
    from news_project.main import Main
except:
    from main import Main


class RunMain():
    def __init__(self):
        self.runData = True
    def runMain(self):
        if self.runData:
            num = 0
            run = RunData()
            while num < 10:
                run.run_topBuzz()
                run.run_newsBreak()
                num += 1
                time.sleep(random.uniform(1, 1.3))
            run.run_buzzFeed()
            run.run_googleNews()
            run.run_smartNews()



class RunData():
    def __init__(self):
        self.m = Main()

    def run_topBuzz(self):
        try:
            self.m.mainTopBuzz()
        except BaseException as a:
            print('run_TB_error\t', a)

    def run_newsBreak(self):
        try:
            self.m.mainNewsBreak()
        except BaseException as b:
            print('run_NB_error\t', b)

    def run_buzzFeed(self):
        try:
            self.m.mainBuzzFeed()
        except BaseException as c:
            print('run_BF_error\t', c)

    def run_googleNews(self):
        try:
            self.m.mainGoogleNews()
        except BaseException as d:
            print('run_GN_error\t', d)

    def run_smartNews(self):
        try:
            self.m.mainSmartNews()
        except BaseException as f:
            print('run_SM_error\t', f)





if __name__ == '__main__':
    rm = RunMain()
    rm.runMain()

