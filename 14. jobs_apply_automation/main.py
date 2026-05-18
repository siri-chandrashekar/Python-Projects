import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


def run_job_search():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    wait = WebDriverWait(driver, 20)

    try:
        driver.get("https://www.workingnomads.com/jobs?location=north-america&postedDate=1")
        driver.maximize_window()

        search_box = wait.until(EC.presence_of_element_located((By.ID, "q")))
        search_box.clear()
        search_box.send_keys("Python")
        search_box.send_keys(Keys.RETURN)

        posted_button = wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, "side-menu-postedDate"))
        )
        posted_button.click()

        today_option = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//label[text()='Today']"))
        )
        today_option.click()

        time.sleep(2)
        jobs = driver.find_elements(By.CLASS_NAME, "job-wrapper")
        print("Jobs found:", len(jobs))

        if not jobs:
            print("No jobs found for the current filter. Exiting safely.")
            return

        first_job = jobs[0]
        title_element = first_job.find_element(By.TAG_NAME, "h4")
        driver.execute_script("arguments[0].click();", title_element)

        apply_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "jd-apply-btn")))
        driver.execute_script("arguments[0].click();", apply_button)

        tabs = driver.window_handles
        if len(tabs) > 1:
            driver.switch_to.window(tabs[-1])

        input("Solve any verification/login, then press Enter here to close browser...")

    except TimeoutException as exc:
        print(f"Timed out waiting for page elements: {exc}")
    finally:
        driver.quit()


if __name__ == "__main__":
    run_job_search()
