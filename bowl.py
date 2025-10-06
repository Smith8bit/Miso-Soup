import kombu_soup as ks
from selenium import webdriver
from selenium_stealth import stealth
import datetime
import sqlite3

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



prefecture = [ ('Hokkaido','Japan-p23937'),
               ('Fukuoka','Japan-p22652'),
               ('Chiba','Japan-p23829'),
               ('Kyoto','Japan-p22451'),
               ('Yamanashi','Japan-p22147'),
               ('Aichi','Japan-p22694'),
               ('Nagano','Japan-p22398'),
               ('Gifu','Japan-p22644'),
               ('Kanagawa','Japan-p22524'),
               ('Shizuoka','Japan-p22266')
            ]

delta = datetime.timedelta(days=1)

for p in prefecture:
    start_date = datetime.date(2025, 12, 1)
    end_date = datetime.date(2026, 1, 1)
    while (start_date <= end_date):
        next_date = start_date+delta
        ks.get_hotel_data(driver, p, [start_date,next_date])
        start_date += delta

driver.quit()
