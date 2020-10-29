#! /usr/bin/env python3
import sys
import os
import platform
from path_data import Cubeprogrammer_Path
    
class Stm32_data :
    def __init__(self):     
        self.CMD=''
        self.stlink_SN_list=[]
        self.stlink_V_list=[]
        self.probe_index_list=[]
        self.MCU_Name_list=[]
        self.stlink_V2_list=[]
        self.stlink_SN_V2_list=[]
        self.stlink_V3_list=[]
        self.stlink_SN_V3_list=[]
        self.MCU_Name_list_V3=[]
        self.UART_PORT=[]
        self.USB_PORT=[]
        self.all_mcu=[]
        self.MCU_flash_size_V2=[]
        self.MCU_flash_size_V3=[]
        self.MCU_flash_size=[]
        self.UART_PORT_V2=[]
        self.UART_PORT_V3_I=[]
        self.UART_PORT_V3_E=[]
        self.all_SN=[]

        self.MCU_Name_list_UART=[]
        #st_ubuntu
        ##self.data_saved_port="//local//home//brhoumam//Desktop//mabrouk//CubeProgrammer_Test_Automation//data_store//data_port.txt"
        #st_native
        self.data_port= "//home//tunvqtvalidadm//Desktop//mabrouk//CubeProgrammer_Test_Automation//data_store//data_port.txt"


    def available_stlink_data(self,protocol):
         cubeprogrammer_path=Cubeprogrammer_Path()
         cube_programmer_path,launcher,self.data_saved1,self.data_saved_mcu,self.data_saved_test,self.data3,self.data1,self.data2,self.data4=cubeprogrammer_path.launcher_path()
         os.chdir(cube_programmer_path)
         #print(launcher)
         self.CMD+=launcher
         self.CMD+=' -l'
         self.CMD+='>>'
         self.CMD+=self.data_saved1
         os.system(self.CMD)
         self.CMD=' '
         if protocol =='swd':
             with open(self.data_saved1,'r') as self.data_saved2 :
                 self.data_saved2=self.data_saved2.read()
                 self.data_saved2=self.data_saved2.replace('\n',' ')
                 self.data_saved2=self.data_saved2.split('ST-Link Probe ')
                 for item in self.data_saved2 :
                     self.data_saved2=item.split()
                     #print(self.data_saved2)
                     if self.data_saved2[4] =='SN':
                         self.stlink_SN_list.append(self.data_saved2[6])
                         self.stlink_V_list.append(self.data_saved2[11])
                         self.probe_index_list.append(self.data_saved2[0])

                 #print('stlink_list-->',self.stlink_SN_list) #extract stlink SN
                 #print('stlink_V_list-->',self.stlink_V_list) #extract stlink SN
                 #print('probe_index_list-->',self.probe_index_list) #extract stlink SN
             os.remove(self.data_saved1)
             return self.stlink_SN_list,self.stlink_V_list,self.probe_index_list

         elif protocol =='UART' :
             with open(self.data_saved1,'r') as self.data_saved3 :
                 self.data_saved3=self.data_saved3.read()
                 self.data_saved3=self.data_saved3.replace('\n',' ')
                 self.data_saved3=self.data_saved3.split('Port:')
                 for item in self.data_saved3 :
                     data_splited=item.split()
                     #print(data_splited)
                     if data_splited[4]== 'STM32' :
                           self.UART_PORT.append(data_splited[0])
                     elif data_splited[4]== 'STLINK-V3' :
                           self.UART_PORT.append(data_splited[0])
             os.remove(self.data_saved1)
             #print(self.UART_PORT)
             return self.UART_PORT

         elif protocol =='usb' :
              with open(self.data_saved1,'r') as self.data_saved4 :
                 self.data_saved4=self.data_saved4.read()
                 self.data_saved4=self.data_saved4.replace('\n',' ')
                 self.data_saved4=self.data_saved4.split('Device Index           :')
              #   print('first---->',self.data_saved4)
                 for item in self.data_saved4 :
                     self.data_saved4=item.split()
               #      print(self.data_saved4)
                     if self.data_saved4[2]=='USB' :
                         self.USB_PORT.append(self.data_saved4[0])

              os.remove(self.data_saved1)
              #print(self.USB_PORT)
              return self.USB_PORT

    def MCU_name_extract(self):
        while True :
            try:
                cubeprogrammer_path=Cubeprogrammer_Path()
                cube_programmer_path,launcher,self.data_saved1,self.data_saved_mcu,self.data_saved_test,self.data3,self.data1,self.data2,self.data4=cubeprogrammer_path.launcher_path()
                os.chdir(cube_programmer_path)
                stm32_data=Stm32_data()
                stlink_SN_list,stlink_V_list,probe_index_list=stm32_data.available_stlink_data('swd')
                UART_PORT=stm32_data.available_stlink_data('UART')

                #print('stlink_V_list------>',stlink_V_list)
                #print('stlink_SN_list-------->',stlink_SN_list)
                #print('\n')

                for i in range(len(stlink_V_list)) :
                    if 'V2' in stlink_V_list[i] :
                        #print(stlink_SN_list[i])
                        self.stlink_V2_list.append(stlink_V_list[i])
                        self.stlink_SN_V2_list.append(stlink_SN_list[i])
                        self.UART_PORT_V2.append(UART_PORT[i])

                        self.CMD+=launcher
                        self.CMD+=' -c port=swd SN='+stlink_SN_list[i]
                        self.CMD+=' >> '
                        self.CMD+=self.data_saved_mcu ###
                        os.system(self.CMD)
                        #print(self.CMD)
                        self.CMD=' '
                        with open(self.data_saved_mcu,'r') as self.data_saved_mcuname :
                            self.data_saved_mcuname=self.data_saved_mcuname.read()
                            self.data_saved_mcuname=self.data_saved_mcuname.replace('\n',' ')
                            self.data_saved_mcuname=self.data_saved_mcuname.split('Device name :')
                            #print(self.data_saved_mcuname)
                            data_B=self.data_saved_mcuname[1].split()
                            MCU_name=data_B[0]
                            #print(MCU_name)
                            self.MCU_Name_list.append(MCU_name)


                        with open(self.data_saved_mcu,'r') as self.data_saved_mcuname :
                            self.data_saved_mcuname=self.data_saved_mcuname.read()
                            self.data_saved_mcuname=self.data_saved_mcuname.replace('\n',' ')
                            self.data_saved_mcuname=self.data_saved_mcuname.split('Flash size  :')
                            self.data_saved_mcuname=self.data_saved_mcuname[1].split(' ')
                            MCU_flash_size=self.data_saved_mcuname[1]+' '+self.data_saved_mcuname[2]
                            self.MCU_flash_size_V2.append(MCU_flash_size)
                            #print(self.MCU_flash_size_V2)


                            #added to ckeck memory size : not mandatory

                            #MCU_flash_size=self.data_saved_mcuname[0]+' '+self.data_saved_mcuname[1]
                            #print(MCU_flash_size)
                        #print('MCU_flash_size_V2-->',self.MCU_flash_size_V2)
                        os.remove(self.data_saved_mcu)


                    elif 'V3' in stlink_V_list[i] and len(stlink_V_list[i])==6:
                        #print(stlink_SN_list[i])
                        self.stlink_V3_list.append(stlink_V_list[i])
                        self.stlink_SN_V3_list.append(stlink_SN_list[i])
                        self.UART_PORT_V3_I.append(UART_PORT[i])


                        self.CMD+=launcher
                        self.CMD+=' -c port=swd SN='+stlink_SN_list[i]
                        self.CMD+=' >> '
                        self.CMD+=self.data_saved_mcu ###
                        os.system(self.CMD)
                        #print(self.CMD)
                        self.CMD=' '

                        with open(self.data_saved_mcu,'r') as self.data_saved_mcuname :
                            self.data_saved_mcuname=self.data_saved_mcuname.read()
                            self.data_saved_mcuname=self.data_saved_mcuname.replace('\n',' ')
                            self.data_saved_mcuname=self.data_saved_mcuname.split('Device name :')
                            #print(self.data_saved_mcuname)
                            data_B=self.data_saved_mcuname[1].split()
                            #print(data_B)
                            MCU_name=data_B[0]+'(V3-integrated probe)'
                            #print(MCU_name)
                            self.MCU_Name_list_V3.append(MCU_name)
                            #print(self.MCU_Name_list_V3)


                        with open(self.data_saved_mcu,'r') as self.data_saved_mcuname :
                            self.data_saved_mcuname=self.data_saved_mcuname.read()
                            self.data_saved_mcuname=self.data_saved_mcuname.replace('\n',' ')
                            self.data_saved_mcuname=self.data_saved_mcuname.split('Flash size  :')
                            self.data_saved_mcuname=self.data_saved_mcuname[1].split(' ')
                            MCU_flash_size=self.data_saved_mcuname[1]+' '+self.data_saved_mcuname[2]
                            self.MCU_flash_size_V3.append(MCU_flash_size)


                            #print(self.MCU_flash_size_V3)

                        os.remove(self.data_saved_mcu)

                    #under test
                    elif 'V3' in stlink_V_list[i] and len(stlink_V_list[i])>6:
                        while True :
                            self.CMD+=launcher
                            self.CMD+=' -c port=swd SN='+stlink_SN_list[i]
                            self.CMD+=' >> '
                            self.CMD+=self.data_saved_mcu ###
                            os.system(self.CMD)
                            #print(self.CMD)
                            self.CMD=' '

                            with open(self.data_saved_mcu,'r') as self.data_saved_mcuname :
                                self.data_saved_mcuname=self.data_saved_mcuname.read()
                                self.data_saved_mcuname=self.data_saved_mcuname.replace('\n',' ')
                                self.data_saved_mcuname=self.data_saved_mcuname.split('Error:')
                                #print(self.data_saved_mcuname)
                                try :
                                    data_B=self.data_saved_mcuname[1].split()
                                    if data_B[0] =='No' :
                                        #print('No board is connected to external stlink-V3 probe')
                                        self.UART_PORT_V3_E.append(UART_PORT[i])
                                        self.stlink_V3_list.append(stlink_V_list[i])
                                        self.stlink_SN_V3_list.append(stlink_SN_list[i])
                                        break
                                except Exception as e  :
                                        self.stlink_V3_list.append(stlink_V_list[i])
                                        self.stlink_SN_V3_list.append(stlink_SN_list[i])
                                        self.UART_PORT_V3_E.append(UART_PORT[i])


                                        with open(self.data_saved_mcu,'r') as self.data_saved_mcuname :
                                             self.data_saved_mcuname=self.data_saved_mcuname.read()
                                             self.data_saved_mcuname=self.data_saved_mcuname.replace('\n',' ')
                                             self.data_saved_mcuname=self.data_saved_mcuname.split('Device name :')
                                            # print(self.data_saved_mcuname)
                                             data_B=self.data_saved_mcuname[1].split()
                                             MCU_name=data_B[0]+'(V3-external probe)'
                                             self.MCU_Name_list_V3.append(MCU_name)

                                        with open(self.data_saved_mcu,'r') as self.data_saved_mcuname :
                                            self.data_saved_mcuname=self.data_saved_mcuname.read()
                                            self.data_saved_mcuname=self.data_saved_mcuname.replace('\n',' ')
                                            self.data_saved_mcuname=self.data_saved_mcuname.split('Flash size  :')
                                            self.data_saved_mcuname=self.data_saved_mcuname[1].split(' ')
                                            MCU_flash_size=self.data_saved_mcuname[1]+' '+self.data_saved_mcuname[2]
                                            self.MCU_flash_size_V3.append(MCU_flash_size)
                                            MCU_flash_size=self.data_saved_mcuname[0]+' '+self.data_saved_mcuname[1]

                            os.remove(self.data_saved_mcu)
                            break


                for i in self.MCU_Name_list_V3 :
                    self.all_mcu.append(i)
                    self.all_SN.append(self.stlink_SN_V3_list[self.MCU_Name_list_V3.index(i)])

                for i in self.MCU_Name_list :
                    self.all_mcu.append(i)
                    self.all_SN.append(self.stlink_SN_V2_list[self.MCU_Name_list.index(i)])

                #print('MCU_Name_list',self.MCU_Name_list)
                #print("MCU_Name_list_V3",self.MCU_Name_list_V3)
                #print("stlink_V2_list",self.stlink_V2_list)
                #print("stlink_SN_V2_list",self.stlink_SN_V2_list)
                #print("all_mcu",self.all_mcu)
                #print('UART_PORT_V3_I',self.UART_PORT_V3_I)
                #print('UART_PORT_V3_E',self.UART_PORT_V3_E)
                #print('UART_PORT_V2',self.UART_PORT_V2)
                #print('MCU_flash_size_V2',self.MCU_flash_size_V2)
                #print('MCU_flash_size_V3',self.MCU_flash_size_V3)
                return self.MCU_Name_list,self.stlink_V2_list,self.stlink_SN_V2_list,self.stlink_V3_list,self.stlink_SN_V3_list,self.MCU_Name_list_V3,self.all_mcu,self.MCU_flash_size_V2,self.MCU_flash_size_V3,self.UART_PORT_V3_I,self.UART_PORT_V3_E,self.UART_PORT_V2,self.all_SN

                #print('MCU_flash_size_V2',self.MCU_flash_size_V2)
                #print('MCU_flash_size_V3',self.MCU_flash_size_V3)
                break

            except Exception as e  :
                print(type(e),e)
                print('please check connected Board !')
                os.remove(self.data_saved_mcu)
                os.system('PAUSE')
                sys.exit()

                
                    

    def Connected_Board(self):
        cubeprogrammer_path=Cubeprogrammer_Path()
        cube_programmer_path,launcher,self.data_saved1,self.data_saved_mcu,self.data_saved_test,self.data3,self.data1,self.data2,self.data4=cubeprogrammer_path.launcher_path()
        os.chdir(cube_programmer_path)
        stm32_data=Stm32_data()
        stlink_SN_list,stlink_V_list,probe_index_list=stm32_data.available_stlink_data('swd')
        MCU_Name_list,stlink_V2_list,stlink_SN_V2_list,stlink_V3_list,stlink_SN_V3_list,MCU_Name_list_V3,all_mcu,MCU_flash_size_V2,MCU_flash_size_V3,UART_PORT_V3_I,UART_PORT_V3_E,UART_PORT_V2,self.all_SN=stm32_data.MCU_name_extract()

        board_list=''
        for item in all_mcu :
            board_list+='\t'+str(all_mcu.index(item)+1)+'.'+item+'   '
        print('DETECTED board:\t',board_list)


    def BOOTLOADER_PORT_MCU_name(self,used_protocol):
        #print("test is ongoing")
        UART_PORT=[]
        USB_PORT=[]
        MCU_Name_list_USB=[]
        MCU_Name_list_UART=[]
        cubeprogrammer_path=Cubeprogrammer_Path()
        cube_programmer_path,launcher,self.data_saved1,self.data_saved_mcu,self.data_saved_test,self.data3,self.data1,self.data2,self.data4=cubeprogrammer_path.launcher_path()
        os.chdir(cube_programmer_path)
        STM32_data=Stm32_data()
        list_used_protocol=["UART","usb"]
        called_list_protocol=[UART_PORT,USB_PORT]
        MCU_name_port=[MCU_Name_list_UART,MCU_Name_list_USB]

        if used_protocol in list_used_protocol:
            called_list_protocol[list_used_protocol.index(used_protocol)]=STM32_data.available_stlink_data(used_protocol)


        for item in called_list_protocol[list_used_protocol.index(used_protocol)]:
            self.CMD+=launcher
            self.CMD+=' -c port='+item
            self.CMD+='>>'
            self.CMD+=self.data_port
            os.system(self.CMD)
            self.CMD=' '
            try:
                with open(self.data_port,'r') as self.data_saved_port :
                    self.data_saved_port=self.data_saved_port.read()
                    self.data_saved_port=self.data_saved_port.replace('\n',' ')
                    self.data_saved_port=self.data_saved_port.split('Device name :')
                    #print(self.data_saved_port)
                    #os.system("PAUSE")
                    data_B=self.data_saved_port[1].split()
                    MCU_name=data_B[0]
                    MCU_name_port[list_used_protocol.index(used_protocol)].append(MCU_name)
                    print(MCU_name_port[list_used_protocol.index(used_protocol)])

                os.remove(self.data_port)

            except IndexError as IE :
                MCU_name_port[list_used_protocol.index(used_protocol)].append("Device not found")
                print(type(IE),IE)
                if used_protocol=="UART" :
                    print("Error: Activating device: KO. Please, verify the boot mode configuration and check the serial port configuration. Reset your device then try again...")
                elif used_protocol =="usb":
                    print("Error: Target device not found Establishing connection with the device failed")

                os.remove(self.data_port)

        #print(self.MCU_Name_list_UART)
        #MCU_name  , used protocol_list
        return MCU_name_port[list_used_protocol.index(used_protocol)],called_list_protocol[list_used_protocol.index(used_protocol)]
            



              
          
          
          
            
            
        
    
            
            
            

        

        
        
            
        
        
        
            
            
        


         

        

                     
                 





















     
        
        
