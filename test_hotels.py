# test_hotels.py
import os
import pytest
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import logging
logger = logging.getLogger("hotel-tests")

# .env should contain:
# HOTEL_USERNAME=your_username
# HOTEL_PASSWORD=your_password
# HOTEL_LOCATIONS=Paris,Sydney,London
load_dotenv()
USERNAME = os.getenv("HOTEL_USERNAME", "").strip()
PASSWORD = os.getenv("HOTEL_PASSWORD", "").strip()
LOCATIONS = [x.strip() for x in os.getenv("HOTEL_LOCATIONS", "Paris").split(",") if x.strip()]

if not USERNAME or not PASSWORD:
    pytest.skip("HOTEL_USERNAME / HOTEL_PASSWORD not set in .env", allow_module_level=True)

@pytest.mark.parametrize("location", LOCATIONS)
def test_hotels_in_location(driver, location):
    wait = WebDriverWait(driver, 12)

    # Login
    driver.get("https://adactinhotelapp.com/index.php")
    wait.until(EC.visibility_of_element_located((By.NAME, "username"))).send_keys(USERNAME)
    driver.find_element(By.NAME, "password").send_keys(PASSWORD)
    wait.until(EC.element_to_be_clickable((By.ID, "login"))).click()

    # Search for location
    select = Select(wait.until(EC.visibility_of_element_located((By.ID, "location"))))
    select.select_by_visible_text(location)
    wait.until(EC.element_to_be_clickable((By.ID, "Submit"))).click()


    try:
        wait.until(EC.url_contains("SelectHotel"))
    except Exception:
        pass

    rows = wait.until(EC.presence_of_all_elements_located(
        (By.XPATH, "//input[@type='radio' and contains(@id,'radiobutton_')]/ancestor::tr")
    ))
    assert rows, f"No hotel rows found for {location}"

    # Extract and verify locations
    def row_location(row_el) -> str:
        hidden = row_el.find_elements(By.XPATH, ".//input[contains(@id,'location_')][@value]")
        if hidden:
            val = (hidden[0].get_attribute("value") or "").strip()
            if val:
                return val
        tds = row_el.find_elements(By.TAG_NAME, "td")
        if len(tds) >= 3:
            txt = (tds[2].text or "").strip()
            if txt:
                return txt
        return ""

    mismatches = []
    for i, row in enumerate(rows, start=1):
        actual = row_location(row)
        if actual != location:
            mismatches.append((i, actual))

    assert not mismatches, (
        "Some rows did not match the selected location:\n" +
        "\n".join([f"Row {idx}: expected '{location}', found '{act}'" for idx, act in mismatches])
    )
    logger.info("Verification passed for %s", location)
    print(f"Verification passed: All hotels are in {location}")

