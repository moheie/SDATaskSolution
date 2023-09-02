import sys
import json

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QBrush, QPixmap
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QLineEdit, \
    QTextBrowser, QApplication


class Book:
    def __init__(self, title, author, cost):
        self.title = title
        self.author = author
        self.cost = cost

    def __str__(self):
        return f"Title: {self.title}\nAuthor: {self.author}\nCost: {self.cost}"


class Section:
    def __init__(self, title):
        self.title = title
        self.books = []

    def add_book(self, book):
        self.books.append(book)


class Library:
    def __init__(self):
        self.sections = []
        self.read_books_from_json("books.json")

    def read_books_from_json(self, filename):
        with open(filename, "r") as file:
            data = json.load(file)
            for title, book_data in data.items():
                author = book_data["author"]
                cost = book_data["cost"]
                section_title = book_data["section"]
                book = Book(title, author, cost)
                self.add_book_to_section(section_title, book)

    def add_book_to_section(self, section_title, book):
        section = next((s for s in self.sections if s.title == section_title), None)
        if not section:
            section = Section(section_title)
            self.sections.append(section)
        section.add_book(book)


class BookStoreGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Book Store Management System")
        self.setGeometry(100, 100, 600, 400)

        self.library = Library()

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setBrush(QPalette.Window, QBrush(QPixmap("pitucre.jpg")))
        self.setPalette(palette)

        self.layout = QVBoxLayout()

        self.label = QLabel("Welcome to the Book Store Management System")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-weight: bold; font-size: 24px; color: white;")
        self.layout.addWidget(self.label)

        self.button_search_books = QPushButton("Search Books")
        self.button_search_books.clicked.connect(self.show_search_books)
        self.layout.addWidget(self.button_search_books)

        self.central_widget.setLayout(self.layout)

        self.search_books_layout = QVBoxLayout()
        self.search_books_widget = QWidget()
        self.search_books_widget.setLayout(self.search_books_layout)
        self.search_books_widget.hide()

        self.create_search_books_ui()

    def create_search_books_ui(self):
        self.title_search_layout = QHBoxLayout()
        self.title_search_label = QLabel("Search Book by Title:")
        self.title_search_entry = QLineEdit()
        self.title_search_button = QPushButton("Search")
        self.title_search_button.clicked.connect(self.search_by_title)
        self.title_search_layout.addWidget(self.title_search_label)
        self.title_search_layout.addWidget(self.title_search_entry)
        self.title_search_layout.addWidget(self.title_search_button)

        self.author_search_layout = QHBoxLayout()
        self.author_search_label = QLabel("Search Author's Books:")
        self.author_search_entry = QLineEdit()
        self.author_search_button = QPushButton("Search")
        self.author_search_button.clicked.connect(self.search_by_author)
        self.author_search_layout.addWidget(self.author_search_label)
        self.author_search_layout.addWidget(self.author_search_entry)
        self.author_search_layout.addWidget(self.author_search_button)

        self.buy_by_title_layout = QHBoxLayout()  # Add Buy Book by Title section
        self.buy_by_title_label = QLabel("Buy Book by Title:")
        self.buy_by_title_entry = QLineEdit()
        self.buy_by_title_button = QPushButton("Buy")
        self.buy_by_title_button.clicked.connect(self.buy_book_by_title)
        self.buy_by_title_layout.addWidget(self.buy_by_title_label)
        self.buy_by_title_layout.addWidget(self.buy_by_title_entry)
        self.buy_by_title_layout.addWidget(self.buy_by_title_button)

        self.books_found_label = QLabel("Books Found:")
        self.books_found_text = QTextBrowser()

        self.back_button_search = QPushButton("Back")
        self.back_button_search.clicked.connect(self.show_main_screen)

        self.search_books_layout.addLayout(self.title_search_layout)
        self.search_books_layout.addLayout(self.author_search_layout)
        self.search_books_layout.addLayout(self.buy_by_title_layout)  # Add Buy Book by Title section
        self.search_books_layout.addWidget(self.books_found_label)
        self.search_books_layout.addWidget(self.books_found_text)
        self.search_books_layout.addWidget(self.back_button_search)
        self.layout.addWidget(self.search_books_widget)

        self.display_all_books()  # Display all books initially

    def display_all_books(self):
        all_books = [(section.title, book) for section in self.library.sections for book in section.books]
        if all_books:
            self.books_found_text.clear()
            current_section = None
            for section_title, book in all_books:
                if current_section != section_title:
                    self.books_found_text.append("")  # Add an empty line as separator
                    self.books_found_text.append(f"--- {section_title} ---")
                    current_section = section_title
                self.books_found_text.append(str(book))
                self.books_found_text.append("-" * 20)
        else:
            self.books_found_text.setText("No books found in the library.")

    def show_main_screen(self):
        self.search_books_widget.hide()
        self.label.show()
        self.button_search_books.show()

    def show_search_books(self):
        self.label.hide()
        self.button_search_books.hide()
        self.search_books_widget.show()

    def search_by_title(self):
        title = self.title_search_entry.text()
        matching_books = []
        for section in self.library.sections:
            for book in section.books:
                if title.lower() in book.title.lower():
                    matching_books.append(book)
        if matching_books:
            self.books_found_text.clear()
            for book in matching_books:
                self.books_found_text.append(str(book))
                self.books_found_text.append("-" * 20)
        else:
            self.books_found_text.setText("No books matching the title were found.")

    def search_by_author(self):
        author = self.author_search_entry.text()
        author_books = [book for section in self.library.sections for book in section.books if
                        author.lower() in book.author.lower()]
        if author_books:
            self.books_found_text.clear()
            for book in author_books:
                self.books_found_text.append(str(book))
                self.books_found_text.append("-" * 20)
        else:
            self.books_found_text.setText("No books by this author were found.")

    def buy_book_by_title(self):
        title = self.buy_by_title_entry.text()
        book = None
        for section in self.library.sections:
            for b in section.books:
                if b.title.lower() == title.lower():
                    book = b
                    break
        if book:
            for section in self.library.sections:
                if book in section.books:
                    section.books.remove(book)
                    self.books_found_text.clear()  # Clear any previous messages
                    self.books_found_text.append("Book is purchased and removed from the library.")
                    return
        else:
            self.books_found_text.clear()  # Clear any previous messages
            self.books_found_text.append("Book not found.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BookStoreGUI()
    window.show()
    sys.exit(app.exec_())
