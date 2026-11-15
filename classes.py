
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
        self.__active_loans.remove(loan)

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
