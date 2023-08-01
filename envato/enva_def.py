import datetime
import os
import pickle
from pathlib import Path

from django.core.files import File
import jdatetime
import time
from custom_logs.models import custom_log
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, WebDriverException

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from envato.models import get_envato_config_settings
from envato_telegram_bot.settings import CHROME_DRIVER_PATH, BASE_DIR

d = DesiredCapabilities.CHROME
d['goog:loggingPrefs'] = {'performance': 'ALL'}


# ------------ Start Scraper functions -------------------
def get_time_sleep():
    time_sleep = get_envato_config_settings().sleep_time
    custom_log("sleep time: " + str(time_sleep), "d")
    return int(time_sleep)


def get_envato_cookie():
    options = Options()
    options.headless = False
    options.add_argument("--window-size=1920,1200")
    driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, options=options, desired_capabilities=d)
    webdriver_problem_number_of_reloading = 0
    while True:
        try:
            number_of_get_accept_cookie_btn_tries = 0
            while True:
                custom_log("get_envato_cookie: starting page load", "d")
                driver.get("https://elements.envato.com/sign-in")
                custom_log("driver.get(url)> url has been fetched. we are waiting for: " + str(get_time_sleep()), 'd')
                time.sleep(get_time_sleep())
                check_chrome_connection_status(driver)
                custom_log("get_envato_cookie: check for accept cookie button", "d")
                try:
                    WebDriverWait(driver, 60).until(
                        EC.element_to_be_clickable((By.ID, "CybotCookiebotDialogBodyButtonAccept")))
                    accept_cookie_button = driver.find_element(By.ID, "CybotCookiebotDialogBodyButtonAccept")
                    accept_cookie_button.click()

                    number_of_sign_in_tries = 0
                    try:
                        WebDriverWait(driver, 60).until(
                            EC.element_to_be_clickable((By.ID, "sso-forms__submit")))
                        username_input = driver.find_element(By.ID, "username")
                        password_input = driver.find_element(By.ID, "password")
                        sign_in_btn = driver.find_element(By.ID, "sso-forms__submit")
                        username_input.send_keys(get_envato_config_settings().envato_user)
                        password_input.send_keys(get_envato_config_settings().envato_pass)
                        sign_in_btn.click()
                        custom_log("get_envato_cookie: waiting for 30 seconds after click sign-in btn", "d")
                        time.sleep(30)
                        cookie_file_path = Path(BASE_DIR / 'envato/cookies/cookies.pkl')
                        pickle.dump(driver.get_cookies(), open(cookie_file_path, "wb"))
                        with cookie_file_path.open(mode="rb") as f:
                            settings = get_envato_config_settings()
                            settings.envato_cookie = File(f, name=cookie_file_path.name)
                            settings.login_status = True
                            settings.save()
                        driver.quit()
                        custom_log('get_envato_cookie: sign-in to Envato has been successful. The cookie has been saved', "d")
                        return True
                    except Exception as e:
                        custom_log("get_envato_cookie: sign-in problem, we cant sign to Envato site using the provided credential. err: " + str(e), "d")
                    number_of_sign_in_tries += 1
                    if number_of_sign_in_tries == 3:
                        driver.quit()
                        custom_log(
                            "get_envato_cookie: after 3 times of reload, we still cant sign to Envato site using the provided credential, sign-in function has been failed",
                            "d")
                        settings = get_envato_config_settings()
                        settings.login_status = False
                        settings.save()
                        return False
                except Exception as e:
                    custom_log("get_envato_cookie: we cant find accept cookie button. err: " + str(e), "d")
                number_of_get_accept_cookie_btn_tries += 1
                if number_of_get_accept_cookie_btn_tries == 3:
                    driver.quit()
                    custom_log(
                        "get_envato_cookie: after 3 times of reload, we cant find accept cookie button, sign-in function has been failed",
                        "d")
                    driver.quit()
                    settings = get_envato_config_settings()
                    settings.login_status = False
                    settings.save()
                    return False
        except NoSuchElementException as e:
            custom_log('get_envato_cookie webdriver exception. err: ' + str(e), "d")
            custom_log('we are waiting for ' + str(get_time_sleep()) + ' second', "d")
            time.sleep(get_time_sleep())
        except WebDriverException as e:
            custom_log('get_envato_cookie webdriver exception. err: ' + str(e), "d")
            custom_log('we are waiting for ' + str(get_time_sleep()) + ' second', "d")
            time.sleep(get_time_sleep())
        except ConnectionError as e:
            custom_log('get_envato_cookie webdriver exception. err: ' + str(e), "d")
            custom_log('we are waiting for ' + str(get_time_sleep()) + ' second', "d")
            time.sleep(get_time_sleep())
        except Exception as e:
            custom_log('get_envato_cookie webdriver exception. err: ' + str(e), "d")
            custom_log('we are waiting for ' + str(get_time_sleep()) + ' second', "d")
            time.sleep(get_time_sleep())
        webdriver_problem_number_of_reloading += 1
        if webdriver_problem_number_of_reloading == 3:
            driver.quit()
            custom_log("get_envato_cookie: webdriver exception caused get cookie to be aborted", 'd')
            settings = get_envato_config_settings()
            settings.login_status = False
            settings.save()
            return False


