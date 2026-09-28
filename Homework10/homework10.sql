
CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    year_published INTEGER,
    price REAL
);

INSERT INTO books (title , author , year_published , price) VALUES
('Кобзар', 'Тарас Шевченко', 1840, 250.00),
('Тіні забутих предків', 'Михайло Коцюбинський', 1911, 180.50),
('Захар Беркут', 'Іван Франко', 1883, 210.00),
('Місто', 'Валер''ян Підмогильний', 1928, 195.75),
('Інтернат', 'Сергій Жадан', 2017, 320.00);

UPDATE books
SET price = 235.00 
WHERE id = 3;

SELECT id ,title FROM books WHERE title = 'Захар Беркут';

DELETE FROM books
WHERE id = 4;
SELECT * FROM books WHERE id = 4;


