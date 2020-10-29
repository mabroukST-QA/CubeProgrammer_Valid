import mysql.connector

from extract_data  import Stm32_data


class Db_wildcat:

      def __init__(self):

        self.release ='C:\\Program Files\\STMicroelectronics\\STM32Cube\\STM32CubeProgrammer\\bin\\'

              #release =#['C:\\Program Files\\STMicroelectronics\\STM32Cube\\STM32CubeProgrammer\\bin\\',
              # 'C:\\Cube_Programmer\\release_test\\2.3.0\\2.3.0[RC8]\\bin\\',
               #=['C:\\Cube_Programmer\\release_test\\2.2.1\\2.2.1[RC2]\\bin\\',
                # ['C:\\Cube_Programmer\\release_test\\2.2.0\\2.2.0[RC4]\\bin\\',
              # "C:\\Cube_Programmer\\release_test\\2.1.0\\2.1.0[RC2]\\bin\\"]

      def Connect_to_DB(self):
        mydb = mysql.connector.connect(
         host="127.0.0.1",
         user="root",
         passwd="mab@50192379",
         database="wildcat_db"
          )
        return mydb

      def add_data_Db_wildcat(self,size,ID,time,Debit,flashed_binary,Status_test,fail_msg):


        mydb=Db_wildcat().Connect_to_DB()
        cubeprogrammer_release=Stm32_data().software_version_detect()

        print(cubeprogrammer_release)
        print("ID==>",ID)
        print("size==>",size)
        print("time==>",time)
        print("Debit==>",Debit)
        mycursor = mydb.cursor()

        for item in range(len(ID)):
            sql = "INSERT INTO Wildcat_DB (CubeProgrammer_Release,Data_ID,Size_ID,Time_ID,Debit) VALUES (%s, %s, %s, %s, %s)"
            val = (cubeprogrammer_release, ID[item],size[item],time[item],Debit[item])
            mycursor.execute(sql, val)
            mydb.commit()

        print(mycursor.rowcount, "record inserted.")

        mycursor.execute("select * from Wildcat_DB ")

        myresult = mycursor.fetchall()

        for x in myresult:
          print(x)

      def show_data_table(self,column,table,tested_column="",condition=""):

               mydb=Db_wildcat().Connect_to_DB()
               mycursor = mydb.cursor()
               if len(condition)==0 :
                    sql_command="select "+column+" from "+table
               else :
                   sql_command="select "+column+" from "+table+" where "+tested_column+"='"+condition+"'"

               print(sql_command)
               mycursor.execute(sql_command)
               data = mycursor.fetchall()

               for x in data:
                   print(x)

               print(data)


               return data

      def data_sorting(self):
          data=Db_wildcat().show_data_table('CubeProgrammer_Release,Data_ID,Debit','Wildcat_DB')
          sql_query='count(distinct CubeProgrammer_Release) as "number of distinct release" ' \
                         ',count(CubeProgrammer_Release) as "full element number ",' \
                         'count(CubeProgrammer_Release)/count(distinct CubeProgrammer_Release) as "number of element per release" '

          data2=Db_wildcat().show_data_table(column=sql_query,table='Wildcat_DB',tested_column="",condition="")
          """
          data2 retrun number of release(exp 4) ,number of all tested element (exp 36),number of testted element per release(9)
               :data structure --> it's a list of data as [(4, 36, Decimal('9.0000'))] containing a tuple !
          """


          self.sorted_data={}
          self.all_data=[]
          self.all_ID=[]
          counter=0
          counter_9_data=0
          release_number=data2[0][0]
          all_data_number=data2[0][1]
          data_ID_number=int(data2[0][2])

          while True :


             if counter_9_data==data_ID_number:
                break
             else:
                print('counter',counter)
                self.all_ID.append(data[counter][1])
                self.all_data.append([data[counter][0],data[counter][2]])
                self.sorted_data[self.all_ID[0]]=self.all_data
                counter+=data_ID_number

                if counter>(release_number-1)*data_ID_number+counter_9_data:
                    self.all_data=[]
                    self.all_ID=[]
                    counter_9_data+=1
                    counter=counter_9_data
                    print('\n')
                    continue


          print(self.all_ID)
          print(self.all_data)
          print(self.sorted_data)

          for item in self.sorted_data :
              print(item)
              for sub_item in self.sorted_data[item]:
                  print( '\t',sub_item[0],':',sub_item[1])
              print('\n')



          return self.sorted_data,release_number,all_data_number,data_ID_number



def main():
    #Db_wildcat().show_data_table('*','Wildcat_DB','CubeProgrammer_Release',Stm32_data().software_version_detect())

    """
    data=Db_wildcat().show_data_table('CubeProgrammer_Release,Data_ID,Debit','Wildcat_DB')
    sql_query='count(distinct CubeProgrammer_Release) as "number of distinct release" ' \
                         ',count(CubeProgrammer_Release) as "full element number ",' \
                         'count(CubeProgrammer_Release)/count(distinct CubeProgrammer_Release) as "number of element per release" '

    data2=Db_wildcat().show_data_table(column=sql_query,table='Wildcat_DB',tested_column="",condition="")

    Db_wildcat().data_sorting()

    """
    cubeprogrammer_release=Stm32_data().software_version_detect(RC="")
    data=Db_wildcat().show_data_table('distinct CubeProgrammer_Release','Wildcat_DB')
    print(cubeprogrammer_release)
    print(data)
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







if __name__=='__main__' :
    main()
