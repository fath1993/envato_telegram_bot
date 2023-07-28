import threading
import ctypes
import jdatetime
import time

from custom_logs.models import custom_log


def codal_scraper():
    while True:
        # from first page
        custom_log("the robot has started task 1", 'p')
        check_and_update_data_with_first_page()
        # from custom link
        company_link_objects = CompanyLink.objects.filter()
        while company_link_objects.count() != 0:
            company_link_object = company_link_objects.latest('id')
            company_badge = company_link_object.badge
            company_link = company_link_object.link
            custom_log("cbot - نماد کمپانی : \n" + str(company_badge), 'p')
            custom_log("cbot - لینک کمپانی : \n" + str(company_link), 'p')
            n = 1
            while True:
                try:
                    while not check_if_last_page(codal_monthly_report_page(company_link, n)):
                        custom_log(str(get_time_sleep()) + " seconds delay after checking " + company_badge + " monthly last page", 'p')
                        time.sleep(get_time_sleep())
                        check_and_update_data_with_first_page()
                        while True:
                            try:
                                custom_log("check and update " + company_badge + " monthly report", 'p')
                                get_codal_data(codal_monthly_report_page(company_link, n))
                                custom_log(str(get_time_sleep()) + " seconds delay after getting monthly report", 'p')
                                time.sleep(get_time_sleep())
                                break
                            except Exception as e:
                                custom_log("problem has happened during the event: " + str(e), 'p')
                                check_proxy_is_available()
                        n += 1
                    break
                except Company.DoesNotExist as e:
                    custom_log("company problem: " + str(e), 'p')
                    n += 1
                except Exception as e:
                    custom_log("problem has happened during the event: " + str(e), 'p')
                    check_proxy_is_available()
            n = 1
            while True:
                try:
                    while not check_if_last_page(codal_seasonal_report_page(company_link, n)):
                        custom_log(
                            str(get_time_sleep()) + " second delay after checking " + company_badge + " seasonal last page",
                            'p')
                        time.sleep(get_time_sleep())
                        check_and_update_data_with_first_page()
                        while True:
                            try:
                                custom_log("check and update " + company_badge + " seasonal report", 'p')
                                get_codal_data(codal_seasonal_report_page(company_link, n))
                                custom_log(str(get_time_sleep()) + " second delay after getting seasonal report", 'p')
                                time.sleep(get_time_sleep())
                                break
                            except Company.DoesNotExist as e:
                                custom_log("company problem : " + str(e), 'p')
                                break
                            except Exception as e:
                                custom_log("problem has happened during the event: " + str(e), 'p')
                                check_proxy_is_available()
                        n += 1
                    break
                except Company.DoesNotExist as e:
                    custom_log("company problem : " + str(e), 'p')
                    n += 1
                except Exception as e:
                    custom_log("problem has happened during the event : " + str(e), 'p')
                    check_proxy_is_available()
            monthly_reports = MonthlyReport.objects.filter(is_finished=False)
            for monthly_report in monthly_reports:
                while True:
                    try:
                        custom_log("getting monthly report data for: " + str(monthly_report.report_title), 'p')
                        get_monthly_report_number(monthly_report)
                        custom_log("monthly report data has been fetched successfully for:  " + str(monthly_report.report_title) + " we are waiting for " + str(
                            get_time_sleep()) + " seconds",
                                   'p')
                        time.sleep(get_time_sleep())
                        break
                    except Company.DoesNotExist as e:
                        custom_log("company problem : " + str(e), 'p')
                        break
                    except Exception as e:
                        custom_log("problem has happened during the event : " + str(e), 'p')
                        check_proxy_is_available()
                check_and_update_data_with_first_page()
            seasonal_reports = SeasonalReport.objects.filter(is_finished=False)
            for seasonal_report in seasonal_reports:
                while True:
                    try:
                        custom_log("getting seasonal report data for: " + str(seasonal_report.report_title), 'p')
                        get_seasonal_report_number(seasonal_report)
                        custom_log("seasonal report data has been fetched successfully for:  " + str(seasonal_report.report_title) + " we are waiting for " + str(
                            get_time_sleep()) + " seconds",
                                   'p')
                        time.sleep(get_time_sleep())
                        break
                    except Company.DoesNotExist as e:
                        custom_log("company problem : " + str(e), 'p')
                        break
                    except Exception as e:
                        custom_log("problem has happened during the event : " + str(e), 'p')
                        check_proxy_is_available()
                while True:
                    try:
                        custom_log("check and update data with first page", 'p')
                        get_codal_data(codal_first_page())
                        custom_log(str(get_time_sleep()) + "second delay after updating data with first page", 'p')
                        time.sleep(get_time_sleep())
                        break
                    except Company.DoesNotExist as e:
                        custom_log("company problem : " + str(e), 'p')
                        break
                    except Exception as e:
                        custom_log("problem has happened during the event : " + str(e), 'p')
                        check_proxy_is_available()
            company_link_object.delete()
            custom_log("---------------------------------- next -------------------------------", 'p')
        custom_log("the robot has finished task 1", 'p')

        # from first page
        custom_log("the robot has started task 2", 'p')
        check_and_update_data_with_first_page()
        monthly_reports = MonthlyReport.objects.filter(is_finished=False)
        for monthly_report in monthly_reports:
            while True:
                try:
                    custom_log("getting monthly report data for: " + str(monthly_report.report_title), 'p')
                    get_monthly_report_number(monthly_report)
                    custom_log("monthly report data has been fetched successfully for:  " + str(
                        monthly_report.report_title) + " we are waiting for " + str(
                        get_time_sleep()) + " seconds",
                               'p')
                    time.sleep(get_time_sleep())
                    break
                except Company.DoesNotExist as e:
                    custom_log("company problem : " + str(e), 'p')
                    break
                except Exception as e:
                    custom_log("problem has happened during the event : " + str(e), 'p')
                    check_proxy_is_available()
            check_and_update_data_with_first_page()
        seasonal_reports = SeasonalReport.objects.filter(is_finished=False)
        for seasonal_report in seasonal_reports:
            while True:
                try:
                    custom_log("getting seasonal report data for: " + str(seasonal_report.report_title), 'p')
                    get_seasonal_report_number(seasonal_report)
                    custom_log("seasonal report data has been fetched successfully for:  " + str(
                        seasonal_report.report_title) + " we are waiting for " + str(
                        get_time_sleep()) + " seconds",
                               'p')
                    time.sleep(get_time_sleep())
                    break
                except Company.DoesNotExist as e:
                    custom_log("company problem : " + str(e), 'p')
                    break
                except Exception as e:
                    custom_log("problem has happened during the event : " + str(e), 'p')
                    check_proxy_is_available()
            while True:
                try:
                    custom_log("check and update data with first page", 'p')
                    get_codal_data(codal_first_page())
                    custom_log(str(get_time_sleep()) + "second delay after updating data with first page", 'p')
                    time.sleep(get_time_sleep())
                    break
                except Company.DoesNotExist as e:
                    custom_log("company problem : " + str(e), 'p')
                    break
                except Exception as e:
                    custom_log("problem has happened during the event : " + str(e), 'p')
                    check_proxy_is_available()
        custom_log("the robot has finished task 2", 'p')


