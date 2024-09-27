import os
import csv
import time
from selenium.webdriver.common.by import By
from database_configration import insert_data_into_mysql
from webdriver_configration import driver_confrigration

CSV_FOLDER_NAME = 'csv_output'
CSV_FILE_NAME = 'question_passages.csv'
WEBSITE_URL =  'https://www.uworld.com/app/index.html#/login/'
USERNAME = 'nickv@testkey.com'
PASSWORD = 'UpUpUpandAway2024#'

data = []

def login(driver):
    # driver = driver_confrigration()
    driver.get(WEBSITE_URL)
    email = driver.find_element(By.ID, 'login-email')
    email.send_keys(USERNAME)
    time.sleep(3)
    password = driver.find_element(By.ID, 'login-password')
    password.send_keys(PASSWORD)
    time.sleep(3)
    login = driver.find_element(By.XPATH, '//*[@id="login_btn"]')
    login.click()
    time.sleep(10)
    print("Login Sucessfully Done")



# def scrap(driver):
#     # driver = driver_confrigration()
#     try:
#         abstract_question_count = driver.find_element(By.ID, 'abstractQuestionCount').text
#         question_count = abstract_question_count.split('Questions')[1].split('–')[1].split(')')[0].strip()
#         print(f"question_count:  {question_count}")
#     except:
#         question_count = 5
#     try:
#         content = driver.find_element(By.ID, 'currentAbstract')
#         content = content.text
#         print(f"content : {content}")

#     except:
#         content = ''
#     try:
#         title = driver.find_element(By.ID, 'abstractTitle').text
#         print(f"title : {title}")
#     except:
#         title = ''
#     try:
#         topic = driver.find_element(By.XPATH, '//*[@id="explanation-container"]/div[3]/div/div/div[2]/div[1]').text
#         print(f"topic : {topic}")
        
#     except:
#         topic = ''
#     try:
#         subject = driver.find_element(By.XPATH, '//*[@id="explanation-container"]/div[3]/div/div/div[1]/div[1]').text
#     except:
#         subject = ''
#     try:
#         click_on_next = driver.find_element(By.XPATH, '/html/body/app-root/gradschool-test-interface/testinterface-gradschool-mainlayout/div/pearson-layout/div/pearson-footer/div/div/div[2]/span[2]/a')
#         click_on_next.click()
#         print("Next Button Found")
#     except:
#         print("No Next Button Found")




def click_next_until_review_complete(driver):
    try:
        # Initialize a variable to control the loop
        review_complete_element_found = False

        # Use a loop to keep clicking on the "Next" button until the desired element is found
        while not review_complete_element_found:
            # Scroll down a bit to make sure the "Next" button is visible
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.6);")
            time.sleep(4)  # Adjust sleep time if necessary

            try:
                # Attempt to find and click the "Next" button
                click_on_next = driver.find_element(By.XPATH, '/html/body/app-root/gradschool-test-interface/testinterface-gradschool-mainlayout/div/pearson-layout/div/pearson-footer/div/div/div[2]/span[2]/a/span')
                click_on_next.click()
                print("Clicked on the 'Next' button.")
                time.sleep(10)  # Wait for the page to load before searching for the desired element

            except Exception as e:
                print(f"Could not click on the 'Next' button. Error: {e}")
                break

            # Check if the "Review Incomplete Questions" element is present
            try:
                reveiew_complete = driver.find_element(By.XPATH, '//*[@aria-label="Review Incomplete Questions"]')
                review_complete_element_found = True  # If found, set flag to True to exit loop
                print("Found the 'Review Incomplete Questions' element. Stopping loop.")
            except:
                # If the element is not found, continue the loop
                print("Did not find 'Review Incomplete Questions' element. Continuing to the next page...")

    except Exception as e:
        print(f"Error in 'click_next_until_review_complete': {e}")


