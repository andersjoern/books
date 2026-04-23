# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 18:55:58 2020

@author: Anders J. Andersen
"""

import tkinter as tk
from tkinter import messagebox, ttk

import bookdb


# function to return key for any value in a dictionary
def get_key(my_dict, val):
    for key, value in my_dict.items():
        if val == value:
            return key
    return None


class SelectAuthor(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.res_val = None
        self.res_key = None
        self.title("Choose an Author")
        self.author_dict = {r[1]: r[0] for r in bookdb.get_authors()}
        self.author = ttk.Combobox(
            self, values=list(self.author_dict.keys()), state="readonly"
        )
        self.author.grid(column=0, row=0, padx=3, pady=3)
        btn_ok = ttk.Button(self)
        btn_ok["text"] = "Ok"
        btn_ok.grid(column=0, row=1, padx=3, pady=3)
        btn_ok["command"] = self.ok_click

        btn_cancel = ttk.Button(self)
        btn_cancel["text"] = "Cancel"
        btn_cancel.grid(column=1, row=1, padx=3, pady=3)
        btn_cancel["command"] = self.cancel_click

        if master is not None:
            self.master = master
        self.transient(master)
        self.grab_set()
        self.wait_window(self)

    def ok_click(self):
        self.res_val = self.author.get()
        if self.res_val is not None:
            self.res_key = self.author_dict[self.res_val]
        self.destroy()

    def cancel_click(self):
        self.res_val = None
        self.res_key = None
        self.destroy()

    def get_result(self):
        return self.res_key, self.res_val


class EditAuthorDlg(tk.Toplevel):
    def __init__(self, master=None, pid=None):
        super().__init__(master)
        self.result = False
        self.pid = pid
        self.pid = pid
        tk.Label(self, text="Id:", width=10, anchor="e").grid(
            column=0, row=0, padx=3, pady=3
        )
        tk.Label(self, text="Name:", width=10, anchor="e").grid(
            column=0, row=1, padx=3, pady=3
        )
        self.author_id = tk.Entry(self)
        self.author_id.grid(column=1, row=0, padx=3, pady=3)

        self.author_name = tk.Entry(self)
        self.author_name.grid(column=1, row=1, padx=3, pady=3)

        btn_ = tk.Button(self)
        btn_["text"] = "Save"
        btn_["command"] = self.save_and_closeWin
        btn_.grid(column=1, row=2, padx=3, pady=3)

        if pid is not None:
            self.author_data = bookdb.get_author(pid)
            if self.author_data is not None:
                self.author_id.insert(0, self.author_data[0])
                self.author_name.insert(0, self.author_data[1])

        self.author_id.config(state="readonly")
        self.title("Author Dialog")
        self.geometry("300x100")
        self.transient(master)
        self.grab_set()
        self.wait_window(self)

    def save_and_closeWin(self):
        name = self.author_name.get()
        self.result = bookdb.save_author(self.pid, name)
        self.destroy()


class EditPublisherDlg(tk.Toplevel):
    def __init__(self, master=None, pid=None):
        super().__init__(master)
        self.result = False
        self.pid = pid
        tk.Label(self, text="Id:", width=10, anchor="e").grid(
            column=0, row=0, padx=3, pady=3
        )
        tk.Label(self, text="Name:", width=10, anchor="e").grid(
            column=0, row=1, padx=3, pady=3
        )
        self.publisher_id = tk.Entry(self)
        self.publisher_id.grid(column=1, row=0, padx=3, pady=3)

        self.publisher_name = tk.Entry(self)
        self.publisher_name.grid(column=1, row=1, padx=3, pady=3)

        btn_ = tk.Button(self)
        btn_["text"] = "Save"
        btn_["command"] = self.save_and_closeWin
        btn_.grid(column=1, row=2, padx=3, pady=3)

        if pid is not None:
            self.publisher_data = bookdb.get_publisher(pid)
            if self.publisher_data is not None:
                self.publisher_id.insert(0, self.publisher_data[0])
                self.publisher_name.insert(0, self.publisher_data[1])

        self.publisher_id.config(state="readonly")
        self.title("Publisher Dialog")
        self.geometry("300x100")
        self.transient(master)
        self.grab_set()
        self.wait_window(self)

    def save_and_closeWin(self):
        name = self.publisher_name.get()
        self.result = bookdb.save_publisher(self.pid, name)
        self.destroy()


class EditBookDlg(tk.Toplevel):
    def __init__(self, master=None, pid=None):
        super().__init__(master)
        self.pid = pid
        ttk.Label(self, text="Id:", width=10, anchor="e").grid(
            column=0, row=0, padx=3, pady=3
        )
        ttk.Label(self, text="Author(s):", width=10, anchor="e").grid(
            column=0, row=1, padx=3, pady=3
        )
        ttk.Label(self, text="Publisher:", width=10, anchor="e").grid(
            column=0, row=2, padx=3, pady=3
        )
        ttk.Label(self, text="ISBN:", width=10, anchor="e").grid(
            column=0, row=3, padx=3, pady=3
        )
        ttk.Label(self, text="Edition:", width=10, anchor="e").grid(
            column=0, row=4, padx=3, pady=3
        )
        ttk.Label(self, text="Title:", width=10, anchor="e").grid(
            column=0, row=5, padx=3, pady=3
        )
        btn_ = ttk.Button(self)

        self.publisher_dict = {r[0]: r[1] for r in bookdb.get_publishers()}

        self.id = ttk.Entry(self)
        self.id.grid(column=1, row=0, padx=3, pady=3)

        self.authors = tk.Listbox(self)
        self.authors.grid(column=1, row=1, padx=3, pady=3)
        self.author_list = []
        self.button_frame = ttk.Frame(self)
        self.add_author_btn = ttk.Button(self.button_frame)
        self.add_author_btn["text"] = "Add author"
        self.add_author_btn["command"] = self.add_an_author
        self.remove_author_btn = ttk.Button(self.button_frame)
        self.remove_author_btn["text"] = "Remove author"
        self.remove_author_btn["command"] = self.remove_an_author
        self.add_author_btn.pack()
        self.remove_author_btn.pack()
        self.button_frame.grid(column=2, row=1, padx=3, pady=3)

        self.publisher = ttk.Combobox(
            self, values=list(self.publisher_dict.values()), state="readonly"
        )
        self.publisher.grid(column=1, row=2, padx=3, pady=3)

        self.isbn = ttk.Entry(self)
        self.isbn.grid(column=1, row=3, padx=3, pady=3)

        self.edition = ttk.Entry(self)
        self.edition.grid(column=1, row=4, padx=3, pady=3)

        self.book_title = ttk.Entry(self)
        self.book_title.grid(column=1, row=5, padx=3, pady=3)

        btn_["text"] = "Save"
        btn_["command"] = self.save_and_closeWin
        btn_.grid(column=1, row=6, padx=3, pady=3)

        if pid is not None:
            self.book_data = bookdb.get_book(pid)
            if self.book_data is not None:
                self.id.insert(0, self.book_data[0])
                self.book_authores = bookdb.get_book_authors(pid)
                for author in self.book_authores:
                    self.authors.insert(author[0], author[1])
                    self.author_list.append(author[0])
                self.publisher.set(self.publisher_dict[self.book_data[1]])
                self.isbn.insert(0, self.book_data[2])
                self.edition.insert(0, self.book_data[3])
                self.book_title.insert(0, self.book_data[4])

        self.id.config(state="readonly")
        if master is not None:
            self.master = master
        self.result = False
        self.title("Books Dialog")
        self.geometry("400x400")
        self.transient(master)
        self.grab_set()
        self.wait_window(self)

    def save_and_closeWin(self):
        publisher_id = get_key(self.publisher_dict, self.publisher.get())
        isbn = self.isbn.get()
        edition = self.edition.get()
        book_title = self.book_title.get()
        if publisher_id is not None:
            self.result = bookdb.save_book(
                self.pid, self.author_list, publisher_id, isbn, edition, book_title
            )
        self.destroy()

    def add_an_author(self):
        sel_author = SelectAuthor()
        author_id, author_name = sel_author.get_result()
        if author_id is not None and author_name is not None:
            self.authors.insert(author_id, author_name)
            self.author_list.append(author_id)

    def remove_an_author(self):
        idx = self.authors.curselection()
        if idx != ():
            self.authors.delete(idx)
            author_list_new = []
            for i, v in enumerate(self.author_list):
                if i != idx[0]:
                    author_list_new.append(v)
            self.author_list = author_list_new


class Application(tk.Frame):
    def __init__(self):
        master = tk.Tk()
        super().__init__(master)
        self.master = master
        self.master.title("Books")
        self.master.geometry("600x400")
        self.luk = ttk.Button(self.master, text="Close", command=self.master.destroy)
        self.tab_control = ttk.Notebook(self.master)
        self.book_tab = ttk.Frame(self.tab_control)
        self.publisher_tab = ttk.Frame(self.tab_control)
        self.author_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.book_tab, text="Books")
        self.tab_control.add(self.publisher_tab, text="Publishers")
        self.tab_control.add(self.author_tab, text="Authors")
        self.tab_control.pack(expand=1, fill="both")
        self._create_books_table()
        self._create_publisher_table()
        self._create_author_table()
        self.luk.pack(side="bottom")

    def _create_books_table(self) -> None:
        self.book_tab.columnconfigure(0, weight=1)
        self.book_tab.rowconfigure(0, weight=1)
        self.books_table = ttk.Treeview(self.book_tab)
        vertical_scroll_bar = ttk.Scrollbar(
            self.books_table, orient="vertical", command=self.books_table.yview
        )
        vertical_scroll_bar.pack(side="right", fill="y")
        self.books_table.configure(xscrollcommand=vertical_scroll_bar.set)
        self.books_table.grid(
            column=0, row=0, padx=3, pady=20, columnspan=3, sticky="nsew"
        )
        ttk.Button(self.book_tab, text="Edit book", command=self.EditBookDialog).grid(
            column=0, row=1, sticky="e"
        )
        ttk.Button(self.book_tab, text="New book", command=self.NewBookDialog).grid(
            column=1, row=1
        )
        ttk.Button(self.book_tab, text="Delete book", command=self.DeleteBook).grid(
            column=2, row=1
        )
        self.books_table["columns"] = ("ISBN", "Title")
        self.books_table.heading("#0", text="Id", anchor=tk.W)
        self.books_table.heading("#1", text="ISBN", anchor=tk.W)
        self.books_table.heading("#2", text="Title", anchor=tk.W)
        self.fill_book_table()

    def _create_publisher_table(self) -> None:
        self.publisher_tab.columnconfigure(0, weight=1)
        self.publisher_tab.rowconfigure(0, weight=1)
        self.publisher_table = ttk.Treeview(self.publisher_tab)
        vertical_scroll_bar = ttk.Scrollbar(
            self.publisher_table, orient="vertical", command=self.publisher_table.yview
        )
        vertical_scroll_bar.pack(side="right", fill="y")
        self.publisher_table.configure(xscrollcommand=vertical_scroll_bar.set)
        self.publisher_table.grid(
            column=0, row=0, padx=3, pady=20, columnspan=3, sticky="nsew"
        )
        ttk.Button(
            self.publisher_tab, text="Edit publisher", command=self.EditPublisherDialog
        ).grid(column=0, row=1, sticky="e")
        ttk.Button(
            self.publisher_tab, text="New publisher", command=self.NewPublisherDialog
        ).grid(column=1, row=1)
        ttk.Button(
            self.publisher_tab, text="Delete publisher", command=self.DeletePublisher
        ).grid(column=2, row=1)
        self.publisher_table["columns"] = ("Name",)
        self.publisher_table.heading("#0", text="Id", anchor=tk.W)
        self.publisher_table.heading("#1", text="Name", anchor=tk.W)
        self.fill_publisher_table()

    def _create_author_table(self) -> None:
        self.author_tab.columnconfigure(0, weight=1)
        self.author_tab.rowconfigure(0, weight=1)
        self.author_table = ttk.Treeview(self.author_tab)
        vertical_scroll_bar = ttk.Scrollbar(
            self.author_table, orient="vertical", command=self.author_table.yview
        )
        vertical_scroll_bar.pack(side="right", fill="y")
        self.author_table.configure(xscrollcommand=vertical_scroll_bar.set)
        self.author_table.grid(
            column=0, row=0, padx=3, pady=20, columnspan=3, sticky="nsew"
        )
        ttk.Button(
            self.author_tab, text="Edit author", command=self.EditAuthorDialog
        ).grid(column=0, row=1, sticky="e")
        ttk.Button(
            self.author_tab, text="New author", command=self.NewAuthorDialog
        ).grid(column=1, row=1)
        ttk.Button(
            self.author_tab, text="Delete author", command=self.DeleteAuthor
        ).grid(column=2, row=1)
        self.author_table["columns"] = ("Name",)
        self.author_table.heading("#0", text="Id", anchor=tk.W)
        self.author_table.heading("#1", text="Name", anchor=tk.W)
        self.fill_author_table()

    def fill_book_table(self):
        self.books_table.delete(*self.books_table.get_children())
        books_data = bookdb.get_books()
        for r in books_data:
            self.books_table.insert("", "end", text=r[0], values=(r[2], r[4], ""))

    def fill_publisher_table(self):
        self.publisher_table.delete(*self.publisher_table.get_children())
        publisher_data = bookdb.get_publishers()
        for r in publisher_data:
            self.publisher_table.insert("", "end", text=r[0], values=(r[1], ""))

    def fill_author_table(self):
        self.author_table.delete(*self.author_table.get_children())
        author_data = bookdb.get_authors()
        for r in author_data:
            self.author_table.insert("", "end", text=r[0], values=(r[1], ""))

    def EditBookDialog(self):
        focus = self.books_table.focus()
        selected_items = self.books_table.item(focus)
        book_id = selected_items["text"]
        if not book_id:
            messagebox.showwarning("Warning", "No book selected")
            return
        d = EditBookDlg(self.master, book_id)
        if d.result:
            self.fill_book_table()

    def EditPublisherDialog(self):
        focus = self.publisher_table.focus()
        selected_items = self.publisher_table.item(focus)
        publisher_id = selected_items["text"]
        if not publisher_id:
            messagebox.showwarning("Warning", "No publisher selected")
            return
        d = EditPublisherDlg(self.master, publisher_id)
        if d.result:
            self.fill_publisher_table()

    def EditAuthorDialog(self):
        focus = self.author_table.focus()
        selected_items = self.author_table.item(focus)
        author_id = selected_items["text"]
        if not author_id:
            messagebox.showwarning("Warning", "No author selected")
            return
        d = EditAuthorDlg(self.master, author_id)
        if d.result:
            self.fill_author_table()

    def NewBookDialog(self):
        d = EditBookDlg(self.master)
        if d.result:
            self.fill_book_table()

    def NewPublisherDialog(self):
        d = EditPublisherDlg(self.master)
        if d.result:
            self.fill_publisher_table()

    def NewAuthorDialog(self):
        d = EditAuthorDlg(self.master)
        if d.result:
            self.fill_author_table()

    def DeleteBook(self):
        focus = self.books_table.focus()
        selected_items = self.books_table.item(focus)
        book_id = selected_items["text"]
        if not book_id:
            messagebox.showwarning("Warning", "No book selected")
            return
        message_delete = messagebox.askyesno(
            title="Question", message="Delete book id: " + str(book_id)
        )
        if message_delete:
            bookdb.delete_book(int(book_id))
            self.fill_book_table()

    def DeletePublisher(self):
        focus = self.publisher_table.focus()
        selected_items = self.publisher_table.item(focus)
        publisher_id = selected_items["text"]
        if not publisher_id:
            messagebox.showwarning("Warning", "No publisher selected")
            return
        message_delete = messagebox.askyesno(
            title="Question", message="Delete publisher id: " + str(publisher_id)
        )
        if message_delete:
            bookdb.delete_publisher(int(publisher_id))
            self.fill_publisher_table()

    def DeleteAuthor(self):
        focus = self.author_table.focus()
        selected_items = self.author_table.item(focus)
        author_id = selected_items["text"]
        if not author_id:
            messagebox.showwarning("Warning", "No author selected")
            return
        message_delete = messagebox.askyesno(
            title="Question", message="Delete author id: " + str(author_id)
        )
        if message_delete:
            bookdb.delete_author(int(author_id))
            self.fill_author_table()


def start_gui():
    app = Application()
    app.mainloop()
