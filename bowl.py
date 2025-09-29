import kombu_soup as ks
from selenium import webdriver
from selenium_stealth import stealth
import datetime

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

start_date = datetime.date(2025, 12, 1)
end_date = datetime.date(2026, 12, 31)
delta = datetime.timedelta(days=1)

while (start_date <= end_date):
    next_date = start_date+delta
    ks.get_hotel_data(driver,50,[start_date,next_date])
    start_date += delta

driver.quit()