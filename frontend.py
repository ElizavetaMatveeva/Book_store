from tkinter import *
from tkinter import messagebox
from backend_OOP import Database


class Window:
    def __init__(self):
        self.window = Tk()
        self.window.title("Book store")

        Label(self.window, text="Title").grid(row=0, column=0)

        Label(self.window, text="Author").grid(row=0, column=2)

        Label(self.window, text="Year").grid(row=1, column=0)

        Label(self.window, text="ISBN").grid(row=1, column=2)

        self.title_value = StringVar()
        self.title = Entry(self.window, textvariable=self.title_value)
        self.title.grid(row=0, column=1)

        self.author_value = StringVar()
        self.author = Entry(self.window, textvariable=self.author_value)
        self.author.grid(row=0, column=3)

        self.year_value = StringVar()
        self.year = Entry(self.window, textvariable=self.year_value)
        self.year.grid(row=1, column=1)

        self.isbn_value = StringVar()
        self.isbn = Entry(self.window, textvariable=self.isbn_value)
        self.isbn.grid(row=1, column=3)

        view = Button(self.window, text="View all", width=15, command=self.view_command)
        view.grid(row=2, column=3, pady=(15, 0))

        search = Button(self.window, text="Search Entry", width=15, command=self.search_command)
        search.grid(row=3, column=3)

        add = Button(self.window, text="Add Entry", width=15, command=self.add_command)
        add.grid(row=4, column=3)

        update = Button(self.window, text="Update Selected",
                             width=15, command=self.update_command)
        update.grid(row=5, column=3)

        delete = Button(self.window, text="Delete Selected",
                             width=15, command=self.delete_command)
        delete.grid(row=6, column=3)

        clear = Button(self.window, text="Clear entry fields",
                            width=15, command=self.clear_entry_windows)
        clear.grid(row=7, column=3)

        # Book list
        self.book_list = Listbox(self.window, height=10, width=30)
        self.book_list.grid(row=2, column=0, rowspan=6,
                            columnspan=2, padx=(5, 0), pady=(15, 12))
        # Retrieving information about selected element
        self.book_list.bind('<<ListboxSelect>>', self.get_selected_row)

        # Vertical scrollbar for the listbox (book list)
        sb_v = Scrollbar(self.window)
        sb_v.grid(row=2, column=2, rowspan=6, sticky=NS, pady=15)
        self.book_list.configure(yscrollcommand=sb_v.set)
        sb_v.configure(command=self.book_list.yview)

        # Horizontal scrollbar for the listbox (book list)
        sb_h = Scrollbar(self.window, orient="horizontal")
        sb_h.grid(row=8, column=0, columnspan=2, pady=(0, 5), sticky=EW)
        self.book_list.configure(xscrollcommand=sb_h.set)
        sb_h.configure(command=self.book_list.xview)

        self.selected_tuple = ()

        self.window.mainloop()

    def clear_entry_windows(self):
        self.title.delete(0, END)
        self.author.delete(0, END)
        self.year.delete(0, END)
        self.isbn.delete(0, END)

    def get_selected_row(self, event):
        try:
            index = self.book_list.curselection()[0]  # Getting line ID
            # Getting info from selected line
            self.selected_tuple = self.book_list.get(index)
            self.clear_entry_windows()
            # Inserting values from selected listbox item into entry windows
            self.title.insert(END, self.selected_tuple[1])
            self.author.insert(END, self.selected_tuple[2])
            self.year.insert(END, self.selected_tuple[3])
            self.isbn.insert(END, self.selected_tuple[4])
        except IndexError:  # Ignore index error generated when user clicks on an empty listbox
            pass

    def view_command(self):
        # Making sure the listbox is empty every time before we view it
        self.book_list.delete(0, END)
        self.clear_entry_windows()
        for row in database.view_all():
            self.book_list.insert(END, row)

    def search_command(self):
        # If user filled at least one field, start the search
        if any((self.title_value.get(), self.author_value.get(), self.year_value.get(), self.isbn_value.get())):
            self.book_list.delete(0, END)  # Clear the book list for search results
            rows = database.search(
                self.title_value.get(), self.author_value.get(), self.year_value.get(), self.isbn_value.get())
            if len(rows) == 0:  # If there's nothing found, print a message saying "no result found"
                self.book_list.insert(END, "No result found")
            else:  # Otherwise, insert search results into the listbox
                for row in rows:
                    self.book_list.insert(END, row)
        else:  # If user hit the "search" button while all fields are empty, throw an error
            messagebox.showerror(
                title="Error", message="Enter information to search for a book")

    def add_command(self):
        # Add a new book if all fields are filled in
        if all((self.title_value.get(), self.author_value.get(), self.year_value.get(), self.isbn_value.get())):
            database.add(self.title_value.get(), self.author_value.get(),
                         self.year_value.get(), self.isbn_value.get())
            self.book_list.insert(
                END, (self.title_value.get(), self.author_value.get(), self.year_value.get(), self.isbn_value.get()))
            self.view_command()  # View updated list of books
            self.clear_entry_windows()  # Clear entry windows with info already added to the list
        else:  # Otherwise throw an error
            messagebox.showerror(
                title="Error", message="You must fill in all fields to add a book")

    def update_command(self):
        if self.book_list.curselection():  # If user selected an element, update it, otherwise throw an error
            # Update only if all fields are filled in
            if all((self.title_value.get(), self.author_value.get(), self.year_value.get(), self.isbn_value.get())):
                database.update(self.selected_tuple[0], self.title_value.get(),
                                self.author_value.get(), self.year_value.get(), self.isbn_value.get())
                self.view_command()  # View updated list of books
            else:
                messagebox.showerror(
                    title="Error", message="All fields must be filled in")
        else:
            messagebox.showerror(
                title="Error", message="Select book you want to update")

    def delete_command(self):
        if self.book_list.curselection():  # If user selected an element, delete it, otherwise throw an error
            database.delete(self.selected_tuple[0])
            self.book_list.delete(self.selected_tuple[0])
            self.view_command()  # View updated list of books
        else:
            messagebox.showerror(
                title="Error", message="Select book you want to delete")


database = Database("book_store.db")
window = Window()
