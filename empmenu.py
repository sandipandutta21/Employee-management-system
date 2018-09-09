#!/bin/sh
# empmenu.py 

from tkinter import *
import sys
import os
import subprocess
from tkinter import messagebox
from datetime import datetime
import mysql.connector
import MySQLdb as my
import pandas as pd
import subprocess
import empentry 
class MySQLDemo:

    # Constructor
    def __init__(self, root):

        self.main_lbl=Label(root, text='MySQL Database Maintenance with PythonGUI/Tkinter and Pandas Lib', fg='blue', font=('Arial', -15, 'bold underline'))
        self.main_lbl.place(x=200, y=250)
       
        # Create menubar
        self.menubar=Menu(root)
        root.config(menu=self.menubar)            # attach the menubar to root
        # Now create Single matrix operation menu
        self.mysql_menu=Menu(root, tearoff=0)
        # Now create menu items under singlematrix_menu 
        self.mysql_menu.add_command(label='Add Record to MySQL', command=self.emp_entry)
        self.mysql_menu.add_command(label='Display Record from MySQL', command=self.emp_qry)
        self.mysql_menu.add_command(label='Delete the Record from MySQL', command=self.emp_del)
        self.mysql_menu.add_command(label='Update the Record from MySQL', command=self.emp_upd)
        
        # Now add a separator
        self.mysql_menu.add_separator()
        # Now create a Exit menu
        self.mysql_menu.add_command(label='Exit', command=root.destroy)
        # Now add the 'singlematrix_menu' with a name 'Emp Master Maintenance under MySQL DB' under 'menubar'
        self.menubar.add_cascade(label='MySQL DB Maintenance', menu=self.mysql_menu)

        ###### #############
        # Now create Data Display in Pandas operation menu
        self.pandas_menu=Menu(root, tearoff=0)
        # Now add the 'Display data in Pandas' with a name 'Display data in Pandas' under 'menubar'
        self.menubar.add_cascade(label='Convert Data into Pandas', menu=self.pandas_menu)
        self.pandas_menu.add_command(label='Convert Data into Pandas', command=self.pandas_conv)
     
        ###### #############
        # Now create Data Display in Excel operation menu
        self.excel_menu=Menu(root, tearoff=0)
        # Now add the 'Display data in Excel' with a name 'Display data in Excel' under 'menubar'
        self.menubar.add_cascade(label='Convert Data into Microsoft Excel', menu=self.excel_menu)
        self.excel_menu.add_command(label='Convert Data into Excel/XLS', command=self.excelxls_conv)
        self.excel_menu.add_command(label='Convert Data into Excel/XLSX', command=self.excelxlsx_conv)
        
    def emp_entry(self):

        def get_values():              # has to be defined before button object command where it is called

            empno_str = empno_txt.get()
            empname_str = empname_txt.get()
            empmarried_str = empmarried_state.get()         #  0 or 1. 0 for unmarried, 1 for married
            gender_str = gender_selected.get()              #  1 for male, 2 for female    
            add1_str = add1.get()
            add2_str = add2.get()
            add3_str = add3.get()
            fulladd_str = add1_str + ' ' + add2_str + ' ' + add3_str 
            pin_str = pin.get()
            empcity_str = empcity_txt.get()
        
            dt = birth_txt.get()
            birth_dt = datetime.strptime(dt,'%d/%m/%Y')     # strptime() parses a time string according to a format.
         
            basic = float(eval(basic_txt.get()))
            if( basic <= 0):
                disp_basic_error()
            
            conv = float(eval(conv_txt.get()))       
            if( conv <= 0):
                disp_conv_error()
            
        # Print on Python shells
        # print(empno_str. empname_str, empmarried_str)       # 0 or 1. 0 for unmarried, 1 for married
        # print(gender_str)           #  1 for male, 2 for female       
        # print(fulladd_str, pin_str, empcity_str, birth_dt)            
        # print(basic)            # type(basic) shows 'int', so converted to float as MySQL DB fields are decimal
        # print(conv)             # type(conv) shows 'int', converted to float

        # Call Function to insert record into MySQL DB
            add_database(empno_str, empname_str, empmarried_str, gender_str, fulladd_str, pin_str, empcity_str, birth_dt, basic, conv)
        
                        
        def chkdate(event):
            try:
                dt = birth_txt.get()
                dt_start = datetime.strptime(dt,'%d/%m/%Y')    # strptime() parses a time string according to a format.
 
            except ValueError:
                disp_date_error()

        def chkempno(event):
            try:
                eno = empno_txt.get()
                if( eno.isdigit()):
                    pass
                else:
                    raise ValueError
            except ValueError:
             disp_empno_error()
        
        def chkbasic(event):
            try:
                basic = basic_txt.get()
                if( basic.isdigit()):           
                    pass
                else:                   # isdigit is False when atleast one char is non digit or values starts with '-'
                    raise ValueError
            except ValueError:
                disp_basic_error()

        def chkconv(event):
            try:
                conv = conv_txt.get()
                if( conv.isdigit()):
                    pass
                else:
                    raise ValueError
            except ValueError:
                disp_conv_error()

        def reset():
            empno_txt.delete(0, END) 
            empname_txt.delete(0, END)
            chk.deselect()
            gender_selected.set(3)    # To reset a Radio button. set the value to a var which is not in your defined range. Here it is 3, as 1 = male, 2 = female
     
            add1.delete(0, END)
            add2.delete(0, END)
            add3.delete(0, END)
            pin.delete(0, END)
            empcity_txt.delete(0, END)
            birth_txt.delete(0, END)
            basic_txt.delete(0, END)
            conv_txt.delete(0,END)
    
        def disp_basic_error():
            messagebox.showerror('Basic Value Error', 'Basic Must be numeric and > 0')
            basic_txt.focus()
    
        def disp_conv_error():
            messagebox.showerror('Conv. Allowance Value Error', 'Conv. Allowance must be numeric and > 0')
            conv_txt.focus()
    
        def disp_empno_error():
            messagebox.showerror('Empno must be Numeric', 'Empno must be Numeric')
            empno_txt.focus()
    
        def disp_date_error():
            messagebox.showerror('Invalid Date Format', 'Date must be in dd/mm/yyyy')
            birth_txt.focus()

        def add_database(eno, name, married_stat, gender_stat, address, pin, city, birth_dt, basic, conv):
            try:
            
                    conn = mysql.connector.connect(user=' ',password='  ', host='127.0.0.1', database='testdb')
            # Check if connected
                    if( conn.is_connected()):
               # print("Connected to MySQL Database")
                        messagebox.showinfo('DB Connected', 'Connected to MySQL Database')
                    else:
                        messagebox.showerror('Error in connecting MySQL DB', 'Could no connect to MySQL DB')

                    cur = conn.cursor()
                    sql_str = "insert into empmaster(empno, empname, married_status, gender, address, pin, city, birth_dt, basic, conv)" \
               "values('%s', '%s', %d, %d, '%s', '%s', '%s', '%s', %f, %f)"
                    args = (eno, name, married_stat, gender_stat, address, pin, city, birth_dt, basic, conv) 
   
            # Execute the SQL query
                    cur.execute(sql_str % args)
            # print(cur.rowcount)                       cur.rowcount gives no. of records affected due to DML statements
            # save the changes
                    conn.commit()
                    comm_mesg = str(cur.rowcount) + " Record Committed"
                    messagebox.showinfo('DB Insert Success' , comm_mesg)
            # print("1 Row inserted")           for Python shell printout

            except  mysql.connector.errors.IntegrityError: 
                    conn.rollback()  # Rolback if there is any error           
                    messagebox.showerror('Error in Inserting Record in MySQL DB', 'Could no commit data. Empno already Exists')       
           
            finally:
                cur.close()
                conn.close()

 
