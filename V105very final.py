import tkinter 
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import filedialog as fd
import sqlite3 as sqltor
import matplotlib.pyplot as plt
import time
conn=sqltor.connect('main.db') #main database
cursor=conn.cursor() #main cursor
cursor.execute("""CREATE TABLE IF NOT EXISTS poll
                    (name)""")

def login():
    def access():
        global go
        user=User.get()
        pwd=int(pswd.get())
        auth_ppl={'admin':110,'panda':141,'pup':111}
        global u_s
        u_s=str(user).lower()
        if user.lower() in auth_ppl.keys():
            if pwd is auth_ppl[u_s]:
                time.sleep(1)
                messagebox.showinfo('Access granted',' Welcome ' + user.upper())
                go=True
                qua.destroy()            
                
            else:
                messagebox.showerror('Access Denied','False PASSWORD')
                return False
                qua.destroy() 
        elif user not in auth_ppl.keys():
            
            messagebox.showerror('Access Denied','False USERNAME')
            return False
            qua.destroy() 
    qua=Tk()
    qua.geometry('300x300')
    color='Lavender'
    qua['bg']='Lavender'
    qua.title('login')
    Label(qua,text='L O G I N',font='Ariel',bg=color).grid(row=1,column=2,columnspan=2,padx=5,pady=5)
    Label(qua,text='Username',font='Ariel',bg=color).grid(row=2,column=1,padx=5,pady=5)
    User = Entry(qua, width=15, font=('Helvetica', 10))
    User.grid(row=2,column=2,padx=5,pady=5)
    User.insert(1,'')
    Label(qua,text='Password',font='Ariel',bg=color).grid(row=3,column=1,padx=5,pady=5)
    pswd = Entry(qua, width=15, font=('Helvetica', 10))
    pswd.grid(row=3,column=2,padx=5,pady=5)
    pswd.insert(1,'Password')
    Button(qua,text='Check Credentintials',command=access,font='Ariel',bg='sky blue').grid(row=4,column=2,padx=5,pady=5)
    qua.mainloop()

    
def pollpage(): #page for polling
     def proceed():
        chose=choose.get()
        print(chose)
        command='update polling set votes=votes+1 where name=?'
        pd.execute(command,(chose,))
        pd.commit()
        messagebox.showinfo('Success!','You have voted')
     choose=StringVar()
     names=[]
     pd=sqltor.connect(plname+'.db') #poll database
     pcursor=pd.cursor() #poll cursor
     pcursor.execute('select name from polling')
     data=pcursor.fetchall()
     for i in range(len(data)):
         data1=data[i]
         ndata=data1[0]
         names.append(ndata)
     print(names)
     ppage=Toplevel()
     ppage.geometry('300x300')
     ppage.title('Poll')


     Label(ppage,text='Vote for any one person!').grid(row=1,column=3)
     for i in range(len(names)):
         Radiobutton(ppage,text=names[i],value=names[i],variable=choose).grid(row=2+i,column=1)
     Button(ppage,text='Vote',command=proceed).grid(row=2+i+1,column=2)


def polls(): #mypolls
    def proceed():
        global pollnames
        global plname
        plname=psel.get()
        if plname=='-select-':
            return messagebox.showerror('Error','select poll')
        else:
            mpolls.destroy()
            pollpage()
    cursor.execute('select name from poll')
    data=cursor.fetchall()
    pollnames=['-select-']
    for i in range(len(data)):
        data1=data[i]
        ndata=data1[0]
        pollnames.append(ndata)
    def clear_list():
        if data==['-select-']:
            cursor.execute('delete from poll')
            messagebox.showinfo('Success!','Polls deleted')    
        else:
            cursor.execute('delete from poll')
            messagebox.showinfo('Success!','Polls deleted')
            mpolls.destroy()
    psel=StringVar()
    mpolls=Toplevel()
    mpolls.geometry('300x300')
    color='#FAF0E6'
    mpolls['bg']='#FAF0E6'
    mpolls.title('Voting Program')
    Label(mpolls,text='Select Poll',font='Helvetica 12 bold',bg=color).grid(row=1,column=3)
    select=ttk.Combobox(mpolls,values=pollnames,state='readonly',textvariable=psel)
    select.grid(row=2,column=3,padx=10,pady=10)
    select.current(0)
    Button(mpolls,text='Proceed',command=proceed).grid(row=2,column=4,padx=5,pady=5)
    Button(mpolls,text='Clear list',command=clear_list).grid(row=2,column=5,padx=5,pady=5)
    


