import csv
import time
import os
from simdispider import settings
from simdispider.controler.log import logger


class DataSave(object):
    def __init__(self):
        self.filepath = settings.Download_Data_Path + '%s_file.csv'% (time.strftime('%m_%d_%H_%M', time.localtime()))
        self.data = []

    def save(self):
        with open(self.filepath, 'a', encoding = 'utf-8') as f:
            writer = csv.writer(f)
            try:
                for book_dict in self.data:
                    info_list = [v for k, v in book_dict.items()]
                    writer.writerow(info_list)
                logger.write_log(level = 'info', data = "文件存储完成......")
                self.data = []

            except Exception as e:
                data = '[' + settings.SAVE_NAME + ']' + e
                logger.write_log(level = 'error', data = data)

    def write_head(self):
        try:
            with open(self.filepath, 'w', encoding='utf-8') as f:
                writer = csv.writer(f)
                title = [k for k, v in self.data[0].items()]
                writer.writerow(title)
            logger.write_log(level = 'info', data = "写入表头成功......")
        except Exception as e :
            data = '[' + settings.SAVE_NAME + ']' + e
            logger.write_log(level = 'error', data = data)

    def write_data(self, data):
        if data:
            self.data = self.data + data
            if len(self.data) > 30:
                if not os.path.exists(self.filepath):
                    self.write_head()
                self.save()

data_controler = DataSave()