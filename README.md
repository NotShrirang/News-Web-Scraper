# News Web Scraper

This Python script is designed to scrape news data from Google, Yahoo, and Bing search engines for a list of companies. The scraped data is then saved into a CSV file.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [License](#license)

## Prerequisites

- Python 3.x
- Required Python libraries (install via `pip install -r requirements.txt`):
  - `pandas`
  - `bs4` (Beautiful Soup)
  - `requests`
  - `tqdm`

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/NotShrirang/News-Web-Scraper.git
    ```

2. Navigate to the project directory:

    ```bash
    cd News-Web-Scraper
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Edit the `config.json` file to configure the companies, keywords, and search engines.

2. Run the main script:

    ```bash
    python main.py
    ```

3. The scraped data will be saved as `output.csv` in the project directory.

## Configuration

- **config.json**: This file contains the configuration for the script. It includes the list of companies, keywords, search engines, and other parameters.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
