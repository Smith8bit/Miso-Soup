from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium import webdriver
import time


def get_hotel_data(driver, pages: int, date: tuple):
    
    sql_command = "INSERT INTO Tokyo_hotels (hotel_name, review_rating, review_score, hotel_stars, price, location, date) VALUES (?, ?, ?, ?, ?, ?, ?)"
    
    url = f"https://www.kayak.com/hotels/Tokyo,Tokyo-Prefecture,Japan-c21033/{date[0]}/{date[1]}/1adults"
    driver.get(url)
    print(f"Start scraping {date[0]}")
    wait = WebDriverWait(driver, 20)
    time.sleep(20)

    for page in range(pages):       
        try:
            container = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "S0Ps")))
        except:
            print(f'Hotel containers of {date[0]} is not available')
            break
        print(f'Start scraping {page+1} of {date[0]}')
        
        for card in container:
            try:
                name = card.find_element(By.CLASS_NAME, 'c9Hnq-hotel-name')
                price = card.find_element()
            except:
                break
            print(name.text)

start = ('2026-01-01', '2026-01-02')
dri = webdriver.Chrome()
get_hotel_data(dri, 1, start)