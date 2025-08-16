# Import required libraries
from seleniumbase import Driver
import time
from bs4 import BeautifulSoup
import pandas as pd
from processor import single_match_data_scrap

# Declare constants and variables
headers = ["date", "league", "country", "home_team", "away_team", "full_time_home_goals", "full_time_away_goals",
           "full_time_home_corners", "full_time_away_corners", "half_time_home_corners", "half_time_away_corners", "match_id"]
crawled_data = []
# Country Name for which we want to scrap the data
country_names_to_scrap = ["Argentina", "Brazil"]
# Dynamic Dates which we can use to scrap from smaller to higher as it is uses as paging filter
dates_to_scrap = ['03/30', '03/31', '04/01']
# Could be dynamic here kept as static
year = '2025'

###
# Page hierarchy is Continent -> Country -> League
# So while scraping also we are following same path

try:
    # Load the Continent data page and get all the list of countries listed
    driver = Driver(uc=True)
    url = "https://www.totalcorner.com/league/continent/5"
    driver.uc_open_with_reconnect(url, 4)
    time.sleep(20)
    html = driver.page_source
    # Parse and extract data
    soup = BeautifulSoup(html, 'html.parser')
    country_rows = soup.find(
        "ul", class_='nav nav-pills league-nav').find_all("li")
    country_level_data = []

    for row in country_rows:
        league_name = row.text.strip()
        link_tag = row.find("a")
        league_link = "https://www.totalcorner.com" + \
            link_tag["href"] if link_tag else ""
        if league_name == "":
            continue
        country_level_data.append(
            {"country_name": league_name, "page_link": league_link})

    # Process all country data and get list of leagues
    for leagues_countries in country_level_data:
        country = leagues_countries["country_name"]
        link = leagues_countries["page_link"]
        if country in country_names_to_scrap:
            print(f"Getting Leagues and URL for {country} -> {link}")
            time.sleep(10)
            # Going inside to get over all leagues present
            driver.get(link)
            internal_leagues = driver.page_source
            soup = BeautifulSoup(internal_leagues, 'html.parser')
            leagues_rows = soup.find(
                "ul", class_='nav nav-pills league-nav').find_all("li")
            total_leagues = []

            # Scrap each leauge page data
            for leauge in leagues_rows:
                league_name = leauge.text.strip()
                link_tag = leauge.find("a")
                league_link = "https://www.totalcorner.com" + \
                    link_tag["href"] if link_tag else ""
                if league_name == "":
                    continue
                # total_leagues.append(
                #     {"league": league_name, "league_link": league_link})

                # Crawl Data for each league
                recursive_flag = True
                page_no = 1
                try:
                    while recursive_flag:
                        print(
                            f"\nRunning for league {league_name} with URL {league_link}")
                        time.sleep(4)
                        driver.get(league_link+f'/page:{page_no}')

                        # Adding wait as it might be blocked for frequent request
                        time.sleep(4)
                        leagues_html = driver.page_source
                        league_data, recursive_flag = single_match_data_scrap(
                            leagues_html, league=league_name, country=country, dates_to_scrap=dates_to_scrap)
                        if len(league_data) > 0:
                            crawled_data.extend(league_data)
                        page_no += 1
                except Exception as e:
                    print(
                        "Failed for league {league_name} with URL {league_link}, moving ahead with next page")

    # Storing Extracted data
    df = pd.DataFrame(crawled_data, columns=headers)
    df.to_csv("data/scrapped_data.csv")

except Exception as e:
    print(e)
