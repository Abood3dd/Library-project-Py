## Features

- Add books with several copies each. Adding a title that already exists increases its copies instead of creating a duplicate.
- Search books by title (partial, case-insensitive) or by ID.
- Add borrowers with unique IDs.
- Lend a book only if a copy is available and the borrower has fewer than 3 active loans.
- Return a book using a return-day number. Late days are 0 if on time, otherwise return day minus due day.
- View overdue loans for a given current day, grouped by borrower, with each borrower's overdue-book count and total late days.

## files

• main.py: Menu and user input (main file)
• classes.py: Book, Borrower, Loan, and Library classes

• books.txt: Books and their available copies
• borrowers.txt: Borrowers and their IDs
• loans.txt: Active loans
## Menu choices

```
===== LIBRARY MANAGEMENT SYSTEM =====
1. Add Book
2. Search Books
3. Add Borrower
4. Lend Book
5. Return Book
6. View Overdue Loans
7. Exit
```

**1. Add Book**
Asks for a title. If a book with the same title (case-insensitive) already exists, it asks only for the number of copies and adds them to the existing stock. Otherwise it asks for a unique numeric ID and the number of copies, then saves the new book to `books.txt`.

**2. Search Books**
Enter an ID or part of a title. A numeric input is tried as an ID first; if no book has that ID, it searches titles. Title search ignores uppercase/lowercase and matches partial words (e.g. `habit` finds Atomic Habits).

**3. Add Borrower**
Asks for a name and a unique numeric ID, then saves the borrower to `borrowers.txt`.

**4. Lend Book**
Asks for the borrower ID, book ID, and the current day number. The loan is due 14 days later. It is refused if the book or borrower does not exist, the borrower already has 3 active loans, or no copies are left. On success the available copies drop by one and the loan is written to `loans.txt`.

**5. Return Book**
Asks for the borrower ID, book ID, and the return day. Returning before the lend day is refused. Otherwise the copy is added back to stock, the loan is removed from `loans.txt`, and the number of late days is shown (0 if on time).

**6. View Overdue Loans**
Asks for the current day number and lists every borrower with overdue books, the number of overdue books, and total late days, followed by each overdue book with its due day.

**7. Exit**
Closes the program.

Invalid menu input prints `Invalid input`. Non-numeric IDs and days are rejected and asked again.


----------------------------------------
### Sample data

`books.txt`

| ID | Title | Copies |
|---|---|---|
| 1 | Atomic Habits | 4 |
| 2 | Think Again | 1 |
| 3 | Deep Work | 0 |
| 4 | Clean Code | 2 |
| 8 | Harry Potter and the Philosopher's Stone | 4 |

`borrowers.txt`: Abdallah (1), Omar (2), Lina (3), Zahi (4), Sara (5).

### Known behavior with the sample data

`loans.txt` currently contains a malformed last entry (only two of the three lines: `2` and `234`) and a loan for book ID `6`, which does not exist in `books.txt`. When the program starts, it prints a data error message for the incomplete entry and skips the loan for book 6. The remaining loans load normally. To get a clean startup, delete the incomplete last entry and the book 6 entry from `loans.txt`.

## Design notes

- `Loan` is a separate class because it holds information a `Book` does not have (the borrower, due day, and return day).
- The loan period (`LOAN_PERIOD`, 14 days) and loan limit (`MAX_LOANS`, 3) are class constants and can be changed in `classes.py`. The "already has 3 active loans" message is written as fixed text, so update it too if you change the limit.
- `Library.lend_book` takes a `loadState` flag. When `True` (a real lend from the menu) it removes a copy and writes to `loans.txt`; when `False` (loading from file) it only rebuilds the loan in memory, because `books.txt` already holds the available copies.

## Who did what

--> included in the report
