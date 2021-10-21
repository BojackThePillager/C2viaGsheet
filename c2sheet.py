import csv
import json
import gspread
import os
import subprocess
import pprint
import time

#insert the path and filename for the json service account key
gc = gspread.service_account(filename='')

#insert the unique sheet key found in the URL for the google spreadsheet
sh = gc.open_by_key('')
worksheet = sh.sheet1

def next_available_row(worksheet):
    str_list = list(filter(None, worksheet.col_values(1)))
    return str(len(str_list)+1)

#get next row to operate on
next_row = next_available_row(worksheet)
target_row = int(next_row)
target_row = target_row - 1
next_row = "A" + str(target_row)

#get command
my_cmd = worksheet.acell(next_row).value
print(my_cmd)
print("Executing...", my_cmd)

#run the command from the spreadsheet
p = subprocess.run([my_cmd], shell=True, stdout=subprocess.PIPE)
cmd_output = p.stdout 
print(cmd_output.decode())

#record time
named_tuple = time.localtime() # get struct_time
exec_time = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)

#record in log
logWrite = exec_time
worksheet.update_cell(target_row, 2, str(cmd_output.decode()))
worksheet.update_cell(target_row, 3, exec_time)
