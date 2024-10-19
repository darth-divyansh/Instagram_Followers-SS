import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager as CM
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service

def save_credentials(username, password):
    with open('credentials.txt', 'w') as file:
        file.write(f"{username}\n{password}")

def load_credentials():
    if not os.path.exists('credentials.txt'):
        return None

    with open('credentials.txt', 'r') as file:
        lines = file.readlines()
        if len(lines) >= 2:
            return lines[0].strip(), lines[1].strip()

    return None

def prompt_credentials():
    username = input("Enter your Instagram username: ")
    password = input("Enter your Instagram password: ")
    save_credentials(username, password)
    return username, password

def login(bot, username, password):
    bot.get('https://www.instagram.com/accounts/login/')
    time.sleep(1)

    # Check if cookies need to be accepted
    try:
        element = bot.find_element(By.XPATH, "/html/body/div[4]/div/div/div[3]/div[2]/button")
        element.click()
    except NoSuchElementException:
        print("[Info] - Instagram did not require to accept cookies this time.")

    print("[Info] - Logging in...")
    username_input = WebDriverWait(bot, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
    time.sleep(5)
    password_input = WebDriverWait(bot, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))
    time.sleep(5)
    username_input.clear()
    username_input.send_keys(username)
    password_input.clear()
    password_input.send_keys(password)

    login_button = WebDriverWait(bot, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
    login_button.click()
    time.sleep(10)

def scrape_followers(bot, username, user_input):
    bot.get(f'https://www.instagram.com/{username}/')
    time.sleep(3.5)
    WebDriverWait(bot, TIMEOUT).until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/followers')]"))).click()
    time.sleep(4)
    print(f"[Info] - Scraping followers for {username}...")

    # Create a folder with the name of the target username
    screenshots_folder = f'{username}_followers'
    os.makedirs(screenshots_folder, exist_ok=True)

    screenshots_taken = 0

    while screenshots_taken < user_input:
        # Take a screenshot of the visible followers list
        screenshot_filename = os.path.join(screenshots_folder, f'{username}_followers_screenshot_{screenshots_taken + 1}.png')
        bot.save_screenshot(screenshot_filename)
        print(f"[Info] - Screenshot saved as {screenshot_filename}")
        
        # Scroll down to reveal more followers
        ActionChains(bot).send_keys(Keys.END).perform()
        time.sleep(1)  # Adjust the sleep time if necessary to allow content to load
        screenshots_taken += 1

def scrape():
    credentials = load_credentials()

    if credentials is None:
        username, password = prompt_credentials()
    else:
        username, password = credentials

    user_input = int(input('[Required] - How many screenshots do you want to take (1-100 recommended): '))

    usernames = input("Enter the Instagram usernames you want to scrape (separated by commas): ").split(",")

    service = Service(executable_path=CM().install())
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument('--no-sandbox')
    options.add_argument("--log-level=3")
    mobile_emulation = {
        "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/90.0.1025.166 Mobile Safari/535.19"}
    options.add_experimental_option("mobileEmulation", mobile_emulation)

    bot = webdriver.Chrome(service=service, options=options)
    bot.set_page_load_timeout(5)  # Set the page load timeout to 15 seconds

    login(bot, username, password)

    for user in usernames:
        user = user.strip()
        scrape_followers(bot, user, user_input)

    bot.quit()

if __name__ == '__main__':
    TIMEOUT = 15
    scrape()
