#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
    This module provide an interface to work with all protocol ['swd_v2','swd_v3','UART','CAN','usb','i2c'] via multiboard,to echieve suveral operation
    {'erase','read_out_protection','remove_data_protection','connect','write','reset'}
"""
import os
import platform
import xlsxwriter
from datetime import date,time,datetime,timedelta
import shutil
from Wildcat_data import Wildcat
from data_graphical_visualisation import data_into_chart



OS=platform.system()

if OS=='Windows':
    from extract_data  import Stm32_data
    timeout='timeout /t 1 /nobreak '

elif OS=='Linux':
    from extract_data_UBUNTU  import Stm32_data
    timeout="timeout 1s bash "

from path_data import Cubeprogrammer_Path
from i2c_data import I2C


class Op:
    def __init__(self,command="",action="",show=""):
        """
        command=['swd_v2','swd_v3','UART','CAN','usb','i2c']:
              ---> provide an available protocol ,keeping this style
        action={'erase','read_out_protection','remove_data_protection','connect','reset'}:
              ---> choose one action to be done with specific protocol
        show=[False,True]:
              --> choose if you want to see data on cmd or nort
        =>NB.some parametre are called based on it"s protocole to optimze code and test launch .

        """
        self.show=show
        self.command=command    #command ==> protocol
        self.action=action

        self.CMD=' '
        self.protocol=''
        self.STM32_data=Stm32_data()
        self.protocol=['swd_v2','swd_v3','UART','CAN','usb','i2c']
        self.stlink_SN_list,self.stlink_V_list,self.probe_index_list=self.STM32_data.available_stlink_data('swd')
        self.MCU_Name_list,self.stlink_V2_list,self.stlink_SN_V2_list,self.stlink_V3_list,self.stlink_SN_V3_list,self.MCU_Name_list_V3,self.all_mcu,self.MCU_flash_size_V2,self.MCU_flash_size_V3,self.all_SN=self.STM32_data.MCU_name_extract()
        self.used_command=[]
        self.detected_error=[]
        self.list_worksheet=[]
        #self.MCU_Name_list_usb=[]
        #self.USB_PORT=[]
        self.MCU_Name_list_UART=[]
        self.UART_PORT=[]
        self.datetime_action_board=[]
        self.datetime_all_action_board=[]

        os.system(timeout)
        if command=='usb':
            self.MCU_Name_list_usb,self.USB_PORT=self.STM32_data.BOOTLOADER_PORT_MCU_name("usb")
            print("USB DATA OINGOING")
            print(self.USB_PORT)
            print(self.MCU_Name_list_usb)
            self.parametre=['','','','',self.USB_PORT]
            self.para4=['swd SN=','swd SN=',"",'',self.USB_PORT]
            self.para2=["","","","",self.MCU_Name_list_usb]
        elif command=='UART':
            self.MCU_Name_list_UART,self.UART_PORT=self.STM32_data.BOOTLOADER_PORT_MCU_name("UART")
            print("UART_MCU_name",self.MCU_Name_list_UART,'\n','UART_PORT :',self.UART_PORT)
            self.parametre=["","",self.UART_PORT,"",""]
            self.para4=['swd SN=','swd SN=',self.UART_PORT,'',""]
            self.para2=[self.MCU_Name_list,self.MCU_Name_list_V3,self.MCU_Name_list_UART,self.all_mcu,self.all_mcu]
        elif command =='i2c':
            self.I2C_add=I2C().Extraire_I2C_ADD()
            self.para2=["","","","","",self.all_mcu]
            self.para4=['','',"",'',"","i2c add="]
            self.parametre=['','','','','',self.I2C_add]
            print("i2c_MCU_name",self.all_mcu,'\n','i2c address :',self.I2C_add)
        else:
            self.parametre=[self.stlink_SN_V2_list,self.stlink_SN_V3_list,"",self.stlink_SN_V2_list,""]
            self.para4=['swd SN=','swd SN=',"",'',""]
            self.para2=[self.MCU_Name_list,self.MCU_Name_list_V3,"",self.all_mcu,self.all_mcu]

        os.system(timeout)
        self.para3=[self.MCU_flash_size_V2,self.MCU_flash_size_V3,self.MCU_flash_size_V2,self.MCU_flash_size_V2,self.MCU_flash_size_V2,self.MCU_flash_size_V2]

        self.para8=['','','','',self.MCU_flash_size_V3,'']
        self.para9=['','','','',self.stlink_V3_list,'']
        
        if OS=='Windows':
            self.data_boot_0="C:\\CubeProgrammer_Valid\\data_store\\data_boot.txt"
            self.data_report="C:\\CubeProgrammer_Valid\\data_store\\data_analyse.txt"
            self.rapport_test="C:\\Programmer_Test_Platform\\Automatic_test_report"
            self.data_test_performance="C:\\CubeProgrammer_Valid\\data_store\\data_performance.txt"
            self.dropped_path="C:\\Programmer_Test_Platform\\STM32CubeProgrammer\\bin\\STM32_Programmer_CLI.exe "

        elif OS=='Linux':
            #on ubutnu_st
            #self.data_boot_0="//local//home/brhoumam//Desktop/mabrouk//CubeProgrammer_Test_Automation//data_store//data_boot.txt"
            # on ubutnu_native
            self.data_boot_0='//home//tunvqtvalidadm//Desktop//mabrouk//CubeProgrammer_Test_Automation//data_store//data_boot.txt'
            self.data_report ='//home//tunvqtvalidadm//Desktop//mabrouk//CubeProgrammer_Test_Automation//data_store//data_analyse.txt'
            self.rapport_test ='//home//tunvqtvalidadm//Desktop//mabrouk//CubeProgrammer_Test_Automation//data_store//automation_test_report'

        self.para7={'Erase':' -e all','Read_out_protection': ' -ob rdp=0xbb','Remove_data_protection':' -rdu','Connect':'','Connect via dropped path':self.dropped_path,'Reset':' -rst'}
        self.cubeprogrammer_path=Cubeprogrammer_Path()
        self.cube_programmer_path,self.launcher,self.data_saved1,self.data_saved_mcu,self.data_saved_test,self.data3,self.data1,self.data2,self.data4,self.data5,self.data6=self.cubeprogrammer_path.launcher_path()
        self.para5=['512 KBytes','2 MBytes','1 MBytes','1.5 MBytes','128 KBytes', '256 KBytes']
        self.para6=[self.data1,self.data2,self.data3,self.data4,self.data5,self.data6]
        os.chdir(self.cube_programmer_path)

    def launch(self):

        """
           this function added together parameters based on entred command connection  and action parametre
        """
        if self.action =="Connect via dropped path":
            self.CMD=self.para7[self.action]

        else :
            self.CMD=self.launcher

        self.CMD+=' -c port='

        if self.command  in self.protocol :
            print("USB DATA OINGOING COMMAND")
            index_=self.protocol.index(self.command)

            for choice in range(len(self.parametre[index_])):
                CMD1=''
                print('\n-----------------------------------------------')
                print('Current Tested Board:' ,self.para2[index_][choice],'\nCurrent Test:',self.action,'\nused protocol:',self.command)
                print('\n-----------------------------------------------')
                #Rapport parametre

                #Connection parametre
                CMD1=self.CMD
                if self.command == 'swd_v2' or self.command =='swd_v3':
                    CMD1+=self.para4[index_]+self.parametre[index_][choice]
                elif self.command =='CAN' :
                    CMD1+=self.command

                elif self.command== 'i2c':
                    CMD1+=self.para4[index_]+self.parametre[index_][choice] #to be updated when multiple ticket is corrected +" SN="+self.stlink_SN_V3_list[choice]

                elif self.command =='usb':
                    try:
                        if len(self.para3[index_]) >0 and self.para3[index_][choice] in self.para5 or self.para8[index_][choice] in self.para5:
                            CMD1+=self.para4[index_][choice]

                    except IndexError:
                        CMD1+=self.para4[index_][choice]
                else:
                    CMD1+=self.para4[index_][choice]

                #Action parametre
                if self.action in self.para7 and self.action != "Connect via dropped path":
                    CMD1+=self.para7[self.action]
                elif self.action == "Connect via dropped path":
                    CMD1+=" "
                else:
                    if self.command =='usb'  and len(self.stlink_V3_list) >0 :
                        try:
                            if len(self.para9[index_][choice])==6:
                               #print('hi1')
                               index__2=self.para5.index(self.para8[index_][choice])
                        except IndexError:
                            #print('hi2')
                            index__2=self.para5.index(self.para8[index_][choice-1])

                    elif self.command=='usb' and len(self.para3[index_]) >0 or len(self.para9[index_])>0 :
                        try:
                            if self.para3[index_][choice] in self.para5 or self.para8[index_][choice] in self.para5:
                                print('hi3')
                                if self.MCU_Name_list_usb[choice] in self.MCU_Name_list:
                                    a=self.MCU_Name_list.index(self.MCU_Name_list_usb[choice])

                                index__2=self.para5.index(self.para3[index_][a])
                                print(self.para5[index__2])
                            else :
                                print("hiiiiiiiiiiiiiii")
                                index__2=self.para6.index(self.data1)
                        except ValueError as VE:
                            print(type(VE),VE)
                            #print('hi4')
                            index__2=self.para6.index(self.data1)
                        except IndexError as IE:
                            print(type(IE),IE)
                            #print('hi5')
                            index__2=self.para6.index(self.data1)
                    elif self.command =='UART' :

                        print(self.para2[index_][choice])
                        print()
                        if self.para2[index_][choice] in self.all_mcu:
                            #print('hi6')
                            index__2=self.all_mcu.index(self.para2[index_][choice])

                        else:
                            #print('hi7')
                            index__2=self.para6.index(self.data1)

                    elif self.command =='swd_v2':
                        #print(self.para3[index_][choice])
                        if self.para3[index_][choice] in self.para5:

                               index__2=self.para5.index(self.para3[index_][choice])
                        else:

                            index__2=self.para6.index(self.data1)

                    else:
                        try:
                            if self.para3[index_][choice] in self.para5:
                               index__2=self.para5.index(self.para3[index_][choice])
                        except:
                            print("data file choice is randomly ,please verify!")
                            index__2=self.para6.index(self.data1)



                    CMD1+=' -w '+self.para6[index__2]+' 0x08000000'


                if self.show==True:
                    #print("hi")
                    print(CMD1)
                    self.used_command.append(CMD1)

                    #add datetime for this MCU start_time


                    os.system(CMD1)


                else:
                    #print("hi2")
                    b=datetime.now()
                    c2=b.day
                    c3=b.hour
                    c4=b.minute
                    c5=b.second
                    c6=b.microsecond
                    a=timedelta(hours=c3,minutes=c4,seconds=c5,microseconds=c6)
                    print(a)

                    os.system(CMD1)

                    print("\n")
                    #print(CMD1)
                    b1=datetime.now()
                    c21=b1.day
                    c31=b1.hour
                    c41=b1.minute
                    c51=b1.second
                    c61=b1.microsecond
                    a2=timedelta(hours=c31,minutes=c41,seconds=c51,microseconds=c61)
                    print(a2)

                    c=a2-a
                    print(c)


                    self.datetime_action_board.append(c)
                    self.used_command.append(CMD1)

            #self.datetime_all_action_board.append(self.datetime_action_board)
        #self.datetime_action_board=[]

        #print("action_data_execution: ",self.datetime_all_action_board)
        return self.used_command,self.datetime_action_board






    def data_analyse(self):
        #data_report

        full_used_command_protocols=[]
        passed_test=[]
        failed_test=[]
        full_used_command=[]
        used_action=['Connect',"Connect via dropped path",'Write','Erase','Read_out_protection','Remove_data_protection','Reset']
        #used_action=['connect','reset']
        used_protocol={'swd_v2':self.MCU_Name_list}
        test_fail_counter=0
        list_fail_test_counter=[]
        test_pass_counter=0
        list_pass_test_counter=[]
        counter_passement=0
        action_time=[]
        #***********************************
        #Original List tested
        #used_protocol={'swd_v2':self.MCU_Name_list,'swd_v3':self.MCU_Name_list_V3,'usb':Op("usb").MCU_Name_list_usb,'UART':Op("UART").MCU_Name_list_UART,'i2c':self.all_mcu,'CAN':self.all_mcu}
        #***********************************

        #print(self.MCU_Name_list_usb)
        #used_action=['connect','write','erase','read_out_protection','remove_data_protection','reset']

        for protocol in used_protocol:
            for action in used_action:
                if action =='Remove_data_protection' and protocol=='usb':
                    Op('swd_v2','Remove_data_protection',show=False).launch()
                else:

                    used_command,datetime_all_action_board=Op(protocol,action,show=False).launch()
                    action_time.append(datetime_all_action_board)

                    counter_passement+=1
                    if counter_passement==1:
                        for i in range(len(used_command)):
                            list_fail_test_counter.append(test_fail_counter)
                        print(list_fail_test_counter)

                        for i in range(len(used_command)):
                            list_pass_test_counter.append(test_pass_counter)
                        print(list_pass_test_counter)
                    else :
                        pass

                    full_used_command.append(used_command)

                    for item in used_command :
                        CMD=item+' >> '+self.data_report
                        os.system(CMD)
                        with open(self.data_report,'r') as data_analyse :
                            data_analyse=data_analyse.read()
                            data_analyse=data_analyse.replace('\n','')
                            data_analyse2=data_analyse.split("Error:")
                            data_analyse1=data_analyse.split()
                            if "failed" in data_analyse1 or "Error" in data_analyse:

                                if action == 'Read_out_protection':
                                    #print("Test FAIL")
                                    self.detected_error.append(data_analyse2[len(data_analyse2)-1])
                                    failed_test.append(item)
                                    print(self.detected_error)
                                else:
                                    print("Test FAIL")
                                    self.detected_error.append(data_analyse2[1])
                                    print(self.detected_error)
                                    failed_test.append(item)
                                    list_fail_test_counter[used_command.index(item)]=list_fail_test_counter[used_command.index(item)]+1

                            else:
                                passed_test.append(item)
                                print("TEST PASS")
                                list_pass_test_counter[used_command.index(item)]=list_pass_test_counter[used_command.index(item)]+1
                        os.remove(self.data_report)
                        CMD=" "
            full_used_command_protocols.append(full_used_command)
            full_used_command=[]


            print(action_time)
            full_time_action_B=action_time[0][0]-action_time[0][0]
            full_time_action_B_all=[]

            for mcu in used_protocol[protocol]:
                    for action in used_action :
                        full_time_action_B+=action_time[used_action.index(action)][used_protocol[protocol].index(mcu)]

                    full_time_action_B_all.append(full_time_action_B)
                    full_time_action_B=full_time_action_B=action_time[0][0]-action_time[0][0]


            print(full_time_action_B_all)

            data_time_action=[]
            data_execution_String=[]
            Somme_data_time=action_time[0][0]-action_time[0][0]
            for i in full_time_action_B_all:
                Somme_data_time+=i
                c=str(i)
                data_time_action.append(datetime.strptime(c,'%H:%M:%S.%f'))
                print(i)
                print(Somme_data_time)
            data_execution_String.append(str(Somme_data_time))
            data_time_action.append(datetime.strptime(str(Somme_data_time),'%H:%M:%S.%f'))

            """
            #print("full_used_command_protocols--->",full_used_command_protocols)
            #print("list_pass_test_counter------->",list_pass_test_counter)
            #print("list_pass_test_counter-------->",list_fail_test_counter)
            """

        return used_action,full_used_command_protocols,list_pass_test_counter,list_fail_test_counter,passed_test,failed_test,self.detected_error,used_protocol,data_time_action,data_execution_String

    def data_test_report(self):
        used_action,full_used_command_protocols,list_pass_test_counter,list_fail_test_counter,passed_test,failed_test,self.detected_error,used_protocol,data_time_action,data_execution_String=Op().data_analyse()
        cube_prog_re=Stm32_data().software_version_detect()
        used_DV=[]
        all_workbook=[]
        counter=-1
        for protocol in used_protocol:
            used_DV.append(used_protocol[protocol])
            end_tab=len(used_protocol[protocol])
            start_tab2=end_tab+12

        used_DV.append(list_pass_test_counter)
        used_DV.append(list_fail_test_counter)
        used_DV.append(data_time_action)

        """
            This part of this function  provide FAIL/PASS status for each connectd board ,which explained error in case of fail
           how it works
            -->we start by creating an exel with protocol name(and used OS and used release)(it may be 1 exel or more base on protocol number entred )
                ::self.workbook=xlsxwriter.Workbook(test_report) creat 1 exel with protocol name
                ::all_workbook.append(self.workbook) --> add exel to a list of execel
            -->based on mcu detected a new sheet is creat witch contient mcu name as title in every sheet
               :: en exception may occurs if mcu name contients special caractere so if it's the case we change every special caracter with "_" then we get it back to it's original form
             -->to make our sheet or workbook visible and more attractive we add some modification as column and row widh and style
              :: we accessed to every sheet by self.list_worksheet[used_protocol[protocol].index(mcu)]
              ::set_column(0,0,20) to change 1 column  length
              ::set_row(i, 40) to change 1 row width
            --> we add every recorded test command for every board

        """

        for protocol in used_protocol:
            counter+=1
            test_report=self.rapport_test+"__"+cube_prog_re+"__"+protocol+".xlsx"
            self.workbook=xlsxwriter.Workbook(test_report)
            all_workbook.append(self.workbook)
            for mcu in used_protocol[protocol]:
                a=mcu
                try :
                    self.list_worksheet.append(all_workbook[counter].add_worksheet(mcu))

                except xlsxwriter.exceptions.InvalidWorksheetName :
                    special_sumbole=['~', ':', "'", '+', '[', '\\', '@', '^', '{', '%', '(', '-', '"', '*', '|', ',', '&', '<', '`', '}', '.', '_', '=', ']', '!', '>', ';', '?', '#', '$', ')', '/']
                    for i in mcu:
                        if i in special_sumbole:
                            mcu=mcu.replace(i,"_")
                            #print(mcu)
                    try :
                        self.list_worksheet.append(all_workbook[counter].add_worksheet(mcu))

                    except xlsxwriter.exceptions.InvalidWorksheetName :
                        if len(mcu) >31 :
                            print("this mcu ",mcu," pass tolerated length")
                            mcu=mcu[0:30]

                        self.list_worksheet.append(all_workbook[counter].add_worksheet(mcu))

                    mcu=a

                bold = all_workbook[counter].add_format({'bold': True})
                self.list_worksheet[used_protocol[protocol].index(mcu)].set_column(0,0,35)
                self.list_worksheet[used_protocol[protocol].index(mcu)].set_column(1,1,80)
                self.list_worksheet[used_protocol[protocol].index(mcu)].set_column(2,2,20)
                self.list_worksheet[used_protocol[protocol].index(mcu)].set_column(3,3,80)
                self.list_worksheet[used_protocol[protocol].index(mcu)].set_column(4,4,20)

                for i in range(len(full_used_command_protocols[counter])+1):
                    self.list_worksheet[used_protocol[protocol].index(mcu)].set_row(i, 40)

                        #data rapport initialize

                self.list_worksheet[used_protocol[protocol].index(mcu)].write("A1","Test Category",bold)
                self.list_worksheet[used_protocol[protocol].index(mcu)].write("B1","Executed Test",bold)
                self.list_worksheet[used_protocol[protocol].index(mcu)].write("C1","Test Status",bold)
                self.list_worksheet[used_protocol[protocol].index(mcu)].write("D1","Error",bold)
                self.list_worksheet[used_protocol[protocol].index(mcu)].write("E1","Tickets",bold)

            print("full_used_command_protocols[counter]==>",full_used_command_protocols[counter] )
            for item in full_used_command_protocols[counter] :
                print("item===>",item)
                for command in item :
                    print("command ===>",command)
                    #print("item.index(command)===>",item.index(command))
                    #print("used_action==>",used_action[item.index(command)])

                    self.list_worksheet[item.index(command)].write("A"+str(full_used_command_protocols[counter].index(item)+2),used_action[full_used_command_protocols[counter].index(item)])
                    self.list_worksheet[item.index(command)].write("B"+str(full_used_command_protocols[counter].index(item)+2),command)
                    if command in failed_test:
                        self.list_worksheet[item.index(command)].write("C"+str(full_used_command_protocols[counter].index(item)+2),"FAIL")
                        self.list_worksheet[item.index(command)].write("D"+str(full_used_command_protocols[counter].index(item)+2),self.detected_error[failed_test.index(command)])
                    elif command in passed_test :
                        self.list_worksheet[item.index(command)].write("C"+str(full_used_command_protocols[counter].index(item)+2),"PASS")


            self.list_worksheet=[]

           #end part1 as data_test_analyse and we start part2 as data visualisation in chart.

            """
                  we start by creating a new sheet wich name is Data_visualization1
                  this sheet contains 2 part PASS/FAIL counting and test time execution for each board explained with graphs
                  So how it works !
                    --->we start by setting sheet configuration size column and row ,with additional data format for date
                    -->we set al gathred data into one list used_DV (mcu name :used_protocol[protocol]--> self.MCU_Name_list this give us in indice for how much tested
                    boards)(test pass couter)(fail counter)(data time action )
                    ---> we set data on 4 column A B C D  ,for D it's a bit special we add datetime wi use write_datetime with date_format
                    --->Once data are well written on sheet we have to add chart :
                         ::chart 1 --->PASS and fail based on each board, histogramme chart with total number of pass and fail.
                           essential element is the tab with demension == end_tab +2(start headings + commands +toltal)
                         ::chart 2 ---> Pie chart with PASS/FAIL total status
            """

            ######## worksheet configuration

            D_V= all_workbook[counter].add_worksheet("MCU_TESTS_SUMMARY")


            D_V.set_column(1,2,15) #from column 1 to 2 applied this config
            D_V.set_column(0,0,25) # applied this config to colum 0
            D_V.set_column(3,3,25) # apploied this config to column 3

            for i in range(end_tab+100):
                D_V.set_row(i, 30)

            date_format = all_workbook[counter].add_format({'num_format': 'hh:mm:ss.000',
                                      'align': 'centre'})

            #########
            ######### ADD tab + char1 charecterisation histogramme

            D_V.write("A1","Used Boards",bold)
            D_V.write("B1","PASS",bold)
            D_V.write("C1","FAIL",bold)
            D_V.write("D1","Tests Run Time",bold)

            D_V.write_column('A2',used_DV[0])
            D_V.write_column('B2',used_DV[1])
            D_V.write_column('C2',used_DV[2])


            for i in range(len(data_time_action)):
                D_V.write_datetime("D"+str(i+2), used_DV[3][i], date_format)


            chart1 = all_workbook[counter].add_chart({'type': 'column'})
            chart1.add_series({
                'name':'=MCU_TESTS_SUMMARY!$B$1:$B$1',
                'categories':'=MCU_TESTS_SUMMARY!$A$2:$A$'+str(end_tab+1),
                'values':'=MCU_TESTS_SUMMARY!$B$2:$B'+str(end_tab+1),
                'fill':   {'color': '#00FF00'},
            })
            chart1.add_series({
                'name':'=MCU_TESTS_SUMMARY!$C$1:$C$1',
                'categories':'=MCU_TESTS_SUMMARY!$A$2:$A$'+str(end_tab+1),
                'values':'=MCU_TESTS_SUMMARY!$C$2:$C$'+str(end_tab+1),
                'fill':   {'color': '#FF0000'},
            })
            chart1.set_x_axis({
                'name': 'All Tested Board Pass/Fail status ',
                'name_font': {'size': 14, 'bold': True},
                'num_font':  {'italic': True }
            })

            #########
            ######### chart2 data charecterisation Pie

            D_V.write(end_tab+1, 0, 'Total',bold)
            D_V.write_formula(end_tab+1, 1, '=SUM(B2:B'+str(end_tab+1)+')',bold)
            D_V.write_formula(end_tab+1, 2, '=SUM(C2:C'+str(end_tab+1)+')',bold)

            chart2 = all_workbook[counter].add_chart({'type': 'pie'})
            chart2.add_series({
                'categories': '=MCU_TESTS_SUMMARY!$B$1:$C$1',
                'values':     '=MCU_TESTS_SUMMARY!$B$'+str(end_tab+2)+':$C$'+str(end_tab+2),
                'points': [
                    {'fill': {'color': '#00FF00'}},
                    {'fill': {'color': '#FF0000'}},
                ],
            })
            chart2.set_title({ 'name': 'Global Test Status  '})
            chart2.set_style(10)
            #########

             ######### to be checked time_execution.append(used_DV[3][len(data_time_action)-1])
            #time_execution=[]

            final_release_exe,final_timing=self.performance_data(data_execution_String)


            D_V.write("A"+str(start_tab2),"CubeProgrammer Release",bold)
            D_V.write("B"+str(start_tab2),"Tests Execution Time",bold)
            D_V.write_column('A'+str(start_tab2+1),final_release_exe)

             #to ckeck index final_timing.index(c)
            for c in final_timing :
                date_time = datetime.strptime(c,'%H:%M:%S.%f')
                D_V.write_datetime("B"+str(start_tab2+1+final_timing.index(c)), date_time, date_format)


            #D_V.write_datetime("B15", time_execution[0], date_format)

            chart3 = all_workbook[counter].add_chart({'type': 'bar'})
            chart3.add_series({
                'name':       '=MCU_TESTS_SUMMARY!$A$'+str(start_tab2)+':$A$'+str(start_tab2),
                'categories': '=MCU_TESTS_SUMMARY!$A$'+str(start_tab2+1)+':$A$'+str(len(final_timing)+start_tab2+1),###Y
                'values':     '=MCU_TESTS_SUMMARY!$B$'+str(start_tab2+1)+':$B$'+str(len(final_timing)+start_tab2+1),##X
            })

            chart3.set_title ({'name': 'TEST RUN TIME EXCUTION '})
            chart3.set_x_axis({'name': 'Time Execution (min)','date_axis': True,'num_format': 'h:mm:ss.000'})
            chart3.set_y_axis({'name': 'Release'})

            # Set an Excel chart style.
            chart3.set_style(11)

            # Insert the chart into the worksheet (with an offset).
            D_V.insert_chart('F1', chart1,{'x_scale': 1.750, 'y_scale': 1.50})
            D_V.insert_chart('T1', chart2,{'x_scale': 1, 'y_scale': 1})
            D_V.insert_chart('F'+str(start_tab2), chart3,{'x_scale': 2.250, 'y_scale': 2.250})
            D_V.set_zoom(85)



            size,ID,time,Debit,flashed_binary,Status_test,fail_msg=Wildcat().wildcat_status()

            print(Debit)

            end_tab_MPU=len(flashed_binary)

            MPU_datasheet= all_workbook[counter].add_worksheet("STM32MP1XX")
            MPU_datasheet.set_column(1,1,60)
            MPU_datasheet.set_column(0,0,10)
            MPU_datasheet.set_column(2,6,15)

            for i in range(end_tab_MPU+5):
                MPU_datasheet.set_row(i, 30)

            date_format = all_workbook[counter].add_format({'num_format': 'hh:mm:ss.000',
                                      'align': 'centre'})


            MPU_datasheet.write("A1",'Data ID',bold)
            MPU_datasheet.write("B1",'Data Binary',bold)
            MPU_datasheet.write("C1",'Test Status',bold)
            MPU_datasheet.write("D1",'Fail Output',bold)
            MPU_datasheet.write("E1",'Size in Mbit',bold)
            MPU_datasheet.write("F1",'Time in s',bold)
            MPU_datasheet.write("G1",'Debit in Mbit/s',bold)

            MPU_datasheet.write_column('A2',ID)
            MPU_datasheet.write_column('B2',flashed_binary)
            MPU_datasheet.write_column('C2',Status_test)
            MPU_datasheet.write_column('D2',fail_msg)
            MPU_datasheet.write_column('E2',size)
            MPU_datasheet.write_column('F2',time)
            MPU_datasheet.write_column('G2',Debit)
            #this function id added above size,ID,time,Debit,flashed_binary,Status_test,fail_msg=Wildcat().wildcat_status()

            pass_number,fail_number=self.Counter_status(Status_test)
            data_into_chart(all_workbook[counter],MPU_datasheet).Set_Data_IntoSheet(pass_number,fail_number)









            all_workbook[counter].close()

        print(used_protocol[protocol])
        print("list_pass_test_counter------->",list_pass_test_counter)
        print("list_pass_test_counter-------->",list_fail_test_counter)

            #os.rename(source, destination)
            #shutil.move(self.rapport_test, rapport_destination)

    def bootloader_verification(self):

        """
           this function, in order to verify if bootlaoder is activated or not ,comapre  data at address 0 vs data at address 0x08000000
        """

        for choice in range(len(self.all_SN)):
            print('\n----------------------------------------------------')
            print('Current Tested Board:' ,self.all_mcu[choice],'\nSN:\t',self.all_SN[choice])
            print('\n----------------------------------------------------')


            self.CMD=self.launcher
            self.CMD1=self.CMD+' -c port=swd SN='+self.all_SN[choice]+" -r32 0 0x40 >>" +self.data_boot_0
            #print(self.CMD1)
            os.system(self.CMD1)
            with open(self.data_boot_0,'r') as self.data_saved_boot :
                self.data_saved_boot=self.data_saved_boot.read().replace('\n',' ').split('0x00000000 :')
                self.data_saved_boot=self.data_saved_boot[1].split(' ')

                binary_boot=self.data_saved_boot[1]
                print('address 0     \t  ',binary_boot)
            os.remove(self.data_boot_0)


            self.CMD2=self.CMD+' -c port=swd SN='+self.all_SN[choice]+" -r32 0x08000000 0x40 >>"+self.data_boot_0
            os.system(self.CMD2)
            with open(self.data_boot_0,'r') as self.data_saved_boot :

                self.data_saved_boot=self.data_saved_boot.read().replace('\n',' ').split('0x08000000 :')
                self.data_saved_boot=self.data_saved_boot[1].split(' ')
                binary_boot_1=self.data_saved_boot[1]
                print('address 0x08000000',binary_boot_1)

            os.remove(self.data_boot_0)
            self.CMD=''

            if binary_boot_1 !=binary_boot:
                print("-------> Board is well connected to BOOTLOADER mode")
                print('\n')
            else:
                print("-------> Board is not connected  to BOOTLOADER mode")
                print('\n')


    def performance_data(self,data_execution_String):
            release_cubeprogrammer=[]
            release_cubeprogrammer.append(Stm32_data().software_version_detect()) # used
            release_exe=[] #used
            timing=[]#used
            data_tobe_analysed=[]
            final_release_exe=[]
            final_timing=[]
            while True :

                try:
                    with open(self.data_test_performance,"a") as file_test :
                         for (r,c) in zip(release_cubeprogrammer,data_execution_String) :
                             file_test.write(r+" --> "+c+"\n")

                    with open(self.data_test_performance,"r") as data_analyse:
                        data_analyse=data_analyse.read()
                        data_analyse1=data_analyse.split()
                        print(data_analyse1)

                    for item in data_analyse1 :
                       if item != '-->' :
                          data_tobe_analysed.append(item)
                    print(data_tobe_analysed)
                    for i in range(len(data_tobe_analysed)) :
                        if i%2==0:
                           release_exe.append(data_tobe_analysed[i])
                        else:
                          timing.append(data_tobe_analysed[i])
                    print(release_exe)
                    print(timing)
                    for item in release_exe:
                        if release_exe.count(item)==1  or release_exe.count(item)>1 and item not in final_release_exe :
                            final_release_exe.append(item)
                            final_timing.append(timing[release_exe.index(item)])
                    print(final_release_exe)
                    print(final_timing)
                    break



                except FileNotFoundError as FNO:
                    with open(self.data_test_performance,"w") as file_test :
                         for (r,c) in zip(release_cubeprogrammer,data_execution_String) :
                             file_test.write(r+" --> "+c+"\n")
                    continue

            return final_release_exe,final_timing

    def Counter_status(self,Status_test):
        pass_number=Status_test.count('PASS')
        fail_number=len(Status_test)-pass_number

        return pass_number,fail_number





















        
        
