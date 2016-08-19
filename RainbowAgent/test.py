import commands
import  os
import subprocess



shell_command = "sudo dmidecode -q -t memory"

{'MemDevice_Not Specified':
     set([('Manufacturer', ' Not Specified'), ('Locator', ' DIMM B'), ('Data Width', ' Unknown'),
          ('Size', ' No Module Installed'), ('Rank', ' Unknown'), ('Asset Tag', ' Not Specified'), ('Total Width', ' Unknown'), ('Part Number', ' Not Specified'), ('Serial Number', ' Not Specified'), ('Type', ' Unknown'), ('Speed', ' Unknown')]), 'MemArray': set([('Location', ' System Board Or Motherboard'), ('Maximum Capacity', ' 16 GB'), ('Use', ' System Memory')]), 'MemDevice_B58C8290': set([('Size', ' 8192 MB'), ('Locator', ' DIMM A'), ('Rank', ' 2'), ('Data Width', ' 64 bits'), ('Type', ' DDR3'), ('Manufacturer', ' Hynix/Hyundai'), ('Total Width', ' 64 bits'), ('Serial Number', ' B58C8290'), ('Asset Tag', ' 9876543210'), ('Part Number', ' HMT41GS6BFR8A-PB  '), ('Speed', ' 1600 MHz')])}