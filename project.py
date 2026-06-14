from tkinter import Tk,Label,Frame,Entry,Button,simpledialog,messagebox
from tkinter.ttk import Combobox 
import time
import dbhandler,generater,sqlite3,mailer,random
from PIL import Image,ImageTk
dbhandler.create_table()


def update_time():   #update the time of strftime
    Lbl_date.configure(text=time.strftime("%a,%d-%b-%y ⏳%r")) # used to time to update per second
    Lbl_date.after(1000,update_time)   # after how much time it change the time

def forgot_screen():
    def main_click():
        frm.destroy()
        main_screen()

    def otp():
        uemail=e_email.get()
        conobj=sqlite3.connect(database="bank.sqlite3")
        curobj=conobj.cursor()
        query="select acn,name,pass from accounts where email=?"
        curobj.execute(query,(uemail,))
        conobj.close()
        tup=curobj.fetchone()
        if tup==None:
            messagebox.showerror("Forgot","Email does not Exists")
        else:
            genotp=random.randint(1000,9000)
            mailer.send_otp_forgot(uemail,tup[1],genotp)
            messagebox.showinfo("Forgot Password","we have sent otp to your email")
            uotp=simpledialog.askinteger("","Enter OTP")
            if genotp==uotp:
                messagebox.showinfo("Password",tup[2])

            else:
                messagebox.showinfo("Forgot Password","Invalid OTP") 

                e_email.delete(0,"end")
                             
    frm=Frame(root,highlightbackground='black',highlightthickness=2)  # create the frame in the root window and highlight window is used to highlight the frame window
    frm.configure(bg="pink") # used to give the name to frame
    frm.place(relx=0,rely=.17,relwidth=1,relheight=0.72)   #used to place the frame 

    back_btn=Button(frm,text="back",font=('arial',20,'bold'),
                    bd=5,bg='powder blue',activebackground='purple',
                    activeforeground='white',command=main_click)
    back_btn.place(relx=0,rely=0)

    lbl_email=Label(frm,text="Email",font=('arial',20,'bold'),bg='pink')   # used to make the acc buttom
    lbl_email.place(relx=.3,rely=.2) # define the location of ACN

    e_email=Entry(frm,font=('arial',20,'bold'),bd=5)  # used to define the entry of ACN 
    e_email.place(relx=.4,rely=.2) # used to define the location of entry of the ACN
    e_email.focus()

    otp_btn=Button(frm,text="Send OTP",font=('arial',20,'bold'),
                    bd=5,bg='powder blue',activebackground='purple',
                    activeforeground='white',command=otp)
    otp_btn.place(relx=.5,rely=.3)



