#! /usr/bin/env python3
import sys
import os,csv
from pathlib import Path
import math
import platform
import codecs
import shutil
from DB_test import Db_wildcat
from extract_data  import Stm32_data
import time

class Wildcat :
    def __init__(self):

        a=platform.system()
        if a == 'Windows':
           self.launcher='STM32_Programmer_CLI.exe'
           self.cube_programmer_path ='C:\\Programmer_Test_Platform\\STM32CubeProgrammer\\bin'
           self.flashing_file_path ='C:\\CubeProgrammer_Valid\\data_store\\'
           self.flashing_file ='C:\\CubeProgrammer_Valid\\data_store\\test_regression_sdcard_ev1.txt'
           self.tsv_file='C:\\Programmer_Test_Platform\\openstlinux_wildcat_FlashingBinary\\FlashLayout_sdcard_stm32mp157c-dk2-basic.tsv'
           self.archive="C:\\CubeProgrammer_Valid\\other test\\data_input_archive\\"

        elif a=='Linux':
           #flashing_file_path ='/local/home/brhoumam/mabrouk'
           #CSV_FILE ='/local/home/brhoumam/mabrouk'
           launcher='/STM32_Programmer_CLI'
           flashing_file_path ='/home/tunvqtvalidadm/STMicroelectronics/STM32Cube/FlashingTest'
           CSV_FILE ='/home/tunvqtvalidadm/STMicroelectronics/STM32Cube/FlashingTest'
           cube_programmer_path ='/home/tunvqtvalidadm/STMicroelectronics/STM32Cube/STM32CubeProgrammer/bin'
           flashing_file ='/home/tunvqtvalidadm/STMicroelectronics/STM32Cube/FlashingTest/test_regression_sdcard_ev1.txt'
           tsv_file='/home/tunvqtvalidadm/STMicroelectronics/STM32Cube/STM32CubeProgrammer/bin/data.tsv'

    def flashing_MPU(self):
        print("=====================================================")
        print("Please press reset to continue")
        print("=====================================================")
        #os.system("pause")
        print("Step 1\nflashing_MPU is ongoing\n")
        os.chdir(self.cube_programmer_path)
        CMD = self.launcher+' -c port=usb1 -d '+self.tsv_file +' >> ' +self.flashing_file
        os.system(CMD)
        print("End of flashing MPU\n")


    def extract_time_size_ID(self,ID=[],size=[],time=[]):
        print("Step 2\nextract_time_size_ID is ongoing\n")
        parametre =['Partition ID  : ','Size          :','Time elapsed during download operation: ']
        for item in parametre :
            with codecs.open(os.path.join(self.flashing_file_path, "test_regression_sdcard_ev1.txt"), "r") as file_object :
                 lines = file_object.read().split(item)
                 for item in lines :
                     item=item.split()
                     test_item=item[0].isdigit()
                     if test_item == True:
                         full_size = item[0]+' '+item[1]
                         size_MBit=self.size_conversion(full_size)
                         size.append(size_MBit)
                     elif test_item== False:
                         if item[0].find('x') == 1 :
                            ID.append(item[0])
                         elif item[0].find('.') != -1 :
                              my_time=item[0]
                              my_time_s=self.time_conversion(my_time,my_time_s=0)
                              time.append(my_time_s)
        """
        print('size=',size)
        print('ID=',ID)
        print('time=',time)
        print("END extract_time_size_ID ")
        """
        print(" End extract_time_size_ID is ongoing\n")
        return ID,size,time


    def time_conversion(self,my_time,my_time_s=0):
        unity=[3600,60,1,0.001]
        for i in range(0,len(my_time)-3,3):
            my_time_s+=int((my_time[i]+my_time[i+1]))*unity[i//3]
        my_time_s+=int(my_time[9:12])*unity[3]
        my_time_s=str(my_time_s)
        return my_time_s

    def size_conversion(self,full_size):
        unity=['Bytes','KBytes','MBytes']
        coef=['6','3','0']
        for i in range(len(unity)) :
            test=full_size.find(unity[i])
            if test != -1 :
                itemm=full_size[0:(test-1)]
                size_MBit=int(itemm)*8*(10**(-(int(coef[unity.index(unity[i])]))))
                size_MBit=str(size_MBit)
        return size_MBit

    def debit_calculation(self,size,time,Debit=[]):
        for i in range(len(size)):
            debit=round(float(size[i])/float(time[i]),4)
            debit=str(debit)
            Debit.append(debit)
        return Debit

    def wildcat_flashing_status(self):
        print("Step 3\n wildcat_flashing_status is ongoing\n")
        flashed_binary=[]
        Status_test=[]
        fail_msg=[]
        with open(self.flashing_file,'r') as data_analyse :
             data_analyse2=data_analyse.read().replace('\n','').split("Opening and parsing file:")
             #print(data_analyse2)

             for item in range(1,len(data_analyse2)) :
                 data_B=data_analyse2[item].split()
                 flashed_binary.append(data_B[0])
                 #print(data_B)
                 if "successfully" in data_analyse2[item] :
                     Status_test.append("PASS")
                     fail_msg.append("-")
                 elif "failed" or "Error" in data_analyse2[item] :
                     Status_test.append("FAIL")
                     msg_fail_extract=data_analyse2[item].split("error")
                     #print("msg_fail_extract==>",msg_fail_extract)
                     msg_fail_extract="error " +msg_fail_extract[1]
                     #print("msg_fail_extract==>",msg_fail_extract)
                     fail_msg.append(msg_fail_extract)

             print("End wildcat_flashing_status\n")
             return flashed_binary,Status_test,fail_msg
    """   
    print(Status_test)
    print('\n')
    print(type(flashed_binary))
    print("flashed_binary--->",flashed_binary)
    """

    """
    print('\n')
    
    for item in flashed_binary :
        print(item,'-->',Status_test[flashed_binary.index(item)],fail_msg[flashed_binary.index(item)],'\n')
    """



    def wildcat_status(self):
        if os.path.isfile(self.flashing_file):
            os.remove(self.flashing_file)
        else :
            pass
        wildcat_init=Wildcat()
        wildcat_init.flashing_MPU()
        ID,size,time=wildcat_init.extract_time_size_ID(ID=[],size=[],time=[])
        Debit=wildcat_init.debit_calculation(size,time,Debit=[])
        flashed_binary,Status_test,fail_msg=wildcat_init.wildcat_flashing_status()

        cubeprogrammer_release=Stm32_data().software_version_detect(RC="")
        data=Db_wildcat().show_data_table('distinct CubeProgrammer_Release','Wildcat_DB')
        counter=0
        for item in data:
           if cubeprogrammer_release in item:
              counter+=1
           else :
              pass
        if counter >0 :
           print("release found ")
        else :
           print("release not found ")
           Db_wildcat().add_data_Db_wildcat(size,ID,time,Debit,flashed_binary,Status_test,fail_msg)

        shutil.copy(self.flashing_file,self.archive)
        os.remove(self.flashing_file)

        print("a")
        return size,ID,time,Debit,flashed_binary,Status_test,fail_msg


def main():
    Wildcat().wildcat_status()



if __name__=='__main__' :
    main()












