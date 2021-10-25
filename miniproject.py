class Library:
    def __init__(self, list_of_books, name_of_library):
        self.list_of_books = list_of_books
        self.name_of_library = name_of_library
        self.lended_book=[]

    def display_book(self):
        for items in self.list_of_books:
             print(items)
        return "This are the books we have"
    def add_book(self, new_book):
         self.list_of_books.append(new_book.capitalize())
    def lend_book(self, book):
        if book in self.list_of_books:
            self.lended_book.append(book)
            self.list_of_books.remove(book)
            print("Book lending permission approved...")
        elif book in self.lended_book:
            print("Sorry the book is already been lended\n"
                  "Currently we only have these:- ")
            for items in self.list_of_books:
                print(items)
        else:
            print("Book's name entered is not available or name is wrong "
                  "and the available books are:- ")
            for items in self.list_of_books:
                print(items)


def system():
    try:
        value = True
        HARSH = Library(["Book-1", "Book-2", "Book-3"], "BEST library")

        while value == True:
            user_name = input("Enter your name:- ")

            user_input = eval(input(f"Welcome {user_name} to {HARSH.name_of_library} \n"
                                    f"Enter (1) To display books we have\n"
                                    f"Enter (2) To donate a book \n"
                                    f"Enter (3) To Lend a book\n"
                                    f"Enter (4) To return a book\n"
                                    f"Enter (5) For exit"
                                    f":- "))

            if user_input == 1:
                print(HARSH.display_book())

            elif user_input == 2:
                new_book = input("Enter name of book you want to donate:- ")
                HARSH.add_book(new_book.capitalize())
                print( "Book has been added thank you for your donation")


            elif user_input == 3:
                book = input("Enter the name of book you want to lend:- ")
                HARSH.lend_book(book.capitalize())


            elif user_input == 4:
                new_book = input("Enter the name of book you want to return:- ")
                HARSH.add_book(new_book.capitalize())
                print("Thank you for returning book hope to se you soon")
            elif user_input == 5:
                value = False
            else:
                print("Wrong input has been entered:- ")
    except:
        print("Error!!!")
        system()
system()
