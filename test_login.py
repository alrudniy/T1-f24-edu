from selenium import webdriver
from selenium.webdriver.common.by import By
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def test_invalid_login():
    driver = webdriver.Chrome() # Or webdriver.Firefox(), etc.  Make sure the driver executable is in your PATH.
    driver.get("http://localhost:5000/") # Replace with your app's URL

    username_field = driver.find_element(By.NAME, "username")
    password_field = driver.find_element(By.NAME, "password")
    submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")

    username_field.send_keys("invalid_user") # Or a known user with an incorrect password
    password_field.send_keys("wrong_password")
    submit_button.click()

    time.sleep(2) # Allow time for the flash message to appear

    error_message = driver.find_element(By.CLASS_NAME, "flash-error") # Assuming you use a 'flash-error' class for error messages
    assert error_message.is_displayed()
    assert "Invalid username or password" in error_message.text # Check for the specific error message
    try:
        # ... rest of your test code ...
    finally:
        driver.quit() # Close the browser window when the test is done, even if it fails
