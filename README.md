# Instagram Followers Scraper

This project is an **Instagram Followers Scraper** built using `Selenium` and Python. It automates the process of logging into Instagram, visiting user profiles, and taking screenshots of their followers list. The script supports scraping multiple users and saves screenshots of followers lists into corresponding folders for each target user.

## Features

- **Automatic Instagram login**: Saves and loads your Instagram credentials from a local `credentials.txt` file.
- **Followers Scraper**: Automates taking screenshots of a user's followers list and saves them to separate folders named after the target users.
- **Headless browser option**: The script is set up for headless scraping (though currently disabled).
- **Custom screenshot count**: Allows users to specify how many screenshots to take.

## Requirements

- Python 3.6+
- Google Chrome browser installed
- The following Python packages:

  - `selenium`
  - `webdriver-manager`

## Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/darth-divyansh/Instagram_Followers-SS.git
    cd Instagram_Followers-SS

    ```

2. **Install dependencies**:

    Install the required dependencies using `pip`:

    ```bash
    pip install -r requirements.txt
    ```

    The `requirements.txt` should include:
    
    ```txt
    selenium
    webdriver-manager
    ```

3. **Setup ChromeDriver**:

    The script automatically installs the latest version of `ChromeDriver` using `webdriver-manager`. Ensure that you have Google Chrome installed.

4. **Run the script**:

    ```bash
    python instagram_scraper.py
    ```

## Usage

1. **Enter Instagram Credentials**:

   - If running the script for the first time, you will be prompted to enter your Instagram username and password.
   - These credentials will be saved to a `credentials.txt` file for future use.

2. **Specify Screenshot Count**:

   - You will be asked to specify how many screenshots you'd like to take per user.

3. **Enter Instagram Usernames**:

   - Provide the usernames of the Instagram profiles you'd like to scrape, separated by commas.

## Script Overview

- **`save_credentials(username, password)`**: Saves credentials in `credentials.txt`.
- **`load_credentials()`**: Loads saved credentials from the file.
- **`login(bot, username, password)`**: Logs into Instagram using the provided credentials.
- **`scrape_followers(bot, username, user_input)`**: Scrapes followers of the given Instagram user and takes screenshots.
- **`scrape()`**: Main function that loads credentials, logs into Instagram, and scrapes followers for all specified usernames.

## Important Notes

- **Instagram Rate Limits**: Be mindful of Instagram's rate limits to avoid getting temporarily banned for suspicious activity.
- **Login Issues**: If Instagram changes its login flow, you might need to update the login-related XPath or CSS Selectors.
- **Headless Mode**: The script is currently not running in headless mode for debugging purposes. You can uncomment the `options.add_argument("--headless")` line in the `scrape()` function to enable it.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

### Disclaimer

This script is for educational purposes only. Use it responsibly and avoid violating Instagram's terms of service. The developer is not responsible for any misuse.
