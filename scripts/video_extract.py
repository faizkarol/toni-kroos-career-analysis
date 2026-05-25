import os
import time
import urllib.request
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920x1080")

# Initialize WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Function to download heatmaps
def download_heatmaps(player_url, save_folder):
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    # Navigate to the player's statistics page
    driver.get(player_url)
    time.sleep(5)  # Wait for the page to load

    # Step 1: Click on the "Statistics" tab
    try:
        stats_tab = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Statistics')]"))
        )
        stats_tab.click()
        time.sleep(5)  # Wait for Statistics tab to load
        print("Navigated to Statistics tab.")
    except Exception as e:
        print(f"Error navigating to Statistics tab: {e}")
        return

    # Step 2: Locate the dropdown container
    try:
        dropdown_container = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//div[@data-testid='tournament_season_selector']"))
        )
        print("Dropdown container located.")
    except Exception as e:
        print(f"Error locating dropdown container: {e}")
        return

    # Step 3: Click on dropdowns and fetch options
    try:
        # Click and fetch competition options
        competition_dropdown = dropdown_container.find_element(By.XPATH, ".//div[contains(@class, 'Box') and contains(text(), 'Competition')]")
        competition_dropdown.click()
        time.sleep(2)

        competition_options = driver.find_elements(By.XPATH, "//div[@data-testid='tournament_season_selector']//div[contains(@class, 'Box')]")
        competition_values = [comp.text for comp in competition_options]
        print(f"Competitions found: {competition_values}")
        competition_dropdown.click()  # Close competition dropdown

        # Click and fetch year options
        year_dropdown = dropdown_container.find_element(By.XPATH, ".//div[contains(@class, 'Box') and contains(text(), 'Year')]")
        year_dropdown.click()
        time.sleep(2)

        year_options = driver.find_elements(By.XPATH, "//div[@data-testid='tournament_season_selector']//div[contains(@class, 'Box')]")
        year_values = [year.text for year in year_options]
        print(f"Years found: {year_values}")
        year_dropdown.click()  # Close year dropdown
    except Exception as e:
        print(f"Error interacting with dropdowns: {e}")
        return

    # Step 4: Iterate through years and competitions to download heatmaps
    for year in year_values:
        for competition in competition_values:
            try:
                # Select year
                year_dropdown.click()
                time.sleep(1)
                year_option = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, f"//div[@data-testid='tournament_season_selector']//div[text()='{year}']"))
                )
                year_option.click()
                time.sleep(2)

                # Select competition
                competition_dropdown.click()
                time.sleep(1)
                competition_option = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, f"//div[@data-testid='tournament_season_selector']//div[text()='{competition}']"))
                )
                competition_option.click()
                time.sleep(2)

                # Locate and download heatmap
                heatmap = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//img[contains(@src, 'heatmap')]"))
                )
                src = heatmap.get_attribute("src")
                if src.startswith("http"):
                    image_file = os.path.join(save_folder, f"{year}_{competition.replace(' ', '_')}.png")
                    urllib.request.urlretrieve(src, image_file)
                    print(f"Downloaded heatmap for {year} - {competition}")
            except Exception as e:
                print(f"Error processing {year} - {competition}: {e}")

# Parameters
player_profile_url = "https://www.sofascore.com/player/toni-kroos/26502/statistics"
output_directory = "Toni_Kroos_Heatmaps"

# Run the script
download_heatmaps(player_profile_url, output_directory)

# Close WebDriver
driver.quit()
