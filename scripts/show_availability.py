import matplotlib.pyplot as plot
from datetime import date, datetime
import db_conn
import pandas as pd
from common_functions import *

logger = get_logger()

def show_current_availability_chart():
    '''
        Extracts latest data set from DB and represents the data in dashboard
    '''

    config_params_info = get_config_params_info()
    car_park_avail_tbl_name = config_params_info['tables']['car_park_availability']['table_name']
    car_park_info_tbl_name = config_params_info['tables']['car_park_information']['table_name']

    # DB connection definition
    db_conn_obj = db_conn.get_connection()
    get_latest_data_sql = f'''
select coalesce(ca.carpark_number, cp.address) as address_cum_car_park_number, 
        ca.total_free_lots, 
        ca.total_lots,
        ca.update_time
        from {car_park_avail_tbl_name} as ca 
        left join {car_park_info_tbl_name} as cp
        on ca.carpark_number = cp.carpark_number
where ca.update_time in (
select max(update_time) from {car_park_avail_tbl_name} );'''

    df = pd.read_sql(get_latest_data_sql, con = db_conn_obj)
    logger.info(f'Extracting latest parking availability data from table - {car_park_avail_tbl_name}')

    if df.empty : print('Data frame is empty, no records to display!!!!'); exit(1)

    dashboard_df = df
    dashboard_df['car_park_free_percent'] = (df['total_free_lots']/df['total_lots'])*100
    df_display = dashboard_df[['address_cum_car_park_number','car_park_free_percent']]

    # Displays the result data set in dashboard
    logger.info(f'Displaying latest parking availability dashboard!!')
    plot.bar(df_display['address_cum_car_park_number'], df_display['car_park_free_percent'])
    plot.xlabel("Car Park Number")
    plot.ylabel("Percent of Available Slots")
    plot.title(f'Current time: %s' % df.iloc[1]['update_time'] )
    plot.show()
    
if __name__ == '__main__': 
    logger.info(f'Preparing the latest parking availability dashboard!!')
    show_current_availability_chart()
