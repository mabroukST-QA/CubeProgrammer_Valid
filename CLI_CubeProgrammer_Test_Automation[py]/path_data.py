#! /usr/bin/env python3
import os
import platform
import getpass

"""
  This module provide neccessary path for multi-OS use

  It permits also to work  with .txt files where to save data to do needed treatment and .bin file to write data later .
  
"""

class Cubeprogrammer_Path :
    def __init__(self):
        self.available_platforme ={'Windows':"STM32_Programmer_CLI.exe",'Linux':"./STM32_Programmer_CLI",'Darwin':"./STM32_Programmer_CLI"}
        self.OS=platform.system()
        self.user_name=getpass.getuser()
        self.cube_programmer_path =' '
        self.launcher=' '


    def launcher_path(self):
        for item in self.available_platforme :
            if self.OS == item :
                if self.OS =='Windows' :
                    self.cube_programmer_path ='C:\\Programmer_Test_Platform\\STM32CubeProgrammer\\bin' #windows original path
                    #self.cube_programmer_path ='C:\\Programmer_Test_Platform\\old_release\\2.4.0-A1\\bin'
                    #self.cube_programmer_path ='C:\\CubeProgrammer_Valid\\release_test\\2.1.0\\bin' ## test path
                    #self.cube_programmer_path ='C:\\CubeProgrammer_Valid\\release_test\\2.0.0\\bin' ## test path
                    #self.cube_programmer_path ='C:\\CubeProgrammer_Valid\\release_test\\1.4.0\\bin' ## test path


                    self.data_saved1="C:\\CubeProgrammer_Valid\\data_store\\protocol_list.txt"
                    self.data_saved_mcu="C:\\CubeProgrammer_Valid\\data_store\\MCU_Name.txt"
                    self.data_saved_test="C:\\CubeProgrammer_Valid\\data_store\\data_test.txt"
                    self.data4="C:\\CubeProgrammer_Valid\\data_store\\data[1.5MB].bin"
                    self.data3="C:\\CubeProgrammer_Valid\\data_store\\data[1MB].bin" #'1 MBytes'
                    self.data1="C:\\CubeProgrammer_Valid\\data_store\\data[512KB].bin" #'512 KBytes'
                    self.data2="C:\\CubeProgrammer_Valid\\data_store\\data_test0.bin" #'2 MBytes'
                    self.data5="C:\\CubeProgrammer_Valid\\data_store\\data[128KB].bin" #'128 KBytes'
                    self.data6="C:\\CubeProgrammer_Valid\\data_store\\data[256KB].bin" #'256 KBytes'
                    
                elif self.OS == 'Linux' :
                    #print(self.user_name)
                    if self.user_name =='tunvqtvalidadm':
                        #print("hiiiiiiiiiiiiiii1")
                        #done on ubtunu_native 18.04
                        self.cube_programmer_path ='//home//tunvqtvalidadm//STMicroelectronics//STM32Cube//STM32CubeProgrammer//bin'
                        self.data_saved1='//home//tunvqtvalidadm//Desktop//mabrouk//CubeProgrammer_Test_Automation//data_store//protocol_list.txt'
                        self.data_saved_mcu='//home//tunvqtvalidadm//Desktop//mabrouk//CubeProgrammer_Test_Automation//data_store//MCU_Name.txt'
                        self.data_saved_test='//home//tunvqtvalidadm//Desktop//mabrouk//CubeProgrammer_Test_Automation//data_store//data_test.txt'
                        self.data4='//home//tunvqtvalidadm//Desktop//mabrouk//CubeProgrammer_Test_Automation//data_store//data[1.5MB].bin'
                        self.data3='//home//tunvqtvalidadm//Desktop//mabrouk//CubeProgrammer_Test_Automation//data_store//data[1MB].bin' #'1 MBytes'
                        self.data1='//home//tunvqtvalidadm//Desktop//mabrouk//CubeProgrammer_Test_Automation//data_store//data[512KB].bin' #'512 KBytes'
                        self.data2='//home//tunvqtvalidadm//Desktop//mabrouk//CubeProgrammer_Test_Automation//data_store//data_test0.bin' #'2 MBytes'
                        self.data5='//home//tunvqtvalidadm//Desktop//mabrouk//CubeProgrammer_Test_Automation//data_store//data[128KB].bin' #'128 KBytes'
                        self.data6='//home//tunvqtvalidadm//Desktop//mabrouk//CubeProgrammer_Test_Automation//data_store/data[256KB].bin' #'256 KBytes'
                    else:
                        #print("hiiiiiiiiiiiiiii222")
                        # done on ST_ubtunu
                        self.cube_programmer_path = '//local//home//' + self.user_name + '//STMicroelectronics//STM32Cube//STM32CubeProgrammer//bin'
                        self.data_saved1 = '//local//home//' + self.user_name + '//Desktop//mabrouk//CubeProgrammer_Test_Automation//data_store//protocol_list.txt'
                        self.data_saved_mcu = '//local//home//' + self.user_name + '//Desktop//mabrouk//CubeProgrammer_Test_Automation//data_store//MCU_Name.txt'
                        self.data_saved_test = '//local//home//' + self.user_name + '//Desktop//mabrouk//CubeProgrammer_Test_Automation//data_store//data_test.txt'
                        self.data4 = '//local//home//' + self.user_name + '//Desktop//mabrouk//CubeProgrammer_Test_Automation//data_store//data[1.5MB].bin'
                        self.data3 = '//local//home//' + self.user_name + '//Desktop//mabrouk//CubeProgrammer_Test_Automation//data_store//data[1MB].bin'  # '1 MBytes'
                        self.data1 = '//local//home//' + self.user_name + '//Desktop//mabrouk//CubeProgrammer_Test_Automation//data_store//data[512KB].bin'  # '512 KBytes'
                        self.data2 = '//local//home//' + self.user_name + '//Desktop//mabrouk//CubeProgrammer_Test_Automation//data_store//data_test0.bin'  # '2 MBytes'

                #/home/tunvqtvalidadm/STMicroelectronics/STM32Cube/STM32CubeProgrammer
                elif self.OS == 'Darwin' :
                    self.cube_programmer_path ='//Applications//STMicroelectronics//STM32Cube//STM32CubeProgrammer//STM32CubeProgrammer.app//Contents//MacOs//bin' #MAC
                    self.data_saved1="//Users//tunvqtvalidadm//Desktop//mabrouk//protocol_list.txt"
                    self.data_saved_mcu="//Users//tunvqtvalidadm//Desktop//mabrouk//MCU_Name.txt"
                    self.data_saved_test="//Users//tunvqtvalidadm//Desktop//mabrouk//data_test.txt"
                    self.data3="//Users//tunvqtvalidadm//Desktop//mabrouk//data_bin_test//data[1MB].bin" #'1 MBytes'
                    self.data1="//Users//tunvqtvalidadm//Desktop//mabrouk//data_bin_test//data.bin" #'512 KBytes'
                    self.data2="//Users//tunvqtvalidadm//Desktop//mabrouk//data_bin_test//data_test.bin" #'2 MBytes'
                else :
                    self.cube_programmer_path =input('please enter cubeprogrammer path:\t')
               
                os.chdir(self.cube_programmer_path)
                #print('cube_programmer_path--->',self.cube_programmer_path)
                self.launcher=self.available_platforme[item]
                #print('launcher-->',self.launcher)
           
        return self.cube_programmer_path,self.launcher,self.data_saved1,self.data_saved_mcu,self.data_saved_test,self.data3,self.data1,self.data2,self.data4,self.data5,self.data6
