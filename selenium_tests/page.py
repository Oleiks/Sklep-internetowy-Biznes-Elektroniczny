import random
import time

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from locator import *


class BasePage(object):
    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver


class MainPage(BasePage):
    def input_search_box(self, input_string: str):
        element = self.driver.find_element(*MainPageLocators.SEARCH_BOX)
        element.send_keys(input_string)
        element.send_keys(Keys.RETURN)  # will submit the search

    def click_go_to_cart(self):
        element = self.driver.find_element(*MainPageLocators.GO_TO_CART_BUTTON)
        element.click()

    def click_log_in(self):
        element = self.driver.find_element(*MainPageLocators.USER_INFO)
        element = element.find_element(By.TAG_NAME, 'a')  # looking for a link in user-info div
        element.click()


class SearchResultPage(MainPage):

    def click_on_random_product(self):
        elements = self.driver.find_elements(*SearchPageLocators.PRODUCT)
        random.choice(elements).click()


class ProductPage(MainPage):

    # returns the name of the product
    def add_product_to_cart(self) -> str:
        element = self.driver.find_element(*ProductPageLocators.ADD_TO_CART_BUTTON)
        product_name = self.driver.find_element(*ProductPageLocators.PRODUCT_NAME)
        element.click()
        return product_name.text

    def go_to_cart_popup_dialog(self):
        element = WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located(ProductPageLocators.POPUP_DIALOG)
        )
        element = element.find_element(*ProductPageLocators.POPUP_DIALOG_CART_BUTTON)
        element.click()


class CartPage(MainPage):
    def is_product_name_matching(self, name: str) -> bool:
        element = self.driver.find_element(*CartPageLocators.CART_OVERVIEW)
        element = element.find_element(*CartPageLocators.TOP_PRODUCT_NAME)

        return name.upper() in element.text.upper()

    def delete_from_cart(self, deletions: int = 1) -> None:
        for _ in range(deletions):
            WebDriverWait(self.driver, 10).until(
                ec.element_to_be_clickable(CartPageLocators.DELETE_BUTTON)
            ).click()
            time.sleep(1)  # otherwise the loop doesn't continue

    def cart_item_number(self) -> int:
        element = self.driver.find_elements(*CartPageLocators.DELETE_BUTTON)

        return len(element)


class MyAccountPage(MainPage):
    def click_sing_up(self):
        element = self.driver.find_element(*MyAccountLocators.SIGN_UP)
        element.click()


class CreateAccountPage(MainPage):
    def check_sex_radio(self, sex: str):
        locator = CreateAccountLocators.MALE_RADIO if sex == 'male' else CreateAccountLocators.FEMALE_RADIO
        element = self.driver.find_element(*locator)
        element.click()

    def input_name(self, first_name: str):
        self.driver.find_element(*CreateAccountLocators.FIRST_NAME).send_keys(first_name)

    def input_surname(self, last_name: str):
        self.driver.find_element(*CreateAccountLocators.LAST_NAME).send_keys(last_name)

    def input_email(self, email: str):
        self.driver.find_element(*CreateAccountLocators.EMAIL).send_keys(email)

    def input_password(self, password: str):
        self.driver.find_element(*CreateAccountLocators.PASSWORD).send_keys(password)

    def input_dob(self, dob: str):
        self.driver.find_element(*CreateAccountLocators.DOB).send_keys(dob)

    def check_opt_ins(self, check_data: list):
        element = self.driver.find_elements(*CreateAccountLocators.OPT_INS)
        elements = []

        for x in element:
            elements.append(x.find_element(By.TAG_NAME, 'input'))

        for element, checkbox_val in zip(elements, check_data):
            if checkbox_val:
                element.click()

    def send_form(self):
        element = self.driver.find_element(*CreateAccountLocators.SUBMIT_BUTTON)
        element.click()

    def is_name_surname_matching(self, name: str, surname: str):
        element = self.driver.find_element(*CreateAccountLocators.USER_INFO)
        element = element.find_element(By.TAG_NAME, 'span')
        return ' '.join([name, surname]) == element.text
