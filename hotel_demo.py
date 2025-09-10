from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def main():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    wait = WebDriverWait(driver, 10)

    try:
        # Open a public demo site
        driver.get("https://www.adactin.com/HotelApp/")

        # Wait for login page and print title
        wait.until(EC.visibility_of_element_located((By.ID, "username")))
        print("Opened Hotel App demo site successfully!")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
