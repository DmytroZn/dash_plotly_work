from pandas import DataFrame as df
import json
import pandas as pd


class GetDF:
    """
    Class can give DataFrame with date start and end.
    And with for each zones.
    GetDF('2019-08-08 11:04:28', '2019-10-31 16:23:15').controller(5).
    """
    
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date

    """Open main data frame"""
    def open_main(self):
        with open('my_json.json', 'r') as f:
            json_list = json.load(f)
        df_data = df(json_list)
        df_data['time_row'] = df_data['zdate'].astype(str) + ' ' + df_data['ztime'].astype(str)
        df_data.drop(['ztime', 't_task', 'zdate', 'base_id', 'controllers', 'sum_capacity', 'sum_capacity_warm', 'sum_w_accumulate', 'sum_w_current', 'sum_capacity_current'], axis=1, inplace=True)
        return df_data

    """Open controllers data frame"""
    def open_controllers(self):
        with open('single_json.json', 'r') as f:
            json_list_2 = json.load(f)
        df_controllers = df(json_list_2)
        df_controllers.drop(['t_delta', 'auto_hand', 'digital_input', 'digital_output', 'id'], axis=1, inplace=True)
        df_controllers.rename(columns={'id_zone':'id'}, inplace=True)
        return df_controllers
    
    """Get data throw dates"""
    def get_from_date(self):
        data_f = self.open_main()
        data_search = data_f['time_row'].map(lambda x: self.start_date <= x <= self.end_date)
        data_f = data_f[data_search]

        return data_f
    
    """Get all date with all controllers"""
    def get_final_data(self):
        main_data = self.get_from_date()
        data_controllers = self.open_controllers()
        res = pd.merge(main_data, data_controllers, on=['id', 'id'], how='inner')
        return res

    """Can get only for one controller"""
    def controller(self, num):
        self.num = num
        final_data = self.get_final_data()
        controller_num = final_data.set_index('time_row')
        controller_num = controller_num[controller_num['number_of_controller'] == self.num]
        return controller_num
     

cre = GetDF('2019-08-08 11:04:28', '2019-10-31 16:23:15')
a = cre.controller(1)
# print(a)
