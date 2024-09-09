import json
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from urllib.parse import urlparse, urlunparse
from photodownload import download_google_drive_image

from read import read_data_from_sheet

url = input("Enter your link: ")

results, v1_name, v2_name, v3_name, v1_category_names, v2_category_names, v3_category_names = read_data_from_sheet(spread_sheet_id)

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

driver.get('https://manager.tryotter.com/menus/brand')
search_box = WebDriverWait(driver, wait_timeout).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Search brands and menus"]'))
)
search_box = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Search brands and menus"]')
search_box.send_keys(v2_name)
is_category = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/div/div[2]/div/div[3]/div[1]/div/div/div/div/div/div/div/div/div/div[2]/div/div/div/div/div/div/div[4]/div/div/div/div/div/div[1]/span')

if is_category:
    try:
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
        all_existing_categories.append(category_name)



    for v2_category_name in v2_category_names:

        if v2_category_name not in all_existing_categories:
            add_category_button  =  WebDriverWait(driver, wait_timeout).until(EC.visibility_of_element_located((By.XPATH, f'//*[text()="Add category"]')))
            add_category_button.click()
            category_name_input = WebDriverWait(driver, wait_timeout).until(EC.visibility_of_element_located((By.XPATH, f'//input[@placeholder="Enter a category name"]')))
            category_name_input.clear()
            category_name_input.send_keys(v2_category_name)
            save_button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//button[div[text()="Save"]]')))
            save_button.click()

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
    item_url = modified_url+'/items'
    driver.get(item_url)
    for index, row in enumerate(results, start=1):
        if index>=5:
            product_name = row[2]
            search_product = WebDriverWait(driver, wait_timeout).until(EC.visibility_of_element_located((By.XPATH, f'//input[@placeholder="Search items"]')))
            search_product.clear()
            search_product.send_keys(product_name)
            product_description = row[15]
            product_price = row[11]
            product_price = product_price.replace("$", '')
            product_category = row[7]

            
            try:
                wait_timeout = 2
                is_product_available = WebDriverWait(driver, wait_timeout).until(EC.visibility_of_element_located((By.XPATH, f'//div[@class="ReactVirtualized__Grid ReactVirtualized__List"]/div/div/div/div/div[2]/div[2]/div[1]/div[1]/div[1]/span')))
                is_product_available.click()
                wait_timeout = 20
                
                enter_product_description = WebDriverWait(driver, wait_timeout).until(EC.visibility_of_element_located((By.XPATH, f'//textarea[@placeholder="Enter an item description here if you\'d like"]')))
                enter_product_description_text=enter_product_description.text
                
                if enter_product_description_text != product_description:
                    enter_product_description.clear()
                    enter_product_description.send_keys(product_description)
                
                enter_product_price = WebDriverWait(driver, wait_timeout).until(EC.visibility_of_element_located((By.XPATH, f'//input[@name="defaultPrice"]')))
                enter_product_price_text=enter_product_price.get_attribute('value')
                enter_product_price_text = enter_product_price_text.replace("CA$", "")
                
                is_category_selected_text = ''
                select_category  =  WebDriverWait(driver, wait_timeout).until(EC.visibility_of_element_located((By.CSS_SELECTOR, f'[data-testid="__css__category-selector-button-toggle-button"]')))
                try:
                    
                    is_category_selected = driver.execute_script('return arguments[0].parentNode', select_category)

                    is_category_selected = driver.execute_script('return arguments[0].querySelectorAll("div")', is_category_selected)
                    is_category_selected_text =  is_category_selected[2].text
                    if is_category_selected_text != '':
                        if is_category_selected_text != product_category:
                            is_category_selected[2].click()
                            select_category.click()
                            alchohol_selection = driver.execute_script('return document.querySelector(\'[data-testid="__css__alcohol-selector-menu"]\');')
                            alchohol_selection = driver.execute_script('return arguments[0].parentNode', alchohol_selection)

                            all_option = alchohol_selection.find_element(By.XPATH, 'div[2]/div[2]')
                            all_options = all_option.text
                            all_options = all_options.split('\n')
                            if product_category in  all_options:
                                clickable_category = alchohol_selection.find_element(By.XPATH, f'span[text()={product_category}]')
                                clickable_category.click()

                            raju = 'raju'
                        else:
                            select_category.click()
                            alchohol_selection = driver.execute_script('return document.querySelector(\'[data-testid="__css__alcohol-selector-menu"]\');')
                            alchohol_selection = driver.execute_script('return arguments[0].parentNode', alchohol_selection)

                            all_option = alchohol_selection.find_element(By.XPATH, 'div[2]/div[2]')
                            all_options = all_option.text
                            all_options = all_options.split('\n')
                            if product_category in  all_options:
                                #clickable_category = alchohol_selection.find_element(By.CSS_SELECTOR, f'span[text()="{product_category}"]')
                                alchohol_selection = driver.execute_script('return document.querySelector(\'[data-testid="__css__alcohol-selector-menu"]\');')
                                alchohol_selection = driver.execute_script('return arguments[0].parentNode', alchohol_selection)

                                clickable_element = alchohol_selection.find_element(By.XPATH, 'div[2]/div[2]')
                                all_elements = clickable_element.find_elements(By.TAG_NAME, 'div')
                                clickable_category.click()
                            
                            


                    
                except Exception as ex:
                    raju = 'raju'
                

                alchohol_selection = driver.execute_script('return document.querySelector(\'[data-testid="__css__alcohol-selector-menu"]\');')
                alchohol_selection = driver.execute_script('return arguments[0].parentNode', alchohol_selection)
                
                
                """ 
                alcholoholic_selection = WebDriverWait(driver, wait_timeout).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'ul[data-testid="__css__alcohol-selector-menu"]')))
                alcholoholic_selection = alcholoholic_selection.find_element(By.XPATH, './parent::*')
                select_catlist = alcholoholic_selection.find_element(By.XPATH, './parent::*')
                select_category_list = select_catlist.find_elements(By.XPATH, '//div/div[2]/div[2]/div/div')
                 """
                element = driver.find_element(By.XPATH, '/html/body/div[10]/div[2]')
                element = element.find_element(By.CLASS_NAME, 'bqgynG')
                elements = element.find_elements(By.CLASS_NAME, 'ilwhpy')
                if enter_product_price_text != product_price:
                    enter_product_price.clear()
                    enter_product_price.send_keys(product_price)
                save_button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//button[div[text()="Save"]]')))
                save_button.click()

                
                
            except Exception as ex:
                
                item_add_button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//button[div[text()="Add item"]]')))
                item_add_button.click()
                enter_product_name = WebDriverWait(driver, wait_timeout).until(EC.visibility_of_element_located((By.XPATH, f'//input[@placeholder="Enter an item name"]')))
                enter_product_name
                add_photo_button  =  WebDriverWait(driver, wait_timeout).until(EC.visibility_of_element_located((By.XPATH, f'//*[text()="Add category"]')))
                add_photo_button.click()
                image_url = row[21]
                
                destination_path = f"{product_name}.jpg"
                download_google_drive_image(image_url, destination_path)
                select_category  =  WebDriverWait(driver, wait_timeout).until(EC.visibility_of_element_located((By.CSS_SELECTOR, f'[data-testid="__css__category-selector-button-toggle-button"]')))
                try:
                    select_category.click()
                except Exception as ex:
                    raju = 'raju'

                time.sleep(5)
                alchohol_selection = driver.execute_script('return document.querySelector(\'[data-testid="__css__alcohol-selector-menu"]\');')
                alchohol_selection = driver.execute_script('return arguments[0].parentNode', alchohol_selection)
                
                alcholoholic_selection  =  WebDriverWait(driver, wait_timeout).until(EC.visibility_of_element_located((By.CSS_SELECTOR, f'[data-testid="__css__alcohol-selector-menu"]')))
                alcholoholic_selection = alcholoholic_selection.find_element(By.XPATH, './parent::*')
                select_catlist = alcholoholic_selection.find_element(By.XPATH, './parent::*')
                select_category_list = select_catlist.find_elements(By.XPATH, '//div/div[2]/div[2]/div/div')


'''
/html/body/div[10]/div[2]/div[2]


'''




