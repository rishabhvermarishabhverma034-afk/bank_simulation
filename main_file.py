from tkinter import Tk,Label,Frame,Button,Entry,messagebox,simpledialog,filedialog
import time
import sqlite3
import table_creater
import Generator
import Email_handler
import re
import os
from datetime import datetime
from PIL import Image,ImageTk

table_creater.create()


def update_time():
    curdate=time.strftime("%d-%b-%Y ⏰%r")
    date.configure(text=curdate)
    date.after(1000,update_time)
    
def forgot_screen():
     def back():
        frm.destroy()
        existuser_screen()
    
     def reset_click():
         e_acn.delete(0,"end")
         e_adhar.delete(0,"end")
         e_acn.focus()
         
     
        
     def send_otp():
        gen_otp=Generator.generate_otp() 
        acn=e_acn.get()
        adhar=e_adhar.get()
        
        conobj=sqlite3.connect(database="mybank.sqlite")
        curobj=conobj.cursor()
        quary='''select name,email,pass from accounts where acn=? and adhar=?'''
        curobj.execute(quary,(acn,adhar))
        tup=curobj.fetchone()
        conobj.close()
        if tup==None:
            messagebox.showerror('Forgot Password','Record not found')
        else:
             Email_handler.send_otp(tup[1],tup[0],gen_otp)
             user_otp=simpledialog.askinteger("Password Recovery","Enter OTP")
            
   
   
             attempt = 1

        while attempt <= 3:
                user_otp = simpledialog.askstring(
        "OTP Verification",
        f"Enter OTP (Attempt {attempt}/3)"
    )

                if user_otp is None:   # user ne cancel dabaya
                 break

                if gen_otp == int(user_otp):
                   messagebox.showinfo(
            "Password Recovery",
            f"Your Password = {tup[2]}"
        )
                   break
                else:
                   messagebox.showerror(
            "Password Recovery",
            "Invalid OTP"
        )
                attempt += 1

        if attempt > 3:
            otp_button.configure(text="Resend OTP")

             
     frm=Frame(root,highlightbackground='black',highlightthickness=2)
     frm.configure(bg='pink')
     frm.place(relx=0,rely=.14,relwidth=1,relheight=.8)
    
     back_button=Button(frm,text="back",font=('arial',20,'bold'),bd=2,bg='powder blue',activebackground='purple',activeforeground='white',command=back)
     back_button.place(relx=0,rely=0)
       
        
     lbl_acn=Label(frm,text='👤Account No',width=12,font=('arial',20,'bold'),bg='purple',fg='white')
     lbl_acn.place(relx=.2,rely=.2)
    
     e_acn=Entry(frm,font=('arial',20,'bold'),bd=5)
     e_acn.place(relx=.4,rely=.2)
     e_acn.focus()
    
     lbl_adhar=Label(frm,text='Adhar',width=12,font=('arial',20,'bold'),bg='purple',fg='white')
     lbl_adhar.place(relx=.2,rely=.3)
    
     e_adhar=Entry(frm,font=('arial',20,'bold'),bd=5)
     e_adhar.place(relx=.4,rely=.3)
    
     otp_button=Button(frm,width=10,text="Send OTP",font=('arial',20,'bold'),bg='powder blue',activebackground='purple',activeforeground='white',bd=2,command=send_otp)
     otp_button.place(relx=.3,rely=.5)
    
     reset_button=Button(frm,width=7,text="Reset",font=('arial',20,'bold'),bg='powder blue',activebackground='purple',activeforeground='white',bd=2,command=reset_click)
     reset_button.place(relx=.5,rely=.5)

