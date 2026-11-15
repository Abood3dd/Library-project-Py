import classes
def UI():
    while True:
        print("===== LIBRARY MANAGEMENT SYSTEM =====")
        print('1. Add Book')
        print('2. Search Books')
        print('3. Return Book')
        print('4. View Overdue Loans')
        print('5. Add Borrower')
        print('6. Exit')
        print('-'*10)
    
        choice = (input('Enter your choice: '))
        print(choice)
        match choice:
            case '1':
                add_book()
            case '2':
                print(2)
            case '3':
                print(3)
            case '4':
                print(4)
            case '5':
                print(5)
            case '6':
                print('Exiting the program')
                print('Good Bye')
                break
            case _:
                print('invalid input \n \n')
def add_book():
    title = input("Title of the book: ")

    while True:
        text = input("ID of the book: ")
        if text.isdigit():
            id = int(text)
            break

    while True:
        text = input("Number of copies: ")
        if text.isdigit():
            copies = int(text)
            break

    print(library.add_book(title, id, copies))




def main():
    
    UI()
main()
