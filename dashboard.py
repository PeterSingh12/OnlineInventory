from tkinter import * #import all the classes and functions of tkinter module
from employees import employee_form
from supplier import supplier_form
from category import category_form
from products import product_form
from sales import sales_form
from employees import connect_database
from tkinter import messagebox
import time


def logout(window):
    confirm = messagebox.askyesno("Logout", "Are you sure you want to logout?")
    if confirm:
        window.destroy()

def update():
    cursor,connection=connect_database()
    if not cursor or not connection:
        return
    cursor.execute('use inventory_system')
    cursor.execute('SELECT * from employee_data')
    emp_records=cursor.fetchall()
    totalemp_count_label.config(text=len(emp_records))
    
    cursor.execute('SELECT * from supplier_data')
    sup_records=cursor.fetchall()
    totalsup_count_label.config(text=len(sup_records))
    
    cursor.execute('SELECT * from category_data')
    cat_records=cursor.fetchall()
    totalcat_count_label.config(text=len(cat_records))
    
    cursor.execute('SELECT * from product_data')
    prod_records=cursor.fetchall()
    totalprod_count_label.config(text=len(prod_records))
    
    cursor.execute('SELECT * from sales_data')
    sales_records=cursor.fetchall()
    totalsales_count_label.config(text=len(sales_records))
    
    date_time=time.strftime('%I:%M:%S %p on %A, %B %d, %Y')
    subtitleLabel.config(text=f'Welcome Admin\t\t\t\t\t\t\t\t\t\t {date_time}')
    subtitleLabel.after(1000,update)

def tax_window():
    def save_tax():
        value=tax_count.get()
        cursor,connection=connect_database()
        if not cursor or not connection:
            return
        cursor.execute('use inventory_system')
        cursor.execute('CREATE TABLE IF NOT EXISTS tax_table (id INT primary key, tax DECIMAL(5,2))')
        cursor.execute('SELECT id from tax_table WHERE id=1')
        if cursor.fetchone():
            cursor.execute('UPDATE tax_table SET tax=%s WHERE id=1',value)
        else:
            cursor.execute('INSERT INTO tax_table (id,tax) VALUES(1,%s)',value)
        connection.commit()
        messagebox.showinfo('Success',f'Tax is set to {value}% and saved successfully.',parent=tax_root)
        
        
    tax_root=Toplevel()
    tax_root.title('Tax window')
    tax_root.geometry('300x200')
    tax_root.grab_set()
    tax_percentage=Label(tax_root,text='Enter Tax Percentage(%)',font=('arial',12))
    tax_percentage.pack(pady=10)
    tax_count=Spinbox(tax_root,from_=0,to=100,font=('arial',12))
    tax_count.pack(pady=10)
    save_button=Button(tax_root,text='Save',font=('arial',12,'bold'),bg='#4d636d',fg='white',width=10,command=save_tax)
    save_button.pack(pady=20)


#GUI Part
window=Tk() #creates dashboard window by creating an obj of tk class

window.title('Dashboard')
window.geometry('1270x668+0+0') #+0+0 means I want it to fit to the screen. dist frm x & y axis is 0
window.resizable(0,0)  #false values 4 both height & width to not allow resizing of the window
window.config(bg='white')

bgImage=PhotoImage(file='inventory.png') #PhotoImage class is used to import image file
titleLabel=Label(window,image=bgImage,compound=LEFT,text=' Inventory Management System',font=('times new roman',40,'bold'),bg='#010c48',fg='white',anchor='w',padx=20)
titleLabel.place(x=0,y=0,relwidth=1) #anywhere, place is used to actually see the stuff on screen. Relwidth=1 makes the text take full width of the screen

logoutButton=Button(window,text='Logout',font=('times new roman',20,'bold'),fg='#010c48',command=lambda:logout(window))
logoutButton.place(x=1100,y=10)

subtitleLabel=Label(window,text='Welcome Admin\t\t Date: 06-04-2025\t\t Time: 11:05 am',font=('times new roman',15),bg='#4d636d',fg='white')
subtitleLabel.place(x=0,y=70,relwidth=1)

leftFrame=Frame(window) #Frame class to create a frame as seen on the left side
leftFrame.place(x=0,y=102,width=200,height=555)

logoImage=PhotoImage(file='logoo.png')
imageLabel=Label(leftFrame,image=logoImage) #not using root here cuz we want our images inside leftFrame
imageLabel.pack() #pack works the same as place but it is used in placing things one below the other

menuLabel=Label(leftFrame,text='Menu',font=('times new roman',20),bg='#009688')
menuLabel.pack(fill=X) #to fill the x axis

employee_icon=PhotoImage(file='man.png')
employee_button=Button(leftFrame,image=employee_icon,compound=LEFT,text=' Employees',font=('times new roman',20,'bold'),anchor='w',padx=10,command=lambda :employee_form(window))
employee_button.pack(fill=X)

supplier_icon=PhotoImage(file='supplier.png')
supplier_button=Button(leftFrame,image=supplier_icon,compound=LEFT,text=' Suppliers',font=('times new roman',20,'bold'),anchor='w',padx=10,command=lambda:supplier_form(window))
supplier_button.pack(fill=X)

