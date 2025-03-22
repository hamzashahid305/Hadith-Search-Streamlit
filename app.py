import streamlit as st
import requests

# API Key for Hadith API
API_KEY = '$2y$10$hNjBWWuv1uJ78usxn7rtJu1Hv7r7BMRK717pCT9ZCJ5V18FwYuu'  # Replace with your actual API key

# Available Hadith books and their slugs (according to the website)
BOOKS = {
    "Sahih Bukhari": "sahih-bukhari",
    "Sahih Muslim": "sahih-muslim",
    "Jami' Al-Tirmidhi": "al-tirmidhi",
    "Sunan Abu Dawood": "abu-dawood",
    "Sunan Ibn-e-Majah": "ibn-e-majah",
    "Sunan An-Nasa`i": "sunan-nasai",
    "Mishkat Al-Masabih": "mishkat",
    "Musnad Ahmad": "musnad-ahmad",
    "Al-Silsila Sahiha": "al-silsila-sahiha"
}

# Function to get Hadiths from API based on Urdu search and selected book
def get_hadiths_from_api(urdu_word, book_slug):
    url = f'https://hadithapi.com/api/hadiths?apiKey={API_KEY}&hadithUrdu={urdu_word}&book={book_slug}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()  # Returns the entire response
    else:
        return {"error": "Unable to fetch data from API"}

# Streamlit Interface
st.title('Urdu Ahadees Search')
st.write('Search for Ahadees in Urdu from different books')

# Dropdown for selecting the book
book_choice = st.selectbox("Select a Hadith Book", list(BOOKS.keys()))

# Input from user for the Urdu word
urdu_word = st.text_input('Enter Urdu word to search for Ahadees')

if urdu_word and book_choice:
    # Get the corresponding book slug from the dictionary
    book_slug = BOOKS[book_choice]

    # Fetch the Ahadees data from API
    data = get_hadiths_from_api(urdu_word, book_slug)
    
    # Displaying the raw API response to inspect its structure
    st.write("API Response:", data)
    
    # Checking if the response contains any error
    if 'error' in data:
        st.error(data['error'])
    else:
        if 'hadiths' in data:  # Ensure we have the 'hadiths' key in the response
            for hadith in data['hadiths']['data']:  # Loop through the list of hadiths inside 'data'
                # Accessing individual Hadith fields safely using `.get()`
                hadith_number = hadith.get('hadithNumber', 'N/A')
                book = hadith.get('book', {}).get('bookName', 'N/A')
                text = hadith.get('hadithUrdu', 'No text available')

                st.write(f"**Hadith Number:** {hadith_number}")
                st.write(f"**Book:** {book}")
                st.write(f"**Text:** {text}")
                st.write("---")
        else:
            st.warning('No Ahadees found for the given search term.')
