import json
import os
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from urllib.parse import urlparse, urlunparse
from photodownload import download_google_drive_image

from read import read_data_from_sheet
print('Please make sure your sheet is shared with the given address: remote-kitchen-otterupload@remote-kitchen-otter-upload.iam.gserviceaccount.com')
url = input("Enter the url: ")

def extract_sheet_id(url):
    # Split the URL by slashes ('/') and get the second-to-last element (before 'edit')
    parts = url.split('/')
    sheet_id = parts[-2]

    return sheet_id

spread_sheet_id = extract_sheet_id(url)
print(f"Your given sheet id is: {spread_sheet_id}")
while True:

    want_update_version = input("Which version do you want to upload? v1/v2/v3: ")
    if want_update_version =='v1' or want_update_version =='v2' or want_update_version == 'v3':
        break
    else:
        print("Please choose a valid version")
while True:

    want_update_description = input("Do you want to update Description? y/n: ")
    if want_update_description =='y' or want_update_description =='n':
        break
    else:
        print("Please choose a valid answer")

while True:

    want_update_price = input("Do you want to update Price? y/n: ")
    if want_update_price =='y' or want_update_price =='n':
        break
    else:
        print("Please choose a valid answer")

while True:

    want_update_image = input("Do you want to update Image? y/n: ")
    if want_update_image =='y' or want_update_image =='n':
        break
    else:
        print("Please choose a valid answer")




brand_name = ''
all_category_names_from_sheet = None
product_name_colum = 0
product_desc_col = 0
product_price_col = 0
product_category_col = 0
image_url_col = 0
results, v1_name, v2_name, v3_name, v1_category_names, v2_category_names, v3_category_names = read_data_from_sheet(spread_sheet_id)
if want_update_version == "v1":
    brnd_name = v1_name
    all_category_names_from_sheet = v1_category_names
    product_name_colum = 1
    product_desc_col = 14
    product_price_col = 11
    product_category_col = 6
    image_url_col = 20
elif want_update_version == "v2":
    brand_name = v2_name
    all_category_names_from_sheet = v2_category_names
    product_name_colum = 2
    product_desc_col = 15
    product_price_col = 7
    image_url_col = 21
elif want_update_version == "v3":
    brand_name = v3_name
    all_category_names_from_sheet = v3_category_names
    product_name_colum = 3
    product_desc_col = 16
    product_price_col = 8
    image_url_col = 22


login_url = "https://manager.tryotter.com/login"
login_email = "bd@heyremotekitchen.com"
login_pass = 'OtterRemote123!'

caps = DesiredCapabilities.CHROME
caps['goog:loggingPrefs'] = {'performance': 'ALL'}
chrome_options = uc.ChromeOptions()
""" chrome_options.add_argument("--log-level=3")
chrome_options.add_argument("--headless")
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument("--no-sandbox") """
driver =  uc.Chrome(uc=True, desired_capabilities=caps, options=chrome_options, seleniumwire_options={})

driver.maximize_window()


driver.get(login_url)
time.sleep(10)


wait_timeout = 20
email_input = WebDriverWait(driver, wait_timeout).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="op-auth_email-field"]'))
)
print('sign in page loaded')
email_input = driver.find_element(By.CSS_SELECTOR, '[data-testid="op-auth_email-field"]')
email_input.send_keys(login_email)

password_input =WebDriverWait(driver, wait_timeout).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="op-auth_password-field"]'))
    
)
password_input = driver.find_element(By.CSS_SELECTOR, '[data-testid="op-auth_password-field"]')
password_input.send_keys(login_pass)

sign_in_button = driver.find_element(By.CSS_SELECTOR, '[data-testid="op-auth_login-button"]')
sign_in_button.click()
wait_timeout = 100
welcome_message = WebDriverWait(driver, wait_timeout).until(
    EC.visibility_of_element_located((By.XPATH, '//span[text()="Today\'s sales"]'))
)
print('You are logged in now')

