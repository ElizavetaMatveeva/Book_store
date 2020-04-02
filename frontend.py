from tkinter import *
from tkinter import messagebox
import backend


def clear_entry_windows():
    title.delete(0, END)
    author.delete(0, END)
    year.delete(0, END)
    isbn.delete(0, END)


def get_selected_row(event):
    try:
        index = book_list.curselection()[0]  # Getting line ID
        global selected_tuple
        # Getting info from selected line
        selected_tuple = book_list.get(index)
        clear_entry_windows()
        # Inserting values from selected listbox item into entry windows
        title.insert(END, selected_tuple[1])
        author.insert(END, selected_tuple[2])
        year.insert(END, selected_tuple[3])
        isbn.insert(END, selected_tuple[4])
    except IndexError:  # Ignore index error generated when user clicks on an empty listbox
        pass


def view_command():
    # Making sure the listbox is empty every time before we view it
    book_list.delete(0, END)
    clear_entry_windows()
    for row in backend.view_all():
        book_list.insert(END, row)


def search_command():
    # If user filled at least one field, start the search
    if any((title_value.get(), author_value.get(), year_value.get(), isbn_value.get())):
        book_list.delete(0, END)  # Clear the book list for search results
        rows = backend.search(
            title_value.get(), author_value.get(), year_value.get(), isbn_value.get())
        if len(rows) == 0:  # If there's nothing found, print a message saying "no result found"
            book_list.insert(END, "No result found")
        else:  # Otherwise, insert search results into the listbox
            for row in rows:
                book_list.insert(END, row)
    else:  # If user hit the "search" button while all fields are empty, throw an error
        messagebox.showerror(
            title="Error", message="Enter information to search for a book")


def add_command():
    # Add a new book if all fields are filled in
    if all((title_value.get(), author_value.get(), year_value.get(), isbn_value.get())):
        backend.add(title_value.get(), author_value.get(),
                    year_value.get(), isbn_value.get())
        book_list.insert(
            END, (title_value.get(), author_value.get(), year_value.get(), isbn_value.get()))
        view_command()  # View updated list of books
        clear_entry_windows()  # Clear entry windows with info already added to the list
    else:  # Otherwise throw an error
        messagebox.showerror(
            title="Error", message="You must fill in all fields to add a book")


def update_command():
    if book_list.curselection():  # If user selected an element, update it, otherwise throw an error
        # Update only if all fields are filled in
        if all((title_value.get(), author_value.get(), year_value.get(), isbn_value.get())):
            backend.update(selected_tuple[0], title_value.get(),
                           author_value.get(), year_value.get(), isbn_value.get())
            view_command()  # View updated list of books
        else:
            messagebox.showerror(
                title="Error", message="All fields must be filled in")
    else:
        messagebox.showerror(
            title="Error", message="Select book you want to update")


def delete_command():
    if book_list.curselection():  # If user selected an element, delete it, otherwise throw an error
        backend.delete(selected_tuple[0])
        book_list.delete(selected_tuple[0])
        view_command()  # View updated list of books
    else:
        messagebox.showerror(
            title="Error", message="Select book you want to delete")


window = Tk()
window.title("Book store")
window.columnconfigure(3, weight=0, pad=10)

Label(window, text="Title").grid(row=0, column=0)

Label(window, text="Author").grid(row=0, column=2)

Label(window, text="Year").grid(row=1, column=0)

Label(window, text="ISBN").grid(row=1, column=2)

title_value = StringVar()
title = Entry(window, textvariable=title_value)
title.grid(row=0, column=1)

author_value = StringVar()
author = Entry(window, textvariable=author_value)
author.grid(row=0, column=3)

year_value = StringVar()
year = Entry(window, textvariable=year_value)
year.grid(row=1, column=1)

isbn_value = StringVar()
isbn = Entry(window, textvariable=isbn_value)
isbn.grid(row=1, column=3)

view = Button(window, text="View all", width=15, command=view_command)
view.grid(row=2, column=3, pady=(15, 0))

search = Button(window, text="Search Entry", width=15, command=search_command)
search.grid(row=3, column=3)

add = Button(window, text="Add Entry", width=15, command=add_command)
add.grid(row=4, column=3)

update = Button(window, text="Update Selected",
                width=15, command=update_command)
update.grid(row=5, column=3)

delete = Button(window, text="Delete Selected",
                width=15, command=delete_command)
delete.grid(row=6, column=3)

clear = Button(window, text="Clear entry fields",
               width=15, command=clear_entry_windows)
clear.grid(row=7, column=3)

# Book list
book_list = Listbox(window, height=10, width=30)
book_list.grid(row=2, column=0, rowspan=6,
               columnspan=2, padx=(5, 0), pady=(15, 12))
# Retrieving information about selected element
book_list.bind('<<ListboxSelect>>', get_selected_row)

# Vertical scrollbar for the listbox (book list)
sb_v = Scrollbar(window)
sb_v.grid(row=2, column=2, rowspan=6, sticky=NS, pady=15)
book_list.configure(yscrollcommand=sb_v.set)
sb_v.configure(command=book_list.yview)

# Horizontal scrollbar for the listbox (book list)
sb_h = Scrollbar(window, orient="horizontal")
sb_h.grid(row=8, column=0, columnspan=2, pady=(0, 5), sticky=EW)
book_list.configure(xscrollcommand=sb_h.set)
sb_h.configure(command=book_list.xview)

window.mainloop()