def welcome_screen(acn=None):
    def logout():
        frm.destroy()
        main_screen()
    
    def check_screen():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.2,rely=.2,relwidth=.7,relheight=.68)
        
        title_lbl=Label(ifrm,text='This is Check Details Screen',
                        font=('arial',30,'bold'),bg='white',fg='purple')
        title_lbl.pack()
        
        conobj=sqlite3.connect(database="mybank.sqlite")
        curobj=conobj.cursor()
        quary='''select acn,bal,adhar,email,opendate from accounts where acn=?'''
        curobj.execute(quary,(acn,))
        tup=curobj.fetchone()
        conobj.close()
        
        details=f'''
Account No = {tup[0]}\n
Account Bal = {tup[1]}\n
Account Adhar = {tup[2]}\n
 Email={tup[3]}\n
Account Opendate={tup[4]}        
'''
        lbl_details=Label(ifrm,text=details,bg='white',fg='purple',font=('arial',25,'bold'),bd=2)
        lbl_details.place(relx=.1,rely=.1)
        
    def update_screen():
        def update_db():
            name=e_name.get()
            email=e_email.get()
            mob=e_mob.get()
            pwd=e_pass.get()
            
            conobj=sqlite3.connect(database="mybank.sqlite")
            curobj=conobj.cursor()
            query='''update accounts set name=?,email=?,mob=?,pass=? where acn=? '''
            curobj.execute(query,(name,email,mob,pwd,acn))
            conobj.commit()
            conobj.close()
            messagebox.showinfo("Update Screen","Details updated successfully")
            welcome_screen(acn)
        
        conobj=sqlite3.connect(database="mybank.sqlite")
        curobj=conobj.cursor()
        query='''select name,email,mob,pass opendate from accounts where acn=?'''
        curobj.execute(query,(acn,))
        tup=curobj.fetchone()
        conobj.close()
        
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.2,rely=.2,relwidth=.7,relheight=.68)
        
        title_lbl=Label(ifrm,text='This is Update Details Screen',
                        font=('arial',30,'bold'),bg='white',fg='purple')
        title_lbl.pack()
        
        lbl_name=Label(ifrm,text='👤Name',width=7,font=('arial',20,'bold'),bg='purple',fg='white')
        lbl_name.place(relx=.02,rely=.2)
    
        e_name=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        e_name.place(relx=.15,rely=.2)
        e_name.focus
    
        lbl_pass=Label(ifrm,text='Password',width=7,font=('arial',20,'bold'),bg='purple',fg='white')
        lbl_pass.place(relx=.02,rely=.4)
    
        e_pass=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        e_pass.place(relx=.15,rely=.4)
    
        lbl_mob=Label(ifrm,text='📱Mob',width=7,font=('arial',20,'bold'),bg='purple',fg='white')
        lbl_mob.place(relx=.52,rely=.2)
    
        e_mob=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        e_mob.place(relx=.65,rely=.2)
    
        lbl_email=Label(ifrm,text='Email',width=7,font=('arial',20,'bold'),bg='purple',fg='white')
        lbl_email.place(relx=.52,rely=.4)
    
        e_email=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        e_email.place(relx=.65,rely=.4)  
    
        e_name.insert(0,tup[0])
        e_email.insert(0,tup[1])
        e_mob.insert(0,tup[2])
        e_pass.insert(0,tup[3])
    
        submit_button=Button(ifrm,width=7,text="Submit",font=('arial',20,'bold'),bg='powder blue',activebackground='purple',activeforeground='white',bd=2,command=update_db)
        submit_button.place(relx=.4,rely=.7)
    
        
    def deposit_screen():
        
        def deposit_db():
            amt=float(e_amt.get())
            conobj=sqlite3.connect(database="mybank.sqlite")
            curobj=conobj.cursor()
            query='''update accounts set bal=bal+? where acn=?'''
            curobj.execute(query,(amt,acn))
            conobj.commit()
            conobj.close()
            messagebox.showinfo("Deposit Screen",f'{amt} deposited successfully')
            e_amt.delete(0,"end")
            e_amt.focus()
            
        
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.2,rely=.2,relwidth=.7,relheight=.68)
        
        title_lbl=Label(ifrm,text='This is Check Deposit Screen',
                        font=('arial',30,'bold'),bg='white',fg='purple')
        title_lbl.pack()
        
        lbl_amt=Label(ifrm,text='Enter Amount',font=('arial',20,'bold'),bg='purple',fg='white')
        lbl_amt.place(relx=.01,rely=.2)
    
        e_amt=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        e_amt.place(relx=.2,rely=.2)
        e_amt.focus()
        
        submit_button=Button(ifrm,width=7,text="Submit",font=('arial',20,'bold'),bg='powder blue',activebackground='purple',activeforeground='white',bd=2,command=deposit_db)
        submit_button.place(relx=.4,rely=.7)
        
    def withdraw_screen():
        
        def withdraw_db():
            amt=float(e_amt.get())
            conobj=sqlite3.connect(database="mybank.sqlite")
            curobj=conobj.cursor()
            query='''select bal,email,name from accounts where acn=?'''
            curobj.execute(query,(acn,))
            tup=curobj.fetchone()
            conobj.close()
           
            if tup[0]>=amt:
                gen_otp=Generator.generate_otp()
                Email_handler.send_otp_withdraw(tup[1],tup[2],gen_otp,amt)
                user_otp=simpledialog.askinteger("Withdraw OTP","OTP")
                if gen_otp==user_otp:
                   
                    conobj=sqlite3.connect(database="mybank.sqlite")
                    curobj=conobj.cursor()
                    query='''update accounts set bal=bal-? where acn=?'''
                    curobj.execute(query,(amt,acn))
                    conobj.commit()
                    conobj.close()
                    messagebox.showinfo("Withdrawl Screen",f'{amt} withdrawl successfully')
                    e_amt.delete(0,"end")
                    e_amt.focus()
                else:
                    messagebox.showerror("Withdraw Screen","Invalid otp")
                    submit_button.configure(text='resendotp')
            else:
                messagebox.showwarning("Withdraw Screen",f'Insufficient Bal:{tup[0]}')
                
           
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.2,rely=.2,relwidth=.7,relheight=.68)
        
        title_lbl=Label(ifrm,text='This is Withdraw Amount Screen',
                        font=('arial',30,'bold'),bg='white',fg='purple')
        title_lbl.pack()
        
        lbl_amt=Label(ifrm,text='Enter Amount',font=('arial',20,'bold'),bg='purple',fg='white')
        lbl_amt.place(relx=.01,rely=.2)
    
        e_amt=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        e_amt.place(relx=.2,rely=.2)
        e_amt.focus()
        
        submit_button=Button(ifrm,text="Submit",font=('arial',20,'bold'),bg='powder blue',activebackground='purple',activeforeground='white',bd=2,command=withdraw_db)
        submit_button.place(relx=.4,rely=.7)
        
    
    def transfer_screen():
        
        def transfer_db():
            to_acn=int(e_to.get())
            amt=float(e_amt.get())
            
            conobj=sqlite3.connect(database="mybank.sqlite")
            curobj=conobj.cursor()
            query='''select * from accounts where acn=?'''
            curobj.execute(query,(to_acn,))
            tup=curobj.fetchone()
            conobj.close()
            
            if tup==None:
                messagebox.showerror("Transfer Screen","Invalid TO ACN")
                return
            conobj=sqlite3.connect(database="mybank.sqlite")
            curobj=conobj.cursor()
            query='''select bal,email,name from accounts where acn=?'''
            curobj.execute(query,(acn,))
            tup=curobj.fetchone()
            conobj.close()
           
            if tup[0]>=amt:
                gen_otp=Generator.generate_otp()
                Email_handler.send_otp_transfer(tup[1],tup[2],gen_otp,amt,to_acn)
                user_otp=simpledialog.askinteger("Transfer OTP","OTP")
                if gen_otp==user_otp:
                   
                    conobj=sqlite3.connect(database="mybank.sqlite")
                    curobj=conobj.cursor()
                    query1='''update accounts set bal=bal-? where acn=?'''
                    query2='''update accounts set bal=bal+? where acn=?'''
                    
                    curobj.execute(query1,(amt,acn))
                    curobj.execute(query2,(amt,to_acn))
                    
                    conobj.commit()
                    conobj.close()
                    messagebox.showinfo("Withdrawl Screen",f'{amt} Transfered successfully')
                    e_amt.delete(0,"end")
                    e_amt.focus()
                else:
                    messagebox.showerror("Transfered Screen","Invalid otp")
                    submit_button.configure(text='resendotp')
            else:
                messagebox.showwarning("Transfered Screen",f'Insufficient Bal:{tup[0]}')
                
        
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.2,rely=.2,relwidth=.7,relheight=.68)
        
        title_lbl=Label(ifrm,text='This is Transfer Amount Screen',
                        font=('arial',30,'bold'),bg='white',fg='purple')
        title_lbl.pack()
        
        lbl_to=Label(ifrm,text='TO ACN',font=('arial',20,'bold'),bg='purple',fg='white')
        lbl_to.place(relx=.1,rely=.25)
    
        e_to=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        e_to.place(relx=.3,rely=.25)
        e_to.focus()
        
        lbl_amt=Label(ifrm,text='Enter Amount',font=('arial',20,'bold'),bg='purple',fg='white')
        lbl_amt.place(relx=.1,rely=.35)
    
        e_amt=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        e_amt.place(relx=.3,rely=.35)
        
        submit_button=Button(ifrm,text="Transfer",font=('arial',20,'bold'),bg='powder blue',activebackground='purple',activeforeground='white',bd=2,command=transfer_db)
        submit_button.place(relx=.3,rely=.59)
        
        
    conobj=sqlite3.connect(database="mybank.sqlite")
    curobj=conobj.cursor()
    quary='''select name from accounts where acn=?'''
    curobj.execute(quary,(acn,))
    tup=curobj.fetchone()
    conobj.close()
    
    frm=Frame(root,highlightbackground='black',highlightthickness=2)
    frm.configure(bg='pink')
    frm.place(relx=0,rely=.14,relwidth=1,relheight=.8)
    
    logout_button=Button(frm,text="Log Out",font=('arial',20,'bold',),bd=2,bg='powder blue',activebackground='purple',activeforeground='white',command=logout)
    logout_button.place(relx=.89,rely=.0)
    
    lbl_welcome=Label(frm,text=f'Welcome,{tup[0]}',font=('arial',40,'bold'),bg='purple',fg='white')
    lbl_welcome.place(relx=.001,rely=.0)
    
    def update_pic():
      
       name=filedialog.askopenfilename()
       os.rename(name,f"{acn}.jpg") 
       img_profile=Image.open(f'{acn}.jpg').resize((250,160))
       imgtk_profile=ImageTk.PhotoImage(img_profile,master=root)
       lbl_img_profile=Label(frm,image=imgtk_profile)
       lbl_img_profile.place(relx=0.01,rely=.13)
       lbl_img_profile.image=imgtk_profile
    
       if os.path.exists(f'{acn}.jpg'):
           img_profile=Image.open(f"{acn}.jpg").resize((250,160))
       else:
           img_profile=Image.open('profile1.jpg').resize((250,160))   

    img_profile=Image.open('profile1.jpg').resize((250,160))
    imgtk_profile=ImageTk.PhotoImage(img_profile,master=root)

    lbl_img_profile=Label(frm,image=imgtk_profile)
    lbl_img_profile.place(relx=0.01,rely=.13)
    lbl_img_profile.image=imgtk_profile
    
    Pic_button=Button(frm,text="Update Profile",width=15,font=('arial',20,'bold'),bd=2,bg='orange',activebackground='purple',activeforeground='white',command=update_pic)
    Pic_button.place(relx=0.01,rely=.40)
     
    check_button=Button(frm,text="Check Details",width=15,font=('arial',20,'bold'),bd=2,bg='powder blue',activebackground='purple',activeforeground='white',command=check_screen)
    check_button.place(relx=0.01,rely=.52)
    
    update_button=Button(frm,text="Update Details",width=15,font=('arial',20,'bold'),bd=2,bg='powder blue',activebackground='purple',activeforeground='white',command=update_screen)
    update_button.place(relx=0.01,rely=.62)
    
    deposit_button=Button(frm,text="Deposit Amount",width=15,font=('arial',20,'bold'),bd=2,bg='red',activebackground='purple',activeforeground='white',command=deposit_screen)
    deposit_button.place(relx=0.01,rely=.72)
    
    withdraw_button=Button(frm,text="Withdraw Amount",width=15,font=('arial',20,'bold'),bd=2,bg='green',activebackground='purple',activeforeground='white',command=withdraw_screen)
    withdraw_button.place(relx=0.01,rely=.82)
    
    transfer_button=Button(frm,text="Transfer Amount",width=15,font=('arial',20,'bold'),bd=2,bg='red',activebackground='purple',activeforeground='white',command=transfer_screen)
    transfer_button.place(relx=0.01,rely=.92)
    


