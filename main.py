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

        # try/except added: keeps the menu alive if any option fails,
        # and exits cleanly on Ctrl+C or end of input
        try:
            choice = input("Enter your choice: ").strip()
            match choice:
                case "1":
                    add_book()
                case "2":
                    print(2)
                    #search_books()
                case "3":
                    add_borrower()
                case "4":
                    print(4)
                    #lend_book()
                case "5":
                    print(5)
                    #return_book()
                case "6":
                    print(6)
                    #view_overdue()
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
    title = input("Title of the book: ")

    while True:
        text = input("ID of the book: ")
        if text.isdigit():
            try:
                id = int(text)
                break
            except ValueError:
                print("Invalid number, please try again.")

    while True:
        text = input("Number of copies: ")
        if text.isdigit():
            try:
                copies = int(text)
                break
            except ValueError:
                print("Invalid number, please try again.")

    print(library.add_book(title, id, copies))

def add_borrower():
    name = input("Name of the borrower: ")

    while True:
        text = input("ID of the borrower: ")
        if text.isdigit():
            try:
                id = int(text)
                break
            except ValueError:
                print("Invalid number, please try again.")

    print(library.add_borrower(id, name))



def main():
    UI()


if __name__ == "__main__":
    main()
