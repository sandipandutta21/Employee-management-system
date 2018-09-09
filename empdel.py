#!/bin/sh
# empqry_and_del.py

import subprocess
from tkinter import *
from tkinter import messagebox
from datetime import datetime
import sys
import mysql.connector
import MySQLdb as my
import pandas as pd

def get_values():              # has to be defined before button object command where it is called

        eno = empno_txt.get()
        qry_database(int(eno))
                       
def chkempno(event):
    try:
        eno = empno_txt.get()
        if( eno.isdigit()):
            pass
        else:
            raise ValueError
    except ValueError:
        disp_empno_error()
        
def reset():
        
    empno_txt.delete(0, END)
    
    empname_txt.config(state=NORMAL)
    empname_txt.delete(0, END)
    empname_txt.config(state=DISABLED)
    
    chk.deselect()
    gender_selected.set(3)
    
    add1.config(state=NORMAL)
    add1.delete(0, END)
    add1.config(state=DISABLED)
    add2.config(state=NORMAL)
    add2.delete(0, END)
    add2.config(state=DISABLED) 
    add3.config(state=NORMAL)
    add3.delete(0, END)
    add3.config(state=DISABLED)

    pin.config(state=NORMAL)
    pin.delete(0, END)
    pin.config(state=DISABLED)

    empcity_txt.config(state=NORMAL)
    empcity_txt.delete(0, END)
    empcity_txt.config(state=DISABLED)

    birth_txt.config(state=NORMAL)
    birth_txt.delete(0, END)
    birth_txt.config(state=DISABLED)

    basic_txt.config(state=NORMAL)
    basic_txt.delete(0, END)
    basic_txt.config(state=DISABLED)

    conv_txt.config(state=NORMAL)
    conv_txt.delete(0,END)
    conv_txt.config(state=DISABLED)
    
def disp_empno_error():
    messagebox.showerror('Empno must be Numeric', 'Empno must be Numeric')
    empno_txt.focus()


def qry_database(eno):

    try:
            
            enter1 = input('Enter your username')
            enter2 = input('Enter your password')
            conn = mysql.connector.connect(user=enter1 ,password= enter2, host='127.0.0.1', database='testdb')
            # Check if connected
            if( conn.is_connected()):
               print("Connected to MySQL Database")    
            else:
               print('Error in connecting MySQL DB')

            cur = conn.cursor()
            sql_str = 'select * from empmaster where empno =' + str(eno)
           
              
            df = pd.read_sql(sql_str, conn)     # Reading from MySQL DB via Pandas Library
            
            if( len(df) == 0):              # If there is no record matching then len of DF would be zero
                print('No Rows Selected')
                messagebox.showerror('Error : No Rows.', 'No Record for this Empno')    
            else:
                for index,row in df.iterrows():
                    print(row['empno'])
                    print(row['empname'])
                                        
                    name=StringVar()
                    name.set(row['empname']) 
                    empname_txt.config(textvariable=name, state=DISABLED)
                    
                    print(row['married_status'])
                    x = row['married_status']
                     
                    if( x==1):        
                        chk.select()    
                    else:
                        chk.deselect()               
                    
                    print(row['gender'])

                    emp_gender = row['gender']
                    if( emp_gender == 1):
                          male_radbtn.select()  
                    else:
                          female_radbtn.select()  
 
                    print(row['address'])
                    full_add = row['address']
                    add_1=StringVar()
                    add_2=StringVar()
                    add_3=StringVar()
                    add_1.set(full_add[0:30])
                    add_2.set(full_add[30:60])
                    add_3.set(full_add[60:90])
                    
                    add1.config(textvariable=add_1, state=DISABLED)
                    add2.config(textvariable=add_2, state=DISABLED)
                    add3.config(textvariable=add_3, state=DISABLED)
                    
                    print(row['pin'])
                    pincode = StringVar()
                    pincode.set(row['pin'])
                    pin.config(textvariable=pincode, state=DISABLED)
                    
                    print(row['city'])
                    cityname = StringVar()
                    cityname.set(row['city'])
                    empcity_txt.config(textvariable=cityname, state=DISABLED)
                    
                    print(row['birth_dt'])
                    birth_dt = StringVar()
                    dt = str(row['birth_dt'])
                    yy,mm,dd = dt.split('-')                            # Coverting date from yyyy-mm-dd to dd/mm/yyyy
                    ddmmyy = dd+'/'+mm+'/'+yy
                    birth_dt.set(ddmmyy)                        
                    birth_txt.config(textvariable=birth_dt, state=DISABLED)
                    
                    print(row['basic'])
                    basic_amt = IntVar()
                    basic_amt.set(row['basic'])
                    basic_txt.config(textvariable=basic_amt, state=DISABLED)
                    
                                      
                    print(row['conv'])
                    conv_amt = IntVar()
                    conv_amt.set(row['conv'])
                    conv_txt.configure(textvariable=conv_amt, state=DISABLED) 
                    
                    
            cur.close()
            conn.close()          
                   
                 
    except  mysql.connector.Error as e:
            print("Error code:", e.errno)         # error number
            print("SQLSTATE value:", e.sqlstate)   # SQLSTATE value
            print("Error message:", e.msg)         # error message
            print("Error:", e)                   # errno, sqlstate, msg values
            s = str(e)
            print("Error:", s)                   # errno, sqlstate, msg values     