def existuser_screen(): 
    def back():
        frm.destroy()
        main_screen()
        
    def fp_click():
        frm.destroy()
        forgot_screen()
    
    def reset_click():
        e_acn.delete(0,"end")
        e_pass.delete(0,"end")
        e_acn.focus()
    def submit_click():
        acn=e_acn.get()
        pwd=e_pass.get()
        
        conobj=sqlite3.connect(database="mybank.sqlite")
        curobj=conobj.cursor()
        quary='''select * from accounts where acn=? and pass=?'''
        curobj.execute(quary,(acn,pwd))
        tup=curobj.fetchone()
        conobj.close()
        if tup==None:
           messagebox.showerror('Login','Invalid Credentials')
        else:
            acn=tup[0]
            frm.destroy()
            welcome_screen(acn)
        
    
          
    frm=Frame(root,highlightbackground='black',highlightthickness='2px')
    frm.configure(bg='pink')
    frm.place(relx=0,rely=.14,relwidth=1,relheight=.8)
    
    back_button=Button(frm,text="back",font=('arial',20,'bold'),bd=2,bg='powder blue',activebackground='purple',activeforeground='white',command=back)
    back_button.place(relx=0,rely=0)
    
    
    
    lbl_acn=Label(frm,text='👤Account No',width=12,font=('arial',20,'bold'),bg='purple',fg='white')
    lbl_acn.place(relx=.2,rely=.2)
    
    e_acn=Entry(frm,font=('arial',20,'bold'),bd=5)
    e_acn.place(relx=.4,rely=.2)
    e_acn.focus
    
    lbl_pass=Label(frm,text='Password',width=12,font=('arial',20,'bold'),bg='purple',fg='white')
    lbl_pass.place(relx=.2,rely=.3)
    
    e_pass=Entry(frm,font=('arial',20,'bold'),bd=5,show='*')
    e_pass.place(relx=.4,rely=.3)
    
    submit_button=Button(frm,width=7,text="Submit",font=('arial',20,'bold'),bg='powder blue',activebackground='purple',activeforeground='white',bd=2,command=submit_click)
    submit_button.place(relx=.3,rely=.5)
    
    reset_button=Button(frm,width=7,text="Reset",font=('arial',20,'bold'),bg='powder blue',activebackground='purple',activeforeground='white',bd=2,command=reset_click)
    reset_button.place(relx=.4,rely=.5)
    
    forgot_button=Button(frm,width=18,text="Forget password",font=('arial',20,'bold'),bg='powder blue',activebackground='purple',activeforeground='white',bd=2,command=fp_click)
    forgot_button.place(relx=.3,rely=.6)
    
    
    
