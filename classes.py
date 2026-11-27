
class Book:
    def __init__(self, title, id, copies):
        self.set_title(title)
        self.set_id(id)
        self.set_copies(copies)

    # Setters
    def set_title(self, title):
        self.__title = title

    def set_id(self, id):
        self.__id = id

    def set_copies(self, copies):
        self.__copies = copies

    # Getters
    def get_title(self):
        return self.__title

    def get_id(self):
        return self.__id

    def get_copies(self):
        return self.__copies

    def __str__(self):
        return f"{self.get_title()} (ID: {self.get_id()}, Copies: {self.get_copies()})"

    # Lending and returning
    def returnBook(self):
        self.__copies += 1

    def lendBook(self):
        if self.get_copies() > 0:
            self.__copies -= 1
            return True
        return False



class Borrower:
    MAX_LOANS = 3 # can be changed
    def __init__(self, id, name):
        self.set_id(id)
        self.set_name(name)
        self.__active_loans = []
    # Setters
    def set_id(self, id):
        self.__id = id

    def set_name(self, name):
        self.__name = name

    # Getters
    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_active_loans(self):
        return (self.__active_loans)

    def active_loan_number(self):
        return len(self.__active_loans)


    # Methods 
    
    def can_borrow(self):
        return self.active_loan_number() < Borrower.MAX_LOANS

    def add_loan(self, loan):
        self.__active_loans.append(loan)

    def remove_loan(self, loan):
        try:
            self.__active_loans.remove(loan)
        except ValueError:
            print("This loan was not found in the borrower's active loans.")

    def __str__(self):
        return f"{self.get_name()} (ID: {self.get_id()}, Active loans: {self.active_loan_number()})"

# Added a separate class for loans because it makes more sense
# it includes the things that the book class doesn't have
# like due day and the borrower
class Loan:
    def __init__(self, book, borrower, due_day):
        self.__book = book
        self.__borrower = borrower
        self.__due_day = due_day
        self.__return_day = 'not returned' #"not returned" if not returned yet otherwise the day it was returned
    #getters
    def get_book(self):
        return self.__book

    def get_borrower(self):
        return self.__borrower

    def get_due_day(self):
        return self.__due_day
    
    #methods

    def late_days(self, day):
        # zero if on time otherwise day minus due day
        if day > self.__due_day:
            return day - self.__due_day
        return 0

    def return_book(self, return_day):
        self.__return_day = return_day
        return self.late_days(return_day)
    
    def is_active(self): #checks if loan is still active so false if it's a number 
        return self.__return_day == 'not returned'

