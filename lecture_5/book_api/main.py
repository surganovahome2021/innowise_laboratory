from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session

# Connection to the database
SQL_DB_URL = 'sqlite:///Library.db'

engine = create_engine(SQL_DB_URL, connect_args={"check_same_thread": False})

session_local = sessionmaker(autoflush=False, autocommit=False, bind=engine)

# Defining a base class for ORM
Base = declarative_base()

# Creating a table
class BookTable(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    author = Column(String, nullable=False, index=True)
    year = Column(Integer, index=True)

# Base class for creating a book
class BaseLibrary(BaseModel):
    title: str
    author: str
    year: int

#
class CreateBook(BaseLibrary):
    pass

# Class for id_book
class Book(BaseLibrary):
    id: int

    class Config:
        from_attributes = True

# Initialization FastAPI
api = FastAPI()
Base.metadata.create_all(engine)

# Session generator
def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()

# HTTP Method for add a new book
@api.post("/books/", response_model=Book)
async def input_book(book: CreateBook, db: Session = Depends(get_db)) -> BookTable:
    db_book = BookTable(title=book.title, author=book.author, year=book.year)
    if db_book:
        raise Exception("Book already exists")
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

# HTTP Method for Get all book
@api.get("/books/", response_model=List[Book])
async def get_all_books(db: Session = Depends(get_db)):
    return db.query(BookTable).all()

# HTTP Method for Delete a book by ID
@api.delete("/books/{book_id}", response_model=Book)
async def delete_book(book_id: int, db: Session = Depends(get_db)) -> BookTable:
    db_book = db.query(BookTable).filter(BookTable.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

# HTTP Method for Update book details
@api.put("/books/{book_id}", response_model=Book)
async def update_books(book_id: int, book: CreateBook, db: Session = Depends(get_db)):
    db_book = db.query(BookTable).filter(BookTable.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    db_book.title = book.title
    db_book.author = book.author
    db_book.year = book.year
    db.commit()
    db.refresh(db_book)
    return db_book


# HTTP Method for Search book in library
@api.get("/books/search/", response_model=List[Book])
async def search_books(book_search: Optional[str or int] = Query(None, min_length=2, description="Search books by tittle or author or year"),
                       db: Session = Depends(get_db)):
    title = (db.query(BookTable).filter(BookTable.title.contains(book_search)).all()
             or db.query(BookTable).filter(BookTable.author.contains(book_search)).all()
             or db.query(BookTable).filter(BookTable.year.contains(book_search)).all())
    if not title:
            raise HTTPException(status_code=404, detail="Book not found")
    return title



























