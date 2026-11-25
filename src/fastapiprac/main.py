
import json
import uvicorn
from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="FastAPIPractice",
    description="First FastAPI application",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Путь к файлу с данными
DATA_FILE = Path(__file__).parent / "data.json"

# Загружаем данные из JSON
with open(DATA_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)


# Модель книги
class Book(BaseModel):
    id: int
    title: str
    author: str
    year: int
    genre: str
    price: float
    in_stock: bool


# Сохраняем данные в JSON
def save_data():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# Получение всех книг
@app.get("/books", response_model=list[Book])
async def get_books():
    return data["books"]


# Получение книги по ID
@app.get("/books/{book_id}", response_model=Book)
async def get_book(book_id: int):
    for book in data["books"]:
        if book["id"] == book_id:
            return book

    raise HTTPException(status_code=404, detail="Книга не найдена")


# Добавление новой книги
@app.post("/books", response_model=Book)
async def add_book(book: Book):
    for existing_book in data["books"]:
        if existing_book["id"] == book.id:
            raise HTTPException(status_code=400, detail="Книга с таким ID уже существует")

    data["books"].append(book.model_dump())
    save_data()

    return book


# Удаление книги по ID
@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
    for book in data["books"]:
        if book["id"] == book_id:
            data["books"].remove(book)
            save_data()
            return {"message": "Книга удалена"}

    raise HTTPException(status_code=404, detail="Книга не найдена")


# Обновление книги по ID
@app.put("/books/{book_id}", response_model=Book)
async def update_book(book_id: int, updated_book: Book):
    for book in data["books"]:
        if book["id"] == book_id:
            updated_book.id = book_id
            book.update(updated_book.model_dump())
            save_data()
            return book

    raise HTTPException(status_code=404, detail="Книга не найдена")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