#----------------------------------------------------------------
        window = Tk()
        window.title("Welcome to Employee Master Data Entry App")
        window.geometry('1000x500')      # width x height

# Labels to display on screen
        lbl = Label(window, text='Add Employee Details', font=('Arial Bold', 10, 'underline'), fg='blue', bg='light grey')
        lbl.grid(column=0, row=0)

# Entry fields - textfields
        empno_lbl=Label(window, text='Empno:')
        empno_lbl.grid(column=0, row=2)    
        empno_txt = Entry(window, width=6)        
        empno_txt.grid(column=1, row=2)
        empno_txt.bind("<FocusOut>", chkempno)               # validate when mouse focus out of the field
        empno_txt.bind("<Return>", chkempno)


        empname_lbl = Label(window, text='Employee Name :')
        empname_lbl.grid(column=2, row=2)
        empname_txt = Entry(window, width=30)
        empname_txt.grid(column=3, row=2)

        empno_txt.focus()           # Always focus from empno field

# Married status Check button. Either checked or unchecked
        empmarried_lbl = Label(window, text='Married :')
        empmarried_lbl.grid(column=5, row=2)
        empmarried_state = IntVar()                    # Use IntVar() in Python. Where 0 is unchecked and 1 is checked 
        empmarried_state.set(0)
        chk = Checkbutton(window, text='', var=empmarried_state)
        chk.grid(column=6, row=2)