def admin_screen():
    def logout_click():
        frm.destroy()
        main_screen()

    def close_click():

        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)  # create the frame in the root window and highlight window is used to highlight the frame window
        ifrm.configure(bg="white") # used to give the name to frame
        ifrm.place(relx=.1,rely=.3,relwidth=.8,relheight=.65)
        Lbl_title=Label(ifrm,text="This is the close Account section",font=('arial',20,'bold','underline'),bg="white")   # make lable of project
        Lbl_title.pack() 

        uacn=simpledialog.askinteger("","Enter ACN",)

        conobj=sqlite3.connect(database="bank.sqlite3")
        curobj=conobj.cursor()
        query="select email,name from accounts where acn=?"
        curobj.execute(query,(uacn,))
        tup=curobj.fetchone()
        conobj.close()
        if tup==None:
            messagebox.showerror("Delete Account","ACN does not Exists")
        else:
            genotp=random.randint(0000,9999)
            mailer.send_otp_close(tup[0],tup[1],genotp)
            messagebox.showinfo("Close Account","we have sent otp to your email")
            uotp=simpledialog.askinteger("","Enter OTP")
            if genotp==uotp:
                conobj=sqlite3.connect(database="bank.sqlite3")
                curobj=conobj.cursor()
                query="delete  from accounts where acn=?"
                curobj.execute(query,(uacn,))
                conobj.commit()
                conobj.close()
                messagebox.showinfo("Account closure","Account closed")
            else:
                messagebox.showinfo("Account Closure","Invalid OTP") 

                



    def view_click():

        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)  # create the frame in the root window and highlight window is used to highlight the frame window
        ifrm.configure(bg="white") # used to give the name to frame
        ifrm.place(relx=.1,rely=.3,relwidth=.8,relheight=.65)
        Lbl_title=Label(ifrm,text="This is the view section",font=('arial',20,'bold','underline'),bg="white")   # make lable of project
        Lbl_title.pack() 
        uacn=simpledialog.askinteger("","Enter ACN",)
        
        conobj=sqlite3.connect(database="bank.sqlite3")
        curobj=conobj.cursor()
        query="select acn,name,adhar,opendate,bal,mob,email from accounts where acn=?"
        curobj.execute(query,(uacn,))
        tup=curobj.fetchone()
        if tup==None:
            messagebox.showerror("View Account","ACN does not Exists")
        else:
            messagebox.showinfo("view Account",f"ACN={tup[0]}\nName={tup[1]}\nAdhar={tup[2]}\nopendate={tup[3]}\nbal={tup[4]}\nmob={tup[5]}\nemail={tup[6]}")

    def open_click():
        def create():
            uname=e_name.get()
            uemail=e_mail.get()
            umob=e_mob.get()
            uadhar=e_adhar.get()
            ubal=0
            uopen=time.strftime("%A,%d-%b-%Y %r")            
            upass=generater.generate_pass()

            conobj=sqlite3.connect(database="bank.sqlite3")
            curobj=conobj.cursor()
            query="insert into accounts values(null,?,?,?,?,?,?,?)"
            curobj.execute(query,(uname,upass,uemail,umob,uadhar,ubal,uopen))
            conobj.commit()
            conobj.close()

            conobj=sqlite3.connect(database="bank.sqlite3")
            curobj=conobj.cursor()
            query="select max(acn) from accounts"
            curobj.execute(query)
            uacn=curobj.fetchone()[0]
            conobj.close()

            mailer.send_openacn_email(uemail,uacn,upass,uname)

            messagebox.showinfo("Account","Account opened and credentials are mailed to customer email")

            e_name.delete(0,"end")
            e_mail.delete(0,"end")
            e_mob.delete(0,"end")
            e_adhar.delete(0,"end")

            e_name.focus()

        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)  # create the frame in the root window and highlight window is used to highlight the frame window
        ifrm.configure(bg="white") # used to give the name to frame
        ifrm.place(relx=.1,rely=.3,relwidth=.8,relheight=.65)
        Lbl_title=Label(ifrm,text="This is the open Account section",font=('arial',20,'bold','underline'),bg="white")   # make lable of project
        Lbl_title.pack() 

        lbl_name=Label(ifrm,text="NAME",font=('arial',20,'bold'),bg='white')   # used to make the acc buttom
        lbl_name.place(relx=.05,rely=.2) # define the location of ACN

        e_name=Entry(ifrm,font=('arial',20,'bold'),bd=5)  # used to define the entry of ACN 
        e_name.place(relx=.15,rely=.2) # used to define the location of entry of the ACN
        e_name.focus()

        lbl_email=Label(ifrm,text="EMAIL",font=('arial',20,'bold'),bg='white')   # used to make the acc buttom
        lbl_email.place(relx=.05,rely=.41) # define the location of ACN

        e_mail=Entry(ifrm,font=('arial',20,'bold'),bd=5)  # used to define the entry of ACN 
        e_mail.place(relx=.15,rely=.4)

        lbl_mob=Label(ifrm,text="MOB",font=('arial',20,'bold'),bg='white')   # used to make the acc buttom
        lbl_mob.place(relx=.5,rely=.2) # define the location of ACN

        e_mob=Entry(ifrm,font=('arial',20,'bold'),bd=5)  # used to define the entry of ACN 
        e_mob.place(relx=.65,rely=.2) # used to define the location of entry of the ACN
        
        lbl_adhar=Label(ifrm,text="ADHAR",font=('arial',20,'bold'),bg='white')   # used to make the acc buttom
        lbl_adhar.place(relx=.5,rely=.42) # define the location of ACN

        e_adhar=Entry(ifrm,font=('arial',20,'bold'),bd=5)  # used to define the entry of ACN 
        e_adhar.place(relx=.65,rely=.4)
        create_btn=Button(ifrm,text="CREATE",font=('arial',20,'bold'),
                    bd=5,bg='powder blue',activebackground='purple',
                    activeforeground='white',command=create)
        create_btn.place(relx=.4,rely=.58)



    frm=Frame(root,highlightbackground='black',highlightthickness=2)  # create the frame in the root window and highlight window is used to highlight the frame window
    frm.configure(bg="pink") # used to give the name to frame
    frm.place(relx=0,rely=.17,relwidth=1,relheight=0.72)

    lbl_welcome=Label(frm,text="WELCOME ADMIN",font=('arial',20,'bold'),bg='pink')   # used to make the acc buttom
    lbl_welcome.place(relx=0,rely=0)

    logout_btn=Button(frm,text="logout",font=('arial',20,'bold'),
                    bd=5,bg='powder blue',activebackground='purple',
                    activeforeground='white',command=logout_click)
    logout_btn.place(relx=.9,rely=.0)

    open_btn=Button(frm,text="open Account",font=('arial',20,'bold'),
                    bd=5,activebackground='purple',
                    activeforeground='white',bg="green",fg="white",command=open_click)
    open_btn.place(relx=.2,rely=.12)

    view_btn=Button(frm,text="view Account",font=('arial',20,'bold'),
                    bd=5,activebackground='purple',
                    activeforeground='white',bg="blue",fg="white",command=view_click)
    view_btn.place(relx=.4,rely=.12)

    close_btn=Button(frm,text="close Account",font=('arial',20,'bold'),
                    bd=5,activebackground='purple',
                    activeforeground='white',bg="red",fg="white",command=close_click)
    close_btn.place(relx=.6,rely=.12)

