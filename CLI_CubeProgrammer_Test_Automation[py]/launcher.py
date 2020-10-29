#! /usr/bin/env python3

import xlsxwriter
import platform
import os

from data_operation import Op
from Wildcat_data import Wildcat

OS=platform.system()
if OS =='Windows':
    from extract_data  import Stm32_data
    timeout='timeout /t 1 /nobreak '

elif OS =='Linux':
    from extract_data_UBUNTU  import Stm32_data
    timeout="timeout 1s bash "





def main():
    # used_action=['connect','reset','write','erase','read_out_protection','remove_data_protection','reset']
    # action_time=[]
    # for action in used_action:
    #     used_command,datetime_all_action_board=Op(command="swd_v2",action=action,show=True).launch()
    #     action_time.append(datetime_all_action_board)
    # print(action_time)
    # full_time_action_B1=action_time[0][0]+action_time[1][0]+action_time[2][0]+action_time[3][0]+action_time[4][0]
    # print(full_time_action_B1)



        #launch wildcat script fro here
    Op().data_test_report()


        #launch wildcat script fro here
    #Wildcat().wildcat_status()


    #Op().data_analyse()
    #Stm32_data().software_version_detect()




if __name__=='__main__' :
    main()
