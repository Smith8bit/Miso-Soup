import requests
from bs4 import BeautifulSoup

url = requests.get('https://www.kayak.com/')
soup = BeautifulSoup(url.content, 'html.parser')

# Find elements with that class
data = soup.find_all(class_='Japq-title')

print(d.get_text(strip=True))
