from bs4 import BeautifulSoup
from gtts import gTTS
import requests, os, codecs

# Ask the user what author they would like to find.
book = input('What author do you want to find? ').split(" ")

print('Getting Top 10 Results...')

# Set Base URL for Project Gutenberg.
base_url = "https://www.gutenberg.org/ebooks/search/?query="

# Create URL query from user input and add to the Gutenberg base url to complete the web address.
sep = "+"
query_sep = sep.join(book)
query_url = base_url + query_sep

# Make a Request for the URL using the Requests library.
res = requests.get(query_url)

# Parse the request text using Beautiful Soup.
soup = BeautifulSoup(res.text, 'html.parser')

# The CSS Selector for the Book Title.
selector_titles = """
    .booklink
    .title
    """

# Then we store the Top 10 book titles in a list called 'book_html'.
book_html = soup.select(selector_titles, limit=10)

# Create a list that will store the stripped book titles.
book_titles = []

# Iterate through the html title to strip them, and then add them to the book_titles list.
for book in book_html:
    book_titles.append(book.text.strip())

# The CSS Selector for the Book Links.
selector_links = """
    .booklink
    .link
    """

# Create list called 'book_links_html' to store the book link html in.
book_links_html = []

# Iterate through HTML to find appropriate links to each book and add them to the book_links_html list.
for a in soup.select(selector_links, href=True, limit=10):
    book_links_html.append(a['href'])

# Create list for final book links with base url and ebook url.
book_links = []

# Iterate through the html links and add these to the end of the base url. Store new link in book_links list.
for y in book_links_html:
    book_links.append("https://www.gutenberg.org" + y)

# Create a dictionary that combines the title list and links list.
book_dict = {book_titles[i]: book_links[i] for i in range(len(book_titles))}

# Create a function that allows the user to pick from a list of the top 10 results.
def let_user_pick(options):

    if len(options) == 0:
        print('No books were available for your search!')

    else:
        print("Please choose:")
        for idx, element in enumerate(options):
            print("{}) {}".format(idx + 1, element))

        let_user_pick.choice = input("Please enter a number: ")

# Call the function with the book_titles list as the options (same as the Dict keys).
let_user_pick(book_titles)

# Convert the user's choice to an integer so that we can access the list value.
choice = int(let_user_pick.choice) - 1

# Print a statement that shows the user what book they picked.
print("Finding: " + book_titles[choice] + "...")

# Save their book choice to a variable so that we can access the link from a dictionary.
book_choice = book_titles[choice]

# Access the book_dict dictionary and grab the link relating to the user's book choice.
book_choice_link = book_dict[book_choice]

# Create a UTF variable that is the same for each book - to add to URL.
utf = ".txt.utf-8"

# Add the UTF text formatter to this URL and save to variable.
utf_book_link = book_choice_link + utf

# Use Requests again to open the UTF URL and write the text to a file called Book.txt that is then saved.
text_res = requests.get(utf_book_link)
with codecs.open('book.txt', 'w', 'utf-8-sig') as file:
    file.write(text_res.text)

# Use gTTS to open Book.txt and convert to MP3 speech. Save this as Audio.mp3.
audiobook = open("book.txt", 'r').read()
speech = gTTS(text=str(audiobook), lang='en', slow=False)
speech.save("audio.mp3")