class Library:
    MAX_LOANS = 3      # active loans allowed
    LOAN_PERIOD = 14   # loan period is 2 weeks (can be changed)

    def __init__(self):
        self.__books = [] # stores the books in the library
        self.__borrowers = [] # the borrowers of the library
        self.__loans = []   # every Loan made ( so we can go back to them to check for overdue loans)


    #Adding 
    def add_book(self, title, id, copies):
        self.__books.append(Book(title, id, copies))
        
        return "Book added."

    def add_borrower(self, id, name):
        self.__borrowers.append(Borrower(id, name))
        return "Borrower added."
    
    def find_book(self, book_id):#created this method to use in lending a book
        for book in self.__books:
            if book.get_id() == book_id:
                return book
        return None

    def find_borrower(self, borrower_id): #created this method to use in lending a book
        for borrower in self.__borrowers:
            if borrower.get_id() == borrower_id:
                return borrower
        return None

    def lend_book(self, borrower_id, book_id, day,loadState):
        book = self.find_book(book_id)
        if book is None:
            return "Book not found."
        borrower = self.find_borrower(borrower_id)
        if borrower is None:
            return "Borrower not found."
        if not borrower.can_borrow():
            return "This borrower already has 3 active loans."
        if loadState and not book.lendBook(): # when loading from file, books.txt already holds the available copies
            return "No copies available."
        loan = Loan(book, borrower, day + Library.LOAN_PERIOD)

        if loadState: 
            self.modify_book(book, book)
            file = open('loans.txt','a')
            file.write(f"{borrower_id}\n")
            file.write(f"{book_id}\n")
            file.write(f"{day}\n")
            file.close()
        self.__loans.append(loan)
        borrower.add_loan(loan)
        return f"{book.get_title()} lent to {borrower.get_name()}. Due on day {loan.get_due_day()}."
    
    def return_book(self, borrower_id, book_id, return_day):
        borrower = self.find_borrower(borrower_id)
        if borrower is None:
            return "Borrower not found."
        book = self.find_book(book_id)
        if book is None:
            return "Book not found."
        for loan in borrower.get_active_loans():
            if loan.get_book() == book:
                if return_day < loan.get_due_day() - Library.LOAN_PERIOD:
                    return "Return day cannot be before the lend day."
                late = loan.return_book(return_day)
                book.returnBook()
                borrower.remove_loan(loan)
                self.modify_book(book, book)
                self.remove_loan(borrower_id, book_id, loan.get_due_day() - Library.LOAN_PERIOD)

                return f"Book returned. Late days: {late}."
        return "This borrower has no active loan for this book."

    def remove_loan(self, borrower_id, book_id, day): # removes a returned loan from the file
        try:
            with open('loans.txt', 'r') as file:
                lines = file.readlines()
        except OSError:
            return
        for i in range(0, len(lines) - 2, 3):
            if (lines[i].strip() == str(borrower_id) and lines[i + 1].strip() == str(book_id)
                    and lines[i + 2].strip() == str(day)):
                del lines[i:i + 3]
                with open('loans.txt', 'w') as file:
                    file.writelines(lines)
                return

    def overdue_report(self, current_day):
        report = {}
        for loan in self.__loans:
            if loan.is_active() and loan.late_days(current_day) > 0:
                borrower = loan.get_borrower()
                if borrower not in report:
                    report[borrower] = {"loans": [], "late_days": 0}
                report[borrower]["loans"].append(loan)
                report[borrower]["late_days"] += loan.late_days(current_day)
        return report
    
    def load_data(self):
        #load books (stock)
        try:
            books = open('books.txt', 'r')
            lines = books.readlines()
            books.close()

            for i in range(0, len(lines), 3):
                title = lines[i].strip()
                book_id = int(lines[i + 1].strip())
                copies = int(lines[i + 2].strip())
                self.add_book(title, book_id, copies)
        except (OSError, ValueError, IndexError) as error:
            print(f'Could not load books: {error}')
        #load borrowers (ppl of the library)
        try:
            borrowers = open('borrowers.txt', 'r')
            lines = borrowers.readlines()
            borrowers.close()
            for i in range(0, len(lines), 2):
                name = lines[i].strip()
                borrower_id = int(lines[i + 1].strip())
                self.add_borrower(borrower_id, name)
        except (OSError, ValueError, IndexError) as error:
            print(f'Could not load borrowers: {error}')
        except ValueError as e:
            print(f'an error has occured with the data: {e}')
        #load loans 
        try:
            loans = open('loans.txt', 'r')
            lines = loans.readlines()
            loans.close()
            for i in range(0, len(lines), 3):
                borrower_id = int(lines[i].strip())
                book_id = int(lines[i + 1].strip())
                day = int(lines[i+2].strip())
                (self.lend_book(borrower_id, book_id, day,False))
        except OSError as error:
            print(f'Could not load loans: {error}')
        except (ValueError, IndexError) as e:
            print(f'an error has occured with the data: {e}')

    def modify_book(self, old_book, new_book):# to modify the books in the file once smth changes
        with open('books.txt', 'r') as file: #took it in lab 12
            lines = file.readlines()

        for i in range(0, len(lines) - 2, 3):
            if lines[i + 1].strip() == str(old_book.get_id()):
                lines[i:i + 3] = [
                    new_book.get_title() + '\n',
                    str(new_book.get_id()) + '\n',
                    str(new_book.get_copies()) + '\n',
                ]
                with open('books.txt', 'w') as file:
                    file.writelines(lines)
                return True

        return False



    def get_books(self):
        return self.__books
    def get_borrowers(self):return self.__borrowers









"""So here's how it's going to work
we have classes for Book, Borrower, Loan and Library
the Library class is the main class that will be used to manage the library and it has the methods that will be used
we have the book class that will be used to create book objects and the borrower class that will be used to create borrower objects
the loan class will be used to create loan objects that will be used to keep track of the loans and the due dates and the return dates
the library class will have a list of books, borrowers and loans and will have methods to add books, borrowers and loans and to search for books and borrowers
and to lend and return books and to view overdue loans"""