"""
================================================================
izle - mpv GUI for watching live streams and YouTube's channels
HLS module
================================================================
Version:    0.1
Author:     Sinan Güngör
License:    GPL v3
"""

import selenium
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from requests import exceptions

import time
import json


def get_m3u8_urls(url, timeout=1, duration=60):
    result = True
    url_list = list()

    # We set desired capabilities before setting driver options
    desired_capabilities = DesiredCapabilities.CHROME
    desired_capabilities["goog:loggingPrefs"] = {"performance": "ALL"}

    # Set up Chrome options
    options = Options()
    options.add_argument("--headless=new")
    # options.add_argument('--ignore-certificate-errors')
    # options.add_argument('--ignore-ssl-errors')
    options.add_argument("--mute-audio")

    print(time.strftime("%H:%M:%S", time.localtime()), "Loading web driver...")
    try:
        driver_path = ChromeDriverManager().install()
        print(time.strftime("%H:%M:%S", time.localtime()),
              "ChromeDriver > path:", driver_path)
    except exceptions.ConnectionError:
        print(time.strftime("%H:%M:%S", time.localtime()),
              "ChromeDriver > Connection error. Are you offline?")
        result = False
        return result, url_list
    except Exception:
        print(time.strftime("%H:%M:%S", time.localtime()),
              "ChromeDriver > Web driver error!")
        result = False
        return result, url_list

    print(time.strftime("%H:%M:%S", time.localtime()), "Web driver loaded.")

    # Initialize the WebDriver service
    service = Service(driver_path)
    # Start WebDriver
    driver = webdriver.Chrome(service=service, options=options)

    # print("ChromeDriver > default_capabilities:", options.default_capabilities)
    # print("ChromeDriver > capabilities:", driver.capabilities)

    driver.set_page_load_timeout(timeout)
    print(time.strftime("%H:%M:%S", time.localtime()), f"Downloading: {url}")

    try:
        driver.get(url)
        print(time.strftime("%H:%M:%S", time.localtime()),
              f"{url} downloaded.")
    except selenium.common.exceptions.TimeoutException:
        print(time.strftime("%H:%M:%S", time.localtime()), "Download timeout!")
    except Exception:
        print(time.strftime("%H:%M:%S", time.localtime()), "Download error!")
        result = False
        driver.quit()
        return result, url_list

    try:
        start_time = time.time()
        urls = set()
        print(time.strftime("%H:%M:%S", time.localtime()),
              f"Capturing network logs for {duration} seconds...")
        while time.time() - start_time < duration:
            logs = driver.get_log('performance')
            for entry in logs:
                log = json.loads(entry['message'])['message']
                if log['method'] == 'Network.responseReceived':
                    log_type = log['params']['type']
                    if log_type == 'XHR':
                        response = log['params']['response']
                        if 'url' in response:
                            url = response['url']
                            if not url.startswith("data:") and not url.startswith("blob:"):
                                if ".m3u8" in url:
                                    urls.add(url)
            time.sleep(1)
        url_list = list(urls)
    finally:
        driver.quit()

    n = len(url_list)
    if n > 0:
        print(time.strftime("%H:%M:%S", time.localtime()),
              f"{n} m3u8 playlist link found.")
    else:
        print(time.strftime("%H:%M:%S", time.localtime()),
              "No m3u8 playlist link found.")

    return result, url_list


if __name__ == "__main__":
    url = "https://foobar.tv/live"
    result, url_list = get_m3u8_urls(url, timeout=5, duration=10)
    for url in url_list:
        print(url)
