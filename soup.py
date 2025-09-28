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

for i in range(10):
    ratings = []
    scores = []
    stars =[]
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
    print(f"page {i+1} have {len(names)} {len(ratings)} {len(scores)} {len(stars)} {len(prices)} {len(locations)}")
    
    driver.find_element(By.XPATH, "//button[@aria-label='Next page']").click()

# for i in range(10):
#     test_classes = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "DOkx")))
#     for items in test_classes:
#         item = items.text.split('\n')
#         if len(item) == 2:
#             a,b = item
#             c = "0"
#         if len(item) == 3:
#             a,b,c = item
    
driver.quit()