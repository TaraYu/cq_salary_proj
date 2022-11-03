#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 22:24:16 2022

@author: tara-r22
"""

from selenium import webdriver
from shutil import which
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException
import pandas as pd
import time
 
def fetch_jobs(keyword, num_pages):
    options = Options()
    options.add_argument("window-size=1920,1080")
    #Enter your chromedriver.exe path below
    chrome_path = r"/Users/tara-r22/Documents/cq_salary_proj/chromedriver"
    driver = webdriver.Chrome(executable_path=chrome_path, options=options)
    url = 'https://www.glassdoor.com/Job/jobs.htm?sc.keyword="' + keyword + '"&locT=&locId=&locKeyword=,%20CA&jobType=all&fromAge=-1&minSalary=0&includeNoSalaryJobs=true&radius=100&cityId=-1&minRating=0.0&industryId=-1&sgocId=-1&seniorityType=all&companyId=-1&employerSizes=0&applicationType=0&remoteWorkType=0'
    driver.get(url)
    time.sleep(2)
    
    company_name = []
    job_title = []
    salary_est = []
    location = []
    job_description = []
    avg_salary_estimate = []
    company_size = []
    company_type = []
    company_sector = []
    company_industry = []
    company_founded = []
    company_revenue = []
    
    #Set current page to 1
    current_page = 1     
    time.sleep(3)
    number = 0
    while current_page <= num_pages:   
    


        done = False
        while not done:
            job_cards = driver.find_elements(By.XPATH,"//article[@id='MainCol']//ul/li[@data-adv-type='GENERAL']")
            print(len(job_cards))   
                    
            for card in job_cards:
                number = number+1
                print(number)
                    
                try:
                    card.click()
                except ElementClickInterceptedException:
                    continue
                time.sleep(2)

                #Closes the signup prompt
                try:
                    driver.find_element(By.XPATH,".//span[@class='SVGInline modal_closeIcon']").click()
                    time.sleep(0.5)
                except NoSuchElementException:
                    time.sleep(0.1)
                    pass

                #Expands the Description section by clicking on Show More
                try:
                    driver.find_element(By.XPATH,"//div[@class='css-t3xrds e856ufb5']").click()
                    time.sleep(0.5)
                except NoSuchElementException:
                    card.click()
                    print(str(current_page) + '#ERROR: no such element')
                    time.sleep(20)
                    try:
                        driver.find_element(By.XPATH,"//div[@class='css-t3xrds e856ufb5']").click()
                    except NoSuchElementException:
                        continue
                except ElementNotInteractableException:
                    card.click()
                    driver.implicitly_wait(10)
                    print(str(current_page) + '#ERROR: not interactable')
                    driver.find_element(By.XPATH,"//div[@class='css-t3xrds e856ufb5']").click()

                #Scrape 
                
                try:
                    job_title.append(driver.find_element(By.XPATH, "//div[@class='css-1vg6q84 e1tk4kwz4']").text)
                except:
                    job_title.append("#N/A")
                    pass
                
                try:
                    location.append(card.find_element(By.XPATH, ".//span[@class='css-l2fjlt pr-xxsm css-iii9i8 e1rrn5ka0']").text)
                except:
                    location.append("#N/A")
                    pass
                
                try:
                    company_name.append(card.find_element(By.XPATH, ".//div[@class='d-flex justify-content-between align-items-start']").text)
                except:
                    company_name.append("#N/A")
                    pass                     

                try:
                    salary_est.append(card.find_element(By.XPATH, ".//div[@class='css-l2fjlt pr-xxsm']").text)
                except NoSuchElementException:
                    salary_est.append("#N/A")    
                    pass
                
                try:
                    job_description.append(driver.find_element(By.XPATH,"//div[@id='JobDescriptionContainer']").text)
                except:
                    job_description.append("#N/A")
                    pass

                try:
                    avg_salary_estimate.append(driver.find_element(By.XPATH,"//div[@class='css-1bluz6i e2u4hf13']").text)
                except:
                    avg_salary_estimate.append("#N/A")
                    pass
                
                try:
                    company_size.append(driver.find_element(By.XPATH,"//div[@id='CompanyContainer']//span[text()='Size']//following-sibling::*").text)
                except:
                    company_size.append("#N/A")
                    pass
                
                try:
                    company_type.append(driver.find_element(By.XPATH,"//div[@id='CompanyContainer']//span[text()='Type']//following-sibling::*").text)
                except:
                    company_type.append("#N/A")
                    pass
                    
                try:
                    company_sector.append(driver.find_element(By.XPATH,"//div[@id='CompanyContainer']//span[text()='Sector']//following-sibling::*").text)
                except:
                    company_sector.append("#N/A")
                    pass
                    
                try:
                    company_industry.append(driver.find_element(By.XPATH,"//div[@id='CompanyContainer']//span[text()='Industry']//following-sibling::*").text)
                except:
                    company_industry.append("#N/A")
                    pass
                    
                try:
                    company_founded.append(driver.find_element(By.XPATH,"//div[@id='CompanyContainer']//span[text()='Founded']//following-sibling::*").text)
                except:
                    company_founded.append("#N/A")
                    pass
                    
                try:
                    company_revenue.append(driver.find_element(By.XPATH,"//div[@id='CompanyContainer']//span[text()='Revenue']//following-sibling::*").text)
                except:
                    company_revenue.append("#N/A")
                    pass
                
                done = True 
                
       # Moves to the next page         
        if done:
            print(str(current_page) + ' ' + 'out of' +' '+ str(num_pages) + ' ' + 'pages done')
            driver.find_element(By.XPATH,"//span[@alt='next-icon']").click()   
            current_page = current_page + 1
            time.sleep(4)
            

    driver.close()
    df = pd.DataFrame({'company': company_name, 
    'job title': job_title,
    'location': location,
    'salavry estimate': salary_est,
    'job description': job_description,
    'average salary estimate': avg_salary_estimate,
    'company_size': company_size,
    'company_type': company_type,
    'company_sector': company_sector,
    'company_industry' : company_industry, 'company_founded' : company_founded, 'company_revenue': company_revenue})
    
    df.to_csv(keyword + '.csv')