#! /usr/bin/env python3
"""
  This module provide an I2C address for each detected Board ans save them into one list to be used later with i2c connection

"""
import platform
OS=platform.system()

if OS=='Windows':
    from extract_data  import Stm32_data
elif OS=='Linux':
    from extract_data_UBUNTU  import Stm32_data


class I2C():
      def __init__(self):
         self.STM32_data=Stm32_data()
         self.MCU_Name_list,self.stlink_V2_list,self.stlink_SN_V2_list,self.stlink_V3_list,self.stlink_SN_V3_list,self.MCU_Name_list_V3,self.all_mcu,self.MCU_flash_size_V2,self.MCU_flash_size_V3,self.UART_PORT_V3_I,self.UART_PORT_V3_E,self.UART_PORT_V2,self.all_SN=self.STM32_data.MCU_name_extract()
         #print(self.stlink_SN_V3_list)
         self.add=[]
         self.list_add={
        'STM32F030xC' :'0x41' ,
        'STM32F04xxx' : '0x3E' ,
        'STM32F070x6' :'0x3E',
        'STM32F070xB':'0x3B',
        'STM32F071xx/072xx':'0x3B',
        'STM32F09xxx':'0x41',
        'STM32F303x4(6/8)/334xx/328xx':'0x3F',
        'STM32F318xx':'0x3B',
        'STM32F358xx':'0x37',
        'STM32F378xx':'0x37',
        'STM32F398xx':'0x40',
        'STM32F401xB(C)':'0x39',
        'STM32F401xD(E)':'0x39' ,
        'STM32F410xx':'0x47',
        'STM32F411xx':'0x39',
        'STM32F412xx':'0x46','STM32F412':'0x46',
        'STM32F413xxx/423xxx':'0x4A','STM32F413/F423':'0x4A',
        'STM32F42xxx/43xxx':'0x38','STM32F42/F43':'0x38',
        'STM32F42xxx/F43xxx':'0x38',
        'STM32F446xx':'0x3C',
        'STM32F469xx/479xx':'0x44',
        'STM32F72xxx/73xxx':'0x49',
        'STM32F74xxx/75xxx':'0x45',
        'STM32F76xxx/77xxx':'0x49',
        'STM32G07xxx/8xxx':'0b1010001x',
        'STM32H74xxx/75xxx':'0x4E','STM32H7xx':'0x4E',
        'STM32L412xx/L422xx':'0b1010010x',
        'STM32L43xxx/44xxx':'0x48',
        'STM32L45xxx/46xxx':'0x4A',
        'STM32L47xxx/48xxx':'0x43',
        'STM32L496xx/4A6xx':'0x4C'
        }

      def Extraire_I2C_ADD(self):
          """
             how it works :
             -->if detected mcu name matches one item form list_add this script provide mcu addresse based on it's name
             -->special case H7 beacause MCU name is differed(integrated probe or externale probe )
          """
          for item in self.all_mcu  :
                if 'H7' in item :
                    if item[0:item.find('(')] in self.list_add :
                       self.add.append(self.list_add[item[0:item.find('(')]])

                elif item in self.list_add :
                    self.add.append(self.list_add[item])

          return self.add





