# ⚽ Football Match Data Scraper and ETL Pipeline

This project is a simple yet effective data pipeline that scrapes football match statistics, processes the data, and stores it in a structured CSV format. It serves as a foundational data engineering portfolio project, showcasing skills in web scraping, data cleaning, and structured data storage.

This project scrapes football match data from totalcorner.com

Currently the code scrapes data as per below hierarchy is Continent -> Country -> League

For this requirement I had scraped specifically for America Continent(https://www.totalcorner.com/league/continent/5)

## As data is very large, we are only getting data for "Argentina", "Brazil". It is dynamic but, to reduce mutiple calls we are using only 2 countries.

## 🚀 Key Features

- **Web Scraping:** Uses **Beautiful Soup** to extract detailed football match data from a designated sports statistics website.
- **Data Processing:** Leverages the **Pandas** library for efficient data cleaning, transformation, and manipulation. The raw, messy HTML data is transformed into a clean, tabular format.
- **Local Data Storage:** The processed data is stored in a clean and organized `.csv` file, making it ready for direct use in analytics, visualization, or as a data source for more complex pipelines.
- **Modular Design:** The codebase is organized into logical components for scraping, cleaning, and saving, making it easy to understand and extend.

---

## 🛠️ Technologies Used

- **Python:** The core programming language for the entire project.
- **Beautiful Soup:** A Python library for parsing HTML and XML documents.
- **Pandas:** A powerful library for data manipulation and analysis.

---

## 📂 Project Structure

```
.
├── src/
│ Beautiful Soup
│   ├── processor.py           # Script for cleaning and transforming data with Pandas
│   └── main.py                # Main script to run the pipeline
├── data/
│   └── scrapped_data.csv   # The output CSV file (will be generated after running the script)
└── README.md                  # This file
```

---

## 📝 How to Run the Project

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/satishf889/football-match-data-processing.git
    cd football-match-data-processing
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```
3.  **Install the required libraries:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run the main script:**
    ```bash
    python src/main.py
    ```
    This script will execute the scraping and processing tasks. Upon successful completion, a `football_matches.csv` file will be created in the `data/` directory.

---

## 📈 Example Data Output

The final `football_matches.csv` file will have a clean, tabular structure similar to this:

| Match ID | Home Team | Away Team | Full Time Result | Home Team Goals | Away Team Goals | Possession (%) | Shots on Target |
| :------: | :-------: | :-------: | :--------------: | :-------------: | :-------------: | :------------: | :-------------: |
|   101    |  Team A   |  Team B   |     Home Win     |        3        |        1        |       55       |        6        |
|   102    |  Team C   |  Team D   |       Draw       |        2        |        2        |       48       |        4        |
|   103    |  Team E   |  Team F   |     Away Win     |        0        |        1        |       62       |        3        |
