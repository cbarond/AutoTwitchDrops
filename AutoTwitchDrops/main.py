"""
main.py file. run main.py.
"""
from time import sleep
import datetime

import settings
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def get_streamers() -> list:
    """
    Parse streamer names from streamers.txt into a list. streamers.txt must be newline separated streamer names. Just
    twitch names not url.
    :return: list of streamers
    """
    with open(settings.STREAMER_TEXT_FILE, "r", encoding="utf-8") as file:
        streamers = [streamer.rstrip() for streamer in file]
    return streamers

# TODO: Update log print statements to something better; Rich?
def main():
    """
    Main method. Opens browser tab for each streamer. Auto refreshes all tabs every settings.BROWSER_REFRESH_TIME
    seconds.
    :return: None
    """
    streamers: list = get_streamers()
    streamer_urls: list = [
        f"https://www.twitch.tv/{streamer}" for streamer in streamers
    ]

    # Setup WebDriver
    options = webdriver.ChromeOptions()
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
    # options.add_argument(f"--user-data-dir={settings.CHROME_PROFILE_PATH}") <- Deprecated syntax
    options.add_argument('--headless')
    options.add_argument("--mute-audio")
    options.add_argument(f"--user-data-dir={settings.CHROME_PROFILE_PATH}")
    options.add_argument(f"--profile-directory={settings.CHROME_PROFILE_NAME}")
    options.add_argument(f"--user-agent={user_agent}")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )

    print('\nDriver Loaded\n') # Log

    # Open every channel in streamers.txt
    for i, streamer_url in enumerate(streamer_urls):
        driver.get(streamer_url)

        # Click "Start Watching" on mature-audience channels
        try:
            button = driver.find_element(by=By.XPATH, value="//button[@data-a-target='player-overlay-mature-accept']")
            button.click()
        except:
            pass

        if i != len(streamer_urls) - 1:
            driver.execute_script("window.open('');")
            tabs = driver.window_handles
            driver.switch_to.window(tabs[-1])

        print(f'\n{streamer_url} Loaded\n') # Log
        
    window_tabs = driver.window_handles

    print('\nAll Streams Loaded\n') # Log

    # Cycle through tabs and refresh them
    while True:
        sleep(settings.BROWSER_REFRESH_TIME)
        for tab in window_tabs:
            driver.switch_to.window(tab)
            driver.refresh()
        
        print(f'\nStreams Refreshed at {datetime.datetime.now()}\n') # Log


if __name__ == "__main__":
    main()
