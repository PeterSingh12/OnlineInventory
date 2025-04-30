from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from employees import connect_database

def delete_sale(treeview):
    index = treeview.selection()
    if not index:
        messagebox.showerror('Error', 'No row is selected')
        return
    content = treeview.item(index)
    row = content['values']
    id = row[0]

    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('USE inventory_system')
        cursor.execute('DELETE FROM sales_data WHERE id=%s', (id,))
        connection.commit()
        treeview_sales_data(treeview)
        messagebox.showinfo('Info', 'Record is deleted')
    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')
    finally:
        cursor.close()
        connection.close()

def clear_sales(id_entry, product_entry, amount_entry):
    id_entry.delete(0, END)
    product_entry.delete(0, END)
    amount_entry.delete(0, END)

def treeview_sales_data(treeview):
    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('USE inventory_system')
        cursor.execute('SELECT * FROM sales_data')
        records = cursor.fetchall()
        treeview.delete(*treeview.get_children())
        for record in records:
            treeview.insert('', END, values=record)
    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')
    finally:
        cursor.close()
        connection.close()

def add_sale(id, product, amount, treeview):
    if id == '' or product == '' or amount == '':
        messagebox.showerror('Error', 'All fields are required')
        return
    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('USE inventory_system')
        cursor.execute('CREATE TABLE IF NOT EXISTS sales_data(id INT PRIMARY KEY, product VARCHAR(100), amount FLOAT)')
        cursor.execute('SELECT * FROM sales_data WHERE id=%s', (id,))
        if cursor.fetchone():
            messagebox.showerror('Error', 'ID already exists')
            return
        cursor.execute('INSERT INTO sales_data VALUES(%s, %s, %s)', (id, product, amount))
        connection.commit()
        messagebox.showinfo('Success', 'Data inserted')
        treeview_sales_data(treeview)
    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')
    finally:
        cursor.close()
        connection.close()

def sales_form(window):
    global back_image,logo
    sales_frame = Frame(window, width=1070, height=567, bg="white")
    sales_frame.place(x=200, y=100)

    heading_label = Label(sales_frame, text='Manage Sales Details',
                          font=('times new roman', 16, 'bold'), bg='#0f4d7d', fg='white')
    heading_label.place(x=0, y=0, relwidth=1)

    back_image = PhotoImage(file='back.png')
    back_button = Button(sales_frame, image=back_image, bg="white", bd=0, cursor='hand2',
                         command=lambda: sales_frame.place_forget())
    back_button.place(x=10, y=30)
    
    logo = PhotoImage(file='sales.png')
    label = Label(sales_frame, image=logo, bg='white')
    label.place(x=20, y=90)

    details_frame = Frame(sales_frame, bg='white')
    details_frame.place(x=500, y=60)

    id_label = Label(details_frame, text='ID', font=('times new roman', 14, 'bold'), bg='white')
    id_label.grid(row=0, column=0, padx=20, sticky='w')
    id_entry = Entry(details_frame, font=('times new roman', 14, 'bold'), bg='lightyellow')
    id_entry.grid(row=0, column=1)

    product_label = Label(details_frame, text='Product', font=('times new roman', 14, 'bold'), bg='white')
    product_label.grid(row=1, column=0, padx=20, sticky='w')
    product_entry = Entry(details_frame, font=('times new roman', 14, 'bold'), bg='lightyellow')
    product_entry.grid(row=1, column=1, pady=20)

    amount_label = Label(details_frame, text='Amount', font=('times new roman', 14, 'bold'), bg='white')
    amount_label.grid(row=2, column=0, padx=20, sticky='w')
    amount_entry = Entry(details_frame, font=('times new roman', 14, 'bold'), bg='lightyellow')
    amount_entry.grid(row=2, column=1)

    button_frame = Frame(sales_frame, bg='white')
    button_frame.place(x=580, y=280)

    add_button = Button(button_frame, text='Add', font=('times new roman', 14), width=8, cursor='hand2',
                        fg='white', bg='#0f4d7d',
                        command=lambda: add_sale(id_entry.get(), product_entry.get(), amount_entry.get(), treeview))
    add_button.grid(row=0, column=0, padx=20)

    delete_button = Button(button_frame, text='Delete', font=('times new roman', 14), width=8, cursor='hand2',
                           fg='white', bg='#0f4d7d', command=lambda: delete_sale(treeview))
    delete_button.grid(row=0, column=1, padx=20)

    clear_button = Button(button_frame, text='Clear', font=('times new roman', 14), width=8, cursor='hand2',
                          fg='white', bg='#0f4d7d',
                          command=lambda: clear_sales(id_entry, product_entry, amount_entry))
    clear_button.grid(row=0, column=2, padx=20)

    treeview_frame = Frame(sales_frame, bg='white')
    treeview_frame.place(x=530, y=340, height=200, width=500)

    scrolly = Scrollbar(treeview_frame, orient=VERTICAL)
    scrollx = Scrollbar(treeview_frame, orient=HORIZONTAL)

    treeview = ttk.Treeview(treeview_frame, column=('id', 'product', 'amount'), show='headings',
                            yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
    scrolly.pack(side=RIGHT, fill=Y)
    scrollx.pack(side=BOTTOM, fill=X)
    scrollx.config(command=treeview.xview)
    scrolly.config(command=treeview.yview)
    treeview.pack(fill=BOTH, expand=1)

    treeview.heading('id', text='ID')
    treeview.heading('product', text='Product')
    treeview.heading('amount', text='Amount')

    treeview.column('id', width=80)
    treeview.column('product', width=140)
    treeview.column('amount', width=100)
    treeview_sales_data(treeview)