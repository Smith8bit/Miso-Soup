from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sqlite3
import time

def get_hotel_data(driver, page: int, day: int):
    
    insert_hotel_command = "INSERT INTO Tokyo_hotels (hotel_name, review_rating, review_score, hotel_stars, price, location, date) VALUES (?, ?, ?, ?, ?, ?, ?)"

    if day < 10:
        inDay = f"0{day}"
        outDay = f"0{day+1}" if day != 9 else "10"
    else:
        inDay = str(day)
        outDay = str(day + 1)

    url = f"https://www.kayak.com/hotels/Tokyo,Tokyo-Prefecture,Japan-c21033/2026-01-{inDay}/2026-01-{outDay}/1adults"
    print(f"Fetching URL for check-in day: {inDay}")
    driver.get(url)

    wait = WebDriverWait(driver, 20)
    hotel_list = []

    for i in range(page):
        container = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "S0Ps")))
        ratings = []
        scores = []
        stars =[]
        try:
            names = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'c9Hnq-hotel-name')))
            reviews = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "DOkx")))
            for review in reviews:
                rinfo = review.text.split('\n')
                if len(rinfo) == 2:
                    rr, rs = rinfo
                    star = "0 stars"
                if len(rinfo) == 3:
                    rr, rs, star = rinfo
                ratings.append(rr)
                scores.append(rs)
                stars.append(star)
            prices = wait.until(EC.presence_of_all_elements_located((By.XPATH, ".//div[contains(@class, 'c1XBO')]")))
            locations = wait.until(EC.presence_of_all_elements_located((By.XPATH, ".//div[contains(@class, 'upS4')]")))
            try:
                for j in range(len(names)):
                    hotel_data = (names[j].text, ratings[j], scores[j], stars[j], prices[j].text, locations[j].text, f"01-{inDay}")
                    hotel_list.append(hotel_data)
            except:
                continue
        except:
            continue
        

        with sqlite3.connect("littledb.db") as conn:
            conn.cursor().executemany(insert_hotel_command, hotel_list)
            print(f"Day {day} : Page {i+1} inserted successfully")
            
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Next page']"))).click()
    return