import os
import classes
library = classes.Library()
def UI():
    while True:
        print("\n===== LIBRARY MANAGEMENT SYSTEM =====")
        print("1. Add Book")
        print("2. Search Books")
        print("3. Add Borrower")
        print("4. Lend Book")
        print("5. Return Book")
        print("6. View Overdue Loans")
        print("7. Exit")
        print("-" * 10)

        try:
            choice = input("Enter your choice: ").strip()
            match choice:
                case "1":
                    add_book()
                case "2":
                    search_books()
                case "3":
                    add_borrower()
                case "4":
                    lend_book()
                case "5":
                    return_book()
                case "6":
                    view_overdue()
                case "7":
                    print("Exiting the program")
                    print("Good Bye")
                    break
                case _:
                    print("Invalid input\n")
        except Exception as e:
            print(f"Something went wrong: {e}")
            print("Returning to the menu.")


def add_book():
    books = library.get_books()
    ids = [book.get_id() for book in books]

    title = input("Title of the book: ").strip() # to make sure that the title doesn't have a space after the user typed it
    existing = None
    for book in books:
        if book.get_title().lower() == title.lower():
            existing = book
            break

    if existing:
        id = existing.get_id()
        print("That book is already in stock -> updating the number of copies ")
    else:
        while True:
            text = input("ID of the book: ")
            if text.isdigit():
                id = int(text)
                if id not in ids:
                    break
                print("That book ID is already in use, please enter a unique ID.")
            else:
                print("Invalid number, please try again.")

    while True:
        text = input("Number of copies: ")
        if text.isdigit() and int(text) > 0:
            copies = int(text)

            break
        print("Invalid number, please try again.")
    if existing:  # Update the existing book record in the file
        updated_copies = existing.get_copies() + copies
        try:
            original = open('books.txt', 'r')
            lines = original.readlines()
            original.close()

            for i in range(0, len(lines) - 2, 3):#the step is 3 because each 3 lines represent one book 
                # used len(lines)-2 because we're sure that the last 2 lines will never be titles
                if lines[i + 1].strip() == str(id):
                    lines[i + 2] = str(updated_copies) + '\n'
                    break

            temp = open('booksTemp.txt', 'w')
            temp.writelines(lines)
            temp.close()
            os.remove('books.txt')
            os.rename('booksTemp.txt', 'books.txt')
        except Exception as e:
            print(f"An error occurred: {e}")
            try:
                os.remove('booksTemp.txt')
            except:
                print('error occured')
            return

        existing.set_copies(updated_copies)
        print(f"Updated copies of '{title}' to {existing.get_copies()}.")
    else:
        try:
            file = open('books.txt', 'a')
            file.write(title + '\n')
            file.write(str(id) + '\n')
            file.write(str(copies) + '\n')
            file.close()
        except IOError as e:
            print(f"Could not update books.txt: {e}")
            return # to stop the the function from running
        print(library.add_book(title, id, copies))

def add_borrower():
    name = input("Name of the borrower: ")
    ids = [borrower.get_id() for borrower in library.get_borrowers()]

    try:
        file = open('borrowers.txt', 'r')
        lines = file.readlines()
        file.close()
        # Borrower records are stored as name and ID on alternating lines
        for i in range(1, len(lines), 2):
            text = lines[i].strip()
            if text.isdigit():
                ids.append(int(text))
    except FileNotFoundError:
        print('error occured')
        pass

    while True:
        text = input("ID of the borrower: ")
        if not text.isdigit():
            print("Invalid number, please try again.")
        else:
            id = int(text)
            if id in ids:
                print("That borrower ID is already in use, please enter a unique ID.")
            else:
                break

    try:
        file = open('borrowers.txt', 'a')
        file.write(name + '\n')
        file.write(str(id) + '\n')
        file.close()
    except IOError as e:
        print(f"Could not update borrowers.txt: {e}")
        return

    print(library.add_borrower(id, name))

def search_books():
    #we need to ask for the title or id
    #then try to look them up in the books list in the library
    query = input('Title or Id: ')
    Flag = False 
    if query.isdigit():
        #then he entered an id and search accordingly
        for i in library.get_books():
                    if int(i.get_id())==int(query):
                        print(i)
                        Flag = True 

    if not Flag:  # not a number, or no book has that ID -> search by title if the title is a number
       for i in library.get_books():
                   if query.lower().strip() in i.get_title().lower(): # Improved search: ignores uppercase/lowercase and finds books by a single word
                       print(i)
                       Flag = True
    if not Flag : print('No Book was Found')       
        # he entered a title and search accordingly

def ask_number(message):
    while True:
        text = input(message)
        if text.isdigit():
            return int(text)
        print("Invalid number, please try again.")

def lend_book():
    borrower_id = ask_number("ID of the borrower: ")
    book_id = ask_number("ID of the book: ")
    day = ask_number("Day number: ")
    print(library.lend_book(borrower_id, book_id, day,True))

def return_book():
    borrower_id = ask_number("ID of the borrower: ")
    book_id = ask_number("ID of the book: ")
    day = ask_number("Return day number: ")
    print(library.return_book(borrower_id, book_id, day))

def view_overdue():
    day = ask_number("Current day number: ")
    report = library.overdue_report(day)
    if not report:
        print("No overdue loans.")
    for borrower in report:
        loans = report[borrower]["loans"]
        late = report[borrower]["late_days"]
        print(f"{borrower.get_name()} (ID: {borrower.get_id()}): {len(loans)} overdue book(s), {late} late day(s)")
        for loan in loans:
            print(f"   - {loan.get_book().get_title()}: due day {loan.get_due_day()}, {loan.late_days(day)} day(s) late")

def main():
    library.load_data()
    UI()


if __name__ == "__main__":
    main()
