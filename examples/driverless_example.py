from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from browser_use import Browser
import asyncio

class DriverlessBrowser(Browser):
    async def initialize_browser(self):
        """Initialize the driverless browser"""
        self.driver = await webdriver.Chrome().start()
        return self.driver

    async def get_page_source(self):
        """Get the page source using driverless selenium"""
        return await self.driver.get_page_source()
    
    async def get_element_by_selector(self, selector):
        """Get element using driverless selenium"""
        return await self.driver.find_element(By.CSS_SELECTOR, selector)

async def main():
    # Initialize the browser
    browser = DriverlessBrowser()
    await browser.initialize_browser()
    
    # Example usage
    try:
        # Navigate to a page
        await browser.driver.get("https://example.com")
        
        # Get the page content
        page_content = await browser.get_page_source()
        print("Page content retrieved successfully")
        
        # Find and interact with elements
        element = await browser.get_element_by_selector("h1")
        text = await element.text
        print(f"Found header text: {text}")
        
        # You can add more browser-use functionality here
        
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Clean up
        await browser.driver.quit()

if __name__ == "__main__":
    asyncio.run(main())