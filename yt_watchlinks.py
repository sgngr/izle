"""
================================================================
izle - mpv GUI for watching live streams and YouTube's channels
YouTube watchlinks module
================================================================
Version:    0.1
Author:     Sinan Güngör
License:    GPL v3
"""

import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By

from webdriver_manager.chrome import ChromeDriverManager
from requests import exceptions

import time


class WatchLink():
    def __init__(self, title=None, href=None):
        self.title = title
        self.href = href


def load_driver():
    driver = None
    desired_capabilities = DesiredCapabilities.CHROME
    desired_capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
    options = Options()
    options.add_argument("--headless=new")
    # options.add_argument("--ignore-certificate-errors")
    # options.add_argument("--ignore-ssl-errors")
    options.add_argument("--mute-audio")
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")

    print(time.strftime("%H:%M:%S", time.localtime()), "Loading web driver...")
    try:
        driver_path = ChromeDriverManager().install()
        print(time.strftime("%H:%M:%S", time.localtime()),
              "ChromeDriver > path:", driver_path)
    except exceptions.ConnectionError:
        print(time.strftime("%H:%M:%S", time.localtime()),
              "ChromeDriver > Connection error. Are you offline?")
        return driver
    except Exception:
        print(time.strftime("%H:%M:%S", time.localtime()),
              "ChromeDriver > Web driver error!")

    # Initialize the WebDriver service
    service = Service(driver_path)
    # Start WebDriver
    driver = webdriver.Chrome(service=service, options=options)
    print(time.strftime("%H:%M:%S", time.localtime()), "Web driver loaded.")

    # print("ChromeDriver > default_capabilities:", options.default_capabilities)
    # print("ChromeDriver > capabilities:", driver.capabilities)

    return driver


def download_page(driver, url):
    print(time.strftime("%H:%M:%S", time.localtime()), "Downloading page:", url)
    driver.get(url)  # put here your link

    # scroll page down
    old_position = 0
    new_position = None
    position_script = """return (window.pageYOffset !== undefined) ?
            window.pageYOffset : (document.documentElement ||
            document.body.parentNode || document.body);"""
    while new_position != old_position:
        old_position = driver.execute_script(position_script)
        print(time.strftime("%H:%M:%S", time.localtime()), "Scrolling down the page:", old_position)
        time.sleep(1)
        driver.execute_script(
            """var scrollingElement = (document.scrollingElement ||
            document.body);scrollingElement.scrollTop =
            scrollingElement.scrollHeight;""")
        new_position = driver.execute_script(position_script)
    source_page = driver.page_source
    return source_page


def get_yt_watchlinks(url, timeout, n):
    result = True
    videolinks = list()
    driver = load_driver()

    if driver is None:
        result = False
        return result, videolinks

    driver.set_page_load_timeout(timeout)

    print(time.strftime("%H:%M:%S", time.localtime()), f"Downloading: {url}")

    try:
        driver.get(url)
        print(time.strftime("%H:%M:%S", time.localtime()),
              f"Downloaded: {url}")
    except selenium.common.exceptions.TimeoutException:
        print(time.strftime("%H:%M:%S", time.localtime()), "Download timeout!")
    except Exception:
        print(time.strftime("%H:%M:%S", time.localtime()), "Download error!")
        result = False
        driver.quit()
        return result, videolinks

    try:
        elements = driver.find_elements(By.ID, "video-title-link")
        for element in elements:
            videolink = WatchLink(title=element.get_attribute("title"),
                                  href=element.get_attribute("href"))
            videolinks.append(videolink)
            if len(videolinks) == n:
                driver.quit()
                return result, videolinks
    except Exception:
        print(time.strftime("%H:%M:%S", time.localtime()),
              "No watchlink not found!")
        result = False
        driver.quit()
        return result, videolinks

    driver.quit()

    return result, videolinks


def get_yt_playlist(url, timeout, n):
    print(url, timeout, n)
    result = True
    videolinks = list()
    driver = load_driver()

    if driver is None:
        result = False
        return result, videolinks

    driver.set_page_load_timeout(timeout)

    print(time.strftime("%H:%M:%S", time.localtime()), f"Downloading: {url}")

    try:
        driver.get(url)
        print(time.strftime("%H:%M:%S", time.localtime()),
              f"Downloaded: {url}")
    except selenium.common.exceptions.TimeoutException:
        print(time.strftime("%H:%M:%S", time.localtime()), "Download timeout!")
    except Exception:
        print(time.strftime("%H:%M:%S", time.localtime()), "Download error!")
        result = False
        driver.quit()
        return result, videolinks

    try:
        elements = driver.find_elements(By.ID, "video-title")
        for element in elements:
            videolink = WatchLink(title=element.get_attribute("title"),
                                  href=element.get_attribute("href"))
            videolinks.append(videolink)
            if len(videolinks) == n:
                driver.quit()
                return result, videolinks
    except Exception:
        print(time.strftime("%H:%M:%S", time.localtime()),
              "No watchlink not found!")
        result = False
        driver.quit()
        return result, videolinks

    driver.quit()

    return result, videolinks


if __name__ == "__main__":

    import sys

    isPlaylist = False
    if len(sys.argv) > 2:
        if sys.argv[2] == "p":
            isPlaylist = True
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        # url = "https://www.youtube.com/foo/bar/videos"
        url = "https://www.youtube.com/foo/bar/streams"
        url = "https://www.youtube.com/playlist?list=..."

    timeout = 30
    maxlinks = 10
    if isPlaylist:
        result, watchlinks = get_yt_playlist(url, timeout, maxlinks)
    else:
        result, watchlinks = get_yt_watchlinks(url, timeout, maxlinks)

    print(result)

    for watchlink in watchlinks:
        print(f"{watchlink.title} ({watchlink.href})")
