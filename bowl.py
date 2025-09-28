import soup

for day in range(1,31):
    hot_soup = soup.get_hotel_data(1, day)
    print(f"Day{day} success")