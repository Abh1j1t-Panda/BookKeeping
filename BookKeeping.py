import sqlite3

# Connect to the database (creates one if it doesn't exist)
conn = sqlite3.connect("library.db")
cursor = conn.cursor()

# Create the books table
cursor.execute('''
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    year INTEGER,
    genre TEXT
)
''')

# Insert demo books (only if table is empty)
cursor.execute("SELECT COUNT(*) FROM books")
if cursor.fetchone()[0] == 0:
    demo_books = [
        ("To Kill a Mockingbird", "Harper Lee", 1960, "Fiction"),
        ("1984", "George Orwell", 1949, "Dystopian"),
        ("The Great Gatsby", "F. Scott Fitzgerald", 1925, "Classic"),
        ("Pride and Prejudice", "Jane Austen", 1813, "Romance"),
        ("The Hobbit", "J.R.R. Tolkien", 1937, "Fantasy")
    ]
    cursor.executemany("INSERT INTO books (title, author, year, genre) VALUES (?, ?, ?, ?)", demo_books)
    conn.commit()

# Show menu
def show_menu():
    print("\n=== Book Library App ===")
    print("1. View all books")
    print("2. Add a new book")
    print("3. Search for a book")
    print("4. Delete a book")
    print("5. Exit")

# View all books
def view_books():
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    print("\n--- Library Books ---")
    for book in books:
        print(f"{book[0]}. '{book[1]}' by {book[2]} ({book[3]}) - {book[4]}")

# Add a new book
def add_book():
    title = input("Enter title: ")
    author = input("Enter author: ")
    year = input("Enter year: ")
    genre = input("Enter genre: ")
    cursor.execute("INSERT INTO books (title, author, year, genre) VALUES (?, ?, ?, ?)",
                   (title, author, year, genre))
    conn.commit()
    print("Book added successfully.")

# Search for a book
def search_books():
    keyword = input("Enter title or author to search: ")
    cursor.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ?", 
                   (f'%{keyword}%', f'%{keyword}%'))
    results = cursor.fetchall()
    if results:
        print("\n--- Search Results ---")
        for book in results:
            print(f"{book[0]}. '{book[1]}' by {book[2]} ({book[3]}) - {book[4]}")
    else:
        print("No matching books found.")

# Delete a book
def delete_book():
    book_id = input("Enter the ID of the book to delete: ")
    cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
    conn.commit()
    print("Book deleted successfully.")

# Run the app
while True:
    show_menu()
    choice = input("Enter your choice (1-5): ")
    if choice == '1':
        view_books()
    elif choice == '2':
        add_book()
    elif choice == '3':
        search_books()
    elif choice == '4':
        delete_book()
    elif choice == '5':
        print("Goodbye!")
        break
    else:
        print("Invalid choice. Please try again.")

# Close the connection
conn.close()