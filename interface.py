from tkinter import *
from backend import Database


class Label_entry:
    def __init__(self, master,row, column, text):
        self.text = StringVar()
        self.e = Entry(master, width=12, textvariable=self.text)
        self.e.grid(row=row, column=column+1, pady=2)
        self.l = Label(master, text=text)
        self.l.grid(row=row, column=column, pady=2)


class Interface(Label_entry):

    def __init__(self, db):
        self.db = db
        self.selected_item = ""

        self.window = Tk()
        self.window.wm_title("Book Inventory")
        self.el_author = Label_entry(self.window, 0, 2, "Author")
        self.el_title = Label_entry(self.window, 0, 0, "Title")
        self.el_year = Label_entry(self.window, 1, 2, "Year")
        self.el_isbn = Label_entry(self.window, 1, 0, "ISBN")

        self.listbox = Listbox(self.window, width=35)
        self.listbox.grid(row=2, column=0, rowspan=6, columnspan=2, pady=2, padx=2)
        self.listbox.bind("<<ListboxSelect>>", self.getSelectedRow)

        self.scrollbar = Scrollbar(self.window)
        self.scrollbar.grid(row=2, column=2, rowspan=6, padx=2, pady=2)

        self.listbox.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.configure(command=self.listbox.yview)

        self.b_viewall = Button(self.window, text="View All", command=self.view_command)
        self.b_viewall.grid(row=2, column=3)

        self.b_searchentry = Button(self.window, text="Search Entry", command=self.search_command)
        self.b_searchentry.grid(row=3, column=3)

        self.b_addentry = Button(self.window, text="Add Entry", command=self.add_command)
        self.b_addentry.grid(row=4, column=3)

        self.b_update = Button(self.window, text="Update", command=self.update_command)
        self.b_update.grid(row=5, column=3)

        self.b_delete = Button(self.window, text="Delete", command=self.delete_command)
        self.b_delete.grid(row=6, column=3)

        self.b_close = Button(self.window, text="Close", command=self.close_command)
        self.b_close.grid(row=7, column=3)

    def view_command(self):
        self.listbox.delete(0, END)
        rows = self.db.view()
        for row in rows:
            self.listbox.insert(END, row)

    def search_command(self):
        self.listbox.delete(0, END)
        rows = self.db.search(self.el_title.text.get(), self.el_author.text.get(),
                               self.el_year.text.get(), self.el_isbn.text.get())
        for row in rows:
            self.listbox.insert(END, row)

    def add_command(self):
        db.insert(self.el_title.text.get(), self.el_author.text.get(), self.el_year.text.get(), self.el_isbn.text.get())
        self.listbox.delete(0, END)
        self.listbox.insert(END, (
            self.el_title.text.get(), self.el_author.text.get(), self.el_year.text.get(), self.el_isbn.text.get()))

    def getSelectedRow(self, event):
        if len(self.listbox.curselection()):
            index = self.listbox.curselection()[0]
            self.selected_item = self.listbox.get(index)
            self.el_title.e.delete(0, END)
            self.el_title.e.insert(0, self.selected_item[1])
            self.el_author.e.delete(0, END)
            self.el_author.e.insert(0, self.selected_item[2])
            self.el_year.e.delete(0, END)
            self.el_year.e.insert(0, self.selected_item[3])
            self.el_isbn.e.delete(0, END)
            self.el_isbn.e.insert(0, self.selected_item[4])

    def delete_command(self):
        self.db.delete(self.selected_item[0])
        self.e_title.e.delete(0, END)
        self.el_author.e.delete(0, END)
        self.e_year.e.delete(0, END)
        self.e_isbn.e.delete(0, END)

    def update_command(self):
        self.db.update(self.selected_item[0], self.el_title.text.get(),
                       self.el_author.text.get(), self.el_year.text.get(), self.el_isbn.text.get())

    def close_command(self):
        del self.db
        self.window.destroy()

db = Database("books.db")
interface = Interface(db)
interface.window.mainloop()

