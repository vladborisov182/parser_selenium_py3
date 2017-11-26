#!/usr/bin/python3
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import csv

vacancies = []

def save_file(vacancy, path):
    
    with open (path, "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Название вакансии", "Название компании", "Зарплата", "Город", "Описание"])

        for vacancy in vacancies:
            writer.writerow((vacancy['vacancy_name'], vacancy['company_name'], vacancy['salary'], vacancy['city'], vacancy['description']))

def search_element(card, class_name):
    
    try:
        elem = card.find_element_by_class_name(class_name).text
    except:
        elem = "Неизвестно"

    return elem

def init_driver():
    
    driver = webdriver.Chrome()
    driver.get("https://dou.ua/")
    return driver    

def web_site_parsing(driver):

    print("Перехожу на нужную страницу...")

    driver.find_element_by_link_text("РАБОТА").click()
    driver.find_element_by_class_name("job").send_keys("Python")
    driver.find_element_by_class_name("btn-search").click()

    print("Открываю весь доступный список вакансий...")
    
    while True:
        try:
            driver.find_element_by_link_text("Больше вакансий").click()
            time.sleep(3)
        except:
            break

    cards = driver.find_elements_by_class_name("l-vacancy")

    print("Анализирую все вакансии...")

    for card in cards:
        
        vacancy = search_element(card, "vt")
        company = search_element(card, "company")
        salary = search_element(card, "salary")
        city = search_element(card, "cities")
        description = search_element(card, "sh-info")
            
        vacancies.append ({
            "vacancy_name" : vacancy,
            "company_name" : company,
            "salary" : salary,
            "city" : city,
            "description" : description
        })

    return vacancies
    
def main():
    print("Программа запущена")
    driver = init_driver()
    vacancies = web_site_parsing(driver)

    print("Сохраняю вакансии в csv файл...")
    save_file(vacancies, "python_vacancies_list.csv")

    print("Найдено", str(len(vacancies)), "вакансий")

    print("Программа выполненна и будет завершена через 5 секунд")
    time.sleep(5)
          
if __name__ == "__main__":
    main()