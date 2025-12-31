from tkinter import *
from tkinter import messagebox
import tkinter.messagebox

objects = []
window = Tk()
window.withdraw()
window.title('PasswordPal - Secure Storage')
window.geometry('800x600')

class popupWindow(object):

    loop = False
    attempts = 0

    def __init__(self, master):
        top = self.top = Toplevel(master)
        top.title('Enter Master Password')
        top.geometry('{}x{}'.format(300, 120))
        top.resizable(width=False, height=False)
        
        x = (top.winfo_screenwidth() // 2) - 150
        y = (top.winfo_screenheight() // 2) - 60
        top.geometry(f'+{x}+{y}')
        
        self.l = Label(top, text="Master Password:", font=('Arial', 14), justify=CENTER)
        self.l.pack(pady=10)
        self.e = Entry(top, show='*', width=30, font=('Arial', 12))
        self.e.pack(pady=7)
        self.e.focus()
        self.b = Button(top, text='Login', command=self.cleanup, font=('Arial', 14), bg='#4CAF50', fg='white')
        self.b.pack(pady=5)
        
        self.e.bind('<Return>', lambda event: self.cleanup())

    def cleanup(self):
        self.value = self.e.get()
        access = 'password'

        if self.value == access:
            self.loop = True
            self.top.destroy()
            window.deiconify()
        else:
            self.attempts += 1
            if self.attempts == 5:
                messagebox.showerror('Access Denied', 'Too many failed attempts. Exiting.')
                window.quit()
            else:
                self.e.delete(0, 'end')
                messagebox.showerror('Incorrect Password', f'Incorrect password\nAttempts remaining: {5 - self.attempts}')

class entity_add:

    def __init__(self, master, n, p, e):
        self.password = p
        self.name = n
        self.email = e
        self.window = master

    def write(self):
        if not self.name or not self.email or not self.password:
            messagebox.showwarning('Missing Fields', 'Please fill in all fields')
            return False
            
        f = open('emails.txt', "a")
        n = self.name
        e = self.email
        p = self.password

        encryptedN = ""
        encryptedE = ""
        encryptedP = ""
        
        for letter in n:
            if letter == ' ':
                encryptedN += ' '
            else:
                encryptedN += chr(ord(letter) + 5)

        for letter in e:
            if letter == ' ':
                encryptedE += ' '
            else:
                encryptedE += chr(ord(letter) + 5)

        for letter in p:
            if letter == ' ':
                encryptedP += ' '
            else:
                encryptedP += chr(ord(letter) + 5)

        f.write(encryptedN + ',' + encryptedE + ',' + encryptedP + ',\n')
        f.close()
        return True

class entity_display:

    def __init__(self, master, n, e, p, i):
        self.password = p
        self.name = n
        self.email = e
        self.window = master
        self.i = i
        self.showing_password = False

        dencryptedN = ""
        dencryptedE = ""
        dencryptedP = ""
        
        for letter in self.name:
            if letter == ' ':
                dencryptedN += ' '
            else:
                dencryptedN += chr(ord(letter) - 5)

        for letter in self.email:
            if letter == ' ':
                dencryptedE += ' '
            else:
                dencryptedE += chr(ord(letter) - 5)

        for letter in self.password:
            if letter == ' ':
                dencryptedP += ' '
            else:
                dencryptedP += chr(ord(letter) - 5)

        self.decrypted_name = dencryptedN
        self.decrypted_email = dencryptedE
        self.decrypted_password = dencryptedP

        self.label_name = Label(self.window, text=dencryptedN, font=('Arial', 12), width=20, anchor='w')
        self.label_email = Label(self.window, text=dencryptedE, font=('Arial', 12), width=30, anchor='w')
        self.label_pass = Label(self.window, text='*' * len(dencryptedP), font=('Arial', 12), width=20, anchor='w')
        self.showButton = Button(self.window, text='Show', command=self.toggle_password, width=6)
        self.copyButton = Button(self.window, text='Copy', command=self.copy_password, width=6)
        self.deleteButton = Button(self.window, text='Delete', fg='red', command=self.delete, width=6)

    def toggle_password(self):
        if self.showing_password:
            self.label_pass.config(text='*' * len(self.decrypted_password))
            self.showButton.config(text='Show')
            self.showing_password = False
        else:
            self.label_pass.config(text=self.decrypted_password)
            self.showButton.config(text='Hide')
            self.showing_password = True

    def copy_password(self):
        self.window.clipboard_clear()
        self.window.clipboard_append(self.decrypted_password)
        messagebox.showinfo('Copied', 'Password copied to clipboard!')

    def display(self):
        self.label_name.grid(row=6 + self.i, column=0, sticky=W, padx=5, pady=2)
        self.label_email.grid(row=6 + self.i, column=1, sticky=W, padx=5, pady=2)
        self.label_pass.grid(row=6 + self.i, column=2, sticky=W, padx=5, pady=2)
        self.showButton.grid(row=6 + self.i, column=3, padx=2, pady=2)
        self.copyButton.grid(row=6 + self.i, column=4, padx=2, pady=2)
        self.deleteButton.grid(row=6 + self.i, column=5, padx=2, pady=2)

    def delete(self):
        answer = tkinter.messagebox.askquestion('Delete', f'Delete entry for {self.decrypted_name}?')

        if answer == 'yes':
            for i in objects:
                i.destroy()

            f = open('emails.txt', 'r')
            lines = f.readlines()
            f.close()

            f = open('emails.txt', "w")
            count = 0

            for line in lines:
                if count != self.i:
                    f.write(line)
                count += 1

            f.close()
            objects.clear()
            readfile()

    def destroy(self):
        self.label_name.destroy()
        self.label_email.destroy()
        self.label_pass.destroy()
        self.showButton.destroy()
        self.copyButton.destroy()
        self.deleteButton.destroy()

def onsubmit():
    m = email.get()
    p = password.get()
    n = name.get()
    
    if not n or not m or not p:
        messagebox.showwarning('Incomplete', 'Please fill in all fields')
        return
    
    e = entity_add(window, n, p, m)
    if e.write():
        name.delete(0, 'end')
        email.delete(0, 'end')
        password.delete(0, 'end')
        messagebox.showinfo('Success', f'Entry added for {n}')
        for obj in objects:
            obj.destroy()
        objects.clear()
        readfile()

def clearfile():
    answer = messagebox.askyesno('Clear All', 'Delete ALL entries? This cannot be undone!')
    if answer:
        f = open('emails.txt', "w")
        f.close()
        for obj in objects:
            obj.destroy()
        objects.clear()
        messagebox.showinfo('Cleared', 'All entries deleted')

def readfile():
    try:
        f = open('emails.txt', 'r')
        count = 0

        for line in f:
            if line.strip():
                entityList = line.split(',')
                if len(entityList) >= 3:
                    e = entity_display(window, entityList[0], entityList[1], entityList[2], count)
                    objects.append(e)
                    e.display()
                    count += 1
        f.close()
    except FileNotFoundError:
        f = open('emails.txt', 'w')
        f.close()

m = popupWindow(window)

title_label = Label(window, text='🔐 PasswordPal', font=('Arial', 20, 'bold'))
title_label.grid(columnspan=6, row=0, pady=10)

entity_label = Label(window, text='Add New Entry', font=('Arial', 16))
entity_label.grid(columnspan=6, row=1, pady=5)

name_label = Label(window, text='Name:', font=('Arial', 12))
email_label = Label(window, text='Email/Username:', font=('Arial', 12))
pass_label = Label(window, text='Password:', font=('Arial', 12))

name = Entry(window, font=('Arial', 12), width=40)
email = Entry(window, font=('Arial', 12), width=40)
password = Entry(window, show='*', font=('Arial', 12), width=40)

name_label.grid(row=2, column=0, sticky=E, padx=5, pady=5)
email_label.grid(row=3, column=0, sticky=E, padx=5, pady=5)
pass_label.grid(row=4, column=0, sticky=E, padx=5, pady=5)

name.grid(row=2, column=1, columnspan=5, padx=5, pady=5, sticky=W)
email.grid(row=3, column=1, columnspan=5, padx=5, pady=5, sticky=W)
password.grid(row=4, column=1, columnspan=5, padx=5, pady=5, sticky=W)

submit = Button(window, text='Add Entry', command=onsubmit, font=('Arial', 12), bg='#4CAF50', fg='white', width=15)
submit.grid(row=4, column=6, pady=5, padx=5)

clear_button = Button(window, text='Clear All', command=clearfile, font=('Arial', 10), bg='#f44336', fg='white', width=10)
clear_button.grid(row=0, column=6, pady=5, padx=5, sticky=E)

separator = Label(window, text='─' * 100, font=('Arial', 10))
separator.grid(columnspan=7, row=5, pady=10)

name_label2 = Label(window, text='Name', font=('Arial', 12, 'bold'), width=20, anchor='w')
email_label2 = Label(window, text='Email/Username', font=('Arial', 12, 'bold'), width=30, anchor='w')
pass_label2 = Label(window, text='Password', font=('Arial', 12, 'bold'), width=20, anchor='w')

name_label2.grid(row=5, column=0, sticky=W, padx=5, pady=5)
email_label2.grid(row=5, column=1, sticky=W, padx=5, pady=5)
pass_label2.grid(row=5, column=2, sticky=W, padx=5, pady=5)

readfile()

window.mainloop()