def customer_screen(cname,acn):
    def logout_click():
        frm.destroy()
        main_screen()

    def details_click():

        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)  # create the frame in the root window and highlight window is used to highlight the frame window
        ifrm.configure(bg="white") # used to give the name to frame
        ifrm.place(relx=.25,rely=.13,relwidth=.7,relheight=.8)
        Lbl_title=Label(ifrm,text="This is the Details section",font=('arial',20,'bold','underline'),
                        bg="white",fg='purple')   # make lable of project
        Lbl_title.pack() 

        conobj=sqlite3.connect(database='bank.sqlite3')
        curobj=conobj.cursor()
        query="select * from accounts where acn=?"
        curobj.execute(query,(acn,))
        tup=curobj.fetchone()
        conobj.close()

        info=f'''Account No = {tup[0]}

        Account open date = {tup[7]}

        Account Bal = {tup[6]}

        Account Adhar = {tup[5]}

        Account Email = {tup[3]}

        Account Mobile = {tup[4]}
        '''
        lbl_info=Label(ifrm,text=info,bg='white',font=('verdana',15,'bold'))
        lbl_info.place(relx=.22,rely=.2)

    def edit_click():
        def update():
            uname=e_name.get()
            upass=e_pass.get()
            uemail=e_email.get()
            umob=e_mob.get()

            conobj=sqlite3.connect(database='bank.sqlite3')
            curobj=conobj.cursor()
            query="update accounts set name=?,pass=?,email=?,mob=? where acn=?"
            curobj.execute(query,(uname,upass,uemail,umob,acn))
            conobj.commit()
            conobj.close() 
            messagebox.showinfo("Edit","Record updated")

            e_name.delete(0,"end")
            e_pass.delete(0,"end")
            e_email.delete(0,"end")
            e_mob.delete(0,"end")

            e_name.focus()



        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)  # create the frame in the root window and highlight window is used to highlight the frame window
        ifrm.configure(bg="white") # used to give the name to frame
        ifrm.place(relx=.25,rely=.13,relwidth=.7,relheight=.8)
        Lbl_title=Label(ifrm,text="This is the Edit section",font=('arial',20,'bold','underline'),bg="white",fg='purple')   # make lable of project
        Lbl_title.pack()

        lbl_name=Label(ifrm,text="NAME",font=('arial',20,'bold'),bg='white')   # used to make the acc buttom
        lbl_name.place(relx=.05,rely=.2) # define the location of ACN

        e_name=Entry(ifrm,font=('arial',20,'bold'),bd=5)  # used to define the entry of ACN 
        e_name.place(relx=.15,rely=.2) # used to define the location of entry of the ACN
        e_name.focus()

        lbl_email=Label(ifrm,text="EMAIL",font=('arial',20,'bold'),bg='white')   # used to make the acc buttom
        lbl_email.place(relx=.05,rely=.41) # define the location of ACN

        e_email=Entry(ifrm,font=('arial',20,'bold'),bd=5)  # used to define the entry of ACN 
        e_email.place(relx=.15,rely=.4)

        lbl_mob=Label(ifrm,text="MOB",font=('arial',20,'bold'),bg='white')   # used to make the acc buttom
        lbl_mob.place(relx=.5,rely=.2) # define the location of ACN

        e_mob=Entry(ifrm,font=('arial',20,'bold'),bd=5)  # used to define the entry of ACN 
        e_mob.place(relx=.65,rely=.2) # used to define the location of entry of the ACN
        
        lbl_pass=Label(ifrm,text="PASS",font=('arial',20,'bold'),bg='white')   # used to make the acc buttom
        lbl_pass.place(relx=.5,rely=.42) # define the location of ACN

        e_pass=Entry(ifrm,font=('arial',20,'bold'),bd=5)  # used to define the entry of ACN 
        e_pass.place(relx=.65,rely=.4)


        update_btn=Button(ifrm,text="update",font=('arial',20,'bold'),
                    bd=5,bg='powder blue',activebackground='purple',
                    activeforeground='white',command=update)
        update_btn.place(relx=.4,rely=.58)

        conobj=sqlite3.connect(database='bank.sqlite3')
        curobj=conobj.cursor()
        query="select name,pass,email,mob from accounts where acn=?"
        curobj.execute(query,(acn,))
        tup=curobj.fetchone()
        conobj.close()        

        e_name.insert(0,tup[0])
        e_pass.insert(0,tup[1])
        e_email.insert(0,tup[2])
        e_mob.insert(0,tup[3])

    def deposit_click():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)  # create the frame in the root window and highlight window is used to highlight the frame window
        ifrm.configure(bg="white") # used to give the name to frame
        ifrm.place(relx=.25,rely=.13,relwidth=.7,relheight=.8)
        Lbl_title=Label(ifrm,text="This is the Deposit section",font=('arial',20,'bold','underline'),
                        bg="white",fg="purple")   # make lable of project
        Lbl_title.pack()

        amt=simpledialog.askfloat("","Amount")
        conobj=sqlite3.connect(database='bank.sqlite3')
        curobj=conobj.cursor()
        query="update accounts set bal=bal+? where acn=?"
        curobj.execute(query,(amt,acn))
        conobj.commit()
        conobj.close()
        messagebox.showinfo("deposit",f"{amt} deposited")


    def withdraw_click():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)  # create the frame in the root window and highlight window is used to highlight the frame window
        ifrm.configure(bg="white") # used to give the name to frame
        ifrm.place(relx=.25,rely=.13,relwidth=.7,relheight=.8)
        Lbl_title=Label(ifrm,text="This is the Widhdraw section",
                        font=('arial',20,'bold','underline'),bg="white",fg="purple")   # make lable of project
        Lbl_title.pack()

        amt=simpledialog.askfloat("","Amount")
        conobj=sqlite3.connect(database='bank.sqlite3')
        curobj=conobj.cursor()
        query="select bal from accounts where acn=?"
        curobj.execute(query,(acn,))
        bal=curobj.fetchone()[0]
        conobj.close()
        if bal>=amt:
            conobj=sqlite3.connect(database='bank.sqlite3')
            curobj=conobj.cursor()
            query="update accounts set bal=bal-? where acn=?"
            curobj.execute(query,(amt,acn))
            conobj.commit()
            conobj.close()
            messagebox.showinfo("withdraw",f"{amt} withdrawn")
        else:
            messagebox.showerror("withdraw",f"Insufficient bal {bal}")
        
        
    def transfer_click():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)  # create the frame in the root window and highlight window is used to highlight the frame window
        ifrm.configure(bg="white") # used to give the name to frame
        ifrm.place(relx=.25,rely=.13,relwidth=.7,relheight=.8)
        Lbl_title=Label(ifrm,text="This is the Transfer section",
                        font=('arial',20,'bold','underline'),bg="white",fg="purple")   # make lable of project
        Lbl_title.pack()

        toacn=simpledialog.askinteger("","TO ACN")
        conobj=sqlite3.connect(database='bank.sqlite3')
        curobj=conobj.cursor()
        query="select * from accounts where acn=?"
        curobj.execute(query,(toacn,))
        tup=curobj.fetchone()
        conobj.close()
        if tup!=None:
            amt=simpledialog.askfloat("","Amount")
            conobj=sqlite3.connect(database='bank.sqlite3')
            curobj=conobj.cursor()
            query="select bal from accounts where acn=?"
            curobj.execute(query,(acn,))
            bal=curobj.fetchone()[0]
            conobj.close()
            if bal>=amt:
                conobj=sqlite3.connect(database='bank.sqlite3')
                curobj=conobj.cursor()
                query1="update accounts set bal=bal-? where acn=?"
                query2="update accounts set bal=bal+? where acn=?"

                curobj.execute(query1,(amt,acn))
                curobj.execute(query2,(amt,toacn))

                conobj.commit()
                conobj.close()
                messagebox.showinfo("Transfer",f"{amt} transfered to {toacn} ACN")
            else:
                messagebox.showerror("withdraw",f"Insufficient bal {bal}")
        else:
            messagebox.showerror("Transfer",f"{toacn} ACN does not exist")
    
    def logout_click():
        frm.destroy()
        main_screen()
    frm=Frame(root,highlightbackground='black',highlightthickness=2)  # create the frame in the root window and highlight window is used to highlight the frame window
    frm.configure(bg="pink") # used to give the name to frame
    frm.place(relx=0,rely=.17,relwidth=1,relheight=0.72)

    lbl_welcome=Label(frm,text=f"WELCOME,{cname},",font=('arial',20,'bold'),bg='pink')   # used to make the acc buttom
    lbl_welcome.place(relx=0,rely=0)

    logout_btn=Button(frm,text="logout",font=('arial',20,'bold'),
                    bd=5,bg='powder blue',activebackground='purple',
                    activeforeground='white',command=logout_click)
    logout_btn.place(relx=.9,rely=.0)

    details_btn=Button(frm,text=" VIEW DETAILS",font=('arial',20,'bold'),
                    bd=5,bg='blue',activebackground='purple', width=15,
                    activeforeground='white',command= details_click)
    details_btn.place(relx=.0,rely=.1)

    edit_btn=Button(frm,text=" EDIT PROFILE",font=('arial',20,'bold'),
                    bd=5,bg='powder blue',activebackground='purple', width=15,
                    activeforeground='white',command=edit_click)
    edit_btn.place(relx=.0,rely=.25)

    deposit_btn=Button(frm,text=" DEPOSIT ",font=('arial',20,'bold'),
                    bd=5,bg='green',activebackground='purple', width=15,
                    activeforeground='white',command=deposit_click)
    deposit_btn.place(relx=.0,rely=.4)

    withdraw_btn=Button(frm,text=" WITHDRAW ",font=('arial',20,'bold'),
                    bd=5,bg='red',activebackground='purple', width=15,
                    activeforeground='white',command=withdraw_click)
    withdraw_btn.place(relx=.0,rely=.55)

    transfer_btn=Button(frm,text=" TRANSFER ",font=('arial',20,'bold'),
                    bd=5,bg='red',activebackground='purple', width=15,
                    activeforeground='white',command=transfer_click)
    transfer_btn.place(relx=.0,rely=.7)


