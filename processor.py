from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime


def single_match_data_scrap(html, league, country, dates_to_scrap):
    soup = BeautifulSoup(html, 'html.parser')
    tables = soup.find('div', class_='col-sm-10').find_all("table")

    if len(tables) >= 2:
        second_table = tables[1]  # Access the second table (index 1)

        league_data = []
        tbody = second_table.find('tbody')
        if tbody:
            for row in tbody.find_all('tr'):
                row_data = []
                table_data = row.find_all('td')
                # Skip the row with Month Name
                if len(table_data) < 2:
                    processing_year = table_data[0].text.strip().split(" ")[1]
                    if int(processing_year) < 2025:
                        print(
                            f"Exiting as year has changed, records added are {len(league_data)}")
                        return league_data, False
                    else:
                        continue
                start_time = table_data[0].text.strip()
                row_date = start_time.split(' ')[0]
                row_time = start_time.split(' ')[1]
                if start_time.split(' ')[0] in dates_to_scrap:
                    # Format date for data
                    start_date = f'2025/{row_date} {row_time}'
                    start_time_format = "%Y/%m/%d %H:%M"
                    start_time = datetime.strptime(
                        start_date, start_time_format)
                    row_data.append(str(start_time))
                    # league
                    row_data.append(league)
                    # country
                    row_data.append(country)
                    # Home Team
                    row_data.append(table_data[2].text.strip())
                    # Away Team
                    row_data.append(table_data[4].text.strip())
                    # Full Time Home Goals
                    row_data.append(table_data[3].text.split('-')[0].strip())
                    # Full Time Away Goals
                    row_data.append(table_data[3].text.split('-')[1].strip())
                    # Full Time Home Corners
                    row_data.append(table_data[6].text.split('-')[0].strip())
                    # Full Time Away Corners
                    row_data.append(table_data[6].text.split('-')[1].strip())
                    # Half Time Home Corners
                    row_data.append(table_data[7].text.split('-')[0].strip())
                    # Half Time Away Corners
                    row_data.append(table_data[7].text.split('-')[1].strip())
                    # Match Id
                    match_id = table_data[-1].find(
                        'a').get('href').split('/')[-1]
                    row_data.append(match_id)

                    league_data.append(row_data)

            # Section to check if we need to move to next page next page
            current_page_last_row = tbody.find_all('tr')[-1].find('td')
            date_string_1 = current_page_last_row.text.split(" ")[0]
            date_string_2 = dates_to_scrap[1]
            date_format = "%m/%d"

            date_object_1 = datetime.strptime(date_string_1, date_format)
            date_object_2 = datetime.strptime(date_string_2, date_format)

            next_page_flag = (date_object_1 >= date_object_2)

        print("\nScraped Data:")
        for row in league_data:
            print(row)
        return league_data, next_page_flag

    else:
        print("There is no data available")
        return []


if __name__ == "__main__":
    with open("Argentina_cup_page.html", encoding='utf-8') as website_data:
        html = website_data.read()
    dates_to_scrap = ['03/30', '03/31', '04/01']
    single_match_data_scrap(
        html, league="Argentiana Cup", country="Argentiana", dates_to_scrap=dates_to_scrap)
