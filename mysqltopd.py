#!/bin/sh
# mysqltopd.py

import mysql.connector
import MySQLdb as my
import pandas as pd
from   tkinter import *
from   tkinter import messagebox
import os

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
              
    df = pd.read_sql(sql_str, conn)     # Reading from MySQL DB via Pandas Library
    df=df.set_index('empno')

    if( len(df) == 0):              # If there is no record matching then len of DF would be zero
       print('No Rows Selected')
       messagebox.showerror('Error : No Rows.', 'No Record for this Empno')
    else:
       print(df)

    cur.close()
    conn.close()
    os.system("pause")
    
except  mysql.connector.Error as e:
    print("Error code:", e.errno)         # error number
    print("SQLSTATE value:", e.sqlstate)   # SQLSTATE value
    print("Error message:", e.msg)         # error message
    print("Error:", e)                   # errno, sqlstate, msg values
    s = str(e)
    print("Error:", s)                   # errno, sqlstate, msg values     
           