def company_profile_updater():
    while True:
        company_profiles = CompanyProfile.objects.filter()
        for company_profile in company_profiles:
            try:
                custom_log("company_profile_updater> start", 'd')
                monthly_report_calculator(company_profile)
                seasonal_report_calculator(company_profile)
                seasonal_report_operating_ratio_calculator(company_profile)
            except Exception as e:
                custom_log("company_profile_updater>try/except err: " + str(e), 'd')
            custom_log("company_profile_updater> finish", 'd')
            custom_log("company_profile_updater> waiting for 1 hour", 'd')
        time.sleep(3600)


def check_and_update_data_with_first_page():
    while True:
        try:
            custom_log("check and update data with first page", 'p')
            get_codal_data(codal_first_page())
            custom_log(str(get_time_sleep()) + "second delay after updating data with first page", 'p')
            time.sleep(get_time_sleep())
            break
        except Exception as e:
            custom_log("problem has happened during the event : " + str(e), 'p')
            if CODAL_SCRAPER_SETTINGS.is_proxy_on:
                while True:
                    custom_log("checking proxy...", 'p')
                    if check_proxy_availability(get_proxy()):
                        break
                    else:
                        custom_log("proxies are not connectable. pls upgrade theme", 'p')
                        custom_log("we check proxy list again after 5 minute", 'p')
                        time.sleep(300)
                    if not CODAL_SCRAPER_SETTINGS.is_proxy_on:
                        break


def check_proxy_is_available():
    if CODAL_SCRAPER_SETTINGS.is_proxy_on:
        while True:
            custom_log("checking proxy...", 'p')
            if check_proxy_availability(get_proxy()):
                break
            else:
                custom_log("proxies are not connectable. pls upgrade theme", 'p')
                custom_log("we check proxy list again after 5 minute", 'p')
                time.sleep(300)
            if not CODAL_SCRAPER_SETTINGS.is_proxy_on:
                break


class CodalScraperThread(threading.Thread):
    def run(self):
        codal_scraper()

    def get_id(self):
        return self.native_id

    def raise_exception(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')


class CompanyProfileUpdaterThread(threading.Thread):
    def run(self):
        company_profile_updater()
