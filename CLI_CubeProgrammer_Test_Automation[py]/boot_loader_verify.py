#! /usr/bin/env python3
import platform
from data_operation import Op


OS=platform.system()
if OS =='Windows':
    timeout='timeout /t 1 /nobreak '
elif OS =='Linux':
    timeout="timeout 1s bash "

"""
  This module provide an interface to verify bootloader activation in every connected board with stlinv-2
     --> It calls bootloader_verification function from data_operation module
     --> It permits to work on every board with embedded SWD_V2 ,
         one limitation to be handled is when stlink-v3 is embedded we can't be sure that bootloader is activated with classic methode (compare add 0 to address 0x08000000,So special treatement has to be done.
          >> a special treatment to H7 has to be added
               #C:\Program Files\STMicroelectronics\STM32Cube\STM32CubeProgrammer\bin>STM32_Programmer_CLI.exe -c port=swd  -ob displ
               #Boot address Option Bytes:
               #BOOT_CM7_ADD0: 0x1FF0  (0x1FF00000)
               #BOOT_CM7_ADD1: 0x1FF0  (0x1FF00000)
"""


if __name__=='__main__' :
    Op().bootloader_verification()
