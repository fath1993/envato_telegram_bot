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

from envato.models import config_settings
from envato_telegram_bot.settings import CHROME_DRIVER_PATH, BASE_DIR

d = DesiredCapabilities.CHROME
d['goog:loggingPrefs'] = {'performance': 'ALL'}


# ------------ Start Scraper functions -------------------
def get_time_sleep():
    time_sleep = config_settings().sleep_time
    custom_log("sleep time: " + str(time_sleep), "d")
    return int(time_sleep)


def get_envato_cookie():
    options = Options()
    options.headless = False
    options.add_argument("--window-size=1920,1200")
    settings = config_settings()
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
                        username_input.send_keys(settings.envato_user)
                        password_input.send_keys(settings.envato_pass)
                        sign_in_btn.click()
                        custom_log("get_envato_cookie: waiting for 30 seconds after click sign-in btn", "d")
                        time.sleep(30)
                        cookie_file_path = Path(BASE_DIR / 'envato/cookies/cookies.pkl')
                        pickle.dump(driver.get_cookies(), open(cookie_file_path, "wb"))
                        with cookie_file_path.open(mode="rb") as f:
                            settings.envato_cookie = File(f, name=cookie_file_path.name)
                            settings.save()
                        driver.quit()
                        return True, custom_log('get_envato_cookie:' + str(
                            "https://elements.envato.com/sign-in") + ' | complete', "d")
                    except Exception as e:
                        custom_log("get_envato_cookie: sign-in problem, 60 second passed and button hasnt shown", "d")
                    number_of_sign_in_tries += 1
                    if number_of_sign_in_tries == 3:
                        driver.quit()
                        custom_log(
                            "get_envato_cookie: after 3 times of reload, we cant sign in",
                            "d")
                        break
                except Exception as e:
                    custom_log(
                        "get_envato_cookie: accept_cookie_button problem, 30 second passed and button hasnt shown", "d")
                number_of_get_accept_cookie_btn_tries += 1
                if number_of_get_accept_cookie_btn_tries == 3:
                    driver.quit()
                    custom_log(
                        "get_envato_cookie: after 3 times of reload, there is no sign of accept cookie button",
                        "d")
                    break
            break
        except NoSuchElementException as noelement:
            custom_log('get_envato_cookie no such element exception: ' + str(noelement), "d")
            custom_log('we are waiting for ' + str(get_time_sleep()) + ' second', "d")
            time.sleep(get_time_sleep())
        except WebDriverException as driver_exception:
            custom_log('get_envato_cookie webdriver exception: ' + str(driver_exception), "d")
            custom_log('we are waiting for ' + str(get_time_sleep()) + ' second', "d")
            time.sleep(get_time_sleep())
        except ConnectionError as e:
            raise e
        except Exception as e:
            custom_log('get_envato_cookie other exception: ' + str(e), "d")
            custom_log('we are waiting for ' + str(get_time_sleep()) + ' second', "d")
            time.sleep(get_time_sleep())
        webdriver_problem_number_of_reloading += 1
        if webdriver_problem_number_of_reloading == 3:
            driver.quit()
            return False, custom_log(
                "get_envato_cookie: after reloading had been tried 3 times, this webdriver exceptions still exist", 'd')
    driver.quit()
    return False, custom_log('get_envato_cookie:' + str("https://elements.envato.com/sign-in") + ' | complete with problem', "d")


