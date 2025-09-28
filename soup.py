from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
    names = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'c9Hnq-hotel-name')))
    ratings = wait.until(EC.presence_of_all_elements_located((By.XPATH, ".//div[contains(@class, 'Dp6Q')]")))
    classes = wait.until(EC.presence_of_all_elements_located((By.XPATH, ".//span[contains(@class, 'hEI8')]")))
    prices = wait.until(EC.presence_of_all_elements_located((By.XPATH, ".//div[contains(@class, 'c1XBO')]")))
    locations = wait.until(EC.presence_of_all_elements_located((By.XPATH, ".//div[contains(@class, 'upS4')]")))
    print("page", i, len(names), len(ratings), len(classes), len(prices), len(locations))
    ##    hotel_list[names[j].text] = [ratings[j].text, classes[j].text, prices[j].text, locations[j].text]
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Next page']"))).click()

#for index, detail in hotel_list.items():
#   print(index, detail)

driver.quit()