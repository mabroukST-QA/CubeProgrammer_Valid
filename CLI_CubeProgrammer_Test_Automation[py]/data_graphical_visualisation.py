import os
import platform
import xlsxwriter
from datetime import date,time,datetime,timedelta
from DB_test import Db_wildcat


class data_into_chart:

     def __init__(self,workbook,MPU_datasheet):

         self.sorted_data,self.release_number,self.all_data_number,self.data_ID_number=Db_wildcat().data_sorting()
         print("1.exract sorted data to be used on sheet ",self.sorted_data)
         self.workbook=workbook
         self.MPU_datasheet=MPU_datasheet


         self.chart1 = self.workbook.add_chart({'type': 'column'})
         self.chart2=self.workbook.add_chart({'type': 'pie'})

         self.chart_color=['#00FF00','#FF0000','#F3FF33','#65DAFE','#C0C0C0','#000000','#4C5EF7','#F74CC8','#F74C5C']
         self.bold = self.workbook.add_format({'bold': True})




     def Set_Data_IntoSheet(self,pass_number,fail_number):
         self.Set_data()

         delta=self.release_number +34
         alpha=35
         color=0

         while delta <= self.all_data_number+35 :
             alpha,delta,color=self.design_data_into_chart(self.chart1,alpha,delta,self.chart_color,color)

         self.chart_settings()
         self.set_Pie_chart(pass_number,fail_number)

         self.workbook.close()




     def design_data_into_chart(self,chart1,alpha,delta,chart_color,color):
         chart1.add_series({
                'name':'=STM32MP1XX!$I$'+str(alpha)+':$I$'+str(alpha),
                'categories':'=STM32MP1XX!$J$'+str(alpha)+':$J$'+str(delta),
                'values':'=STM32MP1XX!$K$'+str(alpha)+':$K$'+str(delta),
                'fill':   {'color': chart_color[color]},
                })
         alpha+=self.release_number
         delta+=self.release_number
         color+=1

         return alpha,delta,color

     def Set_data(self):
         print("checkin worksheet and wiritng data ")
         self.MPU_datasheet.write("I34","Data_ID",self.bold)
         self.MPU_datasheet.write("J34","CubeProgrammer_Release",self.bold)
         self.MPU_datasheet.write("K34","Debit_ID",self.bold)


         #counter represent row abcisse starting from 35
         counter=34


         for item in self.sorted_data:
             for sub_item in self.sorted_data[item]:
                 print(item,type(item))
                 print(sub_item[0],type(sub_item[0]))
                 print(sub_item[1],type(sub_item[1]))
                 self.MPU_datasheet.write_string(counter,8,item)
                 self.MPU_datasheet.write_string(counter,9,sub_item[0])
                 self.MPU_datasheet.write_number(counter,10,float(sub_item[1]))
                 counter+=1

     def chart_settings(self):
         self.chart1.set_title ({'name': 'STM32MP1XX FLASHING performance'})
         self.chart1.set_x_axis({
                'name': 'Release',
                'name_font': {'size': 14, 'bold': True},
                'num_font':  {'italic': True }
            })

         self.chart1.set_y_axis({'name': 'Debit execution (Mbit/s)'})
         self.chart1.set_style(11)

         self.MPU_datasheet.insert_chart('A12', self.chart1,{'x_scale': 2.25, 'y_scale': 1.50})
         self.MPU_datasheet.set_zoom(85)

     def set_Pie_chart(self,pass_number,fail_number):
         #add pass fail data into worksheet

         print("write data into worksheet")
         self.MPU_datasheet.write("M34","PASS",self.bold)
         self.MPU_datasheet.write("N34","FAIL",self.bold)
         self.MPU_datasheet.write_number(34,12,pass_number)
         self.MPU_datasheet.write_number(34,13,fail_number)

         self.chart2.add_series({
                'categories': '=STM32MP1XX!$M$34:$N$34',
                'values':     '=STM32MP1XX!$M$35:$N$35',
                'points': [
                    {'fill': {'color': '#00FF00'}},
                    {'fill': {'color': '#FF0000'}},
                ],
            })
         self.chart2.set_title({ 'name': 'Global Test Status  '})
         self.chart2.set_style(11)

         self.MPU_datasheet.insert_chart('J1', self.chart2,{'x_scale': 1, 'y_scale': 1})


def main():
    #function TEST
    test_report='C:\\data_store\\TEST_GRAPHICAl_lib3.xlsx'
    workbook=xlsxwriter.Workbook(test_report)
    MPU_datasheet=workbook.add_worksheet("MPU_flashing_Status")

    data_into_chart(workbook,MPU_datasheet).Set_Data_IntoSheet()






if __name__=='__main__' :
    main()
