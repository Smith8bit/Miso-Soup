from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
# options.add_argument("--headless") # Can be enabled for running without a visible browser window
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options=options)

# Apply stealth settings to make the browser appear more like a regular user
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
wait = WebDriverWait(driver, 15) # Increased wait time slightly for network variance

# Define the number of pages you want to scrape
PAGES_TO_SCRAPE = 5 

for page in range(PAGES_TO_SCRAPE):
    print(f"\n--- Scraping Page {page + 1} ---")
    try:
        # 1. Wait for the main container of hotel results to be present and get all hotel "cards"
        hotel_cards = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'c71z4')))
        
        # 2. Loop through each hotel card individually
        for card in hotel_cards:
            name, rating, price, location = 'N/A', 'N/A', 'N/A', 'N/A' # Default values
            
            # 3. Use try-except blocks to safely extract data from each card
            try:
                name = card.find_element(By.CLASS_NAME, 'c9Hnq-hotel-name').text
            except NoSuchElementException:
                pass # Name not found, will keep 'N/A'
                
            try:
                rating = card.find_element(By.XPATH, ".//div[contains(@class, 'Dp6Q')]").text
            except NoSuchElementException:
                pass # Rating not found
                
            try:
                # Price is often within a div with a specific class structure
                price = card.find_element(By.XPATH, ".//div[contains(@class, 'c1XBO')]").text
            except NoSuchElementException:
                pass # Price not found
                
            try:
                location = card.find_element(By.XPATH, ".//div[contains(@class, 'upS4')]").text
            except NoSuchElementException:
                pass # Location not found
            
            # Only add to the list if a name was found
            if name != 'N/A' and name not in hotel_list:
                hotel_list[name] = [rating, price, location]
                print(f"Found: {name} - {price}")

        # --- Pagination Logic ---
        # 4. Find the 'Next page' button and prepare to wait for the old content to disappear
        next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Next page']")))
        
        # Store a reference to the first hotel card on the current page
        first_hotel_on_page = hotel_cards[0]
        
        # Click the button to go to the next page
        next_button.click()
        
        # 5. Wait for the first hotel card from the *previous* page to become "stale" (disappear)
        # This confirms the new page has loaded.
        wait.until(EC.staleness_of(first_hotel_on_page))
        
    except TimeoutException:
        print("Reached the last page or content did not load in time.")
        break
    except Exception as e:
        print(f"An error occurred: {e}")
        break

print("\n--- Scraping Complete ---")
for name, details in hotel_list.items():
    print(f"Hotel: {name}\n  Rating: {details[0]}\n  Price: {details[1]}\n  Location: {details[2]}\n")

driver.quit()