import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import yt_dlp
import time
from langdetect import detect, DetectorFactory

# Ensure consistent language detection
DetectorFactory.seed = 0

# Ensure the download folder exists
DOWNLOAD_FOLDER = os.path.join(os.getcwd(), "videos")
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Function to detect English text
def is_english(text):
    try:
        return detect(text) == "en"
    except:
        return False

# Function to download YouTube videos using yt-dlp
def download_youtube_video(video_url, success_count):
    ydl_opts = {
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),  # Save as title.mp4
        'format': 'bestvideo+bestaudio/best',  # Download best quality
        'noplaylist': True,  # Avoid downloading playlists
    }
    try:
        print(f"Attempting to download YouTube video: {video_url}")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        print(f"Successfully downloaded: {video_url}")
        return success_count + 1
    except Exception as e:
        print(f"Error downloading YouTube video: {e}")
        return success_count

# Fetch YouTube videos and download them
def fetch_and_download_youtube(api_key, query, max_results=50):
    success_count = 0
    page_token = None

    while success_count < 20:  # Ensure at least 20 successful downloads
        base_url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            "part": "snippet",
            "q": query,
            "type": "video",
            "maxResults": max_results,
            "relevanceLanguage": "en",
            "pageToken": page_token,
            "key": api_key,
        }
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            videos = data.get("items", [])
            if not videos:
                print("No more videos found.")
                break
            for video in videos:
                video_title = video["snippet"]["title"]
                if is_english(video_title):
                    video_url = f'https://www.youtube.com/watch?v={video["id"]["videoId"]}'
                    success_count = download_youtube_video(video_url, success_count)
                    if success_count >= 20:
                        break
            page_token = data.get("nextPageToken")
        else:
            print(f"Error in YouTube API: {response.status_code}, {response.text}")
            break

# Function to download videos from Instagram or TikTok
def download_video(post_url, platform, success_count):
    driver = webdriver.Chrome()  # Ensure ChromeDriver is installed
    driver.get(post_url)
    time.sleep(5)  # Allow the page to load

    try:
        if platform == "TikTok":
            video_element = driver.find_element(By.TAG_NAME, "video")
            video_url = video_element.get_attribute("src")
        else:
            video_elements = driver.find_elements(By.TAG_NAME, "video")
            video_url = video_elements[0].get_attribute("src") if video_elements else None

        if video_url:
            print(f"Downloading {platform} video from {post_url}")
            video_data = requests.get(video_url).content
            filename = os.path.join(DOWNLOAD_FOLDER, f"{platform}_video_{success_count}.mp4")
            with open(filename, "wb") as file:
                file.write(video_data)
            print(f"Downloaded: {filename}")
            return success_count + 1
    except Exception as e:
        print(f"Error downloading {platform} video: {e}")
    finally:
        driver.quit()
    return success_count

# Scrape Instagram posts and download English videos
def fetch_and_download_instagram(query):
    success_count = 0
    driver = webdriver.Chrome()  # Ensure ChromeDriver is installed
    base_url = f"https://www.instagram.com/explore/tags/{query.replace(' ', '')}/"
    driver.get(base_url)
    time.sleep(5)

    try:
        post_links = driver.find_elements(By.CSS_SELECTOR, "a[href]")
        for link in post_links:
            if success_count >= 10:
                break
            post_url = link.get_attribute("href")
            if "/p/" in post_url:  # Ensure it's a post
                caption = driver.find_element(By.CSS_SELECTOR, "div.C4VMK").text
                if is_english(caption):
                    success_count = download_video(post_url, "Instagram", success_count)
    except Exception as e:
        print(f"Error scraping Instagram: {e}")
    finally:
        driver.quit()

# Scrape TikTok posts and download English videos
def fetch_and_download_tiktok(query):
    success_count = 0
    driver = webdriver.Chrome()  # Ensure ChromeDriver is installed
    base_url = f"https://www.tiktok.com/search?q={query.replace(' ', '%20')}"
    driver.get(base_url)
    time.sleep(5)

    try:
        post_links = driver.find_elements(By.CSS_SELECTOR, "a[href]")
        for link in post_links:
            if success_count >= 10:
                break
            post_url = link.get_attribute("href")
            if "tiktok.com" in post_url:
                title = driver.find_element(By.CSS_SELECTOR, ".tiktok-title-class").text
                if is_english(title):
                    success_count = download_video(post_url, "TikTok", success_count)
    except Exception as e:
        print(f"Error scraping TikTok: {e}")
    finally:
        driver.quit()

# Main Script
if __name__ == "__main__":
    query = "Toni Kroos interviews"
    api_key = "API_KEY"  # Replace with your valid YouTube API key

    print("Fetching and downloading YouTube videos...")
    fetch_and_download_youtube(api_key, query)

    print("\nFetching and downloading Instagram videos...")
    fetch_and_download_instagram(query)

    print("\nFetching and downloading TikTok videos...")
    fetch_and_download_tiktok(query)

    print(f"\nAll videos are saved in the folder: {DOWNLOAD_FOLDER}")
