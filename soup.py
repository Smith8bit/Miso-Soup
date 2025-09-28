from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")

# options.add_argument("--headless")

options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options=options)

stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

url = "https://www.kayak.com/hotels/Tokyo,Tokyo-Prefecture,Japan-c21033/2026-01-01/2026-01-02/1adults"
driver.get(url)

hotel_list = {}
time.sleep(20)
wait = WebDriverWait(driver, 10)

for i in range(0, 10):
    try:
        name = hotel.find_element(By.CLASS_NAME, 'c9Hnq-hotel-name').text
    except NoSuchElementException:
        name = 'N/A'
    
    try:
        rating = hotel.find_element(By.XPATH, ".//div[contains(@class, 'Dp6Q')]").text
    except NoSuchElementException:
        rating = 'N/A'

    try:
        hotel_class = hotel.find_element(By.XPATH, ".//span[contains(@class, 'hEI8')]").text
    except NoSuchElementException:
        hotel_class = 'N/A'

    try:
        price = hotel.find_element(By.XPATH, ".//div[contains(@class, 'c1XBO')]").text
    except NoSuchElementException:
        price = 'N/A'

    try:
        location = hotel.find_element(By.XPATH, ".//div[contains(@class, 'upS4')]").text
    except NoSuchElementException:
        location = 'N/A'

    if name != 'N/A':
        hotel_list[name] = [rating, hotel_class, price, location]

    try:
        driver.find_element(By.XPATH, "//button[@aria-label='Next page']").click()
    except NoSuchElementException:
        print("Could not find the 'Next page' button. Ending scrape.")
        break

for index, detail in hotel_list.items():
    print(index, detail)

driver.quit()