# Radio buttons. to enter Gender of the employee. At a time one selection ( male/female)
        gender_lbl = Label(window, text='Select Gender :')
        gender_lbl.grid(column=0, row=6)
        gender_selected = IntVar()
        male_radbtn = Radiobutton(window, text='Male :', value=1, variable=gender_selected)
        female_radbtn = Radiobutton(window, text='Female :', value=2, variable=gender_selected)
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
        birth_txt.bind("<FocusOut>", chkdate)               # validate when mouse focus out of the field
        birth_txt.bind("<Return>", chkdate)                 # validate when the return key is pressed

# Basic salary
        basic_lbl = Label(window, text='Basic :')
        basic_lbl.grid(column=2, row=13)
        basic_sal = IntVar()
        basic_sal.set(0)
        basic_txt = Entry(window, width=6, textvariable=basic_sal)
        basic_txt.grid(column=3, row=13)
        basic_txt.bind("<FocusOut>", chkbasic)
        basic_txt.bind('<Return>', chkbasic)

# Conveyance Allowance
        conv_lbl = Label(window, text='Conv. Allowance :')
        conv_lbl.grid(column=4, row=13)
        conv_allow = IntVar()
        conv_allow.set(0)
        conv_txt = Entry(window, width=6, textvariable=conv_allow)
        conv_txt.grid(column=5, row=13)
        conv_txt.bind("<FocusOut>", chkconv)
        conv_txt.bind('<Return>', chkconv)

# Button widgets 
        save_btn = Button(window, text='Save Data', bg='Orange', fg='black', command=get_values)
        save_btn.grid(column=1, row=15)

        reset_btn = Button(window, text='Reset', bg='orange', fg='black', command=reset)
        reset_btn.grid(column=2, row=15)

        ext_btn = Button(window, text='Exit', bg='orange', fg='black', command=window.destroy)
        ext_btn.grid(column=3, row=15)

        window.mainloop()
 

    
    def emp_qry(self):    
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
            
                    conn = mysql.connector.connect(user=' ',password='  ', host='127.0.0.1', database='testdb')
                    # Check if connected
                    if( conn.is_connected()):
                       print("Connected to MySQL Database")    
                    else:
                       print('Error in connecting MySQL DB')

                    cur = conn.cursor()
                    sql_str = 'select * from empmaster where empno =' + str(eno)
                    print(sql_str)
              
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
           
 
        #----------------------------------------------------------------
        window = Tk()
        window.title("Welcome to Employee Master Query App")
        window.geometry('900x500')      # width x height

        # Labels to display on screen
        lbl = Label(window, text='Query Employee Details', font=('Arial Bold', 10, 'underline'), fg='blue', bg='light grey')
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
        save_btn = Button(window, text='Query Data', bg='Orange', fg='black', command=get_values)
        save_btn.grid(column=1, row=15)

        reset_btn = Button(window, text='Reset', bg='orange', fg='black', command=reset)
        reset_btn.grid(column=2, row=15)

        ext_btn = Button(window, text='Exit', bg='orange', fg='black', command=window.destroy)
        ext_btn.grid(column=3, row=15)

        window.mainloop()
 


    def emp_del(self):
        import empdel

    def emp_upd(self):
        import empupd
                
    def pandas_conv(self):
        import mysqltopd
    
    def excelxls_conv(self):
        import mysqltoexcel_xls
	
   
    def excelxlsx_conv(self):
       	import mysqltoexcel_xlsx
#=====================================================================================================

   
root=Tk()
root.title('Python MySQL Database Maintenance with Pandas and TkInter GUI')

obj=MySQLDemo(root)
root.geometry('800x600')
root.mainloop()

                                 
        
        
        
        
                 
