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

hotel_names = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'c9Hnq-hotel-name')))
hotel_ratings = wait.until(EC.presence_of_all_elements_located((By.XPATH, ".//div[contains(@class, 'Dp6Q')]")))
print(len(hotel_names))
print(len(hotel_ratings))
for i in range(len(hotel_names)):
    hotel_list[hotel_names[i].text] = hotel_ratings[i].text

for name, rating in hotel_list.items():
    print(name, rating)

#for i in range(0, 1):
 #   hotel_names = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'c9Hnq-hotel-name')))
  #  hotel_ratings = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#resultWrapper > div.c71z4 > div:nth-child(5) > div > div > div.S0Ps-resultInner > div.S0Ps-middleSection > div.c9Hnq.c9Hnq-mod-spacing-default > div > div.c9Hnq-review-rating-resultinfo-wrapper > div > div.DOkx-rating-review-score > div')))
   # hotel_zipped = zip(hotel_names,hotel_ratings)
    #for j in len(hotel_zipped):
     #   hotel_names.updat

#    driver.find_element(By.CLASS_NAME, 'A8fY-chevron').click()

driver.quit()