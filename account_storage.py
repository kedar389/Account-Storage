import tkinter as tk
import string
from random import choice
import sql_connector as sqlc

ALLCHARS = string.ascii_letters + string.digits + string.punctuation


class MainApp:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.geometry = self.master.geometry('450x80')

        self.pathfileLabel = tk.Label(self.frame, text="Pathfile:   ")
        self.pathfileLabel.grid(row=0, column=1, )

        self.pathfileEntry = tk.Entry(self.frame, width=45)
        self.pathfileEntry.grid(row=1, column=1)

        self.openButton = tk.Button(self.frame,
                                    text='Open File',
                                    width=30,
                                    command=self.new_window)
        self.openButton.grid(row=2, column=1)

        self.frame.grid()

        self.newWindow = None
        self.app = None

    def new_window(self):
        pathfile = self.pathfileEntry.get()

        self.newWindow = tk.Toplevel(self.master)
        self.app = AddEntityWindow(self.newWindow, pathfile)


class AddEntityWindow:
    def __init__(self, master, pathfile):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.master.geometry('550x450')
        self.sqlConn = sqlc.SqlConnector(pathfile)
        self.entity_objects = []

        self.Heading = tk.Label(self.frame, text="Add Credentials")
        self.Heading.grid(column=1, row=0)

        self.Sitelbl = tk.Label(self.frame, text="Site:")
        self.Sitelbl.grid(column=0, row=1)

        self.Namelbl = tk.Label(self.frame, text="Name:")
        self.Namelbl.grid(column=0, row=2)

        self.Passwordlbl = tk.Label(self.frame, text="Password:")
        self.Passwordlbl.grid(column=0, row=3)

        self.Filepathlbl = tk.Label(self.frame, text="Filepath:")
        self.Filepathlbl.grid(column=0, row=4)

        self.siteEntry = tk.Entry(self.frame, )
        self.siteEntry.grid(column=1, row=1)

        self.nameEntry = tk.Entry(self.frame, )
        self.nameEntry.grid(column=1, row=2)

        self.passwordEntry = tk.Entry(self.frame, state='normal')
        self.passwordEntry.grid(column=1, row=3)

        self.currentPathfile = tk.Label(self.frame, text=pathfile)
        self.currentPathfile.grid(column=1, row=4)

        self.passwordCheck = tk.IntVar()
        self.chk1 = tk.Checkbutton(self.frame,
                                   text='Generate Password',
                                   variable=self.passwordCheck,
                                   command=self.shadow_box_on_check)
        self.chk1.grid(column=2, row=3)

        self.addButton = tk.Button(self.frame,
                                   text='Add Record',
                                   command=self.submit_entry)
        self.addButton.grid(row=5, column=1)

        self.deleteButton = tk.Button(self.frame,
                                      text="Delete Record",
                                      command=self.delete_entry)
        self.deleteButton.grid(row=6, column=0)

        self.idEntry = tk.Entry(self.frame)
        self.idEntry.grid(row=6, column=1)

        self.showButton = tk.Button(self.frame,
                                    text="Show Records",
                                    command=self.show_records)
        self.showButton.grid(row=7, column=1)
        self.frame.pack()

    def shadow_box_on_check(self):
        if not self.passwordCheck.get():
            self.passwordEntry.config(state=tk.NORMAL)
        elif self.passwordCheck.get():
            self.passwordEntry.config(state=tk.DISABLED)

    def submit_entry(self):
        site = self.siteEntry.get()
        name = self.nameEntry.get()

        if self.passwordCheck.get() == 1:
            password = pass_gen()
        else:
            password = self.passwordEntry.get()

        self.sqlConn.table_creator()

        data = (None, encrypt(site), encrypt(name), encrypt(password))

        self.sqlConn.add_record(data)

        last_id = self.sqlConn.cur.lastrowid
        self.sqlConn.connection.commit()

        if self.entity_objects:
            new_entity = EntityDisplay(self.frame,
                                       site,
                                       name,
                                       password,
                                       last_id)
            new_entity.display()
            self.entity_objects.append(new_entity)

    def delete_entry(self):

        input_id = self.idEntry.get()
        self.sqlConn.delete_record(input_id)

        self.sqlConn.connection.commit()
        for i in self.entity_objects:
            if i.position == int(input_id):
                i.dataLabel.grid_forget()
                del i

    def show_records(self):
        self.entity_objects.clear()

        all_records = self.sqlConn.get_all_records()

        for record in all_records:
            self.entity_objects.append(EntityDisplay(self.frame,
                                                     decrypt(record[1]),
                                                     decrypt(record[2]),
                                                     decrypt(record[3]),
                                                     record[0]))

        for obj in self.entity_objects:
            obj.display()


class EntityDisplay:
    def __init__(self, master, site, name, password, i):
        self.master = master
        self.site = site
        self.password = password
        self.name = name
        self.position = i
        self.data = str(self.position) +\
                    "," + self.site + \
                    "," + self.name + \
                    "," + self.password
        self.dataLabel = tk.Label(master, text=self.data, font="Courier")

    def display(self):
        self.dataLabel.grid(row=8 + self.position, column=1)


def pass_gen():
    return "".join(choice(ALLCHARS) for x in range(11))


def encrypt(text):
    text = text[::-1]
    encrypted = ""
    for char in text:
        encrypted += chr(ord(char) + 8)
    return encrypted


def decrypt(text):
    text = text[::-1]
    decrypted = ""
    for char in text:
        decrypted += chr(ord(char) - 8)

    return decrypted


def main():
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()


main()
