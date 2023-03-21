import sqlite3

# Connect to the database file 'ebookstore'
db = sqlite3.connect('data/ebookstore')
# Create a cursor object to execute SQL statements
cursor = db.cursor()


# Try to create a table 'books' in the database, if it already exists, catch the exception and pass
try: 
    cursor.execute('''
        CREATE TABLE books (id INTEGER PRIMARY KEY, Title TEXT,
                    Author TEXT,	Qty INTEGER)
    ''')
    db.commit()
except sqlite3.OperationalError:
     pass
     

# Try to insert multiple records into the 'books' table, if there is an integrity error, catch the exception and pass

try:
    cursor.executemany('''INSERT INTO books (id, Title, Author, Qty )
        VALUES(?,?,?,?)''', [(3001,  'A Tale of Two Cities', 'Charles Dickens', 30),
                            (3002, "Harry Potter and the Philosopher's Stone", 'J.K. Rowling', 40),
                            (3003, 'The Lion, the Witch and the Wardrobe', 'C. S. Lewis', 25),
                            (3004, 'The Lord of the Rings', 'J.R.R Tolkien', 37),
                            (3005, 'Alice in Wonderland', 'Lewis Carroll', 12),
                            (3006, 'Don Quixote', 'Miguel de Cervantes', 25),
                            (3007, 'The Little Prince', 'Antoine de Saint-Exupery', 13),
                            (3008, 'And Then There Were None', 'Agatha Christie', 22),
                            (3009, 'The Dream of the Red Chamber', 'Cao Xueqin', 9),
                            (3010, 'The Hobbit', 'J.R.R. Tolkien', 43),
                            (3011, 'She: A History of Adventure ', 'H. Rider Haggard', 11),
                            (3012, 'The Da Vinci Code', 'Dan Brown', 54),
                            (3013, 'Think and Grow Rich', 'Napoleon Hill', 18),
                            (3014, 'The Alchemist', 'Paulo Coelho', 6),
                            (3015, 'One Hundred Years of Solitude', 'Gabriel García Marquez', 7)])
    db.commit()
except sqlite3.IntegrityError:
     pass

# Function to add a new book to the 'books' table
def ent_book(title, author, qty):

    # Get the maximum ID value in the 'books' table
    cursor.execute("SELECT MAX(id) FROM books")
    max_id = cursor.fetchone()[0]

    # If the 'books' table is empty, set max_id to 0
    if max_id is None:
        max_id = 0

    # Set the new book's ID to be one more than the maximum ID
    new_id = max_id + 1

    # Insert the new book's information into the 'books' table
    cursor.execute("INSERT INTO books (id, Title, Author, Qty) VALUES (?, ?, ?, ?)", (new_id, title, author, qty))
    db.commit()
    print("Book added successfully with ID", new_id)

# Function to update book in the'books' table
def upd_book():

    # get id and title from books
    cursor.execute("SELECT id, Title FROM books")
    books = cursor.fetchall()

    # print all books id and title in database 
    print("Books in the database:")
    for book in books:
        print(f"ID: {book[0]}, Title: {book[1]}")

    # ask user for to enter id of book to update    
    book_id = int(input("Enter the ID of the book you would like to update: "))

    # select title author and qty from books using book id  
    cursor.execute("SELECT Title, Author, Qty FROM books WHERE id=?", (book_id,))
    book = cursor.fetchone()

    #  error handing for if book doesnt exist
    if book is None:
        print("Book not found.")
        return
    
    # menu for user to update book 
    print("What would you like to update?")
    print("1. Title")
    print("2. Author")
    print("3. Quantity")

    update_choice = int(input("Enter your choice (1, 2, or 3): "))

    # ask user for new title and insert updated info to books
    if update_choice == 1:
        new_title = input("Enter new title: ")
        cursor.execute("UPDATE books SET Title=? WHERE id=?", (new_title, book_id))

    #  ask user for new author and insert updated info to books
    elif update_choice == 2:
        new_author = input("Enter new author: ")
        cursor.execute("UPDATE books SET Author=? WHERE id=?", (new_author, book_id))

    # ask user for new quantity and insert updated info to books
    elif update_choice == 3:

        new_qty = int(input("Enter new quantity: "))

        cursor.execute("UPDATE books SET Qty=? WHERE id=?", (new_qty, book_id))
        db.commit()

    #error handing for wrong input in menu 
    else:
         print("Not Valid Option, Please enter 1,2 or 3")
       


# Function to delete a book from the 'books' table
def del_book():

# Get all the books in the 'books' table and store them in a list of tuples
    cursor.execute("SELECT id, Title FROM books")
    books = cursor.fetchall()

    # Print the list of books
    print("List of books:")
    for book in books:
        print(f"{book[0]}. {book[1]}")

    # Ask the user to enter the ID of the book they want to delete    
    book_id = int(input("Enter the ID of the book you want to delete: "))

    # Delete the book with the specified ID from the 'books' table
    cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
    db.commit()

    # Print a message indicating that the book was deleted successfully
    print(f"Book with ID {book_id} deleted successfully.")



# Function to search for a book within 'books'
def ser_book():

    # Prompt the user to select the search criteria
    search = input('''Choose one of the following options to search by.
                    1. Search by book title
                    2. Search by book author
                    ''')

    # Search by book title            
    if search == '1': 
                    # Get the title of the book to search for
                    title = input('Enter the title of the book: ')
                     # Execute a SELECT statement to search for the book by title
                    cursor.execute('''SELECT * FROM books WHERE title = ?''', (title,))
                    # Fetch the result of the SELECT statement
                    row = cursor.fetchone()

                    # If the book was not found, print a message
                    if row is None:
                        print('Book not in library')
                        exit()
                    # Print the result of the SELECT statement
                    else:
                        print(row)
                     # Commit the changes to the database
                    db.commit()   

    # Search by book author
    elif search == '2': 
                # Get the author of the book to search for
                author = input('Enter the author of the book: ')
                # Execute a SELECT statement to search for the book by author
                cursor.execute('''SELECT * FROM books WHERE author = ?''', (author,))
                # Fetch the result of the SELECT statement
                row = cursor.fetchone()

                # If the book was not found, print a message
                if row is None:
                        print('Book not in library')
                 # Print the result of the SELECT statement        
                else:
                    print(row)
                # Commit the changes to the database
                db.commit()   
                
    else:
        # If the user's selection is invalid, print an error message
        print('Your selection is invalid, please try again.')


# This code creates a menu for a user to interact with a database of books.
while True:
     # Ask the user to select an option from the menu
    menu = input(f'''Select one of the following Options below:
        1. Enter book
        2. Update book
        3. Delete book
        4. Search books
        0. Exit
        -----------------:''')
    # If the user selects option 1, call the function "ent_book" to enter a new book

    if menu == "1":
        # Ask the user for the book title
       title = input("Enter book title: ")
        # Ask the user for the author name
       author = input("Enter author name: ")


    # Ask the user for the quantity, and handle potential ValueErrors
       try:
            qty = int(input("Enter quantity: "))
       except ValueError:
            print("Incorrect input! Please enter a NUMBER")
            continue
       ent_book(title, author, qty)

    # If the user selects option 2, call the function "upd_book" to update a book  
    elif menu == "2":
        upd_book()

    # If the user selects option 3, call the function "del_book" to delete a book    
    elif menu == "3":
        del_book()

    # If the user selects option 4, call the function "ser_book" to search for books    
    elif menu == "4":
        ser_book()

    # If the user selects option 0, close the database and exit the program   
    elif menu == '0':
            print('Goodbye!!!')
            db.close()
            exit()

