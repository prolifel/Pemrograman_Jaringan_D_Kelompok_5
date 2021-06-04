import socket
import os
import json
import tkinter as tk
from tkinter import *
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo

TARGET_IP = "127.0.0.1"
TARGET_PORT = 8889


class ChatClient:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (TARGET_IP,TARGET_PORT)
        self.sock.connect(self.server_address)
        self.tokenid=""
    def proses(self,cmdline):
        j=cmdline.split(" ")
        try:
            command=j[0].strip()
            if (command=='auth'):
                username=j[1].strip()
                password=j[2].strip()
                return self.login(username,password)
            elif (command=='send'):
                usernameto = j[1].strip()
                message=""
                for w in j[2:]:
                   message="{} {}" . format(message,w)
                return self.sendmessage(usernameto,message)
            elif (command=='inbox'):
                return self.inbox()
            else:
                return "*Maaf, command tidak benar"
        except IndexError:
                return "-Maaf, command tidak benar"

    def sendstring(self,string):
        try:
            self.sock.sendall(string.encode())
            receivemsg = ""
            while True:
                data = self.sock.recv(64)
                print("diterima dari server",data)
                if (data):
                    receivemsg = "{}{}" . format(receivemsg,data.decode())  #data harus didecode agar dapat di operasikan dalam bentuk string
                    if receivemsg[-4:]=='\r\n\r\n':
                        print("end of string")
                        return json.loads(receivemsg)
        except:
            self.sock.close()
            return { 'status' : 'ERROR', 'message' : 'Gagal'}

    def login(self,username,password):
        string="auth {} {} \r\n" . format(username,password)
        print(username)
        print(password)
        result = self.sendstring(string)

        if result['status']=='OK':
            self.tokenid=result['tokenid']
            # return "username {} logged in, token {} " .format(username,self.tokenid)
            self.successLogin()
            self.after_sign_in()



        elif(result['status']=='ERROR' and result['message']=='Password Salah'):
            # return "Error, {}" . format(result['message'])
            self.wrongPass()

        elif(result['status']=='ERROR' and result['message']=='User Tidak Ada'):
           self.userNotFound()

    def successLogin(self):
        self.success = Toplevel()
        self.success.geometry("350x250")
        self.success.configure(bg="light green")
        self.success.title("Successfull Sign In")
        self.stop = tk.Button(self.success, text='Success', width=25, height=2, command=self.success.destroy,
                         bg="green", activebackground="light grey", relief=GROOVE)
        self.stop.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.login_win.destroy

    def wrongPass(self):
        self.wrong_pass = Toplevel()
        self.wrong_pass.geometry("350x250")
        self.wrong_pass.title("Wrong PassWord")
        self.wrong_pass.configure(bg="yellow")
        self.stop = tk.Button(self.wrong_pass, text='Wrong Password', width=25, height=2,
                         command=self.wrong_pass.destroy, bg="red", activebackground="red", relief=GROOVE)
        self.stop.place(relx=0.5, rely=0.5, anchor=CENTER)

    def userNotFound(self):
        self.user_not_found = Toplevel()
        self.user_not_found.geometry("350x250")
        self.user_not_found.title("User not Found ")
        self.user_not_found.configure(bg="yellow")
        self.stop = tk.Button(self.user_not_found, text='User not Found Kindly register First', width=30,
                         height=2, command=self.user_not_found.destroy, bg="red", activebackground="red", relief=GROOVE)
        self.stop.place(relx=0.5, rely=0.5, anchor=CENTER)

    def browseFile(self):
        filetypes = (
            ('text files', '*.txt'),
            ('All files', '*.*')
        )

        filename = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes)

        showinfo(
            title='Selected File',
            message=filename
        )

    def sendmessage(self,usernameto="xxx",message="xxx"):
        if (self.tokenid==""):
            return "Error, not authorized"
        string="send {} {} {} \r\n" . format(self.tokenid,usernameto,message)
        print(string)
        result = self.sendstring(string)
        if result['status']=='OK':
            return "message sent to {}" . format(usernameto)
        else:
            return "Error, {}" . format(result['message'])

    def inbox(self):
        if (self.tokenid==""):
            return "Error, not authorized"
        string="inbox {} \r\n" . format(self.tokenid)
        result = self.sendstring(string)
        if result['status']=='OK':
            return "{}" . format(json.dumps(result['messages']))
        else:
            return "Error, {}" . format(result['message'])

    def sign_in(self):
        self.login_win = Tk()
        self.login_win.title('Sign In')
        self.login_win.geometry('500x350')
        self.login_win.configure(bg="light blue")

        self.login_user = StringVar()
        self.login_pass = StringVar()

        self.msg1 = tk.Label(self.login_win, text='User Name', relief=GROOVE)
        self.msg1.place(relx=0.2, rely=0.3, anchor=CENTER)

        self.msg2 = tk.Label(self.login_win, text=' Password ', relief=GROOVE)
        self.msg2.place(relx=0.2, rely=0.5, anchor=S)

        self.user_name = Entry(self.login_win, textvariable=self.login_user, relief=GROOVE)
        self.user_name.place(relx=0.6, rely=0.3, anchor=CENTER, width=300)

        self.user_pass = Entry(self.login_win, show="*",
                          textvariable=self.login_pass, relief=GROOVE)
        self.user_pass.place(relx=0.6, rely=0.5, anchor=S, width=300, )

        self.button = tk.Button(self.login_win, text='Sign In', width=20, height=2, command= lambda: self.login(self.login_user.get(), self.login_pass.get()),
                           activebackground="dark grey", activeforeground="red", relief=GROOVE)
        self.button.place(relx=0.5, rely=0.7, anchor=CENTER)

        self.stop = tk.Button(self.login_win, text='EXIT', width=20, command=self.login_win.destroy,
                         bg="red", activebackground="red", relief=GROOVE)
        self.stop.place(relx=0.3, rely=1, anchor=SE)

        self.login_win.mainloop()

    def after_sign_in(self):
        self.window = Tk()
        self.window.title("Connected To: " )

        self.txtMessages = Text(self.window, width=50)
        self.txtMessages.grid(row=0, column=0, padx=10, pady=10)

        self.txtYourMessage = Entry(self.window, width=50)
        self.txtYourMessage.insert(0, "Your message")
        self.txtYourMessage.grid(row=1, column=0, padx=10, pady=10)

        self.btnSendMessage = Button(self.window, text="Send", width=20)
        self.btnSendMessage.grid(row=2, column=0, padx=10, pady=10)

        self.btnBrowse = Button(self.window, text="Browse File", width=20, command= self.browseFile)
        self.btnBrowse.grid(row=2, column=1, padx=10, pady=10)
        # self.btnBrowse.pack(expand=True)

        # self.window.mainloop()


if __name__=="__main__":
    cc = ChatClient()
    cc.sign_in()

    # while True:
    #     cmdline = input("Command {}:" . format(cc.tokenid))
    #     print(cc.proses(cmdline))

