from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
import time


def get_paraphrase(text):
    website = 'https://www.paraphrase-online.com/'
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    options.add_argument('--incognito')
    options.add_argument('--ignore-certificate-errors')
    # driver = webdriver.Firefox(GeckoDriverManager().install(), firefox_options=options)
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=options)
    driver.get(website)
    time.sleep(2)
    in_field = driver.find_element_by_id('field1')
    in_field.send_keys(text)
    loader = driver.find_element_by_id('synonym')
    loader.click()
    paraphrase = ''
    i = 0
    while i < 15:
        time.sleep(1)
        i += 1
        out_field = driver.find_element_by_id('field2')
        paraphrase = out_field.text
        if paraphrase:
            break
    driver.close()
    return paraphrase

# if __name__ == '__main__':
#     x = get_paraphrase('Hey what is up?')
#     print(x)
