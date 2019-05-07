import time
from simdispider import settings as st





class Time_Limit(object):
    def __init__(self):
        self.old_time = {}
        self.limit_dict = { st.URL_NAME: st.URL_WAIT_LIMIT,
                            st.SAVE_NAME: st.SAVE_WAIT_LIMIT,
                            st.GET_NAME: st.GET_WAIT_LIMIT
                           }

    def judge_timeout(self, proname):
        if not self.old_time.get(proname):
            self.old_time[proname] = time.time()
        #print('[%s] 开始休眠时间是 %s '% (proname, self.old_time[proname]))
        #超时
        if time.time() - self.old_time[proname] > self.limit_dict[proname]:
            print('[%s]长时间休眠, 即将关闭......' % proname)
            return True

        return False

    #重置计时
    def reset_time(self, proname):

        if self.old_time.get(proname):
            self.old_time[proname] = 0
            return True
        return False


time_controler = Time_Limit()