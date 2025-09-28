import sqlite3
import random
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium import webdriver


insert_hotel_command = "INSERT INTO Tokyo_hotels (hotel_name, review_rating, review_score, hotel_stars, price, location, date) VALUES (?, ?, ?, ?, ?, ?, ?)"

def get_hotel_data(driver, page: int, day: int):
    # --- Date formatting logic (unchanged) ---
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
        # --- FIX 2: Removed time.sleep(30). We now wait for the hotel containers directly ---
        try:
            # --- FIX 1: Get a list of the PARENT containers for each hotel ---
            # This is the most reliable way to ensure data stays synchronized.
            hotel_containers = wait.until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "S0Ps-resultInner"))
            )
        except TimeoutException:
            print(f"Could not find hotel containers on page {i+1}. Skipping.")
            break # Exit the loop for this day if no hotels are found

        print(f"Scraping page {i+1} for day {inDay}... Found {len(hotel_containers)} hotels.")

        # Loop through each hotel's container to find its specific data
        for hotel in hotel_containers:
            try:
                # Find elements *within* the context of the 'hotel' container
                name = hotel.find_element(By.CLASS_NAME, 'c9Hnq-hotel-name').text
                price = hotel.find_element(By.XPATH, ".//div[contains(@class, 'c1XBO')]").text
                location = hotel.find_element(By.XPATH, ".//div[contains(@class, 'upS4')]").text

                # --- FIX 4: Safer review parsing with default values ---
                rating, score, star = "N/A", "N/A", "N/A" # Default values
                try:
                    review_element = hotel.find_element(By.CLASS_NAME, "DOkx")
                    rinfo = review_element.text.split('\n')
                    if len(rinfo) == 2:
                        rating, score = rinfo
                    elif len(rinfo) == 3:
                        rating, score, star = rinfo
                except NoSuchElementException:
                    # It's okay if a hotel has no review, just keep the default "N/A"
                    pass

                hotel_data = (name, rating, score, star, price, location, f"01-{inDay}")
                hotel_list.append(hotel_data)

            except NoSuchElementException:
                # This handles cases where a specific hotel card is missing a name, price, etc.
                print("Skipping a hotel card due to missing info.")
                continue

        # Click the 'Next' button to go to the next page
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Next page']"))).click()
            # Add a small delay after clicking to let the next page load
            time.sleep(random.uniform(3, 5))
        except TimeoutException:
            print("No 'Next page' button found. Reached the end.")
            break # Exit the pagination loop

    # --- FIX 3: Write to the database ONCE after collecting all data for the day ---
    if hotel_list:
        with sqlite3.connect("littledb.db") as conn:
            conn.cursor().executemany(insert_hotel_command, hotel_list)
            print(f"Day {day}: Inserted {len(hotel_list)} hotel records successfully.")

    return hotel_list

# --- FIX 5: Example of how to call this function in a loop ---

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
# options.add_argument("--headless")

options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options=options)

for day_num in range(1, 31):
    get_hotel_data(driver=driver, page=1, day=day_num)

driver.quit() 

