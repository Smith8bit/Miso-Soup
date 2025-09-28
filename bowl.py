import soup
import sqlite3

hot_soup = soup.get_a_thing_done(3,"https://www.kayak.com/hotels/Tokyo,Tokyo-Prefecture,Japan-c21033/2026-01-01/2026-01-02/1adults")

# conn = sqlite3.connect("littledb.db")
# cur = conn.cursor()

print(hot_soup)
print(len(hot_soup))