def newuser_screen(): 
    def back():
        frm.destroy()
        main_screen()
    
    def reset_click():
        e_name.delete(0,"end")
        e_mob.delete(0,"end")
        e_email.delete(0,"end")
        e_adhar.delete(0,"end")
        e_name.focus()
    
    def createacn_db():
        name=e_name.get()
        email=e_email.get()
        mob=e_mob.get()
        adhar=e_adhar.get()
        e_name.focus()
        if len(name)==0 or len(email)==0 or len(mob)==0 or len(adhar)==0:
            messagebox.showwarning("New User","Empty fields are not allowed")
            return
        
        match=re.fullmatch(r"^[a-zA-Z0-9_.%+-]+@[a-zA-Z]+\.[a-zA-Z]+",email)
        if match==None:
           messagebox.showwarning("New User","Invalid email")
           return
        match=re.fullmatch(r"^[6-9][0-9]{9}$",mob)
        if match==None:
           messagebox.showwarning("New User","Invalid mob no")
           return
        
        match=re.fullmatch(r"^[2-9][0-9]{11}$",adhar)
        
        if match==None:
           messagebox.showwarning("New User","Invalid Adhaar")
           return
        
        bal=0
        opendate=datetime.now()
        pwd=Generator.generate_pass()
        query='''insert into accounts values(?,?,?,?,?,?,?,?)'''
        conobj=sqlite3.connect(database="mybank.sqlite")
        curobj=conobj.cursor()
        curobj.execute(query,(None,name,pwd,mob,email,adhar,bal,opendate))
        conobj.commit()
        conobj.close()
        
        conobj=sqlite3.connect(database="mybank.sqlite")
        curobj=conobj.cursor()
        query='''select max(acn) from accounts'''
        curobj.execute(query)
        tup=curobj.fetchone()
        conobj.close()
        Email_handler.send_credentials(email,name,tup[0],pwd)
        
        messagebox.showinfo('Account Creation','Your account is opened \nWe have mailed your credentials to given email')
        
    frm=Frame(root,highlightbackground='black',highlightthickness='2px')
    frm.configure(bg='pink')
    frm.place(relx=0,rely=.14,relwidth=1,relheight=.8)
    
    back_button=Button(frm,text="back",font=('arial',20,'bold'),bd=2,bg='powder blue',activebackground='purple',activeforeground='white',command=back)
    back_button.place(relx=0,rely=0)
    

    
    lbl_name=Label(frm,text='👤Name',width=7,font=('arial',20,'bold'),bg='purple',fg='white')
    lbl_name.place(relx=.1,rely=.2)
    
    e_name=Entry(frm,font=('arial',20,'bold'),bd=5)
    e_name.place(relx=.2,rely=.2)
    e_name.focus
    
    lbl_email=Label(frm,text='📤E-Mail',width=7,font=('arial',20,'bold'),bg='purple',fg='white')
    lbl_email.place(relx=.1,rely=.3)
    
    e_email=Entry(frm,font=('arial',20,'bold'),bd=5)
    e_email.place(relx=.2,rely=.3)
    
    lbl_mob=Label(frm,text='📱Mob',width=7,font=('arial',20,'bold'),bg='purple',fg='white')
    lbl_mob.place(relx=.5,rely=.2)
    
    e_mob=Entry(frm,font=('arial',20,'bold'),bd=5)
    e_mob.place(relx=.6,rely=.2)
    
    lbl_adhar=Label(frm,text='Adhar',width=7,font=('arial',20,'bold'),bg='purple',fg='white')
    lbl_adhar.place(relx=.5,rely=.3)
    
    e_adhar=Entry(frm,font=('arial',20,'bold'),bd=5)
    e_adhar.place(relx=.6,rely=.3)  
    
    
    submit_button=Button(frm,width=7,text="Submit",font=('arial',20,'bold'),bg='powder blue',activebackground='purple',activeforeground='white',bd=2,command=createacn_db)
    submit_button.place(relx=.4,rely=.5)
    
    
    reset_button=Button(frm,width=7,text="Reset",font=('arial',20,'bold'),bg='powder blue',activebackground='purple',activeforeground='white',bd=2,command=reset_click)
    reset_button.place(relx=.5,rely=.5)
    
    ''


