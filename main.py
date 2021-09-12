import math
import json
from datetime import datetime

  
def datetime_to_weekday(lags):
    date_list = [5,6,7,1,2,3,4]
    weekday =  date_list[int(lags%7)]
    return weekday

if __name__ == "__main__":
   
    data_json = open('input.json',)
    data = json.load(data_json)

    shift = data["shift"]
    roboRate = data["roboRate"]
    std_day = roboRate["standardDay"]
    std_night = roboRate["standardNight"]
    ext_day = roboRate["extraDay"]
    ext_night = roboRate["extraNight"]


    start_date , start_time = shift["start"].split("T")
    end_date , end_time = shift["end"].split("T")

    # rate
    std_day_charge = std_day["value"]
    std_night_charge = std_night["value"]
    spc_day_charge = ext_day["value"]
    spc_night_charge = ext_night["value"]

    # setup
    base_datetime = datetime( *[int(i) for i in "2038-01-01".split("-")])
    start_datetime = datetime( *[int(i) for i in start_date.split("-")])
    end_datetime = datetime( *[int(i) for i in end_date.split("-")])

    # lags
    
    start_lag = (start_datetime-base_datetime).days+5
    end_lag = (end_datetime-base_datetime).days+5
   

  
    # start weekday
    start_weekday = datetime_to_weekday(start_lag)
    end_weekday = datetime_to_weekday(end_lag)

    
    s_t = int(start_time[:2])
    s_t_minutes = int(start_time[3:5])
    s_t_seconds = int(start_time[-2:])
    s_t = s_t+s_t_minutes/60+s_t_seconds/3600

    e_t = int(end_time[:2])
    e_t_minutes = int(end_time[3:5])
    e_t_seconds = int(end_time[-2:])
    e_t = e_t+e_t_minutes/60+e_t_seconds/3600
 

    
    duration_lags = (end_datetime-start_datetime).days+start_lag+1

    s_day = start_lag

    value = 0
    hour_worked = 0
    remaining_flag = False
    i = 0
    remaining_time = 8
    next_day_flag = False
    over_worked_flag = False
    while True:
      
        # determine if need extra charge
        remaining_time = 8
        if remaining_flag:
            if int(s_t) == 23 or int(s_t) == 24:
                temp_st = s_t - 24
            else:
                temp_st = s_t
            remaining_time = min(8,e_t-temp_st)

        if next_day_flag:
            remaining_time = min(remaining_time ,24-s_t)
            next_day_flag = False

        if over_worked_flag:
            remaining_time = min(remaining_time ,8-hour_worked)
            over_worked_flag = False
       
        if s_day%7 == 6 or s_day%7 == 0:
            day_charge_rate = spc_day_charge
            night_charge_rate = spc_night_charge
        else:
            day_charge_rate = std_day_charge
            night_charge_rate = std_night_charge


        if s_t >= 7 and s_t < 23:
            hour_worked += min(23-s_t,remaining_time)
            value += min(23-s_t,remaining_time)*day_charge_rate*60
            s_t+=min(23-s_t,remaining_time)

        else:
            if int(s_t) == 23 or int(s_t) == 24:
                temp_st = s_t - 24
       
            else:
                temp_st = s_t
            
            hour_worked += min(7-temp_st,remaining_time)
            value += min(7-temp_st,remaining_time)*night_charge_rate*60
            s_t+=min(7-temp_st,remaining_time)

        
        
        if hour_worked != 0:
            over_worked_flag = True
        
        if remaining_flag and( s_t == e_t or s_t%24 == e_t or over_worked_flag):
            if (abs(e_t - s_t) < 1):
                break
      
        if hour_worked >= 8:
            s_t += 1
            
        # over_night
        if s_t >= 24:
            s_day+=1
        if s_t + 8 >= 24:
            next_day_flag = True

        s_t%=24
 
        hour_worked%=8
        

         # break logic
        if (s_day >= duration_lags-1 ) and s_t+9>e_t:
            remaining_flag = True
            
      
    
    print(int(value))
   