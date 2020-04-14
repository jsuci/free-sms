from selenium import webdriver
from time import sleep


def send_sms():

    def check_element(driver):
        return driver.find_element_by_xpath(
            "//*[contains(text(), 'Just a moment...')]")

    who = input("Enter 1 to text A.Love\n"
                "Enter 2 to text Mama\n"
                "Enter 3 to text other phone #: ")

    if who == "1":
        phone = "9754294748"
    elif who == "2":
        phone = "9758442963"
    else:
        phone = input("Enter 10-digit phone #: ")

    message = input("Enter message: ")

    options = webdriver.ChromeOptions()
    options.add_argument("window-size=650,400")

    driver = webdriver.Chrome("chromedriver.exe", options=options)
    driver.get("http://www.afreesms.com/intl/philippines")

    # WebDriverWait(driver, timeout=60).until_not(check_element)

    enter_phone = driver.find_element_by_xpath(
        "//td[@colspan=2]//input[2][@type='text']")
    enter_message = driver.find_element_by_xpath(
        "//textarea")
    enter_code = driver.find_element_by_xpath(
        "//input[@autocomplete]")

    enter_phone.send_keys(phone)
    enter_message.send_keys(message)

    driver.execute_script("window.stop();")
    driver.execute_script("window.scrollTo(0, 700);")

    code = input("Enter code: ")
    enter_code.send_keys(code)

    sleep(3)

    submit = driver.find_element_by_xpath(
        "//input[@type='submit']")

    submit.click()

    sleep(5)


def main():
    send_sms()


if __name__ == "__main__":
    main()
