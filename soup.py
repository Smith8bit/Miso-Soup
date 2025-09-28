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

hotel_list = []
time.sleep(20)
wait = WebDriverWait(driver, 10)
hotel_names = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "c9Hnq-hotel-name")))
for hotel in hotel_names:
   hotel_list.append(hotel.text)
#for i in range(0,2):
 #   hotel_names = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "c9Hnq-hotel-name")))
  #  for hotel in hotel_names:
   #     hotel_list.append(hotel.text)
    #driver.find_element(By.XPATH, '//*[@id="resultWrapper"]/div[6]/nav/div/button[8]').click()

print(len(hotel_list))
print(hotel_list)
driver.quit()