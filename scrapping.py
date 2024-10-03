import os
import csv
import re
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from database_configration import get_or_create_answer_choice_id, get_or_create_passage_id, get_or_create_question_id
from webdriver_configration import driver_confrigration

# Constants
CSV_FOLDER_NAME = 'csv_output'
CSV_FILE_NAME = 'question_passages.csv'
WEBSITE_URL = 'https://www.uworld.com/app/index.html#/login/'
USERNAME = 'nickv@testkey.com'
PASSWORD = 'UpUpUpandAway2024#'

# Data storage
data = []

# Define login function
def login(driver):
    driver.get(WEBSITE_URL)
    email = driver.find_element(By.ID, 'login-email')
    email.send_keys(USERNAME)
    time.sleep(3)
    password = driver.find_element(By.ID, 'login-password')
    password.send_keys(PASSWORD)
    time.sleep(3)
    login_btn = driver.find_element(By.XPATH, '//*[@id="login_btn"]')
    login_btn.click()
    time.sleep(10)
    print("Login Successfully Done")

# Define the main scraping function
def scrap_question_passages():
    driver = driver_confrigration()
    driver.get(WEBSITE_URL)
    # login(driver)  # Call the login function
    time.sleep(10)

    # Navigate through initial steps to start scraping
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
    time.sleep(20)
    print("Clicked on Launch successfully")

    # Navigate to the desired section
    qbank = driver.find_element(By.XPATH, '/html/body/app-root/app-mainlayout/div/div[1]/leftnav/mat-sidenav-container/mat-sidenav/div/div[2]/mat-nav-list/mat-list-item[3]')
    qbank.click()
    time.sleep(5)
    print("Clicked on Qbank successfully")

    preview_test = driver.find_element(By.XPATH, '/html/body/app-root/app-mainlayout/div/div[1]/leftnav/mat-sidenav-container/mat-sidenav/div/div[2]/mat-nav-list/mat-list-item[3]/span/mat-nav-list/mat-list-item[2]/span/span[2]/a')
    preview_test.click()
    time.sleep(5)
    print("Clicked on Preview Test successfully")

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.6);")
    time.sleep(8)

    all_data = driver.find_element(By.ID, 'cdk-drop-list-0')
    rows = all_data.find_elements(By.TAG_NAME, "tr")
    all_rows = len(rows)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.6);")
    # Start scraping questions
    id_counter = 1
    for row in range(1,3):
        icone = driver.find_element(By.XPATH, f'//*[@aria-label="Review Test Analysis for test {row+1}"]')
        print(f"Found icon for row {row + 1}")
        icone.click()
        time.sleep(5)
        current_url = driver.current_url
        print("---------------"*8)
        print("current_url : ", current_url)
        print("---------------"*8)
        # test_name = driver.find_element(By.XPATH, '/html/body/app-root/app-mainlayout/div/div[2]/topnav/mat-toolbar/mat-toolbar-row/div[1]/div[1]').text
        reveiew_test = driver.find_element(By.XPATH, '/html/body/app-root/app-mainlayout/div/div[2]/usmle-peformance/gradschool-individual-test/div/div[1]/button[2]')
        reveiew_test.click()
        time.sleep(10)
        while True:
            try:
                try:
                    content = driver.find_element(By.ID, 'currentAbstract').text
                except:
                    content=''
                try:
                    title = driver.find_element(By.ID, 'abstractTitle').text
                except:
                    title = ''
                try:
                    question = driver.find_element(By.ID, 'questionText').text
                    print("question : ", question)
                except:
                    question = ''
                try:
                    answers = driver.find_element(By.XPATH, '//*[@id="answerContainer"]').text
                    print("answers : ", answers)
                except:
                    answers = ''
                try:
                    correct_answer = driver.find_element(By.XPATH, '//*[@id="questionInformation"]/div[4]/div[1]/div[2]/span[2]').text
                    print("correct_answer : ", correct_answer)
                except:
                    correct_answer = ''
                try:
                    explanation = driver.find_element(By.ID, 'explanation-container').text
                    print("explanation : ", explanation)
                except:
                    explanation = ''
                try:
                    question_count1 = driver.find_element(By.ID, 'abstractQuestionCount').text
                    parts = question_count1.split(' ')
                    
                    first_number = int(parts[1])
                    match = re.search(r'(\d+)–(\d+)', question_count1)
                    if match:
                        second_number = int(match.group(1))  # '35' as an integer
                        third_number = int(match.group(2))   # '39' as an integer
                    else:
                        second_number = third_number = None  # If no match is found
                    if int(first_number) == 1:
                       question_count1 = third_number
                    else:
                        question_count1 = third_number - second_number
                    # question_count = question_count1.split('Questions')[1].split('–')[1].split(')')[0].strip()
                    print("--------------------"*8)
                    print("question count text : ", question_count1)
                    print("--------------------"*8)
                except:
                    question_count = ''
               
                try:
                    topic = driver.find_element(By.XPATH, '//*[@id="explanation-container"]/div[3]/div/div/div[2]/div[1]').text
                except:
                    topic = ''
                try:
                    subject = driver.find_element(By.XPATH, '//*[@id="explanation-container"]/div[3]/div/div/div[1]/div[1]').text
                    print("subject : ------------", subject)
                except:
                    subject = ''
                passage_id = get_or_create_passage_id(title, content, subject, question_count1, topic)
                print("--------------------"*8)
                print("passage_id : ", passage_id)
                print("--------------------"*8)
                question_id = get_or_create_question_id(question, correct_answer, passage_id, explanation)
                try:
                    answers_choices  = driver.find_elements(By.CLASS_NAME, 'answer-choice-parent')
                    for answer in answers_choices:
                        print("answers_choices : ", answer.text)
                        get_or_create_answer_choice_id(answer.text, question_id)
                except:
                    answers_choices = ''
                

                # Save data in dictionary and add to list
                data.append(
                    {
                        "id": id_counter,
                        # "test_url": current_url,
                        # "test_number": test_number,
                        "title": title,
                        "content": content,
                        "subject": subject,
                        "question_count": question_count1,
                        "topic": topic,
                    }
                )
                print(f"Scraped data for question {id_counter}")
                id_counter += 1

                # Attempt to click on the "Next" button
                click_on_next = driver.find_element(By.XPATH, '//*[@aria-label="Navigate to the next question"]')
                click_on_next.click()
                time.sleep(3)  # Adjust sleep time based on page load speed

            except NoSuchElementException:
                try:
                    # Check if "Review Incomplete Questions" element is found
                    reveiew_complete = driver.find_element(By.XPATH, f'//*[@aria-label="Review Incomplete Questions"]')
                    print("Review Incomplete Questions element found, stopping scraping.")
                    break
                except NoSuchElementException:
                    # If neither "Next" button nor "Review Incomplete Questions" are found, exit loop
                    print("Neither Next button nor Review Incomplete Questions found. Ending scraping.")
                    break

            except Exception as e:
                print("Review Incomplete Questions element found, stopping scraping.")
                back = driver.get('https://apps.uworld.com/courseapp/gradschool/v13/previoustests/13343560')
                time.sleep(6) 
                continue

    # Write the scraped data to a CSV file
    os.makedirs(CSV_FOLDER_NAME, exist_ok=True)
    csv_file_path = os.path.join(CSV_FOLDER_NAME, CSV_FILE_NAME)

    with open(csv_file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["id", "title", "content", "subject", "question_count", "topic"])
        writer.writeheader()
        for row in data:
            writer.writerow(row)

    print("Scraping completed successfully")
    print(f"Data has been written to {csv_file_path}")
    driver.quit()

# Call the main scraping function
scrap_question_passages()

