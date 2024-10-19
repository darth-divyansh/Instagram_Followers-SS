import streamlit as st
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

# Your existing functions
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

def login(bot, username, password):
    bot.get('https://www.instagram.com/accounts/login/')
    time.sleep(1)

    # Check if cookies need to be accepted
    try:
        element = bot.find_element(By.XPATH, "/html/body/div[4]/div/div/div[3]/div[2]/button")
        element.click()
    except NoSuchElementException:
        print("[Info] - Instagram did not require to accept cookies this time.")

    st.write("[Info] - Logging in...")
    username_input = WebDriverWait(bot, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
    password_input = WebDriverWait(bot, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))
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
    st.write(f"[Info] - Scraping followers for {username}...")

    # Create a folder with the name of the target username
    screenshots_folder = f'{username}_followers'
    os.makedirs(screenshots_folder, exist_ok=True)

    screenshots_taken = 0

    while screenshots_taken < user_input:
        # Take a screenshot of the visible followers list
        screenshot_filename = os.path.join(screenshots_folder, f'{username}_followers_screenshot_{screenshots_taken + 1}.png')
        bot.save_screenshot(screenshot_filename)
        st.write(f"[Info] - Screenshot saved as {screenshot_filename}")
        
        # Scroll down to reveal more followers
        ActionChains(bot).send_keys(Keys.END).perform()
        time.sleep(1)  # Adjust the sleep time if necessary to allow content to load
        screenshots_taken += 1

def scrape():
    st.title("Instagram Follower Scraper")

    username = st.text_input("Enter your Instagram username:")
    password = st.text_input("Enter your Instagram password:", type='password')
    user_input = st.number_input('[Required] - How many screenshots do you want to take (1-100 recommended):', min_value=1, max_value=100, value=5)
    
    usernames = st.text_input("Enter the Instagram usernames you want to scrape include the one you provided above (separated by commas):")
    st.write("**Note:** Other accounts from the one you provide with username and password need to be public.")
    if st.button("Start Scraping"):
        if username and password and usernames:
            usernames_list = usernames.split(",")

            service = Service(executable_path=CM().install())
            options = webdriver.ChromeOptions()
            options.add_argument('--no-sandbox')
            options.add_argument("--log-level=3")
            mobile_emulation = {
                "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/90.0.1025.166 Mobile Safari/535.19"}
            options.add_experimental_option("mobileEmulation", mobile_emulation)

            bot = webdriver.Chrome(service=service, options=options)
            bot.set_page_load_timeout(5)  # Set the page load timeout to 15 seconds

            login(bot, username, password)

            for user in usernames_list:
                user = user.strip()
                scrape_followers(bot, user, user_input)

            bot.quit()
        else:
            st.warning("Please fill in all fields before starting the scrape.")

if __name__ == '__main__':
    TIMEOUT = 15
    scrape()