def delete_rec():
            
    try:
            eno = empno_txt.get()
            qry_database(int(eno))
            conn = mysql.connector.connect(user=' ',password=' ', host='127.0.0.1', database='testdb')
            # Check if connected
            if( conn.is_connected()):
                   messagebox.showinfo('DB Connected', 'Connected to MySQL Database')        
            else:
                   messagebox.showerror('Error in connecting MySQL DB', 'Could no connect to MySQL DB')
            cur = conn.cursor()
            sql_str = 'delete from empmaster where empno = (%s)' 

            reply = messagebox.askquestion("Delete", "Are You Sure?", icon='warning')
            
            if(reply == 'yes'):
                        args = (eno)  
                        # Execute the SQL query
                        cur.execute(sql_str % args)
                        conn.commit()
                        print("Deleted")
            else:
                        pass
                        reset()
                        empno_txt.focus()           # Always focus from empno field

            cur.close()
            conn.close()          
                                  
    except  mysql.connector.Error as e:
            print("Error code:", e.errno)         # error number
            print("SQLSTATE value:", e.sqlstate)   # SQLSTATE value
            print("Error message:", e.msg)         # error message
            print("Error:", e)                   # errno, sqlstate, msg values
            s = str(e)
            print("Error:", s)                   # errno, sqlstate, msg values     

                      
 
#----------------------------------------------------------------
window = Tk()
window.title("Welcome to Employee Master Delete Row App")
window.geometry('900x500')      # width x height

# Labels to display on screen
lbl = Label(window, text='Delete Employee Details', font=('Arial Bold', 10, 'underline'), fg='blue', bg='light grey')
lbl.grid(column=0, row=0)

# Entry fields - textfields
empno_lbl=Label(window, text='Empno:')
empno_lbl.grid(column=0, row=2)    
empno_txt = Entry(window, width=6)        
empno_txt.grid(column=1, row=2)
empno_txt.bind("<FocusOut>", chkempno)                  # validate when mouse focus out of the field
empno_txt.bind("<Return>", chkempno)                    # Validate when the Enter key is pressed

# Empname column
empname_lbl = Label(window, text='Employee Name :')
empname_lbl.grid(column=2, row=2)
empname_txt = Entry(window, width=30)
empname_txt.grid(column=3, row=2)

empno_txt.focus()           # Always focus from empno field

# Married status Check button. Either checked or unchecked
empmarried_lbl = Label(window, text='Married :')
empmarried_lbl.grid(column=5, row=2)
empmarried_state = IntVar()                             # Use IntVar() in Python. Where 0 is unchecked and 1 is checked 
empmarried_state.set(0)
chk = Checkbutton(window, text='', var=empmarried_state, state=DISABLED)
chk.grid(column=6, row=2)

# Radio buttons. to enter Gender of the employee. At a time one selection ( male/female)
gender_lbl = Label(window, text='Select Gender :')
gender_lbl.grid(column=0, row=6)
gender_selected = IntVar()
male_radbtn = Radiobutton(window, text='Male :', value=1, variable=gender_selected, state=DISABLED)
female_radbtn = Radiobutton(window, text='Female :', value=2, variable=gender_selected, state=DISABLED)
male_radbtn.grid(column=1, row=6)
female_radbtn.grid(column=2, row=6)

# Address details
address_lbl = Label(window, text='Residential Address :')
address_lbl.grid(column=0, row=7)
add1 = Entry(window, width=30)
add1.grid(column=1, row=7)
add2 = Entry(window, width=30)
add2.grid(column=1, row=8)
add3 = Entry(window, width=30)
add3.grid(column=1, row=9)

# Pin code details
pin_lbl = Label(window, text='Pin :')
pin_lbl.grid(column=2, row=7)
pin = Entry(window, width=7)
pin.grid(column=3, row=7)

# City details
empcity_lbl = Label(window, text='City :')
empcity_lbl.grid(column=4, row=7)
city=StringVar()
city.set('Kolkata')
empcity_txt = Entry(window, width=10, textvariable=city)
empcity_txt.grid(column=5, row=7)

# Date of birth
birth_lbl = Label(window, text='Date of Birth (dd/mm/yyyy):')
birth_lbl.grid(column=2, row=9)
birth_txt = Entry(window, width=10)
birth_txt.grid(column=3, row=9)

# Basic salary
basic_lbl = Label(window, text='Basic :')
basic_lbl.grid(column=2, row=13)
basic_sal = IntVar()
basic_sal.set(0)
basic_txt = Entry(window, width=8, textvariable=basic_sal)
basic_txt.grid(column=3, row=13)

# Conveyance Allowance
conv_lbl = Label(window, text='Conv. Allowance :')
conv_lbl.grid(column=4, row=13)
conv_allow = IntVar()
conv_allow.set(0)
conv_txt = Entry(window, width=8, textvariable=conv_allow)
conv_txt.grid(column=5, row=13)

# Button widgets

qry_btn = Button(window, text='Query Row', bg='Orange', fg='black', command=get_values)
qry_btn.grid(column=1, row=15)

delete_btn = Button(window, text='Delete Row', bg='Orange', fg='black', command=delete_rec)
delete_btn.grid(column=2, row=15)

reset_btn = Button(window, text='Reset', bg='orange', fg='black', command=reset)
reset_btn.grid(column=3, row=15)

ext_btn = Button(window, text='Exit', bg='orange', fg='black', command=window.destroy)
ext_btn.grid(column=4, row=15)

window.mainloop()
 