def main_screen():  #in funstion we make the frame of the screen
    def forgot_click():
        frm.destroy()
        forgot_screen()

    def login_click():
        user=combo_user.get()
        uacn=e_acn.get()
        upass=e_pass.get()

        if user=="ADMIN" and uacn=="0" and upass=="Admin":
            frm.destroy()
            admin_screen()
        elif user=="CUSTOMER":
            conobj=sqlite3.connect(database="bank.sqlite3")
            curobj=conobj.cursor()
            query="select * from accounts where acn=? and pass=?"
            curobj.execute(query,(uacn,upass))
            tup=curobj.fetchone()
            if tup==None:
                messagebox.showerror("Login","Invalid Credentials")
            else:
                frm.destroy()
                customer_screen(tup[1],tup[0])

        else:
            messagebox.showerror("Login","Invalid User")

    frm=Frame(root,highlightbackground='black',highlightthickness=2)  # create the frame in the root window and highlight window is used to highlight the frame window
    frm.configure(bg="pink") # used to give the name to frame
    frm.place(relx=0,rely=.17,relwidth=1,relheight=0.72)   #used to place the frame 

    lbl_acn=Label(frm,text="ACN",font=('arial',20,'bold'),bg='pink')   # used to make the acc buttom
    lbl_acn.place(relx=.3,rely=.1) # define the location of ACN

    e_acn=Entry(frm,font=('arial',20,'bold'),bd=5)  # used to define the entry of ACN 
    e_acn.place(relx=.4,rely=.1) # used to define the location of entry of the ACN
    e_acn.focus()

    lbl_pass=Label(frm,text="PASS",font=('arial',20,'bold'),bg='pink')   # used to make the acc buttom
    lbl_pass.place(relx=.3,rely=.21) # define the location of ACN

    e_pass=Entry(frm,font=('arial',20,'bold'),bd=5,show='*')  # used to define the entry of PASS 
    e_pass.place(relx=.4,rely=.2) # used to define the location of entry of the PASS

    lbl_user=Label(frm,text="USER",font=('arial',20,'bold'),bg='pink')   # used to make the acc user
    lbl_user.place(relx=.3,rely=.315) # define the location of user

    e_user=Entry(frm,font=('arial',20,'bold'),bd=5,show='*')  # used to define the entry of PASS 
    e_user.place(relx=.4,rely=.3) # used to define the location of entry of the PASS

    combo_user=Combobox(frm,values=['------select-----','ADMIN','CUSTOMER'],font=('arial',20,'bold')) #used to make the drop down in the combobox
    combo_user.current(0)
    combo_user.place(relx=.40,rely=.31)

    login_btn=Button(frm,text="login",font=('arial',20,'bold',),bd=5,bg='powder blue'
                     ,activebackground='purple',activeforeground='white'
                     ,command=login_click)
    
    login_btn.place(relx=.42,rely=.41)

    reset_btn=Button(frm,text="Reset",font=('arial',20,'bold',),bd=5,bg='powder blue'
                     ,activebackground='purple',activeforeground='white')
    reset_btn.place(relx=.549,rely=.41)

    forgot_btn=Button(frm,text="Forgot Password",font=('arial',20,'bold'),width=18,bd=5,bg='powder blue'
                     ,activebackground='purple',activeforeground='white',command=forgot_click)
    forgot_btn.place(relx=.4,rely=.55)


root=Tk()                      #create root window
root.state("zoomed")           #make window full screen
root.config(bg="powder blue")  # set background color of window
root.resizable(width=False,height=False) # set resizable desable of window

Lbl_title=Label(root,text="Banking Simulation",font=('arial',50,'bold','underline'),bg="powder blue")   # make lable of project
Lbl_title.pack()    # placed at top center the label

Lbl_date=Label(root,text=time.strftime("%a,%d-%b-%y ⏳%r"),fg='blue',font=('arial',20,'bold'),bg="powder blue") # used to show system date and time
Lbl_date.pack()  # used to show the date time of window in project

img=Image.open("logo.jpg").resize((200,150))
tkimg=ImageTk.PhotoImage(img,master=root)
lbl_logo=Label(root,image=tkimg)
lbl_logo.place(relx=0,rely=0)

Lbl_footer=Label(root,text="Developed by \n JITENDER",fg='blue',font=('arial',20,'bold'),bg='powder blue')  # used to add the footer name
Lbl_footer.pack(side='bottom',pady=10) #used to define the location of fotter

update_time() #used to call the time function
main_screen()  # call the main_screen function


root.mainloop()  # used to show the window or make the window visiable

