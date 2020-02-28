# -*- coding: utf-8 -*-
import datetime
import os
import platform
import time
import pandas as pd
import tkinter as tk
from tkinter.filedialog import askopenfilename as askopn


class TrackedTime(object):

    def __init__(self, file_path=None):

        self.file_path = file_path
        self.columns = ('Overtime', 'Night shift', 'Vacation', 'Sickness', 'Sick Time', 'Day-off')
        self.user_specific_df = None
        self._df = None
        if not self.file_path:
            self.file_path = os.path.abspath('.')

    def dir_exist(self, _base_dir=None):
        if os.path.exists(_base_dir):
            return True
        else:
            return False

    def os_result_file_location_path(self, path=None):

        if path:
            if platform.system() == 'Windows':
                _path = ''.join(i + '\\' for i in path.split('\\')[:-1])
                _file_path = _path + 'Time_log\\'
                return _file_path
            elif platform.system() == 'Linux':
                _path = ''.join(i + '/' for i in path.split('/')[:-1])
                _file_path = _path + 'Time_log/'
                return _file_path
            else:
                raise OSError
        else:
            raise ValueError

    def crate_dir(self, _base_dir_name='Vimmi time log'):
        dir_name = str(datetime.date.today()) + '-' + _base_dir_name + '-' + str(time.time())
        _path = self.os_result_file_location_path(self.file_path)
        if not self.dir_exist(_base_dir=_path + dir_name):
            os.makedirs(_path + dir_name)
        return dir_name

    def read_file(self):
        try:
            if platform.system() == 'Windows':
                # df_fl = pd.read_csv(self.file_path + '\\timelog.csv', encoding='ISO-8859-1')
                df_fl = pd.read_csv(self.file_path, encoding='ISO-8859-1')
            elif platform.system() == 'Linux':
                # df_fl = pd.read_csv(self.file_path + '/timelog.csv', encoding='ISO-8859-1')
                df_fl = pd.read_csv(self.file_path, encoding='ISO-8859-1')
            else:
                raise OSError
            return df_fl
        except Exception as e:
            raise ValueError

    def file_columns_names(self):
        return self._df.columns

    def unique_user_names(self):
        return self._df['User'].unique()

    def total_time(self):
        return self.user_specific_df['Hours'].sum()

    def df_data_getter(self):
        list_of_df = []
        if isinstance(self.user_specific_df, pd.DataFrame) and isinstance(self.columns, tuple):
            for column in self.columns:
                if column in ['Overtime', 'Night shift']:
                    list_of_df.append(
                        self.user_specific_df[
                            self.user_specific_df[column] == 'Yes'
                        ]['Hours'].sum()
                    )
                elif column in ['Vacation', 'Sickness', 'Sick Time', 'Day-off']:
                    list_of_df.append(
                        self.user_specific_df[
                            self.user_specific_df['Issue'].str.contains(column, na=False)
                        ]['Hours'].sum()
                    )

            return list_of_df

        raise ValueError('Data-frame or columns have '
                         'invalid type! '
                         'DF: {0} '
                         'Columns: {1}'.format(type(self.user_specific_df),
                                               type(self.columns))
                         )

    def users_data(self):
        self._df = self.read_file()
        dir_name = self.crate_dir()
        user_names = self.unique_user_names()
        data = [self._df[self._df['User'] == str(name)] for name in user_names]
        df_all_user_time = []
        _path = self.os_result_file_location_path(self.file_path)
        # writer_df2 = pd.ExcelWriter(_path + dir_name + '/{0}.xlsx'.format('2 All_filtered_users_time_log'))
        for dat in data:
            self.user_specific_df = dat
            _sum = self.total_time()
            user_spec_time = self.df_data_getter()
            # _over_time, _night_shift, _vacation, _seek_time, _seekness, _day_off_time = self.df_data_getter()
            # _total = (_sum - _vacation - _seek_time - _seekness - _over_time - _night_shift - _day_off_time)
            _total = (_sum - sum(user_spec_time))
            _full_name = dat['User'].iloc[0].split(' ')
            df = [
                # dat['User'].iloc[0],
                _full_name[1],
                _full_name[0],
                _sum,
                _total,
            ] + user_spec_time
            dat.to_excel(_path + dir_name + '/{0}.xlsx'.format(dat['User'].iloc[0]),
                         sheet_name=dat['User'].iloc[0])
            df_all_user_time.append(df)

            # self.ordered_dataset(dat=dat, total=_total, dir_name=dir_name, path=_path, writer=writer_df2)

        # 'Full Name',
        col = ['Surname',
               'Name',
               'Total logged time', 'Normal time', 'Overtime', 'Night shift',
               # 'Production changes',
               'Sickness', 'Seek Time', 'Vacation', 'Day-off']
        df = pd.DataFrame.from_records(df_all_user_time, columns=col)
        df.sort_values(by='Surname', inplace=True)
        writer = pd.ExcelWriter(_path + dir_name + '/{0}.xlsx'.format('1 All_users_time_log'))
        df.to_excel(writer, 'Sheet1', index=False)
        writer.save()

        return _path + dir_name


def main_loop():

    window = tk.Tk()
    path = askopn()
    if path and path.endswith('.csv'):
        result = TrackedTime(file_path=path)
        result = result.users_data()
        message = 'JOB FINISH. Result folder is: {0}'.format(result)
        window_text = tk.Text(window, height=1, width=len(message))
        window_text.pack()
        window_text.insert(tk.END, message)
        tk.mainloop()
    else:
        message = 'Path not chosen or invalid file extension (mist be <filename>.csv)'
        width = len(message)
        window_text = tk.Text(window, height=1, width=width)
        window_text.pack()
        window_text.insert(tk.END, message)
        tk.mainloop()


if __name__ == '__main__':
    main_loop()