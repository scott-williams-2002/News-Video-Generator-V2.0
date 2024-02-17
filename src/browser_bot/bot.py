import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import random


def run_browser_bot(driver, min_delay, max_delay, max_images):
    def scroll_down(driver):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.randrange(min_delay, max_delay))

    image_urls = set()
    skips = 0

    while len(image_urls) + skips < max_images:
        scroll_down(driver)

        thumbnails = driver.find_elements(By.CSS_SELECTOR, '.rg_i, .Q4LuWd')
        for img in thumbnails[len(image_urls) + skips:max_images]:
            try:
                img.click()
                time.sleep(random.randrange(min_delay, max_delay))
            except:
                continue

            images = driver.find_elements(By.CSS_SELECTOR, '.r48jcc, .pT0Scc, .iPVvYb')
            for image in images:
                if image.get_attribute('src') in image_urls:
                    max_images += 1
                    skips += 1
                    break

                if image.get_attribute('src') and 'http' in image.get_attribute('src'):
                    image_urls.add(image.get_attribute('src'))
                    print(f"Found {len(image_urls)}")

    return list(image_urls)



def get_images_from_google(search_query, n_imgs):

    # Create a Chrome driver
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)

    # Open the Google Images search page with the provided search query
    search_url = f"https://www.google.com/search?q={search_query}&tbm=isch"
    driver.get(search_url)

    # Perform image scraping and downloading
    urls = run_browser_bot(driver, 2,10, n_imgs)  # between 2 and 10 second delay between grabbing n # of images
    return urls

