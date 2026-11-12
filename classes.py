import json

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

    # Saving and loading
    def to_dict(self):
        return {"title": self.get_title(), "id": self.get_id(), "copies": self.get_copies()}

    @classmethod
    def from_dict(cls, data):
        return cls(data["title"], data["id"], data["copies"])


def save_books(books, filename="books.json"):
    with open(filename, "w") as f:
        json.dump([b.to_dict() for b in books], f, indent=4)


def load_books(filename="books.json"):
    try:
        with open(filename, "r") as f:
            return [Book.from_dict(d) for d in json.load(f)]
    except FileNotFoundError:
        return []