def check_if_sign_in_is_needed():
    options = Options()
    options.headless = False
    options.add_argument("--window-size=1920,1200")
    settings = config_settings()
    driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, options=options, desired_capabilities=d)

    webdriver_problem_number_of_reloading = 0
    while True:
        try:
            number_of_get_accept_cookie_btn_tries = 0
            while True:
                custom_log("check_if_sign_in_is_needed: starting page load", "d")
                driver.get('https://elements.envato.com/')
                cookies = pickle.load(open(settings.envato_cookie.path, "rb"))
                for cookie in cookies:
                    driver.add_cookie(cookie)
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
                    return False, custom_log("check_if_sign_in_is_needed: sign-in confirmed", "d")
                except Exception as e:
                    custom_log(
                        "check_if_sign_in_is_needed: user detail not found", "d")
                number_of_get_accept_cookie_btn_tries += 1
                if number_of_get_accept_cookie_btn_tries == 3:
                    driver.quit()
                    custom_log(
                        "check_if_sign_in_is_needed: after 3 times of reload, it means sign-in require",
                        "d")
                    break
            break
        except NoSuchElementException as noelement:
            custom_log('check_if_sign_in_is_needed no such element exception: ' + str(noelement), "d")
            custom_log('we are waiting for ' + str(get_time_sleep()) + ' second', "d")
            time.sleep(get_time_sleep())
        except WebDriverException as driver_exception:
            custom_log('check_if_sign_in_is_needed webdriver exception: ' + str(driver_exception), "d")
            custom_log('we are waiting for ' + str(get_time_sleep()) + ' second', "d")
            time.sleep(get_time_sleep())
        except ConnectionError as e:
            raise e
        except Exception as e:
            custom_log('check_if_sign_in_is_needed other exception: ' + str(e), "d")
            custom_log('we are waiting for ' + str(get_time_sleep()) + ' second', "d")
            time.sleep(get_time_sleep())
        webdriver_problem_number_of_reloading += 1
        if webdriver_problem_number_of_reloading == 3:
            driver.quit()
            return True, custom_log("check_if_sign_in_is_needed: after reloading had been tried 3 times, this webdriver exceptions still exist", 'd')
    driver.quit()
    return True, custom_log('check_if_sign_in_is_needed:' + 'sign in require', "d")