driver.get('https://manager.tryotter.com/menus/brand')
search_box = WebDriverWait(driver, wait_timeout).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Search brands and menus"]'))
)
search_box = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Search brands and menus"]')
search_box.send_keys(brnd_name)
is_category = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/div/div[2]/div/div[3]/div[1]/div/div/div/div/div/div/div/div/div/div[2]/div/div/div/div/div/div/div[4]/div/div/div/div/div/div[1]/span')

if is_category:
    try:
        print("We found the Brand")
        is_category.click()
    except Exception as ex:
        print('nothing')

    Categories_button = WebDriverWait(driver, wait_timeout).until(
        EC.visibility_of_element_located((By.XPATH, f'//*[text()="Categories"]'))
    )


    Categories_button.click()
    all_existing_categories = []



    categoryElements = driver.find_elements(By.XPATH, '//div[@class="ReactVirtualized__Grid ReactVirtualized__List"]/div/div')
    for categoryElement in categoryElements:
        category_name = categoryElement.find_element(By.XPATH, './div/div/div[2]/div[1]/span').text
        all_existing_categories.append(category_name.title())



    for v2_category_name in all_category_names_from_sheet:

        if v2_category_name.title() not in all_existing_categories:
            add_category_button  =  WebDriverWait(driver, wait_timeout).until(EC.visibility_of_element_located((By.XPATH, f'//*[text()="Add category"]')))
            add_category_button.click()
            category_name_input = WebDriverWait(driver, wait_timeout).until(EC.visibility_of_element_located((By.XPATH, f'//input[@placeholder="Enter a category name"]')))
            category_name_input.clear()
            category_name_input.send_keys(v2_category_name)
            print(f'The category {v2_category_name} is updated now')
            save_button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//button[div[text()="Save"]]')))
            save_button.click()

    print('All categories ar synced')
    url = driver.current_url
    parsed_url = urlparse(url)

    # Check if the path of the URL contains '/categories'
    if "/categories" in parsed_url.path:
        # Remove '/categories' from the path
        new_path = parsed_url.path.replace("/categories", "")

        # Reconstruct the modified URL
        modified_url = urlunparse((parsed_url.scheme, parsed_url.netloc, new_path, parsed_url.params, parsed_url.query, parsed_url.fragment))
    else:
        # If '/categories' is not present, keep the original URL
        modified_url = url
    item_url = modified_url
    driver.get(item_url)
    for index, row in enumerate(results, start=1):
        if index>=5:
            product_name = row[product_name_colum]

            product_name= product_name.title()
            search_product = WebDriverWait(driver, wait_timeout).until(EC.visibility_of_element_located((By.XPATH, f'//input[@placeholder="Search items and categories"]')))
            search_product.clear()
            search_product.send_keys(product_name)
            product_description = row[product_desc_col]
            product_price = row[product_price_col]
            product_price = product_price.replace("$", '')
            product_category = row[product_category_col]
            product_category = product_category.title()
            overviewpage = driver.find_element(By.XPATH, '//div[@class="ReactVirtualized__Grid ReactVirtualized__List"]')
            print(f"Now we are working on {product_name}")
            try:
                driver.implicitly_wait(5)
                product_element = overviewpage.find_element(By.XPATH, f'//span[text()="{product_name}"]')
                product_element.click()
                wait_timeout = 20
                
                overviewpage = driver.find_element(By.XPATH, '//div[@class="ReactVirtualized__Grid ReactVirtualized__List"]')
                if want_update_description == 'y':
                    enter_product_description = overviewpage.find_element(By.XPATH, f'//textarea[@placeholder="Enter an item description here if you\'d like"]')
                    enter_product_description_text=enter_product_description.text
                    
                    if enter_product_description_text != product_description:
                        enter_product_description.clear()
                        enter_product_description.send_keys(product_description)
                if want_update_price == 'y':    
                    enter_product_price = overviewpage.find_element(By.XPATH, f'//input[@name="defaultPrice"]')
                    
                    enter_product_price_text=enter_product_price.get_attribute('value')
                    enter_product_price_text = enter_product_price_text.replace("CA$", "")

                    if enter_product_price_text != product_price:
                        enter_product_price.clear()
                        enter_product_price.send_keys(product_price)

                if want_update_image == 'y':
                    add_photo_button = driver.find_element(By.CSS_SELECTOR, '[data-testid="__css__add-photo-card"]')
                    driver.execute_script('arguments[0].click()', add_photo_button)
                    
                
                    current_directory = os.getcwd()  # Get the current working directory
                    image_url = row[21]
                    
                    destination_path = f"{product_name}.jpg"
                    download_google_drive_image(image_url, destination_path)

                    image_name = f"{product_name}.jpg"

                    file_path = os.path.join(current_directory, "images", image_name)
                    input_file = driver.execute_script('return document.querySelector("input[type=\'file\']")')
                    input_file.send_keys(file_path)

                    
                    successNotice = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "1 Photo selected")]')))
                    driver.execute_script('document.querySelector("input[type=\'file\']").parentElement.querySelector("div > div:nth-child(2)").querySelectorAll(\'button\')[3].click();')

                    
                save_button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//button[div[text()="Save"]]')))
                save_button.click()
                print(f'{product_name} is updated')
                time.sleep(5)
            except:
                search_product = WebDriverWait(driver, wait_timeout).until(EC.visibility_of_element_located((By.XPATH, f'//input[@placeholder="Search items and categories"]')))
                search_product.clear()
                search_product.send_keys(product_category)
                overviewpage = driver.find_element(By.XPATH, '//div[@class="ReactVirtualized__Grid ReactVirtualized__List"]/div/div')
                product_category = overviewpage.find_element(By.XPATH, f'//span[text()="{product_category}"]')
                add_item = overviewpage.find_element( By.XPATH, '//button[div[text()="Add item"]]')
                
                add_item.click()
                wait_timeout = 20
                
                overviewpage = driver.find_element(By.XPATH, '//div[@class="ReactVirtualized__Grid ReactVirtualized__List"]/div/div')
                product_name_element = overviewpage.find_element(By.XPATH, f'//input[@placeholder="Enter an item name"]')
                product_name_element.clear()
                product_name_element.send_keys(product_name)
                enter_product_description = overviewpage.find_element(By.XPATH, f'//textarea[@placeholder="Enter an item description here if you\'d like"]')
                enter_product_description_text=enter_product_description.text
                
                if enter_product_description_text != product_description:
                    enter_product_description.clear()
                    enter_product_description.send_keys(product_description)
                
                enter_product_price = overviewpage.find_element(By.XPATH, f'//input[@name="defaultPrice"]')
                
                enter_product_price_text=enter_product_price.get_attribute('value')
                enter_product_price_text = enter_product_price_text.replace("CA$", "")

                if enter_product_price_text != product_price:
                    enter_product_price.clear()
                    enter_product_price.send_keys(product_price)
               
                
                add_photo_button = driver.find_element(By.CSS_SELECTOR, '[data-testid="__css__add-photo-card"]')
                driver.execute_script('arguments[0].click()', add_photo_button)
                
               
                current_directory = os.getcwd()  # Get the current working directory
                image_url = row[21]
                
                destination_path = f"{product_name}.jpg"
                download_google_drive_image(image_url, destination_path)

                image_name = f"{product_name}.jpg"

                file_path = os.path.join(current_directory, "images", image_name)
                input_file = driver.execute_script('return document.querySelector("input[type=\'file\']")')
                input_file.send_keys(file_path)

                
                successNotice = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "1 Photo selected")]')))
                driver.execute_script('document.querySelector("input[type=\'file\']").parentElement.querySelector("div > div:nth-child(2)").querySelectorAll(\'button\')[3].click();')

                
                save_button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//button[div[text()="Save"]]')))
                save_button.click()
                print(f'{product_name} is uploaded')
                time.sleep(5)

driver.close()
driver.quit()