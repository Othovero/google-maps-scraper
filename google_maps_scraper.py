from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import json
import os
import urllib.parse
from datetime import datetime
import random

class GoogleMapsRestaurantScraper:
    def __init__(self):
        # Initialize Chrome WebDriver
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 15)  # Increased wait time
        self.location = None
        
    def random_delay(self, min_seconds=2, max_seconds=5):
        """Add a random delay between actions to seem more human-like"""
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)
        
    def search_restaurants(self, location):
        """Search for restaurants in the specified location"""
        self.location = location
        
        # Create the Google Maps local search URL
        base_url = "https://www.google.com/search"
        params = {
            'tbm': 'lcl',  # Local search results
            'q': f"Caribbean restaurants in {location}"
        }
        search_url = f"{base_url}?{urllib.parse.urlencode(params)}"
        
        # Navigate to the search URL
        self.driver.get(search_url)
        print("Waiting for page to load...")
        self.random_delay(4, 6)  # Longer initial wait
    
    def get_restaurant_details(self):
        """Get details for each restaurant in the search results"""
        restaurants = []
        current_page = 1
        
        while True:  # Keep going until no more pages are found
            try:
                print(f"\nProcessing page {current_page}")
                
                # Wait for restaurant listings to appear
                listings_container = self.wait.until(
                    EC.presence_of_element_located((By.CLASS_NAME, "rlfl__tls"))
                )
                
                # Then find all restaurant entries
                restaurant_listings = listings_container.find_elements(By.CSS_SELECTOR, ".rllt__details")
                print(f"Found {len(restaurant_listings)} restaurants on this page")
                
                for i, listing in enumerate(restaurant_listings):
                    try:
                        print(f"\nProcessing restaurant {i+1} on page {current_page}...")
                        
                        # Click on the listing to open details
                        listing.click()
                        self.random_delay(2, 4)  # Random delay after clicking
                        
                        # Extract restaurant information using the provided selectors
                        name = self.safe_get_text("h2.qrShPb")
                        website = self.safe_get_attribute("a.mI8Pwc", "href")
                        
                        # Try to get phone number from the data-phone-number attribute
                        phone_element = self.driver.find_element(By.CSS_SELECTOR, "[data-phone-number]")
                        phone = phone_element.get_attribute("data-phone-number") if phone_element else None
                        
                        # If no phone number found in data attribute, try the href method
                        if not phone:
                            phone_link = self.safe_get_attribute("a.Od1FEc", "href")
                            if phone_link and phone_link.startswith("tel:"):
                                phone = phone_link[4:]
                        
                        # Try to get address from the overview section using the correct selector
                        try:
                            print("Attempting to find address...")
                            # First try the specific address span
                            address_div = self.wait.until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, "div.zloOqf.PZPZlf"))
                            )
                            address = address_div.find_element(By.CSS_SELECTOR, "span.LrzXr").text
                            print(f"Found address: {address}")
                        except Exception as e1:
                            print(f"First address attempt failed: {str(e1)}")
                            try:
                                # Fallback to any element with data-dtype="d3ifr"
                                address_element = self.wait.until(
                                    EC.presence_of_element_located((By.CSS_SELECTOR, "[data-dtype='d3ifr']"))
                                )
                                address = address_element.find_element(By.CSS_SELECTOR, "span.LrzXr").text
                                print(f"Found address (fallback): {address}")
                            except Exception as e2:
                                print(f"Second address attempt failed: {str(e2)}")
                                try:
                                    # Try one more time with a different selector
                                    address = self.safe_get_text("div[data-local-attribute='d3adr'] span.LrzXr")
                                    if address:
                                        print(f"Found address (third attempt): {address}")
                                    else:
                                        address = None
                                        print("Could not find address using any method")
                                except Exception as e3:
                                    address = None
                                    print(f"All address attempts failed: {str(e3)}")
                        
                        restaurant_data = {
                            "name": name,
                            "website": website,
                            "phone": phone,
                            "address": address
                        }
                        
                        print(f"\nFound details for: {name}")
                        if website:
                            print(f"Website: {website}")
                        if phone:
                            print(f"Phone number: {phone}")
                        if address:
                            print(f"Address: {address}")
                        print("-" * 50)
                        restaurants.append(restaurant_data)
                        
                        # Click back or close the details panel if needed
                        try:
                            back_button = self.driver.find_element(By.CSS_SELECTOR, "button.VfPpkd-icon-button")
                            back_button.click()
                            self.random_delay(1, 3)  # Random delay after closing details
                        except:
                            print("Could not find back button, continuing...")
                        
                    except Exception as e:
                        print(f"Error processing restaurant: {str(e)}")
                        continue
                
                # Check if there's a next page
                try:
                    # Find all pagination links
                    pagination = self.driver.find_elements(By.CSS_SELECTOR, ".NKTSme a")
                    
                    # Look for the next page button
                    next_page = None
                    
                    # First try to find the next sequential page number
                    for page_link in pagination:
                        if page_link.text.strip() == str(current_page + 1):
                            next_page = page_link
                            break
                    
                    # If we didn't find the next sequential page, look for a "Next" button
                    if not next_page:
                        # Try to find a "Next" button or last number in pagination
                        for page_link in pagination:
                            # Check if this is the last visible page number
                            try:
                                page_num = int(page_link.text.strip())
                                if page_num > current_page:
                                    next_page = page_link
                            except ValueError:
                                continue
                    
                    if next_page:
                        next_page.click()
                        print(f"Moving to page {current_page + 1}")
                        current_page += 1
                        self.random_delay(3, 5)  # Longer delay between pages
                        
                        # After clicking, wait for the new results to load
                        self.wait.until(
                            EC.presence_of_element_located((By.CLASS_NAME, "rlfl__tls"))
                        )
                    else:
                        # Try to find and click "More results" button if it exists
                        try:
                            more_results = self.driver.find_element(By.CSS_SELECTOR, "[aria-label*='More results']")
                            more_results.click()
                            print("Clicked 'More results' button")
                            current_page += 1
                            self.random_delay(3, 5)
                        except:
                            print("No more pages or results found")
                            break
                        
                except Exception as e:
                    print(f"Error with pagination: {str(e)}")
                    break
                    
            except Exception as e:
                print(f"Error finding restaurant listings: {str(e)}")
                break
        
        return restaurants
    
    def safe_get_text(self, selector):
        """Safely get text from an element if it exists"""
        try:
            element = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
            return element.text
        except (NoSuchElementException, TimeoutException):
            print(f"Could not find element with selector: {selector}")
            return None
            
    def safe_get_attribute(self, selector, attribute):
        """Safely get attribute from an element if it exists"""
        try:
            element = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
            return element.get_attribute(attribute)
        except (NoSuchElementException, TimeoutException):
            print(f"Could not find element with selector: {selector}")
            return None
    
    def save_results(self, restaurants, filename=None):
        """Save scraped data to a JSON file"""
        if filename is None:
            # Create filename with location and timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            location_slug = self.location.lower().replace(" ", "_")
            filename = f"restaurants_{location_slug}_{timestamp}.json"
        
        # Create the full data structure
        data = {
            "location": self.location,
            "scrape_date": datetime.now().isoformat(),
            "total_restaurants": len(restaurants),
            "restaurants": restaurants
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
        print(f"Results saved to: {filename}")
    
    def close(self):
        """Close the browser"""
        self.driver.quit()

def main():
    # Create scraper instance
    scraper = GoogleMapsRestaurantScraper()
    
    try:
        # Ask if user wants to resume a previous session
        resume = input("Do you want to resume a previous session? (y/n): ").lower()
        
        locations = []
        completed_locations = []
        
        if resume.startswith('y'):
            # Try to load progress file
            try:
                with open('scraper_progress.json', 'r', encoding='utf-8') as f:
                    progress = json.load(f)
                    locations = progress.get('locations', [])
                    completed_locations = progress.get('completed', [])
                    
                    if not locations:
                        print("No pending locations found in progress file.")
                        return
                        
                    print(f"Resuming with {len(locations)} pending locations.")
                    print(f"Already completed: {', '.join(completed_locations) if completed_locations else 'None'}")
            except FileNotFoundError:
                print("No progress file found. Starting a new session.")
                resume = 'n'
            except Exception as e:
                print(f"Error loading progress file: {str(e)}")
                return
        
        if not resume.startswith('y'):
            # Ask user if they want to load locations from a file
            file_input = input("Do you want to load locations from a file? (y/n): ").lower()
            
            if file_input.startswith('y'):
                # Get locations from file
                filename = input("Enter the filename with locations (one location per line): ")
                try:
                    with open(filename, 'r', encoding='utf-8') as f:
                        locations = [line.strip() for line in f.readlines() if line.strip()]
                    print(f"Loaded {len(locations)} locations from {filename}")
                except Exception as e:
                    print(f"Error loading file: {str(e)}")
                    return
            else:
                # Get locations from user
                print("Enter locations to search (one per line, enter blank line when done):")
                while True:
                    location = input("Location (or press Enter to finish): ")
                    if not location:
                        break
                    locations.append(location)
        
        if not locations:
            print("No locations entered. Exiting.")
            return
        
        print(f"\nScraping restaurants for {len(locations)} locations...")
        
        # Save initial progress
        if not resume.startswith('y'):
            save_progress(locations, completed_locations)
        
        # Process each location
        for i, location in enumerate(locations):
            print(f"\n{'=' * 50}")
            print(f"Processing location {i+1}/{len(locations)}: {location}")
            print(f"{'=' * 50}\n")
            
            try:
                # Search for restaurants
                scraper.search_restaurants(location)
                
                # Get restaurant details
                restaurants = scraper.get_restaurant_details()
                
                # Save results
                scraper.save_results(restaurants)
                
                print(f"\nScraped {len(restaurants)} restaurants for {location}.")
                
                # Mark this location as completed
                completed_locations.append(location)
                
                # Remove from pending locations
                locations_left = [loc for loc in locations if loc not in completed_locations]
                
                # Save progress
                save_progress(locations_left, completed_locations)
                
                # Add a longer delay between processing different locations to avoid being blocked
                # Only add the delay if this is not the last location
                if i < len(locations) - 1:
                    delay = random.uniform(45, 120)  # Random delay between 45 and 120 seconds
                    print(f"Waiting {delay:.1f} seconds before processing the next location...")
                    time.sleep(delay)
            except Exception as e:
                print(f"Error processing location '{location}': {str(e)}")
                print("Saving progress and continuing with next location...")
                # Save progress even on error
                locations_left = [loc for loc in locations if loc not in completed_locations]
                save_progress(locations_left, completed_locations)
                continue
        
        print("\nAll locations have been processed!")
        
        # Clear progress file when complete
        try:
            os.remove('scraper_progress.json')
            print("Progress file cleared.")
        except:
            pass
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    
    finally:
        scraper.close()

def save_progress(pending_locations, completed_locations):
    """Save current progress to a file"""
    progress = {
        'locations': pending_locations,
        'completed': completed_locations,
        'timestamp': datetime.now().isoformat()
    }
    
    with open('scraper_progress.json', 'w', encoding='utf-8') as f:
        json.dump(progress, f, indent=2)
    
    print(f"Progress saved. {len(pending_locations)} locations pending, {len(completed_locations)} completed.")

if __name__ == "__main__":
    main() 