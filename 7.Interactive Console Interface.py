import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt

# Load the data
csv_file = "library_data.csv"
df = pd.read_csv(csv_file)

# Function to view all books
def view_books():
    """Display all books in the library."""
    print("\n--- All Books in the Library ---")
    print(df)

# Function to validate book ID format
def validate_book_id(book_id):
    """Validate book ID format (e.g., BK-001)."""
    return bool(re.match(r"^BK-\d{3}$", book_id))

# Function to add a book
def add_book():
    """Add a new book to the library."""
    book_id = input("Enter Book ID (format BK-001): ").strip()
    if not validate_book_id(book_id):
        print("Invalid Book ID format. Please use format BK-001.")
        return

    if book_id in df["Book ID"].values:
        print("Book ID already exists. Please enter a unique ID.")
        return

    title = input("Enter Book Title: ")
    author = input("Enter Author Name: ")
    genre = input("Enter Genre: ")
    availability = input("Is the book available? (Yes/No): ")
    borrower = input("Enter Borrower (or leave empty): ")
    borrower = borrower if borrower else None

    new_book = {
        "Book ID": book_id,
        "Title": title,
        "Author": author,
        "Genre": genre,
        "Availability": availability,
        "Borrower": borrower
    }
    df = pd.concat([df, pd.DataFrame([new_book])], ignore_index=True)
    print(f"Book '{title}' has been added to the library.")
    save_to_csv()

# Function to remove a book
def remove_book():
    """Remove a book by its ID."""
    book_id = input("Enter Book ID to remove: ").strip()
    if book_id not in df["Book ID"].values:
        print(f"No book found with ID {book_id}. Please try again.")
        return

    df.drop(df[df["Book ID"] == book_id].index, inplace=True)
    print(f"Book with ID {book_id} has been removed.")
    save_to_csv()

# Function to update book details
def update_book():
    """Update a book's details."""
    book_id = input("Enter Book ID to update: ").strip()
    if book_id not in df["Book ID"].values:
        print(f"No book found with ID {book_id}. Please try again.")
        return

    # Get new details for the book
    availability = input("Enter new Availability (Yes/No): ")
    borrower = input("Enter new Borrower (or leave empty): ")
    borrower = borrower if borrower else None

    df.loc[df["Book ID"] == book_id, "Availability"] = availability
    df.loc[df["Book ID"] == book_id, "Borrower"] = borrower
    print(f"Book with ID {book_id} has been updated.")
    save_to_csv()

# Function to borrow a book
def borrow_book():
    """Allow a user to borrow a book."""
    book_id = input("Enter Book ID to borrow: ").strip()
    if book_id not in df["Book ID"].values:
        print(f"No book found with ID {book_id}. Please try again.")
        return

    if df.loc[df["Book ID"] == book_id, "Availability"].values[0] == "No":
        print(f"Book with ID {book_id} is already borrowed.")
        return

    borrower = input("Enter your name: ").strip()
    df.loc[df["Book ID"] == book_id, "Availability"] = "No"
    df.loc[df["Book ID"] == book_id, "Borrower"] = borrower
    print(f"Book with ID {book_id} has been borrowed by {borrower}.")
    save_to_csv()

# Function to return a book
def return_book():
    """Allow a user to return a borrowed book."""
    book_id = input("Enter Book ID to return: ").strip()
    if book_id not in df["Book ID"].values:
        print(f"No book found with ID {book_id}. Please try again.")
        return

    if df.loc[df["Book ID"] == book_id, "Availability"].values[0] == "Yes":
        print(f"Book with ID {book_id} is not borrowed.")
        return

    df.loc[df["Book ID"] == book_id, "Availability"] = "Yes"
    df.loc[df["Book ID"] == book_id, "Borrower"] = None
    print(f"Book with ID {book_id} has been returned.")
    save_to_csv()

# Function to search for a book
def search_books():
    """Search for books by title, author, or genre."""
    print("\nSearch by:")
    print("1. Title")
    print("2. Author")
    print("3. Genre")
    choice = int(input("Enter your choice: "))
    
    query = input("Enter your search term: ").strip().lower()
    
    if choice == 1:
        results = df[df["Title"].str.lower().str.contains(query, na=False)]
    elif choice == 2:
        results = df[df["Author"].str.lower().str.contains(query, na=False)]
    elif choice == 3:
        results = df[df["Genre"].str.lower().str.contains(query, na=False)]
    else:
        print("Invalid choice. Returning to menu.")
        return
    
    if not results.empty:
        print("\nSearch Results:")
        print(results)
    else:
        print("No books found matching your search.")

# Function to save DataFrame to CSV
def save_to_csv():
    """Save the DataFrame back to the CSV file."""
    df.to_csv(csv_file, index=False)

# Function to display statistics (book counts, most borrowed genre, etc.)
def show_statistics():
    """Show library statistics."""
    print("\n--- Library Statistics ---")
    total_books = len(df)
    print(f"Total number of books: {total_books}")
    
    # Most borrowed genre
    borrowed_books = df[df["Availability"] == "No"]
    if not borrowed_books.empty:
        most_borrowed_genre = borrowed_books["Genre"].value_counts().idxmax()
        print(f"Most borrowed genre: {most_borrowed_genre}")
    else:
        print("No books are currently borrowed.")

    # Visualization of genre distribution
    genre_counts = df["Genre"].value_counts()
    genre_counts.plot(kind="bar", color="skyblue", title="Books by Genre")
    plt.xlabel("Genre")
    plt.ylabel("Number of Books")
    plt.show()

    # Availability status pie chart
    availability_counts = df["Availability"].value_counts()
    availability_counts.plot(kind="pie", autopct="%1.1f%%", startangle=90, colors=["green", "red"])
    plt.title("Availability Status (Available vs Borrowed)")
    plt.ylabel("")  # Hide y-axis label
    plt.show()

# Main menu to interact with the system
while True:
    print("\n--- Library Management System ---")
    print("1. View All Books")
    print("2. Add, Remove, or Update a Book")
    print("3. Borrow or Return a Book")
    print("4. Search for a Book")
    print("5. View Statistics and Visualizations")
    print("6. Exit")

    choice = int(input("Enter your choice: "))
    if choice == 1:
        view_books()
    elif choice == 2:
        print("\nAdd, Remove, or Update Book:")
        print("1. Add Book")
        print("2. Remove Book")
        print("3. Update Book")
        sub_choice = int(input("Enter your choice: "))
        if sub_choice == 1:
            add_book()
        elif sub_choice == 2:
            remove_book()
        elif sub_choice == 3:
            update_book()
        else:
            print("Invalid choice.")
    elif choice == 3:
        print("\nBorrow or Return Book:")
        print("1. Borrow Book")
        print("2. Return Book")
        sub_choice = int(input("Enter your choice: "))
        if sub_choice == 1:
            borrow_book()
        elif sub_choice == 2:
            return_book()
        else:
            print("Invalid choice.")
    elif choice == 4:
        search_books()
    elif choice == 5:
        show_statistics()
    elif choice == 6:
        print("Exiting Library Management System.")
        break
    else:
        print("Invalid choice. Please try again.")
