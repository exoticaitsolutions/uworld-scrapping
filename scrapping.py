import os
import re
import time
import uuid
import requests
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from database_configration import get_or_create_answer_choice_id, get_or_create_passage_id, get_or_create_question_id
from webdriver_configration import driver_confrigration


WEBSITE_URL = 'https://www.uworld.com/app/index.html#/login/'
USERNAME = 'nickv@testkey.com'
PASSWORD = 'UpUpUpandAway2024#'
image_folder = 'download_images'

# Create the folder if it does not exist
if not os.path.exists(image_folder):
    os.makedirs(image_folder)
    print(f"Folder '{image_folder}' created successfully.")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
}
# Data storage
data = []

# Main function to scrape question passages
def scrap_question_passages():
    driver = driver_confrigration()
    driver.get(WEBSITE_URL)
    time.sleep(12)

    # Initial navigation to start scraping
    skip = driver.find_element(By.ID, 'skip_btn')
    skip.click()
    time.sleep(3)
    print("Clicked on Skip successfully")

    skip_yes = driver.find_element(By.XPATH, '/html/body/div[9]/div/div/div[3]/button[1]')
    skip_yes.click()
    time.sleep(5)
    print("Clicked on Skip_Yes successfully")

    launch = driver.find_element(By.XPATH, '//*[@id="BtnLaunch13343560"]')
    launch.click()
    time.sleep(15)
    print("Clicked on Launch successfully")

    # Navigate to the QBank section
    qbank = driver.find_element(By.XPATH, '/html/body/app-root/app-mainlayout/div/div[1]/leftnav/mat-sidenav-container/mat-sidenav/div/div[2]/mat-nav-list/mat-list-item[3]')
    qbank.click()
    time.sleep(5)
    print("Clicked on Qbank successfully")

    preview_test = driver.find_element(By.XPATH, '/html/body/app-root/app-mainlayout/div/div[1]/leftnav/mat-sidenav-container/mat-sidenav/div/div[2]/mat-nav-list/mat-list-item[3]/span/mat-nav-list/mat-list-item[2]/span/span[2]/a')
    preview_test.click()
    time.sleep(5)
    print("Clicked on Preview Test successfully")
    all_data = driver.find_element(By.ID, 'cdk-drop-list-0')
    rows = all_data.find_elements(By.TAG_NAME, "tr")
    all_rows = len(rows)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.9);")
    next_button = driver.find_element(By.XPATH, '//*[@aria-label="Next page"]')
    next_button.click()
    time.sleep(10)

    
    print("-------------"*88)
    print("all_rows : ", all_rows)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.6);")

    id_counter = 1
    data = []
    

    for row in range(0, all_rows+1):
        try:
            print(f"Processing row {row}...")
            icone = driver.find_element(By.XPATH, f'//*[@aria-label="Review Test Analysis for test {row+1}"]')
            icone.click()
            time.sleep(5)
            current_url = driver.current_url
            print(f"Current URL: {current_url}")

            reveiew_test = driver.find_element(By.XPATH, '/html/body/app-root/app-mainlayout/div/div[2]/usmle-peformance/gradschool-individual-test/div/div[1]/button[2]')
            reveiew_test.click()
            time.sleep(12)

            while True:
                try:
                    print()
                    print("=============================="*8)
                    # Scrape the question data
                    try:
                        content = driver.find_element(By.ID, 'currentAbstract').text
                    except:
                        content = ''
                    try:
                        explanation = driver.find_element(By.XPATH, '//*[@id="explanation"]/div').text
                    except:
                        explanation = ''
                    try:
                        title = driver.find_element(By.ID, 'abstractTitle').text
                    except:
                        title = ''
                    try:
                        question = driver.find_element(By.ID, 'questionText').text
                    except:
                        question = ''
                    try:
                        correct_answer = driver.find_element(By.XPATH, '//*[@id="questionInformation"]/div[4]/div[1]/div[2]/span[2]').text
                    except:
                        correct_answer = ''
                   

                    question_count1 = driver.find_element(By.ID, 'abstractQuestionCount').text
                    parts = question_count1.split(' ')
                    first_number = int(parts[1])
                    match = re.search(r'(\d+)–(\d+)', question_count1)
                    if match:
                        second_number = int(match.group(1))
                        third_number = int(match.group(2))
                    else:
                        second_number = third_number = None
                    if int(first_number) == 1:
                        question_count1 = third_number
                    else:
                        question_count1 = third_number - second_number

                    topic = driver.find_element(By.XPATH, '//*[@id="explanation-container"]/div[3]/div/div/div[2]/div[1]').text
                    subject = driver.find_element(By.XPATH, '//*[@id="explanation-container"]/div[3]/div/div/div[1]/div[1]').text
                    print()
                    print("---------------------------------"*5)
                    print("title : ", title)
                    print("content : ", content)
                    print("subject : ", subject)
                    print("question_count1 : ", question_count1)
                    print("topic : ", topic)
                    print("---------------------------------"*5)
                    print()

                    # Create or retrieve passage and question IDs
                    passage_id = get_or_create_passage_id(title, content, subject, question_count1, topic)
                    question_id = get_or_create_question_id(question, correct_answer, passage_id, explanation)

           
                    # Save answer choices
                    answers_choices = driver.find_elements(By.CLASS_NAME, 'answer-choice-parent')
                    for answer in answers_choices:
                        get_or_create_answer_choice_id(answer.text, question_id)
                    print("=============================="*8)
                    print()
                    # Scraping images
                    try:
                        explanation = driver.find_element(By.XPATH, '//*[@id="explanation"]/div')
        
                        image_elements = explanation.find_elements(By.TAG_NAME, 'img')
                        image_urls = [img.get_attribute('src') for img in image_elements]
                        
                        for index, url in enumerate(image_urls):
                            print(f"Image {index + 1} URL:", url)
                            response = requests.get(url, headers=headers)
                            print(f"Status code for Image {index + 1}:", response.status_code)
                            if response.status_code == 200:
                                # Include question_id in the unique image name
                                unique_name = f'question_{question_id}.jpg'
                                image_path = os.path.join(image_folder, unique_name)
                                with open(image_path, 'wb') as file:
                                    file.write(response.content)

                                print(f"Image {index + 1} saved successfully to {image_path}")
                                if os.path.exists(image_path):
                                    print(f"Image {index + 1} successfully saved at {image_path}")
                                else:
                                    print(f"Image {index + 1} was not saved successfully.")
                            else:
                                print(f"Failed to download Image {index + 1} from {url}")
                    except:
                        explanation = ''

                    # Save data to list
                    data.append(
                        {
                            "id": id_counter,
                            "title": title,
                            "content": content,
                            "subject": subject,
                            "question_count": question_count1,
                            "topic": topic,
                        }
                    )
                    print(f"Scraped data for question {id_counter}")
                    id_counter += 1

                    # Click the "Next" button to continue scraping
                    click_on_next = driver.find_element(By.XPATH, '//*[@aria-label="Navigate to the next question"]')
                    click_on_next.click()
                    time.sleep(3)

                except NoSuchElementException:
                    print("No more questions or elements found. Breaking out of the loop.")
                    break
                except Exception as e:
                    # print(f"Encountered an error: {e}. Returning to the main page and continuing with the next row.")
                    print("No more questions found for this test")
                    driver.get('https://apps.uworld.com/courseapp/gradschool/v13/previoustests/13343560')
                    time.sleep(6)
                    break

        except NoSuchElementException:
            print(f"Row {row} not found. Skipping to the next.")
            continue
        except Exception as e:
            print(f"Error while processing row {row}: {e}. Returning to main loop.")
            driver.get('https://apps.uworld.com/courseapp/gradschool/v13/previoustests/13343560')
            time.sleep(6)
            continue

    driver.quit()
    
# Run the scraper function
scrap_question_passages()
