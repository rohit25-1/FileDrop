import tkinter as tk
from tkinter import filedialog,messagebox,LabelFrame,CENTER,FLAT,RAISED
import socket
import os

button="none"
location=""
file_name=""
file_size=0

def open_file():
    global button,location,file_name,file_size
    button="opened"
    location=filedialog.askopenfilename()
    file_name=os.path.basename(location)
    if(len(file_name)>15):
        label_nameOffile["text"]="File: "+file_name[:15]+".."
    else:
        label_nameOffile["text"]="File: "+file_name
    file_size=os.path.getsize(location)


def send():
    if(button != "opened" or file_name==""):
        messagebox.showinfo("my message","Please Open A File To Transfer")
    else:
        print(file_name," ",file_size," ",location)
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.bind(("<Enter The IP Adddress of Your sending machine>",12345))#enter the ip address of current machine
        SEPARATOR = "<SEPARATOR>"
        s.listen(10)
        c,addr=s.accept()
        c.send(f'{name}{SEPARATOR}{filesize}').encode()
        f=open(location,'rb')
        datas=f.read(1024)
        while datas:
            c.send(datas)
            datas=f.read(1024)
        f.close()
        messagebox.showinfo("my message","Done Transferring!")
def receive():#this function reveives the  file
    SEPARATOR="<SEPARATOR>"
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect(("<Enter the ip address of receiving machine>",12345))#Enter the ip address from the receiving machine
    received = s.recv(1024).decode()
    filename, filesize = received.split(SEPARATOR)
    filesize = int(filesize)
    name="C:/Users/<USERNAME>/Downloads/"+filename#username of your pc
    f=open(name,"wb")
    while True:
        datas=s.recv(1024)
        while datas:
            f.write(datas)
            datas=s.recv(1024)
        break
    f.close()
	messagebox.showinfo("my message","Done Receiving!")


window=tk.Tk()#creates a tkinter window
windowWidth = window.winfo_reqwidth()
windowHeight = window.winfo_reqheight()
positionRight = int(window.winfo_screenwidth()/2 - windowWidth/2)
positionDown = int(window.winfo_screenheight()/2 - windowHeight/2)
window.geometry("+{}+{}".format(positionRight, positionDown))#used to position the tkinter window to the center
window.geometry("400x200")#sets the width and height; its x not *
labelframe = LabelFrame(window,bd=0,height=400)#makes a frame to store widgets with 0 border
labelframe.pack(fill="both", expand="yes")
labelframe.place(relx=0.5, rely=0.5, anchor=CENTER)#location of frame
window.title("Airdrop")#titlebar
lable1=tk.Label(labelframe,text="AirDrop",font=('Helvetica',50),pady=5)#displays the label "airdrop"
lable1.pack()
label_nameOffile=tk.Label(labelframe,text="",font=('Helvetica',15),fg="gray46")#displays the name of file opened, kept ready for transfer
label_nameOffile.pack()
labelframe2 = LabelFrame(labelframe,bd=0,height=10)
labelframe2.pack(fill="both", expand="no")
open_button=tk.Button(labelframe2,text="open",relief=RAISED,width=5,command=open_file)
open_button.grid(row=0,column=1,pady=10)
send_button=tk.Button(labelframe2,text="send",relief=RAISED,width=5,command=send)
send_button.grid(row=0,column=2,padx=50)
receive_button=tk.Button(labelframe2,text="receive",relief=RAISED,width=5,command=receive)
receive_button.grid(row=0,column=3)
window.mainloop()