def main_screen():
    
    def newuser_click():
        frm.destroy()
        newuser_screen()
    
    def existuser_click():
        frm.destroy()
        existuser_screen()
        
    frm=Frame(root,highlightbackground='black',highlightthickness='2px')
    frm.configure(bg='pink')
    frm.place(relx=0,rely=.14,relwidth=1,relheight=.8)
    
    newuser_btn=Button(frm,text='New User \n Create Account',
                       font=('arial',15,'bold'),
                       bg='powder blue',
                       fg='black',
                       width=15,
                       activebackground='purple',
                       border='2px',
                       activeforeground='white',
                       command=newuser_click)
                    
                       
    newuser_btn.place(relx=.3,rely=.3)
    
    existuser_btn=Button(frm,text='Existing User \nSign In',
                       font=('arial',15,'bold'),
                       bg='powder blue',
                       fg='black',
                       width=15,
                       activebackground='purple',
                       border='2px',
                       activeforeground='white'
                       ,command=existuser_click)
    existuser_btn.place(relx=.5,rely=.3)
    
    
root=Tk()#it make top level window
root.state('zoomed') #to make fullscreen window
root.resizable(width=False,height=False)
root.configure(bg='powder blue')
title=Label(root,text="Banking Simulation",font=('arial',40,'bold','underline'),bg='powder blue')
title.pack()
curdate=time.strftime("%d-%b-%Y %r")
date=Label(root,text=curdate,font=('arial',20,'bold'),bg='powder blue',fg='blue')
date.pack(pady=15)
update_time()

img=Image.open('logo1.jpg',).resize((320,130))
imgtk=ImageTk.PhotoImage(img,master=root)

lbl_img=Label(root,image=imgtk)
lbl_img.place(relx=0,rely=0)

img2=Image.open('logo2.jpg',).resize((250,140))
imgtk2=ImageTk.PhotoImage(img2,master=root)

lbl_img2=Label(root,image=imgtk2)
lbl_img2.place(relx=0.84,rely=0)


footer=Label(root,text="Developed by:Rishabh Verma \n📱9999999",font=('arial',15,'bold'),bg='powder blue')
footer.pack(side='bottom')
main_screen() 
root.mainloop() #to make window visible