import unittest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
import os
import time
from xml.etree import ElementTree as ET
from bs4 import BeautifulSoup
import csv

# Define the desired capabilities for the Appium session
capabilities = dict(
    platformName='Android',
    automationName='UiAutomator2',
    deviceName='emulator-5554',  # Adjust as needed
    appPackage='com.application.zomato',
    appActivity='.routers.DeepLinkRouter',
    noReset=True  # Ensure the app is not reset
)

appium_server_url = 'http://localhost:4723'

class TestAppium(unittest.TestCase):
    def setUp(self) -> None:
        self.csv_file = open("/home/era/Desktop/Work/app_scrapper/zomato_offers.csv", "w+", newline='')
        self.csv_file1 = open("/home/era/Desktop/Work/app_scrapper/zomato_payment_coupons.csv", "w+", newline='')
        self.csv_writer2 = csv.writer(self.csv_file1)
        self.csv_writer2.writerow(["Discription", "Offer","Code"])
        self.csv_writer = csv.writer(self.csv_file)
        self.csv_writer.writerow(['Restaurant Name', 'Offer Type', 'Offer', 'Description', 'Code','selected dish'])
        # Initialize the driver and connect to Appium server
        self.driver = webdriver.Remote(appium_server_url, options=UiAutomator2Options().load_capabilities(capabilities))

    def tearDown(self) -> None:
        if self.csv_file:
            self.csv_file.close()
            self.csv_file1.close()
        # Do not close the session to keep it alive
        if self.driver:
            # Commented out to keep the session alive
            # self.driver.quit()
            pass

    def test_resto_brand_app(self) -> None:
        try:

            self.driver.press_keycode(3)
            self.driver.implicitly_wait(5)
            zomato_element = self.driver.find_element(AppiumBy.XPATH, '//android.widget.TextView[@text="Zomato"]')
            zomato_element.click()
            time.sleep(4)
            time.sleep(2)

            # location of brand packs
            # brand_pack.click()
            # self.driver.swipe(500, 2500, 500, 1000, 1000)
            time.sleep(1)
            
            self.driver.tap([(550, 2400)], 100)
            time.sleep(2)
            print("scrolling")
            scroll_count = 1
            scroll_count_selected_dish = 1
            for _ in range(scroll_count):
                self.driver.tap([(400, 1400)], 100)
                time.sleep(1)

                button = self.driver.find_element(AppiumBy.ID, 'com.application.zomato:id/right_button')
                button.click()
                
               
                try:
                    time.sleep(1)
                    page_source = self.driver.page_source
                    resto =  self.extract_resto_data(page_source)
                    time.sleep(1)
                    buttons2 = self.driver.find_element(AppiumBy.ID, 'com.application.zomato:id/subtitle2_button')
                    buttons2.click()
                    
                    for _ in range(scroll_count_selected_dish):
                        time.sleep(1)
                        page_source = self.driver.page_source
                        time.sleep(1)
                        dish = self.extract_dish_data(page_source)
                        resto.extend(dish)
                        self.driver.swipe(600, 2400, 600, 700, 1000)
                    self.csv_writer.writerow(resto)
                    self.driver.back()
                except:
                    print("No selected dish")
                    time.sleep(1)
                    page_source = self.driver.page_source
                    time.sleep(1)
                    resto =  self.extract_resto_data(page_source)
                    resto.extend([('N/A')])
                    self.csv_writer.writerow(resto)
                    self.driver.back()
                    time.sleep(1)
                    self.driver.back()
                    time.sleep(1)

                self.driver.tap([(1000, 1400)], 100)
                time.sleep(1)
                button = self.driver.find_element(AppiumBy.ID, 'com.application.zomato:id/right_button')
                button.click()
                
                try:
                    time.sleep(1)
                    page_source = self.driver.page_source
                    resto =  self.extract_resto_data(page_source)
                    time.sleep(1)
                    buttons2 = self.driver.find_element(AppiumBy.ID, 'com.application.zomato:id/subtitle2_button')
                    buttons2.click()
                    
                    for _ in range(scroll_count_selected_dish):
                        time.sleep(1)
                        page_source = self.driver.page_source
                        time.sleep(1)
                        dish = self.extract_dish_data(page_source)
                        resto.extend(dish)
                        self.driver.swipe(600, 2400, 600, 700, 1000)
                    self.csv_writer.writerow(resto)
                    self.driver.back()
                except:
                    print("No selected dish")
                    time.sleep(1)
                    page_source = self.driver.page_source
                    time.sleep(1)
                    resto =  self.extract_resto_data(page_source)
                    resto.extend([('N/A')])
                    self.csv_writer.writerow(resto)
                    self.driver.back()
                    time.sleep(1)
                    self.driver.back()
                    time.sleep(1)

                self.driver.swipe(350, 2000, 350, 1350, 1000)
            self.driver.implicitly_wait(2)
            print("Scrolled")
            self.driver.back()
            self.driver.back()
            self.driver.back()
        
            
        except Exception as e:
            print(f"An error occurred: {e}")

    def test_brand_pack(self) -> None:
        try:
            print("Brand pack")
            self.driver.press_keycode(3)
            self.driver.implicitly_wait(5)
            zomato_element = self.driver.find_element(AppiumBy.XPATH, '//android.widget.TextView[@text="Zomato"]')
            zomato_element.click()
            time.sleep(4)
            time.sleep(2)
            
            # self.driver.swipe(500, 2500, 500, 1000, 1000)
            time.sleep(1)
            
            self.driver.tap([(550, 2600)], 100)
            self.driver.swipe(350, 1800, 350, 1350, 900)
            scroll_count = 5
            for _ in range(scroll_count):
                page_source = self.driver.page_source
                self.extract_brand_pack(page_source)
                time.sleep(1)
                self.driver.swipe(350, 2600, 350, 600, 1000)
                time.sleep(1)
            
            
            
            self.driver.back()
            self.driver.back()
            self.driver.press_keycode(3)
            
        except Exception as e:
            print(f"An error occurred: {e}")

    def test_payment_coupons(self) -> None:
        try:
            
            self.driver.press_keycode(3)
            self.driver.implicitly_wait(5)
            zomato_element = self.driver.find_element(AppiumBy.XPATH, '//android.widget.TextView[@text="Zomato"]')
            zomato_element.click()
            time.sleep(4)
            time.sleep(2)
            self.driver.tap([(260, 1200)], 100)
            time.sleep(2)
            self.driver.swipe(350, 2000, 350, 1350, 1000)
            self.driver.swipe(350, 2000, 350, 1350, 1000)
            self.driver.swipe(350, 2000, 350, 1350, 1000)
            self.driver.swipe(350, 2000, 350, 1350, 1000)

            add_button = self.driver.find_element(AppiumBy.ID,"com.application.zomato:id/text_view_title")
            add_button.click()
            time.sleep(1)
            try:
                print("handling toppings")
                button_add_item = self.driver.find_element(AppiumBy.ID,"com.application.zomato:id/button" )
                button_add_item.click()
                time.sleep(1)
            except:
                print("No toppings")
            
            number_of_clicks = 5
            for _ in range(number_of_clicks):
                try:
                    print("handling add more")
                    add_more = self.driver.driver.find_element(AppiumBy.ID,"com.application.zomato:id/button_add")
                    add_more.click()
                    time.sleep(1)
                    try:
                        add_more = self.driver.driver.find_element(AppiumBy.ID,"com.application.zomato:id/button_add")
                        add_more.click()
                        time.sleep(1)
                        self.driver.back()
                    except:
                        print("No more add")
                except:
                    add_more = self.driver.find_element(AppiumBy.ID,"com.application.zomato:id/button_add")
                    add_more.click()
                    time.sleep(1)
            time.sleep(1)
            
            try:
                close_button = self.driver.find_element(AppiumBy.ID,"com.application.zomato:id/closeButton")
                close_button.click()
            except:
                print("No close button")
            
            
            
            self.driver.tap([(700,2800)], 100)
            time.sleep(1)
            self.driver.swipe(350, 2000, 350, 1350, 1000)
            time.sleep(1)
            
            
            
            element = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "View all payment coupons")
            element.click()
            time.sleep(2)
            
            data = []
            scroll_times = 6
            for _ in range(scroll_times):
                page_soucre = self.driver.page_source
                data1 = self.extract_payment_coupons(page_soucre)
                data.extend(data1)
                self.driver.swipe(350, 2500, 350, 1500, 1000)
                time.sleep(1)
            
            for d in data:
                self.csv_writer2.writerow(d)
            
            
            
            
            self.driver.back()
            self.driver.back()
            self.driver.press_keycode(3)
        except Exception as e:
            print(f"An error occurred: {e}")
    
    def test_invoice_loop(self) -> None:
        try:
            self.driver.press_keycode(3)
            self.driver.implicitly_wait(5)
            zomato_element = self.driver.find_element(AppiumBy.XPATH, '//android.widget.TextView[@text="Zomato"]')
            zomato_element.click()
            time.sleep(4)
            
            print("Selecting dish")
            self.select_dish()
            print("Dish selected")
            
            for _ in range(3):
                self.driver.swipe(350, 2000, 350, 350, 1000)
            
            time.sleep(2)
            

            add_button = self.driver.find_element(AppiumBy.ID,"com.application.zomato:id/text_view_title")
            add_button.click()
            time.sleep(1)
            try:
                print("handling toppings")
                button_add_item = self.driver.find_element(AppiumBy.ID,"com.application.zomato:id/button" )
                button_add_item.click()
                time.sleep(1)
            except:
                print("No toppings")
            
            time.sleep(1)
            self.driver.tap([(700,2800)], 100)
            time.sleep(1)
            
            number_of_clicks = 10
            for _ in range(number_of_clicks):
                try:
                    print("Invoice loop")
                    self.driver.swipe(350, 2000, 350, 1350, 1000)
                    self.driver.swipe(350, 2000, 350, 1350, 1000)
                    
                    Invoice_button = self.driver.find_element(AppiumBy.XPATH, "//android.widget.TextView[@text='Incl. taxes, charges & donation']")
                    location = Invoice_button.location
                    x = location['x']
                    y = location['y']
                    
                    self.driver.tap([(x, y)], 100)
                    time.sleep(1)
                    page_source = self.driver.page_source
                    with open('invoice_page.xml', 'w') as f:
                        f.write(page_source)
                    time.sleep(1)
                    self.driver.back()
                    time.sleep(1)
                    self.driver.swipe( 350, 1350, 350, 2000, 1000)
                    self.driver.swipe( 350, 1350, 350, 2000, 1000)
                    button_add_item = self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().resourceId("com.application.zomato:id/button_add")')
                    button_add_item.click()
                    time.sleep(5)
                except:
                    print("No more add")
            
            time.sleep(1)
            self.driver.back()
            self.driver.back()
            self.driver.press_keycode(3)
            time.sleep(1)
        except Exception as e:
            print(f"An error occurred: {e}")
    
    def extract_payment_coupons(self, page_source):
        return []
            
    def te1st_page_source(self) -> None:
        page_soucre = self.driver.page_source
        with open('brand_pack_page_source.xml', 'w') as f:
            f.write(page_soucre)
           
            
    def extract_resto_data(self, page_source):
        soup = BeautifulSoup(page_source, 'xml')

        # Find the root container
        root_container = soup.find('android.widget.FrameLayout', {'resource-id': 'com.application.zomato:id/root_container'})
        if not root_container:
            print("Root container not found.")
            return []

        # Extract the restaurant name
        title_element = root_container.find('android.widget.TextView', {'resource-id': 'com.application.zomato:id/title'})
        resto_name = title_element.get_text() if title_element else 'N/A'

        # Find all coupon elements
        coupon_elements = root_container.find_all('android.view.ViewGroup', {'checkable': 'false'})

        extracted_data = []
        
        for coupon in coupon_elements:
            offer_type = 'N/A'
            offer = 'N/A'
            description = 'N/A'
            code = 'N/A'

            # Determine the offer type and extract data accordingly
            title_element = coupon.find('android.widget.TextView', {'resource-id': 'com.application.zomato:id/title'})
            if title_element:
                offer = title_element.get_text()
                if "Brand Pack" in offer:  # You can adjust this check based on the actual content
                    offer_type = 'Brand Pack'
                else:
                    offer_type = 'Restaurant Coupon'

            # Extract description
            subtitle_element = coupon.find('android.view.View', {'resource-id': 'com.application.zomato:id/subtitle_view'})
            if subtitle_element:
                description = subtitle_element.get('content-desc')

            # Extract code if present
            code_element = coupon.find('android.widget.TextView', {'resource-id': 'com.application.zomato:id/subtitle2_tag_view'})
            if code_element:
                code = code_element.get_text()

            # If either offer or description is present, add it to the data list
            if offer != 'N/A' or description != 'N/A':
                data = {
                    "resto_name": resto_name,
                    "Offer Type": offer_type,
                    'Offer': offer,
                    'Description': description,
                    'Code': code
                }
                extracted_data.append([data['resto_name'], data['Offer Type'], data['Offer'], data['Description'], data['Code']])
        print(extracted_data)
        return extracted_data

    def extract_brand_pack(self, page_source):
        return []

    def extract_dish_data(self, page_source):
        soup = BeautifulSoup(page_source, 'xml')
        data = []

        # Find all root containers for dishes
        root_containers = soup.find_all('android.widget.LinearLayout', {'resource-id': 'com.application.zomato:id/root_container'}, limit=2)

        for container in root_containers:
            # Extract dish name
            dish_name_element = container.find('android.widget.TextView', {'resource-id': 'com.application.zomato:id/dish_name'})
            dish_name = dish_name_element.get_text() if dish_name_element else 'N/A'

            # Extract rating
            rating_element = container.find('android.widget.TextView', {'resource-id': 'com.application.zomato:id/ratingText'})
            rating = rating_element.get_text() if rating_element else 'N/A'

            # Extract final price
            price_element = container.find('android.widget.TextView', {'resource-id': 'com.application.zomato:id/dish_final_price'})
            price = price_element.get_text() if price_element else 'N/A'

            # Append the data tuple
            data.append((dish_name, rating, price))

        return data

    def select_dish(self):
        try:
            picking_dish = self.driver.find_element(AppiumBy.XPATH,  "//android.widget.TextView[@text='NEAR & FAST']")
            # picking_dish = self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().resourceId("com.application.zomato:id/ztag_text").text("NEAR &amp; FAST")')
            location = picking_dish.location
            print(location)
            x = location['x']
            y = location['y']
            self.driver.tap([(x, y)], 300)
        except:
            self.driver.swipe(350, 2000, 350, 1000, 1000)
            print("No near and fast")
            self.select_dish()
 
def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestAppium('test_invoice_loop'))
    # suite.addTest(TestAppium('test_page_source'))
    # suite.addTest(TestAppium('test_resto_brand_app'))
    # suite.addTest(TestAppium('test_payment_coupons'))
    # suite.addTest(TestAppium('test_brand_pack'))
    return suite


if __name__ == '__main__':
   runner = unittest.TextTestRunner()
   runner.run(suite())
    
    