def envato_download_file():
    options = Options()
    options.headless = False
    options.add_argument("--window-size=1920,1200")
    settings = config_settings()
    driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, options=options, desired_capabilities=d)

    webdriver_problem_number_of_reloading = 0
    while True:
        try:
            number_of_get_accept_cookie_btn_tries = 0
            while True:
                custom_log("check_if_sign_in_is_needed: starting page load", "d")
                driver.get('https://elements.envato.com/')
                cookies = pickle.load(open(settings.envato_cookie.path, "rb"))
                for cookie in cookies:
                    driver.add_cookie(cookie)
                driver.refresh()
                custom_log("driver.get(url)> url has been fetched. we are waiting for: " + str(get_time_sleep()), 'd')
                time.sleep(get_time_sleep())
                check_chrome_connection_status(driver)
                custom_log("check_if_sign_in_is_needed: check for user detail", "d")
                try:

                    while True:
                        pass
                    custom_log("check_if_sign_in_is_needed: check for user detail", "d")
                    WebDriverWait(driver, 3600).until(
                        EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/nav/div/div/div[1]/div[4]/ul/li/button/div/span')))
                    driver.quit()
                    return False, custom_log("check_if_sign_in_is_needed: sign-in confirmed", "d")
                except Exception as e:
                    custom_log(
                        "check_if_sign_in_is_needed: user detail not found", "d")
                number_of_get_accept_cookie_btn_tries += 1
                if number_of_get_accept_cookie_btn_tries == 3:
                    driver.quit()
                    custom_log(
                        "check_if_sign_in_is_needed: after 3 times of reload, it means sign-in require",
                        "d")
                    break
            break
        except NoSuchElementException as noelement:
            custom_log('check_if_sign_in_is_needed no such element exception: ' + str(noelement), "d")
            custom_log('we are waiting for ' + str(get_time_sleep()) + ' second', "d")
            time.sleep(get_time_sleep())
        except WebDriverException as driver_exception:
            custom_log('check_if_sign_in_is_needed webdriver exception: ' + str(driver_exception), "d")
            custom_log('we are waiting for ' + str(get_time_sleep()) + ' second', "d")
            time.sleep(get_time_sleep())
        except ConnectionError as e:
            raise e
        except Exception as e:
            custom_log('check_if_sign_in_is_needed other exception: ' + str(e), "d")
            custom_log('we are waiting for ' + str(get_time_sleep()) + ' second', "d")
            time.sleep(get_time_sleep())
        webdriver_problem_number_of_reloading += 1
        if webdriver_problem_number_of_reloading == 3:
            driver.quit()
            return True, custom_log("check_if_sign_in_is_needed: after reloading had been tried 3 times, this webdriver exceptions still exist", 'd')
    driver.quit()
    return True, custom_log('check_if_sign_in_is_needed:' + 'sign in require', "d")

# ------------ End Scraper functions -------------------


# ------------ Start Calculator Functions -------------------
def monthly_report_calculator(company_profile_object):
    custom_log("---------------- monthly report calculation start------------------\n", 'd')
    company_object = company_profile_object.company
    monthly_report_comparison_1_4 = None
    monthly_report_comparison_2_5 = None
    monthly_report_comparison_3_6 = None
    is_monthly_report_ready = False
    try:
        latest_monthly_report = MonthlyReport.objects.filter(company=company_object).latest('month_reported_date')
        this_year = latest_monthly_report.month_reported_date.year
        this_month = latest_monthly_report.month_reported_date.month
        custom_log("latest monthly report year: " + str(this_year), "d")
        custom_log("latest monthly report month: " + str(this_month), "d")
        x01 = latest_monthly_report.reported_number
        company_profile_object.monthly_report_1_date = latest_monthly_report.month_reported_date
        if this_month == 1:
            try:
                m2 = MonthlyReport.objects.filter(company=company_object,
                                                  month_reported_date__range=date_range_generator(this_year - 1,
                                                                                                  12)).latest(
                    'month_reported_date')
                x02 = m2.reported_number
                company_profile_object.monthly_report_2_date = m2.month_reported_date
            except:
                custom_log("مشکل در دریافت گزارش ماه یکی مانده به آخر امسال", "d")
                x02 = 0
            try:
                m3 = MonthlyReport.objects.filter(company=company_object,
                                                  month_reported_date__range=date_range_generator(this_year - 1,
                                                                                                  11)).latest(
                    'month_reported_date')
                x03 = m3.reported_number
                company_profile_object.monthly_report_3_date = m3.month_reported_date
            except:
                custom_log("مشکل در دریافت گزارش ماه دوتا مانده به آخر امسال", "d")
                x03 = 0
            try:
                m4 = MonthlyReport.objects.filter(company=company_object,
                                                  month_reported_date__range=date_range_generator(this_year - 1,
                                                                                                  1)).latest(
                    'month_reported_date')
                x04 = m4.reported_number
            except:
                custom_log("مشکل در دریافت گزارش ماه آخر سال قبل", "d")
                x04 = 0
            try:
                m5 = MonthlyReport.objects.filter(company=company_object,
                                                  month_reported_date__range=date_range_generator(this_year - 2,
                                                                                                  12)).latest(
                    'month_reported_date')
                x05 = m5.reported_number
            except:
                custom_log("مشکل در دریافت گزارش ماه یکی مانده به آخر سال قبل", "d")
                x05 = 0
            try:
                m6 = MonthlyReport.objects.filter(company=company_object,
                                                  month_reported_date__range=date_range_generator(this_year - 2,
                                                                                                  11)).latest(
                    'month_reported_date')
                x06 = m6.reported_number
            except:
                custom_log("مشکل در دریافت گزارش ماه دوتا مانده به آخر سال قبل", "d")
                x06 = 0
        elif this_month == 2:
            try:
                m2 = MonthlyReport.objects.filter(company=company_object,
                                                  month_reported_date__range=date_range_generator(this_year,
                                                                                                  1)).latest(
                    'month_reported_date')
                x02 = m2.reported_number
                company_profile_object.monthly_report_2_date = m2.month_reported_date
            except:
                custom_log("مشکل در دریافت گزارش ماه یکی مانده به آخر امسال", "d")
                x02 = 0
            try:
                m3 = MonthlyReport.objects.filter(company=company_object,
                                                  month_reported_date__range=date_range_generator(this_year - 1,
                                                                                                  12)).latest(
                    'month_reported_date')
                x03 = m3.reported_number
                company_profile_object.monthly_report_3_date = m3.month_reported_date
            except:
                custom_log("مشکل در دریافت گزارش ماه دوتا مانده به آخر امسال", "d")
                x03 = 0
            try:
                m4 = MonthlyReport.objects.filter(company=company_object,
                                                  month_reported_date__range=date_range_generator(this_year - 1,
                                                                                                  2)).latest(
                    'month_reported_date')
                x04 = m4.reported_number
            except:
                custom_log("مشکل در دریافت گزارش ماه آخر سال قبل", "d")
                x04 = 0
            try:
                m5 = MonthlyReport.objects.filter(company=company_object,
                                                  month_reported_date__range=date_range_generator(this_year - 1,
                                                                                                  1)).latest(
                    'month_reported_date')
                x05 = m5.reported_number
            except:
                custom_log("مشکل در دریافت گزارش ماه یکی مانده به آخر سال قبل", "d")
                x05 = 0
            try:
                m6 = MonthlyReport.objects.filter(company=company_object,
                                                  month_reported_date__range=date_range_generator(this_year - 2,
                                                                                                  12)).latest(
                    'month_reported_date')
                x06 = m6.reported_number
            except:
                custom_log("مشکل در دریافت گزارش ماه دوتا مانده به آخر سال قبل", "d")
                x06 = 0
        else:
            try:
                m2 = MonthlyReport.objects.filter(company=company_object,
                                                  month_reported_date__range=date_range_generator(this_year,
                                                                                                  this_month - 1)).latest(
                    'month_reported_date')
                x02 = m2.reported_number
                company_profile_object.monthly_report_2_date = m2.month_reported_date
            except:
                custom_log("مشکل در دریافت گزارش ماه یکی مانده به آخر امسال", "d")
                x02 = 0
            try:
                m3 = MonthlyReport.objects.filter(company=company_object,
                                                  month_reported_date__range=date_range_generator(this_year,
                                                                                                  this_month - 2)).latest(
                    'month_reported_date')
                x03 = m3.reported_number
                company_profile_object.monthly_report_3_date = m3.month_reported_date
            except:
                custom_log("مشکل در دریافت گزارش ماه دوتا مانده به آخر امسال", "d")
                x03 = 0
            try:
                m4 = MonthlyReport.objects.filter(company=company_object,
                                                  month_reported_date__range=date_range_generator(this_year - 1,
                                                                                                  this_month)).latest(
                    'month_reported_date')
                x04 = m4.reported_number
            except:
                custom_log("مشکل در دریافت گزارش ماه آخر سال قبل", "d")
                x04 = 0
            try:
                m5 = MonthlyReport.objects.filter(company=company_object,
                                                  month_reported_date__range=date_range_generator(this_year - 1,
                                                                                                  this_month - 1)).latest(
                    'month_reported_date')
                x05 = m5.reported_number
            except:
                custom_log("مشکل در دریافت گزارش ماه یکی مانده به آخر سال قبل", "d")
                x05 = 0
            try:
                m6 = MonthlyReport.objects.filter(company=company_object,
                                                  month_reported_date__range=date_range_generator(this_year - 1,
                                                                                                  this_month - 2)).latest(
                    'month_reported_date')
                x06 = m6.reported_number
            except:
                custom_log("مشکل در دریافت گزارش ماه دوتا مانده به آخر سال قبل", "d")
                x06 = 0
        try:
            c1 = ((x01 / x04) - 1) * 100
            c1 = round(c1, 2)
            custom_log("c1: " + str(c1), "d")
            monthly_report_comparison_1_4 = c1
        except Exception as e:
            custom_log("c1 cant calculate because: " + str(e), "d")
        try:
            c2 = ((x02 / x05) - 1) * 100
            c2 = round(c2, 2)
            custom_log("c2: " + str(c2), "d")
            monthly_report_comparison_2_5 = c2
        except Exception as e:
            custom_log("c2 cant calculate because: " + str(e), "d")
        try:
            c3 = ((x03 / x06) - 1) * 100
            c3 = round(c3, 2)
            custom_log("c3: " + str(c3), "d")
            monthly_report_comparison_3_6 = c3
        except Exception as e:
            custom_log("c3 cant calculate because: " + str(e), "d")
        if monthly_report_comparison_1_4 is None:
            custom_log("monthly report comparison 1_4: None ", "d")
        else:
            custom_log("monthly report comparison 1_4: " + str(monthly_report_comparison_1_4), "d")

        if monthly_report_comparison_2_5 is None:
            custom_log("monthly report comparison 2_5: None ", "d")
        else:
            custom_log("monthly report comparison 2_5: " + str(monthly_report_comparison_2_5), "d")

        if monthly_report_comparison_3_6 is None:
            custom_log("monthly report comparison 3_6: None ", "d")
        else:
            custom_log("monthly report comparison 3_6: " + str(monthly_report_comparison_3_6), "d")

        if monthly_report_comparison_1_4 and monthly_report_comparison_2_5 and monthly_report_comparison_3_6 is not None:
            is_monthly_report_ready = True
            custom_log("is all report ok?: " + "True", "d")
        else:
            is_monthly_report_ready = False
            custom_log("is all report ok?: " + "False", "d")
    except Exception as e:
        custom_log("this is monthly main exception: " + str(e), "d")

    company_profile_object.monthly_report_comparison_1_4 = monthly_report_comparison_1_4
    company_profile_object.monthly_report_comparison_2_5 = monthly_report_comparison_2_5
    company_profile_object.monthly_report_comparison_3_6 = monthly_report_comparison_3_6
    company_profile_object.is_monthly_report_ready = is_monthly_report_ready
    company_profile_object.save()
    custom_log("---------------- monthly report calculation end------------------\n", 'd')


def seasonal_report_calculator(company_profile_object):
    custom_log("---------------- seasonal report calculation starts ------------------\n", 'd')
    company_object = company_profile_object.company
    latest_seasonal_report = SeasonalReport.objects.filter(company=company_object).latest('season_reported_date')
    this_year = latest_seasonal_report.season_reported_date.year
    custom_log("latest seasonal report year: " + str(this_year), "d")
    this_month = latest_seasonal_report.season_reported_date.month
    custom_log("latest seasonal report month: " + str(this_month), "d")

    if this_month == 1 or this_month == 2 or this_month == 3:
        # spring
        spring_report = latest_seasonal_report
        company_profile_object.seasonal_report_spring_date_order = 1

        # summer
        summer_date_range_from = jdatetime.date(year=(this_year - 1), month=4, day=1)
        summer_date_range_to = jdatetime.date(year=(this_year - 1), month=6, day=31)
        summer_report = SeasonalReport.objects.filter(company=company_object,
                                                      season_reported_date__range=[summer_date_range_from,
                                                                                   summer_date_range_to]).latest(
            'season_reported_date')
        company_profile_object.seasonal_report_summer_date_order = 4

        # fall
        fall_date_range_from = jdatetime.date(year=(this_year - 1), month=7, day=1)
        fall_date_range_to = jdatetime.date(year=(this_year - 1), month=9, day=30)
        fall_report = SeasonalReport.objects.filter(company=company_object,
                                                    season_reported_date__range=[fall_date_range_from,
                                                                                 fall_date_range_to]).latest(
            'season_reported_date')
        company_profile_object.seasonal_report_fall_date_order = 3

        # winter
        winter_date_range_from = jdatetime.date(year=(this_year - 1), month=10, day=1)
        winter_date_range_to = jdatetime.date(year=(this_year - 1), month=12, day=30)
        winter_report = SeasonalReport.objects.filter(company=company_object,
                                                      season_reported_date__range=[winter_date_range_from,
                                                                                   winter_date_range_to]).latest(
            'season_reported_date')
        company_profile_object.seasonal_report_winter_date_order = 2
    elif this_month == 4 or this_month == 5 or this_month == 6:
        # spring
        spring_date_range_from = jdatetime.date(year=this_year, month=1, day=1)
        spring_date_range_to = jdatetime.date(year=this_year, month=3, day=31)
        spring_report = SeasonalReport.objects.filter(company=company_object,
                                                      season_reported_date__range=[spring_date_range_from,
                                                                                   spring_date_range_to]).latest(
            'season_reported_date')
        company_profile_object.seasonal_report_spring_date_order = 2

        # summer
        summer_report = latest_seasonal_report
        company_profile_object.seasonal_report_summer_date_order = 1

        # fall
        fall_date_range_from = jdatetime.date(year=(this_year - 1), month=7, day=1)
        fall_date_range_to = jdatetime.date(year=(this_year - 1), month=9, day=30)
        fall_report = SeasonalReport.objects.filter(company=company_object,
                                                    season_reported_date__range=[fall_date_range_from,
                                                                                 fall_date_range_to]).latest(
            'season_reported_date')
        company_profile_object.seasonal_report_fall_date_order = 4

        # winter
        winter_date_range_from = jdatetime.date(year=(this_year - 1), month=10, day=1)
        winter_date_range_to = jdatetime.date(year=(this_year - 1), month=12, day=30)
        winter_report = SeasonalReport.objects.filter(company=company_object,
                                                      season_reported_date__range=[winter_date_range_from,
                                                                                   winter_date_range_to]).latest(
            'season_reported_date')
        company_profile_object.seasonal_report_winter_date_order = 3
    elif this_month == 7 or this_month == 8 or this_month == 9:
        # spring
        spring_date_range_from = jdatetime.date(year=this_year, month=1, day=1)
        spring_date_range_to = jdatetime.date(year=this_year, month=3, day=31)
        spring_report = SeasonalReport.objects.filter(company=company_object,
                                                      season_reported_date__range=[spring_date_range_from,
                                                                                   spring_date_range_to]).latest(
            'season_reported_date')
        company_profile_object.seasonal_report_spring_date_order = 3

        # summer
        summer_date_range_from = jdatetime.date(year=this_year, month=4, day=1)
        summer_date_range_to = jdatetime.date(year=this_year, month=6, day=31)
        summer_report = SeasonalReport.objects.filter(company=company_object,
                                                      season_reported_date__range=[summer_date_range_from,
                                                                                   summer_date_range_to]).latest(
            'season_reported_date')
        company_profile_object.seasonal_report_summer_date_order = 2

        # fall
        fall_report = latest_seasonal_report
        company_profile_object.seasonal_report_fall_date_order = 1

        # winter
        winter_date_range_from = jdatetime.date(year=(this_year - 1), month=10, day=1)
        winter_date_range_to = jdatetime.date(year=(this_year - 1), month=12, day=30)
        winter_report = SeasonalReport.objects.filter(company=company_object,
                                                      season_reported_date__range=[winter_date_range_from,
                                                                                   winter_date_range_to]).latest(
            'season_reported_date')
        company_profile_object.seasonal_report_winter_date_order = 4
    else:
        # spring
        spring_date_range_from = jdatetime.date(year=this_year, month=1, day=1)
        spring_date_range_to = jdatetime.date(year=this_year, month=3, day=31)
        spring_report = SeasonalReport.objects.filter(company=company_object,
                                                      season_reported_date__range=[spring_date_range_from,
                                                                                   spring_date_range_to]).latest(
            'season_reported_date')
        company_profile_object.seasonal_report_spring_date_order = 4

        # summer
        summer_date_range_from = jdatetime.date(year=this_year, month=4, day=1)
        summer_date_range_to = jdatetime.date(year=this_year, month=6, day=31)
        summer_report = SeasonalReport.objects.filter(company=company_object,
                                                      season_reported_date__range=[summer_date_range_from,
                                                                                   summer_date_range_to]).latest(
            'season_reported_date')
        company_profile_object.seasonal_report_summer_date_order = 3

        # fall
        fall_date_range_from = jdatetime.date(year=this_year, month=7, day=1)
        fall_date_range_to = jdatetime.date(year=this_year, month=9, day=30)
        fall_report = SeasonalReport.objects.filter(company=company_object,
                                                    season_reported_date__range=[fall_date_range_from,
                                                                                 fall_date_range_to]).latest(
            'season_reported_date')
        company_profile_object.seasonal_report_fall_date_order = 2

        # winter
        winter_report = latest_seasonal_report
        company_profile_object.seasonal_report_winter_date_order = 1

    # spring
    seasonal_report_spring_percentage = spring_report.reported_percentage
    seasonal_report_spring_color = spring_report.reported_percentage_color
    seasonal_report_spring_date = spring_report.season_reported_date
    custom_log("seasonal report spring date: " + str(seasonal_report_spring_date), "d")
    custom_log("seasonal report spring percentage: " + str(seasonal_report_spring_percentage), "d")
    custom_log("seasonal report spring color: " + str(seasonal_report_spring_color), "d")

    # summer
    seasonal_report_summer_percentage = summer_report.reported_percentage
    seasonal_report_summer_color = summer_report.reported_percentage_color
    seasonal_report_summer_date = summer_report.season_reported_date
    custom_log("seasonal report summer date: " + str(seasonal_report_summer_date), "d")
    custom_log("seasonal report summer percentage: " + str(seasonal_report_summer_percentage), "d")
    custom_log("seasonal report summer color: " + str(seasonal_report_summer_color), "d")

    # fall
    seasonal_report_fall_percentage = fall_report.reported_percentage
    seasonal_report_fall_color = fall_report.reported_percentage_color
    seasonal_report_fall_date = fall_report.season_reported_date
    custom_log("seasonal report fall date: " + str(seasonal_report_fall_date), "d")
    custom_log("seasonal report fall percentage: " + str(seasonal_report_fall_percentage), "d")
    custom_log("seasonal report fall color: " + str(seasonal_report_fall_color), "d")

    # winter
    seasonal_report_winter_percentage = winter_report.reported_percentage
    seasonal_report_winter_color = winter_report.reported_percentage_color
    seasonal_report_winter_date = winter_report.season_reported_date
    custom_log("seasonal report winter date: " + str(seasonal_report_winter_date), "d")
    custom_log("seasonal report winter percentage: " + str(seasonal_report_winter_percentage), "d")
    custom_log("seasonal report winter color: " + str(seasonal_report_winter_color), "d")

    company_profile_object.seasonal_report_spring_percentage = seasonal_report_spring_percentage
    company_profile_object.seasonal_report_spring_color = seasonal_report_spring_color
    company_profile_object.seasonal_report_spring_date = seasonal_report_spring_date

    company_profile_object.seasonal_report_summer_percentage = seasonal_report_summer_percentage
    company_profile_object.seasonal_report_summer_color = seasonal_report_summer_color
    company_profile_object.seasonal_report_summer_date = seasonal_report_summer_date

    company_profile_object.seasonal_report_fall_percentage = seasonal_report_fall_percentage
    company_profile_object.seasonal_report_fall_color = seasonal_report_fall_color
    company_profile_object.seasonal_report_fall_date = seasonal_report_fall_date

    company_profile_object.seasonal_report_winter_percentage = seasonal_report_winter_percentage
    company_profile_object.seasonal_report_winter_color = seasonal_report_winter_color
    company_profile_object.seasonal_report_winter_date = seasonal_report_winter_date

    if seasonal_report_spring_percentage is not None or seasonal_report_summer_percentage is not None \
            or seasonal_report_fall_percentage is not None or seasonal_report_winter_percentage is not None:
        company_profile_object.is_seasonal_report_ready = True
    company_profile_object.save()
    custom_log("---------------- seasonal report calculation ends ------------------\n", 'd')


def seasonal_report_operating_ratio_calculator(company_profile_object):
    custom_log("---------------- seasonal report operating ratio calculator starts ------------------\n", 'd')
    company = company_profile_object.company
    seasonal_reports = SeasonalReport.objects.filter(company=company)
    three_month_reports = []
    for report in seasonal_reports:
        if report.report_time_period == '3 ماهه':
            three_month_reports.append(report)
            report.operating_ratio = int(round(((report.gross_profit_and_loss / report.operating_income) * 100), 0))
            report.save()
    custom_log("three_month_reports: " + str(three_month_reports), 'd')

    for report in seasonal_reports:
        if report.report_time_period != '3 ماهه':
            for three_month_report in three_month_reports:
                if report.season_reported_date.year == three_month_report.season_reported_date.year:
                    report.operating_ratio = int(
                        round((((report.gross_profit_and_loss - three_month_report.gross_profit_and_loss) / (
                                report.operating_income - three_month_report.operating_income)) * 100), 0))
                    report.save()
                    custom_log("report company name: " + str(report.report_title) + ' report date: ' + str(
                        report.season_reported_date), 'd')
                    custom_log("source three_month_report: " + str(three_month_report.season_reported_date), 'd')
                    break
            custom_log('--------')
    custom_log("---------------- seasonal report operating ratio calculator ends ------------------\n", 'd')


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
