from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException, ElementClickInterceptedException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from utils import config_setup
from database_connections import db_base
from utils import data_helpers, file_helpers, database_helpers
from dateutil.parser import parse
import time

# this is the parent of all pages #
from utils.performance_helpers import Performance


class BasePage:
    def __init__(self, driver,
                 master_config=config_setup.master_config(),
                 config=config_setup.config()):
        self.driver = driver
        self.master_config = master_config
        self.config = config
        self.data_helpers = data_helpers
        self.file_helpers = file_helpers
        self.database_helpers = database_helpers

    def wait(self, timeout, ignored_exceptions: list = None):
        """Initializes WebDriverWait"""
        return WebDriverWait(self.driver, timeout, ignored_exceptions=ignored_exceptions)

    # click methods #
    def click_element(self, by_locator=None, how=None, path=None, ajax=True, alert=False, element=None):
        perf = Performance(self.driver)
        timing = None

        if ajax:
            self.wait_for_ajax()

        if by_locator is not None:
            try:
                self.get_web_element(by_locator).click()
            except:
                self.scroll_to_and_click(by_locator)
            if not alert:
                timing = perf.get()
        elif how is not None:
            try:
                self.get_web_elements(how, path, ajax)[0].click()
            except:
                self.scroll_to_and_click(how=how, path=path)
            if not alert:
                timing = perf.get()
        elif element is not None:
            element.click()
            if not alert:
                timing = perf.get()

        if alert:
            text = self.wait_for_alert_and_get_text()
            return text
        if ajax:
            # checks for a soothing thoughts error after clicking
            if "/admin/notify/show" in self.driver.current_url:
                raise Exception("A PS error was raised after clicking on the element")
            self.wait_for_ajax()

        return timing

    def scroll_to_and_click(self, by_locator=None, how=None, path=None, element=None, alert=False):
        self.wait_for_ajax()
        if element is not None:
            el = element
        elif by_locator is not None:
            el = self.get_web_element(by_locator)
        else:
            el = self.get_web_elements(how, path)[0]
        self.scroll_to_js(el)
        self.wait_for_ajax()
        el.click()
        if alert:
            self.wait_for_and_accept_alert()
        self.wait_for_ajax()

    def scroll_to_bottom(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        self.sleep(1.5)

    def scroll_to_top(self):
        self.driver.execute_script("window.scrollTo(0, 0)")
        self.sleep(1.5)

    def scroll_to_halfpage(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2)")
        self.sleep(1.5)

    def scroll_element_to_center(self, element):
        action = ActionChains(self.driver)
        action.move_to_element(element).perform()

    # preferably this method can be used to scroll inside an iframe, although it works on elements not inside an iframe as well
    def scroll_into_view(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        self.sleep(1.5)

    # text_box_methods #
    def fill_out_text_field(self, by_locator, value):
        el = self.get_web_element(by_locator)
        el.click()
        el.clear()
        el.send_keys(value)

    def scroll_to_and_fill_out_text_field(self, value, by_locator=None, how=None, path=None):
        if by_locator is not None:
            el = self.get_web_element(by_locator)
        else:
            el = self.get_web_elements(how, path)[0]
        self.scroll_to_js(el)
        self.wait_for_ajax()
        el.click();
        el.clear()
        el.send_keys(value)

    # if there is no by_locator for the text field, use this method to pass in a how and a path
    def fill_out_text_field_no_locator(self, how, path, value):
        el = self.get_web_elements(how, path)[0]
        el.click()
        el.clear()
        el.send_keys(value)

    def fill_out_text_field_date_picker(self, by_locator, string):
        el = self.get_web_element(by_locator)
        el.click()
        el.clear()
        self.wait_for_ajax()
        el.send_keys(string)
        el.send_keys(Keys.ESCAPE)

    def fill_out_text_field_date_picker_no_locator(self, how, path, string):
        el = self.get_web_elements(how=how, path=path)[0]
        el.click()
        el.clear()
        self.wait_for_ajax()
        el.send_keys(string)
        el.send_keys(Keys.ESCAPE)

    def fill_out_text_field_by_element(self, web_element, value):
        web_element.click()
        web_element.clear()
        self.wait_for_ajax()
        web_element.send_keys(value)

    # Instead of text, send a key such as Keys.TAB, Keys.ENTER, etc.
    def send_key_to_text_field(self, by_locator, key):
        el = self.get_web_element(by_locator)
        el.click()
        el.send_keys(key)

    def send_key_to_text_field_2(self, by_locator, key):
        el = self.get_web_element(by_locator)
        el.click()
        el.clear()
        el.send_keys(key)

    def send_key_to_text_field_no_locator(self, how, path, keys):
        el = self.get_web_elements(how, path)[0]
        el.click()
        el.send_keys(keys)

    # get text methods #

    def get_element_text(self, by_locator=None, how=None, path=None, element=None):
        if by_locator is not None:
            el = self.get_web_element(by_locator).text
        elif how is not None:
            temp = self.get_web_elements(how, path)[0]
            el = temp.text
        elif element is not None:
            el = element.text
        return el

    def get_elements_text(self, how, path):
        els = self.get_web_elements(how, path)
        text = map(lambda x: x.text, els)
        return list(text)

    def get_text_field_text(self, by_locator=None, how=None, path=None):
        if by_locator:
            el = self.get_element_attribute(by_locator, 'value')
        else:
            el = self.get_elements_attribute(how=how, path=path, attribute='value')[0]
        return el

    # checkbox methods #

    def checkbox_actions(self, by_locator=None, how=None, path=None, check=True, element=None):
        if element is None:
            if by_locator is not None:
                el = self.get_web_element(by_locator)
            else:
                el = self.get_web_elements(how, path)[0]
        else:
            el = element

        if check and el.get_attribute("checked") is None:
            el.click()
        elif not check and el.get_attribute("checked") == "true":
            el.click()
        self.wait_for_ajax()

    def is_checkbox_checked(self, by_locator=None, how=None, path=None, element=None):
        if element is None:
            if by_locator is not None:
                el = self.get_web_element(by_locator)
            else:
                el = self.get_web_elements(how, path)[0]
        else:
            el = element

        if el.get_attribute("checked") == "true":
            return True
        else:
            return False

    def checkbox_by_label(self, how, label_path, checkbox_path, checked=True):
        el_label = self.get_web_elements(how, label_path)[0]
        el_checkbox = self.get_web_elements(how, checkbox_path)[0]
        if el_checkbox.is_selected() and not checked:
            el_label.click()
        elif not el_checkbox.is_selected() and checked:
            el_label.click()

    def checkbox_by_label_with_element(self, label_el, checkbox_el, checked=True):
        if checkbox_el.is_selected() and not checked:
            label_el.click()
        elif not checkbox_el.is_selected() and checked:
            label_el.click()

    def check_multiple_boxes_by_label_name(self, labels_xpath, checkbox_input_xpaths, checkbox_name_array, check=True):
        """This takes an array of checkbox label names and will click on each one"""
        element_array = self.get_web_elements("xpath", labels_xpath)
        checked_status = self.get_elements_attribute("xpath", checkbox_input_xpaths, "checked")
        text = list(map(lambda x: x.text, element_array))

        for name in checkbox_name_array:
            if name in text:
                index = text.index(name)
                if not checked_status[index] and check:
                    element_array[index].click()
                elif checked_status[index] == 'true' and not check:
                    element_array[index].click()

    # get attribute methods #
    def get_element_attribute(self, by_locator, attribute, wait=10):
        el = self.get_web_element(by_locator, wait=wait)
        return el.get_attribute(attribute)

    def get_elements_attribute(self, how, path, attribute):
        attrs = []
        els = self.get_web_elements(how, path)
        for i in els:
            attrs.append(i.get_attribute(attribute))
        return attrs

    # select methods #
    def select_list_by_text(self, by_locator=None, value=None, select_object=None):
        if select_object is None:
            el = self.get_web_element(by_locator)
            select = Select(el)
        else:
            select = select_object
        select.select_by_visible_text(value)

    def deselect_all_list_items(self, by_locator=None, select_object=None):
        if select_object is None:
            el = self.get_web_element(by_locator)
            select = Select(el)
        else:
            select = select_object
        select.deselect_all()

    def select_list_by_index(self, by_locator=None, how=None, path=None, index=None):
        if by_locator is not None:
            el = self.get_web_element(by_locator)
        else:
            el = self.get_web_elements(how, path)[0]
        select = Select(el)
        select.select_by_index(index)

    def select_list_by_text_no_locator(self, how, path, value):
        el = self.get_web_elements(how, path)[0]
        select = Select(el)
        select.select_by_visible_text(value)

    def select_list_by_value(self, by_locator, value):
        el = self.get_web_element(by_locator)
        select = Select(el)
        select.select_by_value(value)

    def select_list_options(self, by_locator=None, how=None, path=None):
        if by_locator is not None:
            el = self.get_web_element(by_locator)
        else:
            el = self.get_web_elements(how=how, path=path)[0]
        select = Select(el)
        return select.options

    def select_list_options_text(self, by_locator=None, how=None, path=None):
        if by_locator is not None:
            el = self.get_web_element(by_locator)
        else:
            el = self.get_web_elements(how, path)[0]
        select = Select(el)
        my_list = select.options
        return list(map(lambda x: x.text, my_list))

    # this returns the text of the selected option
    def get_selected_option(self, by_locator):
        el = self.get_web_element(by_locator)
        select = Select(el)
        return select.first_selected_option.text

    def select_list_select_all(self, how, path):
        el = self.get_web_elements(how, path)
        for i in el:
            i.click()
            self.wait_for_ajax()

    # this method takes either a singular benefit (String) or several (Array) as the 'options' argument
    def multiselect_options_by_text(self, by_locator=None, how=None, path=None, options=None):
        bool = by_locator is not None
        if bool:
            el_list = self.select_list_options(by_locator)
            text_fields = self.select_list_options_text(by_locator)
            el_text = list(text_fields)
        else:
            el_list = self.select_list_options(how, path)
            text_fields = self.select_list_options_text(how=how, path=path)
            el_text = list(text_fields)

        if isinstance(options, str):
            if bool:
                self.select_list_by_text(by_locator, options)
            else:
                self.select_list_by_text_no_locator(how, path, options)

        if isinstance(options, list):
            for i in options:
                if i in el_text:
                    index = el_text.index(i)
                    el_list[index].click()

    # elements displayed method can be used when you have an xpath or an ID or when you are wanting to check for multiple elements#
    def elements_displayed(self, how, path, wait=3):
        count = 0
        displayed_list = []

        my_list = self.get_web_elements(how, path, wait=wait)
        while not my_list and count < wait:
            self.sleep(0.5)
            count += 1
            my_list = self.get_web_elements(how, path, wait=wait)

        for i in my_list:
            if i.is_displayed():
                displayed_list.append(i)

        if not my_list or not displayed_list:
            return False
        elif displayed_list:
            return True

    # element_displayed should be the preferred method when you have a by locator/aren't needing interpolation

    def element_displayed(self, by_locator, wait=3):
        try:
            el = WebDriverWait(self.driver, wait).until(EC.visibility_of_element_located(by_locator))
            if el.is_displayed():
                return True
        except(TimeoutException, WebDriverException):
            return False

    def element_enabled(self, by_locator=None, how=None, path=None, element=None):
        if element is not None:
            el = element
        elif by_locator is not None:
            el = self.get_web_element(by_locator)
        else:
            el = self.get_web_elements(how, path)[0]
        return el.is_enabled()

    def wait_until_element_enabled(self, by_locator=None, how=None, path=None):
        if by_locator is not None:
            el = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(by_locator))
        else:
            count = 0
            el = self.get_web_elements(how, path)
            while not el and count <= 2:
                el = self.get_web_elements(how, path)
                count += 1
            if el:
                while not el[0].is_enabled and count <= 10:
                    count += 1
                    self.sleep(0.5)

    # element present/exists methods #

    def does_element_exist(self, by_locator=None, how=None, path=None, ajax=True, timeout=10):
        if ajax:
            self.wait_for_ajax()

        if by_locator is not None:
            try:
                el = WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(by_locator))
                if el:
                    bool_check = True
            except(TimeoutException, WebDriverException):
                bool_check = False
        else:
            els = self.get_web_elements(how, path, wait=0)
            if els:
                bool_check = True
            else:
                bool_check = False

        return bool_check

    # goto methods
    def goto_page(self, page_url):
        self.driver.get(page_url)
        if "/admin/notify/show" in self.driver.current_url:
            raise Exception(f"A PS error was raised after navigating directly to {page_url}")

    def refresh_page(self, wait=None):
        if wait:
            self.sleep(wait)
        self.driver.refresh()

    # use this if you want to check that an element is not displayed without the built in Expected Conditions wait
    def short_check_for_displayed_elements(self, how, path):
        if how == "xpath":
            try:
                el = self.driver.find_element_by_xpath(path)
                return True
            except:
                print("Element not found")
                return False
        elif how == "id":
            try:
                el = self.driver.find_element_by_id(path)
                return True
            except:
                print("Element not found")
                return False

    # get web element and elements methods #
    def get_xpath_el(self, path, timeout=10, max_attempts=5):
        """Finds the DOM element that matches the `xpath` selector.
        * If timeout > 0, waits the equivalent seconds.
        * If timeout=0, poll the DOM immediately without any waiting
        * Use this to return the first found element in the xpath

        Args:
            path: The selector to use
            timeout: The number of seconds to wait
            max_attempts: The amount of times to try finding the element. Useful for when enrollment is the worst
        Returns:
            The first element that is found, even if multiple elements match"""
        by = By.XPATH
        if "/admin/notify/show" in self.driver.current_url:
            raise Exception("A PS error was raised")

        if timeout == 0:
            element = self.driver.find_element(by, path)
        else:
            element = self._wait_for_selector(by, path, max_attempts=max_attempts)
        return element

    def get_xpath_els(self, path, timeout=10, max_attempts=5):
        """Finds the DOM element that matches the `xpath` selector.
        * If timeout > 0, waits the equivalent seconds.
        * If timeout=0, poll the DOM immediately without any waiting
        * Use this to return multiple elements in the xpath

        Args:
            path: The selector to use
            timeout: The number of seconds to wait
            max_attempts: The amount of times to try finding the element. Useful for when enrollment is the worst
        Returns:
            A list of the found elements. """
        by = By.XPATH

        if "/admin/notify/show" in self.driver.current_url:
            raise Exception("A PS error was raised")

        try:
            if timeout == 0:
                elements = self.driver.find_elements(by, path)
            else:
                elements = self._wait_for_selector(by, path, True, timeout, max_attempts)
        except TimeoutException:
            elements = []
        return elements

    def get_css_el(self, path, timeout=10, max_attempts=5):
        """Finds the DOM element that matches the `css` selector.
                * If timeout > 0, waits the equivalent seconds.
                * If timeout=0, poll the DOM immediately without any waiting
                * Use this to return the first found element in the css
                * Note that CSS can also find IDs with a # symbol. Eg, #username is the same as id['username'] etc


                Args:
                    path: The selector to use
                    timeout: The number of seconds to wait
                    max_attempts: The amount of times to try finding the element. Useful for when enrollment is the worst
                Returns:
                    The first element that is found, even if multiple elements match"""
        by = By.CSS_SELECTOR
        if "/admin/notify/show" in self.driver.current_url:
            raise Exception("A PS error was raised")

        if timeout == 0:
            element = self.driver.find_element(by, path)
        else:
            element = self._wait_for_selector(by, path, max_attempts=max_attempts)
        return element

    def get_css_els(self, path, timeout=10, max_attempts=5):
        """Finds the DOM elements that match the `css` selector.
                * If timeout > 0, waits the equivalent seconds.
                * If timeout=0, poll the DOM immediately without any waiting
                * Use this to return multiple elements
                * Note that CSS can also find IDs with a # symbol. Eg, #username is the same as id['username'] etc

                Args:
                    path: The selector to use
                    timeout: The number of seconds to wait
                    max_attempts: The amount of times to try finding the element. Useful for when enrollment is the worst
                Returns:
                    A list of the found elements. """
        by = By.CSS_SELECTOR

        if "/admin/notify/show" in self.driver.current_url:
            raise Exception("A PS error was raised")

        try:
            if timeout == 0:
                elements = self.driver.find_elements(by, path)
            else:
                elements = self._wait_for_selector(by, path, True, timeout, max_attempts)
        except TimeoutException:
            elements = []
        return elements

    def get_web_element(self, by_locator, wait=10):
        """Use either get_xpath_el or get_css_el instead of this method where possible"""
        if "/admin/notify/show" in self.driver.current_url:
            raise Exception("A PS error was raised")
        try:
            el = WebDriverWait(self.driver, wait).until(EC.presence_of_element_located(by_locator))
        except TimeoutException:
            print("Wait for element timed out")
            el = self.driver.find_element(*by_locator)
        return el


    def get_web_elements(self, how, path, ajax=True, wait=2, error_when_empty=False):
        if ajax:
            self.wait_for_ajax()
        if how == 'id':
            els = self.driver.find_elements_by_id(path)
        elif how == 'xpath':
            els = self.driver.find_elements_by_xpath(path)
        elif how == 'css':
            els = self.driver.find_elements_by_css_selector(path)
        count = 0
        while not els and count < wait:
            count += 1
            if how == 'id':
                els = self.driver.find_elements_by_id(path)
            else:
                els = self.driver.find_elements_by_xpath(path)
            if count > wait and error_when_empty:
                raise Exception("Element not found on page")
        return els

    # region UI Helpers #
    def scroll_to_js(self, element):
        script = '''var viewPortHeight = Math.max(document.documentElement.clientHeight, window.innerHeight || 0);var
        elementTop = arguments[0].getBoundingClientRect().top;window.scrollBy(0, elementTop - (viewPortHeight / 2));'''
        self.driver.execute_script(script, element)

    # endregion UI Helpers #

    # region Wait Methods #

    def wait_for_elements(self, by_locator: object = None, how: str = None, path: str = None, timeout: int = 60):
        """
        :param by_locator: Element object
        :param how: Accepts id, xpath, or css as strings, or the By.CLASS type
        :param path: Path to element as a string
        :param timeout: Timeout value. Default is 60 seconds
        This will wait for one or multiple elements
        """
        element = None
        if by_locator is not None:
            element = by_locator
        elif how == "id" or how == By.ID:
            element = By.ID, path
        elif how == "xpath" or how == By.XPATH:
            element = By.XPATH, path
        elif how == "css" or how == By.CSS_SELECTOR:
            element = By.CSS_SELECTOR, path

        try:
            WebDriverWait(self.driver, timeout).until(EC.presence_of_all_elements_located(element))
            return True
        except (StaleElementReferenceException, TimeoutException):
            return False

    def wait_for_elements_to_be_displayed(self, by_locator=None, how=None, path=None, timeout=60):
        # Takes element(s) and waits until all elements are visible
        element = None
        if by_locator is not None:
            element = by_locator
        elif how == "id" or how == By.ID:
            element = By.ID, path
        elif how == "xpath" or how == By.XPATH:
            element = By.XPATH, path

        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_all_elements_located(element))
        except (StaleElementReferenceException, TimeoutException):
            print("Wait for element to be displayed timed out or element was stale in the Dom")

    def click_and_wait_for_page_change(self, by_locator=None, how=None, path=None, timeout=10, element=None):
        """This will click an element and wait for it to become stale. Useful for clicks
        that will change the page, especially in enrollment"""
        count = 0

        if by_locator:
            link = self.get_web_element(by_locator)

        if how:
            if how == 'xpath':
                link = self.get_xpath_el(path)
            else:
                link = self.get_web_elements(how, path)[0]

        if element:
            link = element

        def link_has_gone_stale():
            try:
                self.wait_for_ajax()
                link.click()
                return False
            except StaleElementReferenceException:
                return True
            except ElementClickInterceptedException:
                print("Not sure what happened here")
                return True

        while not link_has_gone_stale():
            link_has_gone_stale()
            count += 1

            if count >= timeout:
                print("Page did not change")
                break

        return link_has_gone_stale()

    def wait_for_page_title_change(self, current_title, timeout=30):
        # Takes current title and waits until it changes
        WebDriverWait(self.driver, timeout).until(lambda x: current_title not in x.title)

    def wait_for_page_title(self, expected_title):
        count = 0
        page_title = self.driver.title

        while (page_title != expected_title) and count <= 10:
            self.sleep(1)
            count += 1
            page_title = self.driver.title

    def do_titles_match(self, expected_title):
        return self.driver.title == expected_title

    def wait_for_element_to_be_clickable(self, how=None, path=None, by_locator=None, timeout=10):
        element = None
        if how == "id" or how == By.ID:
            element = By.ID, path
        elif how == "xpath" or how == By.XPATH:
            element = By.XPATH, path
        elif how == "css" or how == By.CSS_SELECTOR:
            element = By.CSS_SELECTOR, path
        elif by_locator is not None:
            element = by_locator

        WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(element))

    def is_element_clickable(self, how=None, path=None, by_locator=None, element=None):
        click_element = None
        if element:
            click_element = element
        elif how == "id" or how == By.ID:
            click_element = By.ID, path
        elif how == "xpath" or how == By.XPATH:
            click_element = By.XPATH, path
        elif how == "css" or how == By.CSS_SELECTOR:
            click_element = By.CSS_SELECTOR, path
        elif by_locator is not None:
            click_element = by_locator
        try:
            self.click_element(element=click_element)
            return True
        except WebDriverException:
            return False

    def wait_for_expected_url(self, expected_url, timeout=20):
        WebDriverWait(self.driver, timeout).until(EC.url_contains(expected_url))
        if expected_url in self.driver.current_url:
            return True
        else:
            print(f"Actual URL was different than expected. Actual: {self.driver.current_url}")
            return False

    def wait_for_ajax(self, timeout=10):
        count = 0
        timeout_count = 0
        # check for ps_error in title before proceeding
        if "/admin/notify/show" in self.driver.current_url:
            raise Exception("A PS error was raised")

        jquery_loaded = self.driver.execute_script("return typeof jQuery === 'function'")

        while not jquery_loaded or count >= 300:
            jquery_loaded = self.driver.execute_script("return typeof jQuery === 'function'")
            self.sleep(0.1)
            count += 1
        while timeout_count <= timeout:
            jquery_loaded = self.driver.execute_script("return typeof jQuery === 'function'")
            doc_ready_state = self.driver.execute_script("return document.readyState === 'complete'")
            jquery_not_active = self.driver.execute_script("return jQuery.active === 0")
            self.sleep(0.75)
            if jquery_loaded and doc_ready_state and jquery_not_active: break

    def wait_for_and_accept_alert(self, timeout=20):
        try:
            WebDriverWait(self.driver, timeout).until(EC.alert_is_present(), 'Timed out wait for Alert')
            alert = self.driver.switch_to.alert
            alert.accept()
        except TimeoutException:
            print("No alert")

    def wait_for_alert_and_get_text(self):
        try:
            WebDriverWait(self.driver, 20).until(EC.alert_is_present(), 'Timed out wait for Alert')
            alert = self.driver.switch_to.alert
            text = alert.text
            alert.accept()
            return text
        except TimeoutException:
            print('No alert')

    def wait_for_element_to_disappear(self, by_locator, timeout=20):
        WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element, by_locator)

    def wait_for_loadmask_to_disappear(self, by_locator=None, how=None, path=None, timeout=10):
        if by_locator:
            element = by_locator
        elif how == "xpath":
            element = By.XPATH, path
        elif how == "id":
            element = By.ID, path
        try:
            if "/admin/notify/show" in self.driver.current_url:
                raise Exception("A PS error was raised")
            else:
                while self.element_displayed(element):
                    WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located, element)
                    if self.element_displayed(element):
                        continue
                    else:
                        break
        except WebDriverException:
            pass

    def is_date(self, string, fuzzy=False):
        try:
            parse(string, fuzzy=fuzzy)
            return True
        except ValueError:
            return False

    # Handling IFrames
    def enter_iframe(self, iframe):
        frame = self.get_web_element(iframe)
        self.driver.switch_to.frame(frame)

    def exit_iframe(self):
        self.driver.switch_to.default_content()

    def switch_to_popup(self):
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def close_popup(self):
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def switch_to_new_window(self, main_window=False, sleep=1):
        if not main_window:
            self.driver.switch_to.window(self.driver.window_handles[-1])
            self.sleep(sleep)
        else:
            self.driver.switch_to.window(self.driver.window_handles[0])
            self.sleep(sleep)

    @staticmethod
    def sleep(wait_time):
        time.sleep(wait_time)

    # endregion Wait Methods

    # region Hover/Mouse Over methods

    def hover_over_element(self, how, path):
        el = self.get_web_elements(how, path)[0]
        action = ActionChains(self.driver)
        action.move_to_element(el).perform()

    def get_hover_text(self, how=None, target_path=None, hover_path=None):
        """target_path is the element you are going to hover over
        hover_path is the path in the html that contains the text you want to get"""
        self.hover_over_element(how, target_path)
        self.wait_for_ajax()
        text = self.get_elements_text(how, hover_path)
        return text

    # endregion Hover/Mouse Over methods

    @staticmethod
    def establish_db_connection(my_shard=None):
        my_db = db_base.establish_connection(shard=my_shard)
        return my_db

    # region javascript helpers

    def disable_default_click_action(self, element_id):
        """this javascript will ensure that the button does not perform the action that the click is supposed to initiate
            so this would include opening a file directory, redirecting to a url, etc"""
        self.driver.execute_script(f"document.getElementById('{element_id}')."
                                "addEventListener('click', function(event){event.preventDefault()})")

    # endregion javascript helpers

    def click_spooky_element(self, how=None, path=None, element=None, wait=20):

        """This Frankenstein of a method is for elements that are notoriously slow to load or finnicky to deal with,
                in other words, spooky"""
        self.wait_for_ajax()
        if element:
            el = element
        elif how == "id":
            try:
                el = self.get_web_element((By.ID, path), wait=wait)
                self.wait_for_element_to_be_clickable(how='id', path=path)
            except (TimeoutException, IndexError):
                self.driver.refresh()
                self.wait_for_ajax()
                el = self.get_web_element((By.ID, path), wait=wait)
                self.wait_for_element_to_be_clickable(how='id', path=path)
        elif how == "xpath":
            try:
                el = self.get_web_element((By.XPATH, path), wait=wait)
                self.wait_for_element_to_be_clickable(how='xpath', path=path)
            except (TimeoutException, IndexError):
                self.driver.refresh()
                self.wait_for_ajax()
                el = self.get_web_element((By.XPATH, path), wait=wait)
                self.wait_for_element_to_be_clickable(how='xpath', path=path)
        self.scroll_to_js(el)
        self.sleep(1)
        self.driver.execute_script("arguments[0].click();", el)
        self.wait_for_ajax()

    def _wait_for_selector(self, how, path, return_all_elements=False, timeout=10, max_attempts=5):
        attempts = 0
        element = None
        el = None
        while not el and attempts < max_attempts:
            attempts += 1
            if return_all_elements:
                try:
                    if timeout == 0:
                        element = self.driver.find_elements(how, path)
                    else:
                        element = self.wait(timeout).until(
                            lambda x: x.find_elements(how, path), f"Could not find an element with xpath: ``{path}``"
                        )
                except TimeoutException:
                    element = []
            else:
                el = self.wait(timeout, ignored_exceptions=[NoSuchElementException, TimeoutException]).until(
                    lambda x: x.find_element(how, path), f"Count not find an element with xpath: ``{path}``"
                )
                try:
                    if el.is_displayed():
                        element = el
                        break
                except NoSuchElementException:
                    continue
        return element

    def _safe_get_first_element(self, els):
        try:
            return els[0]
        except IndexError:
            raise ValueError("Element not found")

    def action_chains(self, element, value):
        actions = ActionChains(self.driver)
        actions.click(element).send_keys(value).send_keys(Keys.ENTER).perform()
        self.sleep(5)