category_icon=PhotoImage(file='categories.png')
category_button=Button(leftFrame,image=category_icon,compound=LEFT,text=' Categories',font=('times new roman',20,'bold'),anchor='w',padx=10,command=lambda:category_form(window))
category_button.pack(fill=X)

products_icon=PhotoImage(file='order.png')
products_button=Button(leftFrame,image=products_icon,compound=LEFT,text=' Products',font=('times new roman',20,'bold'),anchor='w',padx=10,command=lambda:product_form(window))
products_button.pack(fill=X)

sales_icon=PhotoImage(file='growth.png')
sales_button=Button(leftFrame,image=sales_icon,compound=LEFT,text=' Sales',font=('times new roman',20,'bold'),anchor='w',padx=10,command=lambda:sales_form(window))
sales_button.pack(fill=X)

tax_icon=PhotoImage(file='taxes.png')
tax_button=Button(leftFrame,image=tax_icon,compound=LEFT,text=' Tax',font=('times new roman',20,'bold'),anchor='w',padx=10,command=tax_window)
tax_button.pack(fill=X)

exit_icon=PhotoImage(file='exit.png')
exit_button=Button(leftFrame,image=exit_icon,compound=LEFT,text=' Exit',font=('times new roman',20,'bold'),anchor='w',padx=10)
exit_button.pack(fill=X)

emp_frame=Frame(window,bg='#2C3E50',bd=3,relief=RIDGE)
emp_frame.place(x=400,y=125,height=170,width=280)
totalemp_icon=PhotoImage(file='division.png')
totalemp_icon_label=Label(emp_frame,image=totalemp_icon,bg='#2C3E50')
totalemp_icon_label.pack() #pack cuz we want one thing below the other: pic, Total Employees,10

totalemp_label=Label(emp_frame,text='Total Employees',bg='#2C3E50',fg='white',font=('times new roman',15))
totalemp_label.pack()

totalemp_count_label=Label(emp_frame,text='0',bg='#2C3E50',fg='white',font=('times new roman',30))
totalemp_count_label.pack()

sup_frame=Frame(window,bg='#8E44AD',bd=3,relief=RIDGE)
sup_frame.place(x=800,y=125,height=170,width=280)
totalsup_icon=PhotoImage(file='supp.png')
totalsup_icon_label=Label(sup_frame,image=totalsup_icon,bg='#8E44AD')
totalsup_icon_label.pack() #pack cuz we want one thing below the other: pic, Total Employees,10

totalsup_label=Label(sup_frame,text='Total Suppliers',bg='#8E44AD',fg='white',font=('times new roman',15))
totalsup_label.pack()

totalsup_count_label=Label(sup_frame,text='0',bg='#8E44AD',fg='white',font=('times new roman',30))
totalsup_count_label.pack()

cat_frame=Frame(window,bg='#27AE60',bd=3,relief=RIDGE)
cat_frame.place(x=400,y=310,height=170,width=280)
totalcat_icon=PhotoImage(file='cat.png')
totalcat_icon_label=Label(cat_frame,image=totalcat_icon,bg='#27AE60')
totalcat_icon_label.pack() #pack cuz we want one thing below the other: pic, Total Employees,10

totalcat_label=Label(cat_frame,text='Total Categories',bg='#27AE60',fg='white',font=('times new roman',15))
totalcat_label.pack()

totalcat_count_label=Label(cat_frame,text='0',bg='#27AE60',fg='white',font=('times new roman',30))
totalcat_count_label.pack()

prod_frame=Frame(window,bg='blue',bd=3,relief=RIDGE)
prod_frame.place(x=800,y=310,height=170,width=280)
totalprod_icon=PhotoImage(file='prod.png')
totalprod_icon_label=Label(prod_frame,image=totalprod_icon,bg='blue')
totalprod_icon_label.pack() #pack cuz we want one thing below the other: pic, Total Employees,10

totalprod_label=Label(prod_frame,text='Total Products',bg='blue',fg='white',font=('times new roman',15))
totalprod_label.pack()

totalprod_count_label=Label(prod_frame,text='0',bg='blue',fg='white',font=('times new roman',30))
totalprod_count_label.pack()

sales_frame=Frame(window,bg='#E74C3C',bd=3,relief=RIDGE)
sales_frame.place(x=600,y=495,height=170,width=280)
totalsales_icon=PhotoImage(file='svg.png')
totalsales_icon_label=Label(sales_frame,image=totalsales_icon,bg='#E74C3C')
totalsales_icon_label.pack() #pack cuz we want one thing below the other: pic, Total Employees,10

totalsales_label=Label(sales_frame,text='Total Sales',bg='#E74C3C',fg='white',font=('times new roman',15))
totalsales_label.pack()

totalsales_count_label=Label(sales_frame,text='0',bg='#E74C3C',fg='white',font=('times new roman',30))
totalsales_count_label.pack()

update()

window.mainloop() #to see the window (root) on the screen. Write everything b4 mainloop otherwise it won't show()