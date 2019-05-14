import time
from simdispider import settings as st



class Log(object):
    def __init__(self):
        self.error_log = st.LOG_PATH + '%s_error.txt'% time.strftime('%Y_%m_%d')
        self.run_log = st.LOG_PATH + '%s_run.txt'% time.strftime('%Y_%m_%d')
        self.level_list = ['info', 'run', 'error']
        self.run_data = []
        self.error_data = []


    def write_log(self, level, data):
        if level in self.level_list:
            data = '[' + time.strftime('%m_%d_%H_%M_%S') + ']' + data
            if level == 'info':
                print(data)
            elif level == 'run':
                data = data + '\n'
                self.run_data.append(data)
                if len(self.run_data) > 10:
                    self.save(level)

            elif level == 'error':
                data = data + '\n'
                self.error_data.append(data)
                if len(self.error_data) > 5:
                    self.save(level)

        else:
            print('事件等级错误......')

    def save(self, level):
        if level == 'run':
            try:
                with open(self.run_log, 'a', encoding = 'utf-8') as f:
                    f.write(self.run_data)
                self.run_data = []
            except:
                pass

        elif level == 'error':
            try:
                with open(self.error_log, 'a', encoding = 'utf-8') as f:
                    f.write(self.error_data)

                self.error_data = []

            except:
                pass

    def save_all(self):
        if self.run_data:
            try:
                with open(self.run_log, 'a', encoding='utf-8') as f:
                    f.write(self.run_data)
                self.run_data = []
            except:
                print('运行日志保存失败......')

        if self.error_data:
            try:
                with open(self.error_log, 'a', encoding='utf-8') as f:
                    f.write(self.error_data)

                self.error_data = []
            except:
                print('错误日志保存失败......')



logger = Log()