def create():
    def proceed():
        global pcursor
        pname=name.get() #pollname
        can=cname.get()   #candidatename
        if pname=='':
            return messagebox.showerror('Error','Enter poll name')
        elif can=='':
            return messagebox.showerror('Error','Enter candidates')
        else:
            candidates=can.split(',') #candidate list
            cursor.execute('delete from poll')
            command='insert into poll (name) values (?);'
            cursor.execute(command,(pname,))
            conn.commit()
            pd=sqltor.connect(pname+'.db') #poll database
            pcursor=pd.cursor() #poll cursor
            pcursor.execute('drop table if exists polling')
            pcursor.execute("""CREATE TABLE polling
                 (name TEXT,votes INTEGER)""")
            for i in range(len(candidates)):
                command='insert into polling (name,votes) values (?, ?)'
                data=(candidates[i],0)
                pcursor.execute(command,data)
                pd.commit()
            pd.close()
            messagebox.showinfo('Success!','Poll Created')
            cr.destroy()

    name=StringVar()
    cname=StringVar()
    cr=Toplevel()
    cr.geometry('560x440')
    color='#FAF0E6'
    cr['bg']='#FAF0E6'
    cr.title('Create a new poll')
    Label(cr,text='Enter Details',font='Helvetica 12 bold',bg=color).grid(row=1,column=2)
    Label(cr,text='Enter Poll name: ',bg=color).grid(row=2,column=1)
    Entry(cr,width=40,textvariable=name).grid(row=2,column=2,padx=2,pady=3,sticky='nsw') #poll name
    Label(cr,text='(eg: captain elections)',bg=color).place(x=353,y=35)
    Label(cr,text='Enter Candidates: ',bg=color).grid(row=3,column=1,columnspan=1,padx=2,pady=3)
    Entry(cr,width=40,textvariable=cname,font='Sans 12').grid(row=3,column=2,columnspan=1,padx=2,pady=3,sticky='w') #candidate name
    Label(cr,text='Note: Enter the candidate names one by one by putting commas',bg=color).grid(row=4,column=2)
    Label(cr,text='eg: candidate1,candate2,candidate3....',bg=color).grid(row=5,column=2)
    Button(cr,text='Proceed',command=proceed).grid(row=6,column=2)
def selpl(): #pollresults
    def results():
        sel=sele.get()  #selected option
        if sel=='-select-':
            return messagebox.showerror('Error','Select Poll')
        else:
            pl.destroy()
            def project():
                names=[]
                votes=[]
                for i in range(len(r)):
                    data=r[i]
                    names.append(data[0])
                    votes.append(data[1])
                    plt.title('Poll Result')
                plt.pie(votes,labels=names,autopct='%1.1f%%',shadow=True,startangle=140)
                plt.axis('equal')
                plt.show()

            res=Toplevel() #result-page
            res.geometry('300x300')
            res.title('Results!')
            Label(res,text='Here is the Result!',font='Helvetica 12 bold').grid(row=1,column=2)
            con=sqltor.connect(sel+'.db')
            pcursor=con.cursor()
            pcursor.execute('select * from polling')
            r=pcursor.fetchall() #data-raw
            for i in range(len(r)):
                data=r[i]
                Label(res,text=data[0]+': '+str(data[1])+' votes').grid(row=2+i,column=1)
            Button(res,text='Project Results',command=project).grid(row=2+i+1,column=2)


    cursor.execute('select name from poll')
    data=cursor.fetchall()
    pollnames=['-select-']
    for i in range(len(data)):
        data1=data[i]
        ndata=data1[0]
        pollnames.append(ndata)
    sele=StringVar()
    pl=Toplevel()
    pl.geometry('300x200')
    pl['bg']='#FAF0E6'
    pl.title('Voting System')
    Label(pl,text='Select Poll',font='Helvetica 12 bold').grid(row=1,column=1)
    sel=ttk.Combobox(pl,values=pollnames,state='readonly',textvariable=sele)
    sel.grid(row=2,column=1)
    sel.current(0)
    Button(pl,text='Get Results',command=results).grid(row=2,column=2)

def about():
    messagebox.showinfo('About','Developed by Trimastishk')


def exit1():
    
    home.destroy()

#__________________________________________________________________
go=False
login()
if go:
    home=Tk()
    home.geometry('340x340')
    home.title('Voting Program')
    #home.iconbitmap('C:\\Users\\computer lab\\Desktop\\V-111\\qqq.ico')
    home['bg'] = '#00CCFF'
    Label(home,text='Voting program made in python',font='Helvetica 12 italic',bg='#00CCFF').pack(pady=5)
    Button(home,text='Create new Poll +',command=create,width=20).pack(pady=5,padx=10)
    Button(home,text='My Polls',command=polls,width=20).pack(pady=5,padx=10)
    Button(home,text='Poll Results',command=selpl,width = 20).pack(pady=5,padx=10)
    Button(home,text='About',command=about,width=20).pack(padx=5,pady=5)
    Button(home,text='Exit Program',command=exit1,width=10,bg='black',fg='white').pack(padx=5,pady=5)
    home.mainloop()
