from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from time import sleep
from datetime import datetime
import PySimpleGUI as sg
from random import choice, randint
import replase_1
from os import path, listdir, path

def window_1():
    sg.theme('DarkTeal12')

    layout = [
        [sg.T('spam_TG_bot')],
        [sg.T('состояние:')],
        [sg.HorizontalSeparator()],
        [sg.T('ожидаю приказа, мой господин', key='clawn')],
        [sg.HorizontalSeparator()],
        [sg.T('количество скринов:'), sg.Input('', key='counter')],
        [sg.Button('начать')]
        ]

    window = sg.Window('TG_samostoyalka', layout, finalize=True, size=(600,400), resizable=True)

    window.set_min_size((600, 400))

    window.finalize()

    return window

def read():
    replase_1.replace_characters()
    with open('coms.txt', 'r', encoding='UTF-8') as comment:
        com = comment.readlines()
    with open('groups.txt', 'r', encoding='UTF-8') as groups:
        all_groups = groups.readlines()
    return com, all_groups

def accounts():
    with open('numbers.txt', 'r', encoding='UTF=8') as numbers_for_login:
        numbers = numbers_for_login.readlines()
    return numbers
        
def starting_browser():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    return driver

def logining(driver, number):
    with open('logs.txt', 'a', encoding='UTF-8') as log:
        driver.get('https://web.telegram.org/a/')
        log.write('telegram open\n')
        print('get')
        try:
            button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[text()="Log in by phone Number"]')))
            sleep(2)
            button.click()
            print('click')
        except Exception:
            js = f"""
            var xpathResult = document.evaluate(
                '//*[@id="auth-qr-form"]/div/button',
                document,
                null, 
                XPathResult.FIRST_ORDERED_NODE_TYPE, 
                null 
            );""" + """
            var element = xpathResult.singleNodeValue;
            if (element) {
                element.click(); 
            } else {
                console.error('Element not found');
            }
            """
            sleep(2)
            driver.execute_script(js)
        number_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="sign-in-phone-number"]')))
        print('find')
        number_input.clear()
        print('clear')
        number_input.send_keys(number)
        log.write('number finded\n')
        print('print')
        enter = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="auth-phone-number-form"]/div/form/button[1]')))
        try:
            enter.click()
        except Exception:
            pass
        print('enter')
        sg.popup('нажми когда отсканируешь и войдёшь в аккаунт')

def open_group(log, driver):
    WebDriverWait(driver, 12).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="LeftColumn-main"]/div[2]/div[2]/div/div[2]/div/div[1]/div[1]/div'))).click() #открытие группы    
    print('open group')
    log.write('group open\n')

def post_update(driver):
    try:
        WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="MiddleColumn"]/div[4]/div[3]/div[3]/button'))).click() #кнопка спуска на нижний пост
        print('down')
    except Exception:
        pass

def list_posts(driver, log, coms, groups, counter):
    print('input string')
    while 1!=0:
        for com in coms:
            group = choice(groups)
            print(group)
            WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="telegram-search-input"]'))).send_keys(group) #строка поиска
            print(1)
            log.write(f'find group {group}\n')
            print('find groups')
            sleep(7)
            print(open)
            try:
                open_group(log, driver)
            except Exception:
                driver.get('https://web.telegram.org/a/')
                continue
            try:
                post_update(driver)
            except Exception:
                pass   
            try:
                posts1 = driver.find_elements(By.XPATH, '//div[@data-message-id]') #сбор постов канала    
                posts = list(set(posts1))
                print('find posts') 
                log.write(f'finded {len(posts)} posts\n')
                print(f'finded {len(posts)} posts\n')
                list_id = []
                for post in posts:
                    post_id = post.get_attribute('data-message-id')
                    if post_id in list_id:
                        print('group complete')
                        break
                    list_id.append(post_id)
                    print(f'id = {post_id}')
                    try:
                        sleep(2)
                        js = f"""
                        var element = document.querySelector('[data-message-id="{post_id}"]');
                        var commentsButton = element.querySelector('.CommentButton');
                        commentsButton.click();
                        """
                        driver.execute_script(js)
                        a = 0
                        try:
                            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="message{post_id}"]/div[3]/div/div[2]')))
                        except Exception:
                            print('messange without coms')
                            continue
                        while a != 1:
                            try:
                                driver.execute_script(js)
                                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="editable-message-text"]')))
                                a += 1
                            except Exception:
                                pass
                        print('open comments')
                        log.write('coms open\n')
                        try:
                            try:
                                input_coms = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="editable-message-text"]')))
                            except Exception:
                                print(1)
                                try:
                                    driver.find_element(By.XPATH, '//*[@id="portals"]/div[2]/div/div/div[2]/div[2]/div/button').click()
                                finally:
                                    break
                            sleep(2)
                            input_coms.send_keys(com)
                            print(com)
                            log.write(f'sended {com}')
                            sleep(2)
                            try:
                                post_update()
                            except Exception:
                                pass
                            try:
                                WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '//i[@class="icon icon-message-succeeded"]')))
                            except Exception:
                                WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '//i[@class="icon icon-message-read"]')))
                            counter += 1
                            screenshots_folder = 'screenshots/'
                            print('screenshot')
                            driver.save_screenshot(screenshots_folder + f'screenshot_{counter}.png')    
                        except Exception:
                            print('comments closed')
                            log.write('comments closed\n')
                            driver.find_element(By.XPATH, '//*[@id="portals"]/div[2]/div/div/div[2]/div[2]/div/button').click()
                        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="MiddleColumn"]/div[4]/div[1]/div[1]/div[2]/div/button'))).click() #кнопка выхода из коментариев
                        print('back')
                    except Exception:
                        print('coms no clicable')
            except Exception:
                print('haven`t posts')
                #driver.find_element(By. XPATH, '//*[@id="portals"]/div[2]/div/div/div[2]/div[2]/div/button').click()
                #WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="MiddleColumn"]/div[4]/div[1]/div[1]/div[2]/div/button'))).click() #кнопка выхода из коментариев
            driver.get('https://web.telegram.org/a/')

def starter():
    folder_path = "screenshots"
    counter = len([f for f in listdir(folder_path) if path.isfile(path.join(folder_path, f))])
    with open('logs.txt', 'a', encoding='UTF-8') as log:
        time = datetime.now()
        log.write(f'\n\n\n----work start at {time}----\n')
        driver = starting_browser()
        log.write('browser start\n')
        print('starting_browser')
        numbers = accounts()
        print('accounts')
        for number in numbers:
            coms, groups = read()
            print('read')
            logining(driver, number)
            log.write('logining finished\n')
            print('logining')
            list_posts(driver, log, coms, groups, counter)
                    
def work():
    window = window_1()
    while True:
        try:
            event, values = window.read()

            if event == sg.WINDOW_CLOSED:
                break        

            if event == 'начать':
                starter()
        except Exception as error1:
            sg.popup(error1)
            print(error1)
            with open('logs.txt', 'a', encoding='UTF-8') as log:
                log.write(error1)

if __name__ == '__main__':
    work()