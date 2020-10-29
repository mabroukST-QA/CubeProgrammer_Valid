import os
import platform
import xlsxwriter
from datetime import date,time,datetime,timedelta
from DB_test import Db_wildcat


class data_into_chart:

     def __init__(self):

         self.sorted_data,self.release_number,self.all_data_number,self.data_ID_number=Db_wildcat().data_sorting()
         print(self.sorted_data)
         self.rapport_test='C:\\data_store\\'
         self.test_report=self.rapport_test+"TEST_GRAPHICAl_lib.xlsx"

         self.workbook=xlsxwriter.Workbook(self.test_report)
         self.MPU_datasheet=self.workbook.add_worksheet("MPU_flashing_Status")
         self.bold = self.workbook.add_format({'bold': True})


     def design_data_into_chart(self,chart1,alpha,delta,chart_color,color):
         chart1.add_series({
                'name':'=MPU_flashing_Status!$A$'+str(alpha)+':$A$'+str(alpha),
                'categories':'=MPU_flashing_Status!$B$'+str(alpha)+':$B$'+str(delta),
                'values':'=MPU_flashing_Status!$C$'+str(alpha)+':$C$'+str(delta),
                'fill':   {'color': chart_color[color]},
                })
         alpha+=self.release_number
         delta+=self.release_number
         color+=1

         return alpha,delta,color

     def Set_Data_IntoSheet(self):

         print("checkin worksheet and wiritng data ")
         self.MPU_datasheet.write("A1","Data_ID",self.bold)
         self.MPU_datasheet.write("B1","CubeProgrammer_Release",self.bold)
         self.MPU_datasheet.write("C1","Debit_ID",self.bold)

         chart_color=['#00FF00','#FF0000','#F3FF33','#65DAFE','#C0C0C0','#000000','#4C5EF7','#F74CC8','#F74C5C']
         counter=1
         delta=self.release_number +1
         alpha=2
         color=0
         chart1 = self.workbook.add_chart({'type': 'column'})
         for item in self.sorted_data:
             for sub_item in self.sorted_data[item]:
                 print(item,type(item))
                 print(sub_item[0],type(sub_item[0]))
                 print(sub_item[1],type(sub_item[1]))
                 self.MPU_datasheet.write_string(counter,0,item)
                 self.MPU_datasheet.write_string(counter,1,sub_item[0])
                 self.MPU_datasheet.write_number(counter,2,float(sub_item[1]))
                 counter+=1

         while delta <= self.all_data_number+1 :
             alpha,delta,color=data_into_chart().design_data_into_chart(chart1,alpha,delta,chart_color,color)

         chart1.set_title ({'name': 'Flashing Binary Debit Execution'})
         chart1.set_x_axis({
                'name': 'Release',
                'name_font': {'size': 14, 'bold': True},
                'num_font':  {'italic': True }
            })
         chart1.set_y_axis({'name': 'Debit execution (Mbyte/s)'})
         chart1.set_style(11)

         self.MPU_datasheet.insert_chart('F1', chart1,{'x_scale': 1.750, 'y_scale': 1.50})

         self.workbook.close()









def main():

    data_into_chart().Set_Data_IntoSheet()






if __name__=='__main__' :
    main()
