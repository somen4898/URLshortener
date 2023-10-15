import sqlite3
from urllib.parse import urlparse
import hashlib
import base64

# Connect to the SQLite database
conn = sqlite3.connect("url_shortener.db")
conn.execute('''
    CREATE TABLE IF NOT EXISTS url_mappings (
        id INTEGER PRIMARY KEY,
        original_url TEXT NOT NULL,
        short_url TEXT NOT NULL
    )
''')


def insertdb(original_url, short_url):
    conn.execute('''
        INSERT INTO url_mappings (original_url, short_url)
        VALUES (?, ?)
    ''', (original_url, short_url))
    conn.commit()


def URLLong(short_url):
    cursor = conn.execute('''
        SELECT original_url FROM url_mappings WHERE short_url = ?
    ''', (short_url,))
    result = cursor.fetchone()
    return result[0] if result else None


def short_url_exists(short_url):
    cursor = conn.execute('SELECT original_url FROM url_mappings WHERE short_url = ?', (short_url,))
    result = cursor.fetchone()
    return result[0] if result else None


def is_valid(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


# Function to shorten a URL (placeholder implementation)
def generate_short_url(original_url):
    # Generate a unique identifier using MD5 hash
    md5_hash = hashlib.md5(original_url.encode()).digest()
    unique_id = base64.urlsafe_b64encode(md5_hash)[:6].decode()  # Take the first 6 characters

    # Check if the short URL already exists
    existing_short_url = short_url_exists(unique_id)
    if existing_short_url:
        return existing_short_url

    # Construct the full short URL
    full_short_url = f"https://short.url/{unique_id}"


    return full_short_url



while True:
    # Get user input for the operation they want to perform
    n = input("Enter 1 to shorten URL and Enter 2 to get orignal URL type 'stop' to stop: ")

    if n == "1":
        # User wants to shorten a URL
        URL = input("Enter URL that you want to shorten: ")
        temp=is_valid(URL)
        if temp:
            val = short_url_exists(URL)
            if val is None:
                surl = generate_short_url(URL)  # Placeholder logic
                insertdb(URL,surl)
                print(surl)  # Print the shortened URL (placeholder)
            else:
                print(val)

        else:
            print("enter valid url")

    elif n == "2":
        # User wants to lengthen a URL
        URL = input("Enter the short url for it's orignal: ")
        temp = is_valid(URL)
        if temp:
            lurl = URLLong(URL)
            if lurl is None:
                print("no orignal url for given short url in database")
            else:
                print(lurl)
        else:
            print("enter short url for which orignal url exists")

    elif n == "stop":
        # User wants to stop the program
        break

    else:
        # Invalid input, ask for valid input
        print("Enter valid number")


# Close the connection to the database
conn.close()
