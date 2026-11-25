
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

    def lend_book(self, borrower_id, book_id, day):
        book = self.find_book(book_id)
        if book is None:
            return "Book not found."
        borrower = self.find_borrower(borrower_id)
        if borrower is None:
            return "Borrower not found."
        if not borrower.can_borrow():
            return "This borrower already has 3 active loans."
        if not book.lendBook():
            return "No copies available."
        loan = Loan(book, borrower, day + Library.LOAN_PERIOD)
        self.__loans.append(loan)
        borrower.add_loan(loan)
        return f"Book lent. Due on day {loan.get_due_day()}."
    
    def load_data(self):
        try:
            books = open('books.txt', 'r')
            lines = books.readlines()
            books.close()

            for i in range(0, len(lines), 3):
                title = lines[i].strip()
                book_id = int(lines[i + 1].strip())
                copies = int(lines[i + 2].strip())
                self.add_book(title, book_id, copies)
        except ValueError as error:
            print(f'Could not load books: {error}')
        try:
            borrowers = open('borrowers.txt', 'r')
            lines = borrowers.readlines()
            borrowers.close()
            for i in range(0, len(lines), 2):
                name = lines[i].strip()
                borrower_id = int(lines[i + 1].strip())
                self.add_borrower(borrower_id, name)
        except (OSError, ValueError) as error:
            print(f'Could not load borrowers: {error}')
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