def check_if_sign_in_is_needed():
    options = Options()
    options.headless = False
    options.add_argument("--window-size=1920,1200")
    driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, options=options, desired_capabilities=d)
    webdriver_problem_number_of_reloading = 0
    while True:
        try:
            number_of_get_accept_cookie_btn_tries = 0
            while True:
                custom_log("check_if_sign_in_is_needed: starting page load", "d")
                driver.get('https://elements.envato.com/')
                try:
                    cookies = pickle.load(open(get_envato_config_settings().envato_cookie.path, "rb"))
                    for cookie in cookies:
                        driver.add_cookie(cookie)
                except Exception as e:
                    custom_log("check_if_sign_in_is_needed: cookie does not exist. err: " + str(e), "d")
                    return True
                driver.refresh()
                custom_log("driver.get(url)> url has been fetched. we are waiting for: " + str(get_time_sleep()), 'd')
                time.sleep(get_time_sleep())
                check_chrome_connection_status(driver)
                custom_log("check_if_sign_in_is_needed: check for user detail", "d")
                try:
                    custom_log("check_if_sign_in_is_needed: check for user detail", "d")
                    WebDriverWait(driver, 3600).until(
                        EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/nav/div/div/div[1]/div[4]/ul/li/button/div/span')))
                    driver.quit()
                    custom_log("check_if_sign_in_is_needed: sign-in confirmed", "d")
                    return False
                except Exception as e:
                    custom_log(
                        "check_if_sign_in_is_needed: user detail not found", "d")
                number_of_get_accept_cookie_btn_tries += 1
                if number_of_get_accept_cookie_btn_tries == 3:
                    driver.quit()
                    custom_log(
                        "check_if_sign_in_is_needed: after 3 times of reload, sign-in with cookie has been failed. it means new sign-in require",
                        "d")
                    driver.quit()
                    return True
        except NoSuchElementException as e:
            custom_log('check_if_sign_in_is_needed webdriver exception. err: ' + str(e), "d")
            custom_log('we are waiting for ' + str(get_time_sleep()) + ' second', "d")
            time.sleep(get_time_sleep())
        except WebDriverException as e:
            custom_log('check_if_sign_in_is_needed webdriver exception. err: ' + str(e), "d")
            custom_log('we are waiting for ' + str(get_time_sleep()) + ' second', "d")
            time.sleep(get_time_sleep())
        except ConnectionError as e:
            custom_log('check_if_sign_in_is_needed webdriver exception. err: ' + str(e), "d")
            custom_log('we are waiting for ' + str(get_time_sleep()) + ' second', "d")
            time.sleep(get_time_sleep())
        except Exception as e:
            custom_log('check_if_sign_in_is_needed webdriver exception. err: ' + str(e), "d")
            custom_log('we are waiting for ' + str(get_time_sleep()) + ' second', "d")
            time.sleep(get_time_sleep())
        webdriver_problem_number_of_reloading += 1
        if webdriver_problem_number_of_reloading == 3:
            driver.quit()
            custom_log("check_if_sign_in_is_needed: webdriver exception caused sign-in to be aborted", 'd')
            return False


def envato_auth():
    if check_if_sign_in_is_needed():
        get_envato_cookie()


def envato_download_file(envato_files):
    options = Options()
    options.headless = False
    options.add_argument("--window-size=1920,1200")
    envato_files_path = BASE_DIR / 'media/envato-files/'
    prefs = {"download.default_directory": f"{envato_files_path}"}
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, options=options, desired_capabilities=d)
    webdriver_problem_number_of_reloading = 0
    while True:
        try:
            number_of_get_accept_cookie_btn_tries = 0
            while True:
                custom_log("envato_download_file: starting page load", "d")
                driver.get('https://elements.envato.com/')
                # driver.get('https://file-examples.com/index.php/sample-audio-files/sample-mp3-download/')
                cookies = pickle.load(open(get_envato_config_settings().envato_cookie.path, "rb"))
                for cookie in cookies:
                    driver.add_cookie(cookie)
                time.sleep(1)
                driver.refresh()
                custom_log("driver.get(url)> url has been fetched. we are waiting for: " + str(get_time_sleep()), 'd')
                # time.sleep(get_time_sleep())
                time.sleep(1)
                check_chrome_connection_status(driver)
                custom_log("envato_download_file: start downloading the files", "d")
                try:
                    print(envato_files)
                    i = 0
                    for envato_file in envato_files:
                        while not get_envato_config_settings().login_status:
                            time.sleep(5)
                        driver.switch_to.new_window(f'tab_{i}')
                        driver.get(envato_file.page_link)

                        number_of_checking_categories = 0
                        try:
                            custom_log("envato_download_file: check that if categories are visible", "d")
                            WebDriverWait(driver, 60).until(
                                EC.visibility_of_element_located((By.XPATH,
                                                                  '//*[@id="app"]/div[1]/main/div/div[1]/section[1]/div[1]/div/div[1]/div/div/a[2]')))
                            custom_log("envato_download_file: categories are visible", "d")
                        except Exception as e:
                            custom_log(
                                "envato_download_file: failed to find categories", "d")
                        number_of_checking_categories += 1
                        if number_of_checking_categories == 3:
                            driver.quit()
                            custom_log(
                                "envato_download_file: after 3 times of reload, failed to find categories",
                                "d")
                            envato_file.is_acceptable_file = False
                            envato_file.save()
                            continue

                        categories_section = driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/main/div/div[1]/section[1]/div[1]/div/div[1]/div/div/a[2]')

                        if categories_section.text == '3D': # check if category is 3d
                            number_of_try_to_pick_psd_btn = 0
                            try:
                                custom_log("envato_download_file: check for psd btn", "d")
                                WebDriverWait(driver, 60).until(
                                    EC.visibility_of_element_located((By.XPATH,
                                                                      '//*[@id="app"]/div[1]/main/div/div/section[1]/div[2]/div/div[2]/div/div[3]/button[2]')))
                                custom_log("envato_download_file: psd btn has showed up", "d")
                            except Exception as e:
                                custom_log(
                                    "envato_download_file: failed to find psd btn", "d")
                            number_of_try_to_pick_psd_btn += 1
                            if number_of_try_to_pick_psd_btn == 3:
                                driver.quit()
                                custom_log(
                                    "envato_download_file: after 3 times of reload, failed to find psd btn",
                                    "d")
                                envato_file.is_acceptable_file = False
                                envato_file.save()
                                continue
                            psd_btn = driver.find_element(By.XPATH,
                                                               '//*[@id="app"]/div[1]/main/div/div/section[1]/div[2]/div/div[2]/div/div[3]/button[2]')
                            psd_btn.click()
                            time.sleep(1)

                            download_this_angle_btn = driver.find_element(By.XPATH,
                                                          '//*[@id="app"]/div[1]/main/div/div/section[1]/div[2]/div/div[2]/div/button')
                            download_this_angle_btn.click()
                            time.sleep(1)

                            download_without_license_btn = driver.find_element(By.XPATH,
                                                                               '/html/body/div[9]/div/div/div/div/form/footer/div[1]/div[2]/button')
                            download_without_license_btn.click()
                            time.sleep(1)
                        else:
                            number_of_checking_download_btn_visibility = 0
                            try:
                                custom_log("envato_download_file: check for download btn", "d")
                                WebDriverWait(driver, 60).until(
                                    EC.visibility_of_element_located((By.XPATH,
                                                                      '//*[@id="app"]/div[1]/main/div/div[2]/div/div[2]/button')))
                                custom_log("envato_download_file: download btn has showed up", "d")
                            except Exception as e:
                                custom_log(
                                    "envato_download_file: failed to find download btn", "d")
                            number_of_checking_download_btn_visibility += 1
                            if number_of_checking_download_btn_visibility == 3:
                                driver.quit()
                                custom_log(
                                    "envato_download_file: after 3 times of reload, failed to find download btn",
                                    "d")
                                envato_file.is_acceptable_file = False
                                envato_file.save()
                                continue
                            download_btn = driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/main/div/div[2]/div/div[2]/button')
                            download_btn.click()

                            number_of_checking_download_without_license_btn_visibility = 0
                            try:
                                custom_log("envato_download_file: check for download without license btn", "d")
                                WebDriverWait(driver, 60).until(
                                    EC.visibility_of_element_located((By.XPATH,
                                                                      '/html/body/div[9]/div/div/div/div/form/footer/div[1]/div[2]/button')))
                                custom_log("envato_download_file: without license btn btn has showed up", "d")
                            except Exception as e:
                                custom_log(
                                    "envato_download_file: failed to find without license btn btn", "d")
                            number_of_checking_download_without_license_btn_visibility += 1
                            if number_of_checking_download_without_license_btn_visibility == 3:
                                driver.quit()
                                custom_log(
                                    "envato_download_file: after 3 times of reload, failed to find without license btn btn",
                                    "d")
                                envato_file.is_acceptable_file = False
                                envato_file.save()
                                continue

                            download_without_license_btn = driver.find_element(By.XPATH,
                                                                      '/html/body/div[9]/div/div/div/div/form/footer/div[1]/div[2]/button')
                            download_without_license_btn.click()
                            time.sleep(1)

                        driver.switch_to.new_window(f'tab_download_{i}')
                        driver.get('chrome://downloads')
                        print(f'''driver.execute_script(f"window.open('chrome://downloads', 'tab_downloads');")''')
                        time.sleep(15)
                        while True:
                            download_status = driver.execute_script('''
                                                    var tag = document.querySelector('downloads-manager').shadowRoot;
                                                    var item_tags = tag.querySelectorAll('downloads-item');
                                                    var all_downloaded_items = tag.querySelectorAll('downloads-item');
                                                    var first_download_item = all_downloaded_items[0].shadowRoot;
                                                    var description = first_download_item.querySelector('#description')
                                                    if (description.hidden === true){ return true } else if (description.hidden === false) {
                                                         return false
                                                    }
                                                    ''')
                            print(download_status)
                            if str(download_status) == 'True':
                                print(datetime.datetime.now().time())
                                break
                            time.sleep(15)
                        item_link_item_title = driver.execute_script('''
                                                    var tag = document.querySelector('downloads-manager').shadowRoot
                                                    var item_tags = tag.querySelectorAll('downloads-item');
                                                    var all_downloaded_items = tag.querySelectorAll('downloads-item');
                                                    var first_download_item = all_downloaded_items[0].shadowRoot;
                                                    var item_link = first_download_item.querySelector("#file-link").getAttribute('href');
                                                    var item_title = first_download_item.querySelector("#name").textContent;
                                                    return item_link + " ////// " + item_title
                                                    ''')
                        item_link_item_title = str(item_link_item_title).split(' ////// ')
                        item_link = item_link_item_title[0]
                        item_title = item_link_item_title[1]
                        print(item_link_item_title)
                        envato_file.src_link = item_link
                        envato_file.file.name = str(BASE_DIR / f'media/envato-files/{item_title}')
                        envato_file.save()
                        i += 1
                    custom_log("envato_download_file: finish a list.", "d")
                    return True
                except Exception as e:
                    custom_log("envato_download_file: err: " + str(e), "d")
                number_of_get_accept_cookie_btn_tries += 1
                if number_of_get_accept_cookie_btn_tries == 3:
                    driver.quit()
                    custom_log(
                        "envato_download_file: after 3 times of reload, download has been failed. it means sign-in require",
                        "d")
                    driver.quit()

                    # بررسی اینکه آیا کوکی کار می کند یا خیر
                    envato_auth()
                    custom_log("envato_download_file: waiting for 60 seconds after envato_auth function", "d")
                    time.sleep(60)
                    return False
        except NoSuchElementException as e:
            custom_log('envato_download_file webdriver exception. err: ' + str(e), "d")
            custom_log('we are waiting for ' + str(get_time_sleep()) + ' second', "d")
            time.sleep(get_time_sleep())
        except WebDriverException as e:
            custom_log('envato_download_file webdriver exception. err: ' + str(e), "d")
            custom_log('we are waiting for ' + str(get_time_sleep()) + ' second', "d")
            time.sleep(get_time_sleep())
        except ConnectionError as e:
            custom_log('envato_download_file webdriver exception. err: ' + str(e), "d")
            custom_log('we are waiting for ' + str(get_time_sleep()) + ' second', "d")
            time.sleep(get_time_sleep())
        except Exception as e:
            custom_log('envato_download_file webdriver exception. err: ' + str(e), "d")
            custom_log('we are waiting for ' + str(get_time_sleep()) + ' second', "d")
            time.sleep(get_time_sleep())
        webdriver_problem_number_of_reloading += 1
        if webdriver_problem_number_of_reloading == 3:
            driver.quit()
            custom_log(
                "envato_download_file: webdriver exception caused download to be aborted", 'd')
            settings = get_envato_config_settings()
            settings.login_status = False
            settings.save()
            return False


