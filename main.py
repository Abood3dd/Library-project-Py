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
                title = input('Title of the Book: ')
                id= int(input('id of the book: '))
                number= int(input('number of copies of the book: '))
                addBook(title,id,number)
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
Books = []
def addBook(title,id,number):
    book1 = classes.Book(title,id,number)
    Books.append(book1)
    print(Books)






def main():
    
    UI()
main()
