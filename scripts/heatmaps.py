import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains

class UnderstatScraper:
    def __init__(self, player_id):
        self.base_url = f"https://understat.com/player/{player_id}"
        self.driver = None
        self.output_dir = "understat_images"
        
    def setup_driver(self):
        """Initialize Chrome WebDriver with options"""
        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(options=options)
        
    def create_output_directory(self):
        """Create directory for saving images if it doesn't exist"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.output_dir = os.path.join(current_dir, "understat_images")
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            print(f"Created directory: {self.output_dir}")

    def wait_for_chart_load(self):
        """Wait for charts to fully load"""
        time.sleep(3)  # Increased wait time
        
    def select_filters(self, season=None, situation=None, result=None):
        """Select values in the dropdowns and wait for update"""
        try:
            # Season selection
            if season:
                season_dropdown = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "[name='scheme-season']"))
                )
                Select(season_dropdown).select_by_visible_text(season)
                time.sleep(2)

            # Situation selection
            if situation:
                situation_dropdown = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "[name='scheme-situation']"))
                )
                Select(situation_dropdown).select_by_visible_text(situation)
                time.sleep(2)

            # Result selection
            if result:
                result_dropdown = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "[name='scheme-result']"))
                )
                Select(result_dropdown).select_by_visible_text(result)
                time.sleep(2)

            self.wait_for_chart_load()
            
        except Exception as e:
            print(f"Error in filter selection: {str(e)}")

    def save_full_page_screenshot(self, filename):
        """Save full page screenshot"""
        try:
            filepath = os.path.join(self.output_dir, filename)
            self.driver.save_screenshot(filepath)
            print(f"Saved screenshot: {filepath}")
            return filepath
        except Exception as e:
            print(f"Error saving screenshot: {str(e)}")
            return None

    def save_element_screenshot(self, element, filename):
        """Save screenshot of specific element"""
        try:
            filepath = os.path.join(self.output_dir, filename)
            
            # Scroll element into view
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(1)
            
            # Take screenshot
            element.screenshot(filepath)
            print(f"Saved element screenshot: {filepath}")
            return filepath
        except Exception as e:
            print(f"Error saving element screenshot: {str(e)}")
            return None

    def scrape_player_stats(self):
        """Main method to scrape player stats and save visualizations"""
        try:
            self.setup_driver()
            self.create_output_directory()
            
            # Load the page
            print(f"Accessing URL: {self.base_url}")
            self.driver.get(self.base_url)
            time.sleep(5)  # Wait for initial page load
            
            # Get all seasons
            season_dropdown = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[name='scheme-season']"))
            )
            seasons = [option.text for option in Select(season_dropdown).options]
            
            data = []
            
            for season in seasons:
                print(f"\nProcessing season: {season}")
                
                # Select season
                self.select_filters(season=season)
                
                # Save shot map
                shot_map = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "scheme-block"))
                )
                shot_map_file = f"shotmap_{season.replace('/', '_')}.png"
                shot_map_path = self.save_element_screenshot(shot_map, shot_map_file)
                
                # Save radar chart if it exists
                try:
                    radar_chart = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, ".block-content:not(.filters)"))
                    )
                    radar_file = f"radar_{season.replace('/', '_')}.png"
                    radar_path = self.save_element_screenshot(radar_chart, radar_file)
                except:
                    radar_path = None
                    print(f"No radar chart found for season {season}")
                
                # Save full page for reference
                full_page_file = f"full_{season.replace('/', '_')}.png"
                full_page_path = self.save_full_page_screenshot(full_page_file)
                
                data.append({
                    'season': season,
                    'shot_map_file': shot_map_path,
                    'radar_chart_file': radar_path,
                    'full_page_file': full_page_path
                })
                
            return pd.DataFrame(data)
            
        except Exception as e:
            print(f"Error during scraping: {str(e)}")
            return None
            
        finally:
            if self.driver:
                self.driver.quit()
                
    def save_data(self, data, filename):
        """Save scraped data to CSV"""
        if isinstance(data, pd.DataFrame):
            filepath = os.path.join(self.output_dir, filename)
            data.to_csv(filepath, index=False)
            print(f"Data saved to {filepath}")