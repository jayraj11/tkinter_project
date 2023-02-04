from distutils.util import execute
from tkinter import *
from PIL import Image, ImageTk  #pip install pillow
from tkinter import ttk, messagebox
import mysql.connector as sql
from numpy import delete

class supplierClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+230+130")
        self.root.title("Invenotry Management System | By Anushka & Jayraj")
        self.root.config(bg="white")
        self.root.focus_force()
        #**************************
        #All Variables************
        self.var_searchby=StringVar()
        self.var_searchtxt=StringVar()
       
        self.var_sup_invoice=StringVar()
        self.var_name=StringVar()
        self.var_contact=StringVar()
        
        
    
        #*****Search_Frame*******
        
        #*****Options*******
        lbl_search=Label(self.root,text="Invoice No.",bg="white",font=("goudy old style",12))
        lbl_search.place(x=700,y=80,width=80)
        

        txt_search=Entry(self.root,textvariable=self.var_searchtxt,font=("goudy old style",15),bg="lightyellow").place(x=800,y=80,width=160)
        btn_search=Button(self.root,text="Search",command=self.search,font=("goudy old style",15),bg="#4caf50",fg="White",cursor="hand2").place(x=980,y=79,width=100,height=28)

        #*****title*******
        title=Label(self.root,text="SUPPLIER DETAILS",font=("goudy old style",20,"bold"),bg="#0f4d7d",fg="white").place(x=50,y=10,width=1000,height=40)

        #***********Content***************

        #**********Row_1***********
        lbl_supplier_invoice=Label(self.root,text="Invoice No.",font=("goudy old style",15),bg="White").place(x=50,y=80)
        
        txt_supplier_invoice=Entry(self.root,textvariable=self.var_sup_invoice,font=("goudy old style",15),bg="lightyellow").place(x=180,y=80,width=180)
       
       
        #**********Row_2***********
        lbl_name=Label(self.root,text="Name",font=("goudy old style",15),bg="White").place(x=50,y=120)
        
        txt_name=Entry(self.root,textvariable=self.var_name,font=("goudy old style",15),bg="lightyellow").place(x=180,y=120,width=180)
        
        #**********Row_3***********

        lbl_contact=Label(self.root,text="Contact",font=("goudy old style",15),bg="White").place(x=50,y=160)
        
        txt_contact=Entry(self.root,textvariable=self.var_contact,font=("goudy old style",15),bg="lightyellow").place(x=180,y=160,width=180)
                
        #**********Row_4***********

        lbl_descr=Label(self.root,text="Description",font=("goudy old style",15),bg="White").place(x=50,y=200)
        
        self.txt_descr=Text(self.root,font=("goudy old style",15),bg="lightyellow")
        self.txt_descr.place(x=180,y=200,width=470,height=140)
        
        #**********Buttons***********
        btn_add=Button(self.root,text="Save",command=self.add,font=("goudy old style",15),bg="#2196f3",fg="White",cursor="hand2").place(x=180,y=370,width=110,height=35)
        btn_update=Button(self.root,text="Update",command=self.update,font=("goudy old style",15),bg="#4caf50",fg="White",cursor="hand2").place(x=300,y=370,width=110,height=35)
        btn_delete=Button(self.root,text="Delete",command=self.delete,font=("goudy old style",15),bg="#f44336",fg="White",cursor="hand2").place(x=420,y=370,width=110,height=35)
        btn_clear=Button(self.root,text="Clear",command=self.clear,font=("goudy old style",15),bg="#607d8b",fg="White",cursor="hand2").place(x=540,y=370,width=110,height=35)
       

        #*******Supplier Details**********

        emp_frame=Frame(self.root,bd=3,relief=RIDGE)
        emp_frame.place(x=700,y=120,width=380,height=350)
        
        scrolly=Scrollbar(emp_frame,orient=VERTICAL)
        scrollx=Scrollbar(emp_frame,orient=HORIZONTAL)

        self.supplierTable=ttk.Treeview(emp_frame,columns=("invoice","name","contact","descr"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.supplierTable.xview)
        scrolly.config(command=self.supplierTable.yview)
        
        self.supplierTable.heading("invoice",text="Invoice No.")
        self.supplierTable.heading("name",text="Name")
        self.supplierTable.heading("contact",text="Contact")
        self.supplierTable.heading("descr",text="Description")
                
        self.supplierTable["show"]="headings"
        
        self.supplierTable.column("invoice",width=90)
        self.supplierTable.column("name",width=100)
        self.supplierTable.column("contact",width=100)
        self.supplierTable.column("descr",width=100)
        self.supplierTable.pack(fill=BOTH,expand=1)
        self.supplierTable.bind("<ButtonRelease-1>",self.get_data)
        
        self.show()
#***************************************************************
    def add(self):
        con=sql.connect(host="localhost", user="root", password="jayraj11",database="IMS")
        cur=con.cursor()
        try:
            if self.var_sup_invoice.get()=="":
                messagebox.showerror("Error","Invoive No. Required",parent=self.root)
            else:
                cur.execute("select * from employee where eid=%s",(self.var_sup_invoice.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","This Invoice No. is already assigned, try a different one",parent=self.root)
                else:
                    cur.execute("insert into supplier(invoice,name,contact,descr) values(%s,%s,%s,%s)",(
                                            self.var_sup_invoice.get(),
                                            self.var_name.get(),
                                            self.var_contact.get(),
                                            
                                            self.txt_descr.get('1.0',END),
                                            
                        
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Supplier added successfully")
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}",parent=self.root)



    def show(self):
        con=sql.connect(host="localhost", user="root", password="jayraj11",database="IMS")
        cur=con.cursor()
        try:
            cur.execute("select * from supplier")
            rows=cur.fetchall()
            self.supplierTable.delete(*self.supplierTable.get_children())
            for row in rows:
                self.supplierTable.insert('',END,values=row)


        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}",parent=self.root)


    def get_data(self,ev):
        f=self.supplierTable.focus()
        content=(self.supplierTable.item(f))
        row=content['values']
        #print(row)
        self.var_sup_invoice.set(row[0])
        self.var_name.set(row[1])
        self.var_contact.set(row[2])
        self.txt_descr.delete('1.0',END)
        self.txt_descr.insert(END,row[3])
        


#***************update*************                       
    def update(self):
        con=sql.connect(host="localhost", user="root", password="jayraj11",database="IMS")
        cur=con.cursor()
        try:
            if self.var_sup_invoice.get()=="":
                messagebox.showerror("Error","Invoice No. Required",parent=self.root)
            else:
                cur.execute("select * from supplier where invoice=%s",(self.var_sup_invoice.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Invoice No.",parent=self.root)
                else:
                    cur.execute("update supplier set name=%s,contact=%s,desc=%s where invoice=%s",(
                
                                            self.var_name.get(),
                                            self.var_contact.get(),
                                            
                                            self.txt_descr.get('1.0',END),
                                            self.var_sup_invoice.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Supplier updated successfully")
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}",parent=self.root)                 



#***************delete*************
    def delete(self):
        con=sql.connect(host="localhost", user="root", password="jayraj11",database="IMS")
        cur=con.cursor()
        try:
            if self.var_sup_invoice.get()=="":
                messagebox.showerror("Error","Invoice No. Required",parent=self.root)
            else:
                cur.execute("select * from supplier where invoice=%s",(self.var_sup_invoice.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Invoice No.",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete?",parent=self.root)
                    if op==True:
                        cur.execute("delete from supplier where invoice=%s",(self.var_sup_invoice.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Supplier Deleted Successfully",parent=self.root)
                        self.clear()
        
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}",parent=self.root)                 


#*************Clear******************
    def clear(self):
        self.var_sup_invoice.set("")
        self.var_name.set("")
        self.var_contact.set("")
        self.txt_descr.delete('1.0',END)
        
        self.var_searchtxt.set("")
        
        self.show()


#*************Clear******************
    def search(self):
        con=sql.connect(host="localhost", user="root", password="jayraj11",database="IMS")
        cur=con.cursor()
        try:
            if self.var_searchtxt.get()=="":
                messagebox.showerror("Error","Invoice number is required",parent=self.root)
            else:
                cur.execute("select * from supplier where invoice=%s",(self.var_searchtxt.get(),))
                row=cur.fetchone()
                if row!=None:
                    self.supplierTable.delete(*self.supplierTable.get_children())
                    self.supplierTable.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","No Record Found!",parent=self.root)


        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}",parent=self.root)



if __name__=="__main__":
    root=Tk()
    obj=supplierClass(root)
    root.mainloop()