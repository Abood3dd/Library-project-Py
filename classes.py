
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
    MAX_LOANS = 3

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