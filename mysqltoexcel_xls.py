#!/bin/sh
# mysqltoexcel_xls.py
# xls file

import mysql.connector
import MySQLdb as my
import pandas as pd
from   tkinter import *
from   tkinter import messagebox
import os
from pandas import ExcelWriter

try:
    
    conn = mysql.connector.connect(user=' ',password=' ', host='127.0.0.1', database='testdb')
    # Check if connected
    if( conn.is_connected()):
       print("Connected to MySQL Database")    
    else:
       print('Error in connecting MySQL DB')

    cur = conn.cursor()
    sql_str = 'select empno, empname, birth_dt, basic, conv, city from empmaster' 
    #print(sql_str)
              
    empdf = pd.read_sql(sql_str, conn)     # Reading from MySQL DB via Pandas Library
    empdf = empdf.set_index('empno')

    if( len(empdf) == 0):              # If there is no record matching then len of DF would be zero
       print('No Rows Selected')
       messagebox.showerror('Error : No Rows.', 'No Record for this Empno')
    else:
       print(empdf)
       writer = pd.ExcelWriter('home/user_name/Documents/empmaster.xls')
       empdf.to_excel(writer,'Sheet1')
       writer.save()
       
    cur.close()
    conn.close()
    messagebox.showinfo('Excel Conversion', 'MySQL/Pandas DF converted to Excel')
   
    
except  mysql.connector.Error as e:
    print("Error code:", e.errno)         # error number
    print("SQLSTATE value:", e.sqlstate)   # SQLSTATE value
    print("Error message:", e.msg)         # error message
    print("Error:", e)                   # errno, sqlstate, msg values
    s = str(e)
    print("Error:", s)                   # errno, sqlstate, msg values     
           