# ------------ End Scraper functions -------------------


# ------------ Start Calculator Functions -------------------

# ------------ End Calculator Functions -------------------


# ------------ Start Helper Functions -------------------
def envato_sign_in_page():
    url = "https://elements.envato.com/sign-in"
    return url


def check_chrome_connection_status(driver_object):
    for entry in driver_object.get_log('performance'):
        if str(entry['message']).find('"errorText":"net::ERR_TIMED_OUT"') != -1:
            errorText = "net::ERR_NO_SUPPORTED_PROXIES"
            custom_log(errorText, "d")
            return ConnectionError
        elif str(entry['message']).find('"errorText":"net::ERR_NO_SUPPORTED_PROXIES"') != -1:
            errorText = "net::ERR_NO_SUPPORTED_PROXIES"
            custom_log(errorText, "d")
            return ConnectionError
        elif str(entry['message']).find('"errorText":"net::ERR_INTERNET_DISCONNECTED"') != -1:
            errorText = "net::ERR_INTERNET_DISCONNECTED"
            custom_log(errorText, "d")
            return ConnectionError
        elif str(entry['message']).find('"errorText":"net::ERR_CONNECTION_TIMED_OUT"') != -1:
            errorText = "net::ERR_CONNECTION_TIMED_OUT"
            custom_log(errorText, "d")
            return ConnectionError
        elif str(entry['message']).find('"errorText":"net::ERR_CONNECTION_RESET"') != -1:
            errorText = "net::ERR_CONNECTION_RESET"
            custom_log(errorText, "d")
            return ConnectionError
        elif str(entry['message']).find('"errorText":"net::ERR_CONNECTION_REFUSED"') != -1:
            errorText = "net::ERR_CONNECTION_REFUSED"
            custom_log(errorText, "d")
            return ConnectionError
# ------------ End Helper Functions -------------------
