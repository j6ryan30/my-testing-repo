import sqlite3

DB_NAME = "books.db"

def seed_books():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    books = [
        {
            "title": "The Great Gatsby",
            "author": "F. Scott Fitzgerald",
            "isbn": "9780743273565",
            "price": 15.00,
            "quantity": 10,
            "description": "Classic American novel set in the Jazz Age.",
            "category": "Classics"
        },
        {
            "title": "1984",
            "author": "George Orwell",
            "isbn": "9780451524935",
            "price": 12.50,
            "quantity": 15,
            "description": "Dystopian novel about surveillance and totalitarianism.",
            "category": "Dystopian"
        },
        {
            "title": "The Hobbit",
            "author": "J.R.R. Tolkien",
            "isbn": "9780547928227",
            "price": 20.00,
            "quantity": 8,
            "description": "Fantasy adventure featuring Bilbo Baggins.",
            "category": "Fantasy"
        },
        {
            "title": "Attack on Titan",
            "author": "Hajime Isayama",
            "isbn": "9781612620244",
            "price": 15.99,
            "quantity": 10,
            "description": "Post-apocalyptic manga series.",
            "category": "Manga"
        },
        {
            "title": "Atomic Habits",
            "author": "James Clear",
            "isbn": "9780735211292",
            "price": 18.00,
            "quantity": 20,
            "description": "Practical guide to building good habits.",
            "category": "Self-Help"
        },
        {
            "title": "Harry Potter and the Sorcerer's Stone",
            "author": "J.K. Rowling",
            "isbn": "9780439708180",
            "price": 20.99,
            "quantity": 25,
            "description": "Popular fantasy novel about a young wizard.",
            "category": "Fantasy"
        },
        {
            "title": "The New Noble",
            "author": "Ryan Downes",
            "isbn": "9088779456541",
            "price": 9.99,
            "quantity": 6,
            "description": "A group of people from different walks of life come together to confront the world’s most complex challenges and rise as the most powerful team the universe has ever seen.",
            "category": "Fiction"
        },
        {
            "title": "Dune",
            "author": "Frank Herbert",
            "isbn": "9780441172719",
            "price": 18.99,
            "quantity": 12,
            "description": "Epic science fiction saga set on the desert planet Arrakis.",
            "category": "Sci-Fi"
        },
        {
            "title": "To Kill a Mockingbird",
            "author": "Harper Lee",
            "isbn": "9780061120084",
            "price": 14.99,
            "quantity": 18,
            "description": "A powerful story of racial injustice in the American South.",
            "category": "Classics"
        },
        {
            "title": "The Alchemist",
            "author": "Paulo Coelho",
            "isbn": "9780061122415",
            "price": 16.99,
            "quantity": 14,
            "description": "A philosophical journey of self-discovery and destiny.",
            "category": "Fiction"
        },
        {
            "title": "Chainsaw Man Vol. 1",
            "author": "Tatsuki Fujimoto",
            "isbn": "9781974709939",
            "price": 12.99,
            "quantity": 22,
            "description": "A gritty manga about devils, hunters, and survival.",
            "category": "Manga"
        },
        {
            "title": "The Way of Kings",
            "author": "Brandon Sanderson",
            "isbn": "9780765326355",
            "price": 24.99,
            "quantity": 7,
            "description": "The first epic entry in The Stormlight Archive.",
            "category": "Fantasy"
        },
        {
            "title": "Educated",
            "author": "Tara Westover",
            "isbn": "9780399590504",
            "price": 17.99,
            "quantity": 11,
            "description": "A memoir about resilience, family, and the pursuit of knowledge.",
            "category": "Nonfiction"
        },
        {
            "title": "The Book of Mormon",
            "author": "Various",
            "isbn": "9781592975036",
            "price": 8.99,
            "quantity": 30,
            "description": "A sacred text of the Latter-day Saint movement.",
            "category": "Religion & Inspirational"
        },
        {
            "title": "The Lightning Thief",
            "author": "Rick Riordan",
            "isbn": "9780786838653",
            "price": 12.99,
            "quantity": 16,
            "description": "Percy Jackson discovers he is the son of a Greek god.",
            "category": "Kids / Young Readers"
        },
        {
            "title": "Shadowblade Academy",
            "author": "Lena Arkwright",
            "isbn": "9912345678001",
            "price": 14.50,
            "quantity": 10,
            "description": "A young warrior trains at a secret academy hidden in the mountains.",
            "category": "Fantasy"
        },
        {
            "title": "The Quantum Archivist",
            "author": "Dorian Vale",
            "isbn": "9912345678002",
            "price": 19.99,
            "quantity": 9,
            "description": "A scientist discovers a device that stores memories from alternate timelines.",
            "category": "Sci-Fi"
        },
        {
            "title": "Moonlit Harbor",
            "author": "Elara Finch",
            "isbn": "9912345678003",
            "price": 13.99,
            "quantity": 12,
            "description": "A quiet coastal town hides a supernatural secret.",
            "category": "Fiction"
        },
        {
            "title": "Rise of the Ember Knights",
            "author": "Kael Thorn",
            "isbn": "9912345678004",
            "price": 17.99,
            "quantity": 8,
            "description": "A band of warriors must unite to stop an ancient evil.",
            "category": "Fantasy"
        },
        {
            "title": "The Last Algorithm",
            "author": "Mira Solis",
            "isbn": "9912345678005",
            "price": 18.50,
            "quantity": 10,
            "description": "A rogue AI threatens to rewrite the digital world.",
            "category": "Sci-Fi"
        },
        {
            "title": "Whispers of the Willow",
            "author": "Hannah Crest",
            "isbn": "9912345678006",
            "price": 11.99,
            "quantity": 14,
            "description": "A heartfelt story about family, healing, and rediscovery.",
            "category": "Fiction"
        },
        {
            "title": "The Scholar’s Oath",
            "author": "Elias Rowan",
            "isbn": "9912345678007",
            "price": 15.99,
            "quantity": 9,
            "description": "A young academic uncovers a conspiracy buried in ancient texts.",
            "category": "Nonfiction"
        },
        {
            "title": "Garden of Starlight",
            "author": "Marin Solara",
            "isbn": "9912345678008",
            "price": 13.50,
            "quantity": 11,
            "description": "A magical garden that blooms only under the night sky.",
            "category": "Fantasy"
        },
        {
            "title": "The Silent Choir",
            "author": "Jonas Hale",
            "isbn": "9912345678009",
            "price": 12.50,
            "quantity": 10,
            "description": "A mystery surrounding a monastery where no one speaks.",
            "category": "Fiction"
        },
        {
            "title": "Beyond the Nebula Gate",
            "author": "Seren Locke",
            "isbn": "9912345678010",
            "price": 16.99,
            "quantity": 7,
            "description": "Explorers discover a portal leading to an uncharted galaxy.",
            "category": "Sci-Fi"
        }
    ]

    for b in books:
        cursor.execute("""
            INSERT INTO books 
            (title, author, isbn, price, quantity, description, category)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            b["title"],
            b["author"],
            b["isbn"],
            b["price"],
            b["quantity"],
            b["description"],
            b["category"]
        ))

    conn.commit()
    conn.close()
    print("✅ Book seeding complete.")

if __name__ == "__main__":
    seed_books()