def scrap_question_passages():
    driver = driver_confrigration()
    login(driver)
    # driver.get(WEBSITE_URL)
    time.sleep(15)
    skip = driver.find_element(By.ID, 'skip_btn')
    skip.click()
    time.sleep(3)
    print("Click On Skip Suceesfully")
    skip_yes = driver.find_element(By.XPATH, '/html/body/div[9]/div/div/div[3]/button[1]')
    skip_yes.click()
    time.sleep(5)
    print("Click On Skip_Yes Suceesfully")
    launch = driver.find_element(By.XPATH, '//*[@id="BtnLaunch13343560"]')
    launch.click()
    time.sleep(20)
    print("Click On Launch Suceesfully")

    qbank = driver.find_element(By.XPATH, '/html/body/app-root/app-mainlayout/div/div[1]/leftnav/mat-sidenav-container/mat-sidenav/div/div[2]/mat-nav-list/mat-list-item[3]')
    qbank.click()
    print("Click On Qbank Suceesfully")
    preview_test = driver.find_element(By.XPATH, '/html/body/app-root/app-mainlayout/div/div[1]/leftnav/mat-sidenav-container/mat-sidenav/div/div[2]/mat-nav-list/mat-list-item[3]/span/mat-nav-list/mat-list-item[2]/span/span[2]/a')
    preview_test.click()
    time.sleep(5)
    print("Click On Preview Test Suceesfully")

    all_data = driver.find_element(By.ID, 'cdk-drop-list-0')
    rows = all_data.find_elements(By.TAG_NAME, "tr")
    all_rows = len(rows)
    print("all_rows------------------------", all_rows)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.6);")
    time.sleep(8)
    id_counter = 1


    for row in range(0, all_rows):
        try:
            icone = driver.find_element(By.XPATH, f'//*[@aria-label="Review Test Analysis for test {row+1}"]')
            # icone = driver.find_element(By.XPATH, '//*[@aria-label="Review Test Analysis for test 9"]')

            print(f"Found icon for row {row + 1}")
            icone.click()
            time.sleep(5)
            reveiew_test = driver.find_element(By.XPATH, '/html/body/app-root/app-mainlayout/div/div[2]/usmle-peformance/gradschool-individual-test/div/div[1]/button[2]')
            reveiew_test.click()
            time.sleep(10)
    
            try:
                abstract_question_count = driver.find_element(By.ID, 'abstractQuestionCount').text
                question_count = abstract_question_count.split('Questions')[1].split('–')[1].split(')')[0].strip()
                print(f"question_count:  {question_count}")
            except:
                question_count = 5
            try:
                content = driver.find_element(By.ID, 'currentAbstract')
                content = content.text
                print(f"content : {content}")

            except:
                content = ''

            try:
                answers = driver.find_element(By.XPATH, '//*[@id="answerContainer"]')
                answers = answers.text
                print("-----------"*8)
                print(f"answers : {answers}")
                print("-----------"*8)

            except:
                answers = ''
            try:
                title = driver.find_element(By.ID, 'abstractTitle').text
                print(f"title : {title}")
            except:
                title = ''
            try:
                topic = driver.find_element(By.XPATH, '//*[@id="explanation-container"]/div[3]/div/div/div[2]/div[1]').text
                print(f"topic : {topic}")
                
            except:
                topic = ''
            try:
                subject = driver.find_element(By.XPATH, '//*[@id="explanation-container"]/div[3]/div/div/div[1]/div[1]').text
            except:
                subject = ''
            try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.9);")
                time.sleep(4)
                click_next_until_review_complete(driver)
                click_on_next = driver.find_element(By.XPATH, '/html/body/app-root/gradschool-test-interface/testinterface-gradschool-mainlayout/div/pearson-layout/div/pearson-footer/div/div/div[2]/span[2]/a/span')
                click_on_next.click()
                time.sleep(10)
                # scrap(driver)
                reveiew_complete = driver.find_element(By.XPATH, f'//*[@aria-label="Review Incomplete Questions"]')

                print("Next Button Found")
            except:
                print("No Next Button Found")
            back = driver.get('https://apps.uworld.com/courseapp/gradschool/v13/previoustests/13343560')
            time.sleep(5)
            data.append(
                    {
                        "id": id_counter,
                        "title": title,
                        "content": content,
                        "subject": subject,
                        "question_count": question_count,
                        "topic": topic,
                    }
                )
            id_counter += 1
            insert_data_into_mysql(data)
            print("Data Insert Succssfully In MySql Database")
        except Exception as e:
            print(f"Could not find icon for row {row + 1}. Error: {e}")
            time.sleep(5)

    os.makedirs(CSV_FOLDER_NAME, exist_ok=True)  # Create folder if it doesn't exist
    csv_file_path = os.path.join(CSV_FOLDER_NAME, CSV_FILE_NAME)

    with open(csv_file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "id",
                "title",
                "content",
                "subject",
                "question_count",
                "topic"
            ],
        )
        writer.writeheader()
        for row in data:
            writer.writerow(row)
    print("Scraping completed for max hbo website")
    print(f"Data has been written to {csv_file_path}")
    print()
    driver.quit()
scrap_question_passages()


