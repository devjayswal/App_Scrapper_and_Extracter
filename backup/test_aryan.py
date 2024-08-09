import unittest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
import os
import time
from xml.etree import ElementTree as ET
import csv
import pandas as pd
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
        self.driver = webdriver.Remote(appium_server_url, options=UiAutomator2Options().load_capabilities(capabilities))

    def tearDown(self) -> None:
        
        # Do not close the session to keep it alive
        if self.driver:
            # Commented out to keep the session alive
            # self.driver.quit()
            pass
    
    def extract_food_items(self,xml_string, offer_string):
        if xml_string==None:
            return "N/A"
        tree = ET.fromstring(xml_string)
        root = tree
        food_items = []
        cnt=0

        # Search for offer elements
        offer_elements = root.findall(".//android.widget.TextView[@text]")
        for i in offer_elements:
            if offer_string in i.get('text'):
              cnt+=1

        if cnt>0:
            food_elements = root.findall(".//android.widget.FrameLayout[@content-desc]")
            for food_name in food_elements:
                food_items.append(food_name.get('content-desc'))
            return list(set(food_items))
        else:
            return "N/A"

    def get_full_description(self,element):
        description_parts = []

        # Get main title
        title = element.find(".//android.view.View[@resource-id='com.application.zomato:id/title_view']")
        if title is not None:
            description_parts.append(title.get('content-desc'))

        # Get subtitle
        subtitle = element.find(".//android.view.View[@resource-id='com.application.zomato:id/subtitle_view']")
        if subtitle is not None:
            description_parts.append(subtitle.get('content-desc'))

        # Get additional info (e.g., "See items on offer")
        additional_info = element.find(".//android.widget.Button[@resource-id='com.application.zomato:id/subtitle2_button']")
        if additional_info is not None:
            description_parts.append(additional_info.get('text'))

        return " | ".join(filter(None, description_parts))

    def csv_json_main(self,p1,p2):

        # Parse the XML
        tree = ET.fromstring(p1)
        root = tree

        # Find the restaurant name
        for element in root.findall(".//android.widget.TextView"):
            if "Offers at" in element.get('text'):
                restaurant_name = element.get('text').replace('Offers at ', '')
                print(restaurant_name)
                break

        # Initialize a list to store the coupon data
        coupons = []

        # Find all ViewGroup elements that represent coupons
        coupon_elements = root.findall(".//android.view.ViewGroup[@clickable='true']")

        # Find all section titles
        section_titles = root.findall(".//android.view.ViewGroup/android.widget.TextView[@resource-id='com.application.zomato:id/title']")
        section_titles = [title.get('text') for title in section_titles]

        current_type = "Unknown"


        for element in coupon_elements:
            # Check if this element is preceded by a section title
            element_index = list(root.iter()).index(element)
            for title in section_titles:
                title_element = root.find(f".//android.widget.TextView[@text='{title}']")
                if title_element is not None:
                    title_index = list(root.iter()).index(title_element)
                    if title_index < element_index:
                        current_type = title

            description = self.get_full_description(element)
            # items
            itm= self.extract_food_items(p2,description.split('|')[0].strip())
            if itm:
                items=str(itm).strip("[ ']'").replace(",",'\n')  
            else:
                items="N/A"
            
                
                
            coupon_code = "N/A"
            code_element = element.find(".//android.widget.TextView[@resource-id='com.application.zomato:id/subtitle2_tag_view']")
            if code_element is not None:
                coupon_code = code_element.get('text')

            coupons.append({
            'restaurant_name': restaurant_name,
            'coupon_type': current_type,
            'coupon_code': coupon_code,
            'description': description,
            'items_with_offers_price': items
        })
            
        # Define the path to your CSV file
        csv_file = './restro_coupons.csv'

        # Try to load the existing DataFrame from the CSV

        try:
          df = pd.read_csv(csv_file)
        except FileNotFoundError:
          # If the CSV doesn't exist, create an empty DataFrame with the desired columns
             fieldnames = ['restaurant_name', 'coupon_type', 'coupon_code', 'description', 'items_with_offers_price']
             df = pd.DataFrame(columns=fieldnames)
             print("CSV file 'restro_coupons.csv' has been created successfully.")

        # Convert the new data into a DataFrame
        new_df = pd.DataFrame(coupons)

        # Append the new data to the existing DataFrame
        df = pd.concat([df, new_df], ignore_index=True)

        # Save the updated DataFrame back to the CSV file
        df.to_csv(csv_file, index=False)
           

        print("restro_coupons.csv updated")

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
            scroll_count = 5
            scroll_count_selected_dish = 1
            for _ in range(scroll_count):
                self.driver.tap([(400, 1400)], 100)
                time.sleep(1)

                button = self.driver.find_element(AppiumBy.ID, 'com.application.zomato:id/right_button')
                button.click()
                
               
                try:
                    time.sleep(1)
                    page_source = self.driver.page_source
                    p1=page_source
                    time.sleep(1)
                    buttons2 = self.driver.find_element(AppiumBy.ID, 'com.application.zomato:id/subtitle2_button')
                    buttons2.click()
                    
                    for _ in range(scroll_count_selected_dish):
                        time.sleep(1)
                        page_source = self.driver.page_source
                        time.sleep(1) 
                        p2=page_source
                        self.driver.swipe(600, 2400, 600, 700, 1000)
                    self.csv_json_main(p1,p2)    
                    self.driver.back()
                except:
                    print("No selected dish")
                    time.sleep(1)
                    page_source = self.driver.page_source
                    time.sleep(1)
                    p1=page_source
                    self.driver.back()
                    time.sleep(1)
                    self.driver.back()
                    time.sleep(1)
                    self.csv_json_main(p1,p2=None)

                self.driver.tap([(1000, 1400)], 100)
                time.sleep(1)
                button = self.driver.find_element(AppiumBy.ID, 'com.application.zomato:id/right_button')
                button.click()
                
                try:
                    time.sleep(1)
                    page_source = self.driver.page_source
                    p1=page_source
                    time.sleep(1)
                    buttons2 = self.driver.find_element(AppiumBy.ID, 'com.application.zomato:id/subtitle2_button')
                    buttons2.click()
                    
                    for _ in range(scroll_count_selected_dish):
                        time.sleep(1)
                        page_source = self.driver.page_source
                        time.sleep(1)
                        p2=page_source
                        self.driver.swipe(600, 2400, 600, 700, 1000)
                    self.csv_json_main(p1,p2)
                    self.driver.back()
                except:
                    print("No selected dish")
                    time.sleep(1)
                    page_source = self.driver.page_source
                    time.sleep(1)
                    p1=page_source
                    
                    self.driver.back()
                    time.sleep(1)
                    self.driver.back()
                    time.sleep(1)
                self.csv_json_main(p1,p2=None)
                self.driver.swipe(350, 2000, 350, 1350, 1000)
            self.driver.implicitly_wait(2)
            print("Scrolled")
            self.driver.back()
            self.driver.back()
            self.driver.back()
        
            
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
                self.extract_payment_coupons(page_source=page_soucre)
                self.driver.swipe(350, 2500, 350, 1500, 1000)
                time.sleep(1)
            
            self.driver.back()
            self.driver.back()
            self.driver.press_keycode(3)
        except Exception as e:
            print(f"An error occurred: {e}")
    
    def extract_payment_coupons(self, page_source):
        tree=ET.fromstring(page_source)
        root = tree
        payments_coupans = []
    
        offers_name_element=root.findall(".//android.widget.TextView[@resource-id='com.application.zomato:id/title']")
        offers_descriptions_element=root.findall(".//android.widget.TextView[@resource-id='com.application.zomato:id/subtitle']")
        offers_code_element=root.findall(".//android.widget.TextView[@resource-id='com.application.zomato:id/display_code_title']")
        offer_names=[]

        for i in offers_name_element:
            if i.get('text')!="BEST OFFERS FOR YOU":
                offer_names.append(i.get('text'))
            
        offers_descriptions=[]
        for i in offers_descriptions_element:
            offers_descriptions.append(i.get('text'))
            
        offers_codes=[]
        for i in offers_code_element:
            offers_codes.append(i.get('text'))
        

        for i in range(len(offer_names)-1):
            payments_coupans.append({
                'offer_names': offer_names[i],
                'offer_descriptions': offers_descriptions[i],
                'offer_codes': offers_codes[i]
            })
                
        # Define the path to your CSV file
        csv_file = './payment_coupons.csv'

        # Try to load the existing DataFrame from the CSV

        try:
            df = pd.read_csv(csv_file)
        except FileNotFoundError:
            # If the CSV doesn't exist, create an empty DataFrame with the desired columns
            fieldnames = ['offer_names','offer_descriptions','offer_codes']
            df = pd.DataFrame(columns=fieldnames)
            print("CSV file 'payments_coupans.csv' has been created successfully.")

        # Convert the new data into a DataFrame
        new_df = pd.DataFrame(payments_coupans)
        # Append the new data to the existing DataFrame
        df = pd.concat([df, new_df], ignore_index=True)
        # Remove duplicate rows based on all columns
        df = df.drop_duplicates()
        # Reset the index after removing duplicates
        df = df.reset_index(drop=True)
        # Save the updated DataFrame back to the CSV file
        df.to_csv(csv_file, index=False)
        print("payments_coupans.csv updated")
            
        
        
        
        
   
           
            
def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestAppium('test_resto_brand_app'))
    suite.addTest(TestAppium("test_payment_coupons"))
    
    return suite


if __name__ == '__main__':
   runner = unittest.TextTestRunner()
   runner.run(suite())
    
    
