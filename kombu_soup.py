from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sqlite3
import time


def get_hotel_data(driver, place, date):
    
    url = f"https://www.kayak.com/hotels/{place[0]}-Prefecture,{place[1]}/{date[0]}/{date[1]}/1adults"
    driver.get(url)
    print(f"---- Start scraping {date[0]} at {place[0]} ----")
    wait = WebDriverWait(driver, 20)
    time.sleep(20)

    table_name = f'{place[0]}_hotels'
    create_command = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        hotel_id INTEGER PRIMARY KEY AUTOINCREMENT,
        hotel_name TEXT NOT NULL,
        review_rating TEXT,
        review_score TEXT,
        hotel_stars TEXT,
        price TEXT,
        location TEXT,
        date TEXT
    )
    """
    insert_command = f"""
    INSERT INTO {table_name} (
        hotel_name, 
        review_rating, 
        review_score, 
        hotel_stars, 
        price, 
        location, 
        date
        ) 
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    with sqlite3.connect("littledb.db") as conn:
        cur = conn.cursor()
        cur.execute(create_command)

        try:
            for page in range(50): 
                try:
                    container = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "S0Ps")))
                except:
                    print(f'Hotel containers of {date[0]} is not available')
                    continue
                print(f' Scraping page {page+1} of {date[0]}')

                for card in container:
                    try:
                        name,rating, score, star, price, location = None, None, None, "0 star", None, None 
                        name = card.find_element(By.CLASS_NAME, 'c9Hnq-hotel-name')
                        review = card.find_element(By.CLASS_NAME, "DOkx")
                        try:
                            rating, score, star = review.text.split('\n')
                        except:
                            rating, score = review.text.split('\n')
                        price = card.find_element(By.XPATH, ".//div[contains(@class, 'c1XBO')]")
                        location = card.find_element(By.XPATH, ".//div[contains(@class, 'upS4')]")
                    except:
                        break
                    info = (name.text, rating, score, star, price.text, location.text, date[0])
                    cur.execute(insert_command, info)
                conn.commit()

                wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Next page']"))).click()
        except:
            return