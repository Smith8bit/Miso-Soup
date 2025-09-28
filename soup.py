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

# parts = "my loving".split(' ')
# if len(parts) == 2:
#     x, y = parts
#     z = None
# elif len(parts) == 3:
#     x, y, z = parts
# else:
#     x, y, z = None, None, None 
#     print("Input does not have 2 or 3 words.")

# # Only print if variables were assigned successfully
# if x is not None:
#     print(f'x = {x}, y = {y}, z = {z}')


# for i in range(10):
#     names = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'c9Hnq-hotel-name')))
#     ratings = wait.until(EC.presence_of_all_elements_located((By.XPATH, ".//div[contains(@class, 'Dp6Q')]")))
#     classes = wait.until(EC.presence_of_all_elements_located((By.XPATH, ".//span[contains(@class, 'hEI8')]")))
#     prices = wait.until(EC.presence_of_all_elements_located((By.XPATH, ".//div[contains(@class, 'c1XBO')]")))
#     locations = wait.until(EC.presence_of_all_elements_located((By.XPATH, ".//div[contains(@class, 'upS4')]")))
#     print(f"page {i+1} have {len(names)} {len(ratings)} {len(classes)} {len(prices)} {len(locations)}")
    
#     driver.find_element(By.XPATH, "//button[@aria-label='Next page']").click()

for i in range(10):
    test_classes = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "DOkx")))
    for items in test_classes:
        item = items.text.split('\n')
        if len(item) == 2:
            a,b = item
            c = "0"
        if len(item) == 3:
            a,b,c = item
        print(f"Review rating: {a} Review score: {b} Class: {c}")
    print(len(test_classes))
    driver.find_element(By.XPATH, "//button[@aria-label='Next page']").click()
    

# driver.quit()