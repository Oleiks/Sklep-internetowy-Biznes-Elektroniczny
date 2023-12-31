import random
import time

from selenium import webdriver
from selenium.common import TimeoutException
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
        element = element.find_element(By.TAG_NAME, 'a')
        element.click()

    def click_on_account(self):
        self.driver.find_element(*MainPageLocators.ACCOUNT).click()

    def is_name_surname_matching(self, name: str, surname: str):
        element = self.driver.find_element(*CreateAccountPageLocators.USER_INFO)
        element = element.find_element(By.TAG_NAME, 'span')
        return ' '.join([name, surname]) == element.text

    def go_to_category(self, category_num: int):
        element = self.driver.find_element(By.XPATH, f'//li[@id=\'category-{28 + category_num}\']//a[@class=\'dropdown'
                                                     f'-item\']')  # categories indexes start with '3'
        element.click()


class CategoryPage(MainPage):
    def add_random_products_from_category(self, category_url: str):
        product_names = []
        added_products = []

        while len(added_products) < 5:  # will cause an infinite loop if more than 7 products are unavailable on the
            # page
            products = WebDriverWait(self.driver, 4).until(
                ec.presence_of_element_located(CategoryProductsLocators.PRODUCT_AREA)
            )
            products = products.find_elements(*CategoryProductsLocators.INDIVIDUAL_PRODUCT)
            for product in products:
                product = product.find_element(*CategoryProductsLocators.PRODUCT_NAME)
                if product.text not in product_names:
                    product_names.append(product.text)
                    potential_add = product.text
                    product = product.find_element(*CategoryProductsLocators.PRODUCT_NAME_LINK)
                    product.click()
                    product_page = ProductPage(self.driver)
                    try:
                        product_page.add_product_to_cart(random.randint(1, 4))
                        time.sleep(0.5)
                        added_products.append(potential_add)
                    except (TimeoutException, RuntimeError):
                        pass
                    finally:
                        self.driver.get(category_url)
                    break


class SearchResultPage(MainPage):

    def click_on_random_product(self):
        elements = self.driver.find_elements(*SearchPageLocators.PRODUCT)
        random.choice(elements).click()


class ProductPage(MainPage):
    def add_product_to_cart(self, amount: int = 1) -> str:
        add = self.driver.find_element(
            By.CSS_SELECTOR,
            "#add-to-cart-or-refresh > div.product-add-to-cart.js-product-add-to-cart > div > div.qty "
            "> div > span.input-group-btn-vertical > "
            "button.btn.btn-touchspin.js-touchspin.bootstrap-touchspin-up",
        )

        for _ in range(amount - 1):
            add.click()

        product_name = self.driver.find_element(*ProductPageLocators.PRODUCT_NAME)
        element = WebDriverWait(self.driver, 3).until(
            ec.element_to_be_clickable(ProductPageLocators.ADD_TO_CART_BUTTON)
        )
        element.click()
        return product_name.text

    def go_to_cart_popup_dialog(self):
        element = WebDriverWait(self.driver, 3).until(
            ec.presence_of_element_located(ProductPageLocators.POPUP_DIALOG)
        )
        element = element.find_element(*ProductPageLocators.POPUP_DIALOG_CART_BUTTON)
        element.click()


class CartPage(MainPage):
    def is_product_name_matching(self, name: str) -> bool:
        element = self.driver.find_element(*CartPageLocators.CART_OVERVIEW)
        element = element.find_element(*CartPageLocators.TOP_PRODUCT_NAME)

        return all(word in element.text.upper().split() for word in name.upper().split())

    def delete_from_cart(self, deletions: int = 1) -> None:
        for _ in range(deletions):
            WebDriverWait(self.driver, 10).until(
                ec.element_to_be_clickable(CartPageLocators.DELETE_BUTTON)
            ).click()
            time.sleep(1)  # otherwise the loop won't continue

    def cart_item_number(self) -> int:
        element = self.driver.find_elements(*CartPageLocators.DELETE_BUTTON)

        return len(element)

    def proceed_to_checkout(self):
        element = self.driver.find_element(*CartPageLocators.CART_DETAILS)
        element = element.find_element(*CartPageLocators.PROCEED_TO_CHECKOUT_BUTTON)
        element.click()


class CheckoutPage(BasePage):
    def delete_address(self):
        WebDriverWait(self.driver, 5).until(
            ec.presence_of_element_located((By.CLASS_NAME, "delete-address.text-muted"))
        ).click()

    def fill_in_checkout_info_and_submit(self, info: dict):
        for val in info:
            # text data
            if info[val] is not None and info[val] not in (True, False):
                locator = getattr(CheckoutPageLocators, f'{val}'.upper())
                element = WebDriverWait(self.driver, 10).until(
                    ec.presence_of_element_located(locator)
                )
                element.clear()
                element.send_keys(info[val])
            # checkbox
            elif info[val] is not None:
                if val == 'USE_SAME_ADDRESS' and info[val] is False:  # same address checkbox is set by default
                    locator = getattr(CheckoutPageLocators, f'{val}'.upper())
                    WebDriverWait(self.driver, 10).until(
                        ec.presence_of_element_located(locator)
                    ).click()
        element = WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located(CheckoutPageLocators.SUBMIT_DATA_AREA)
        )
        element = element.find_element(*CheckoutPageLocators.SUBMIT_DATA_BUTTON)
        element.click()

        # delivery option
        self.driver.find_element(*CheckoutPageLocators.DELIVERY_OPTION).click()
        self.driver.find_element(*CheckoutPageLocators.CONFIRM_DELIVERY_BUTTON).click()

        WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located(CheckoutPageLocators.PAYMENT_OPTION)
        ).click()

        self.driver.find_element(*CheckoutPageLocators.TOS).click()

        element = self.driver.find_element(*CheckoutPageLocators.SUBMIT_ORDER_AREA)
        element = element.find_element(*CheckoutPageLocators.SUBMIT_ORDER_BUTTON)
        element.click()


class OrderConfirmationPage(MainPage):
    def get_order_id(self) -> str:
        element = WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located(OrderConfirmationLocators.ORDER_ID)
        )
        order_id = element.text.split(":")[1].strip()

        return order_id


class MyAccountPage(MainPage):
    def click_sign_up(self):
        element = self.driver.find_element(*MyAccountLocators.SIGN_UP)
        element.click()

    def login(self, email: str, password: str):
        self.driver.find_element(*MyAccountLocators.EMAIL).send_keys(email)
        self.driver.find_element(*MyAccountLocators.PASSWORD).send_keys(password)
        self.driver.find_element(*MyAccountLocators.SUBMIT_LOGIN).click()

    def go_to_order_history(self):
        self.driver.find_element(*MyAccountLocators.ORDER_HISTORY).click()


class OrderHistoryPage(MainPage):
    def get_order_ids(self) -> list:
        element = self.driver.find_element(*OrderHistoryLocators.ORDERS)
        order_ids = element.find_elements(*OrderHistoryLocators.ORDER_ID)

        return [order_id.text for order_id in order_ids]

    def get_order_status(self, order_id: str) -> str:
        element = self.driver.find_element(By.XPATH, f"//th[text()='{order_id}']")
        order_status = element.find_element(By.XPATH, "./following-sibling::td[4]/span").text
        return order_status


class CreateAccountPage(MainPage):
    def check_sex_radio(self, sex: str):
        locator = CreateAccountPageLocators.MALE_RADIO if sex == 'male' else CreateAccountPageLocators.FEMALE_RADIO
        element = self.driver.find_element(*locator)
        element.click()

    def input_text_fields(self, first_name: str, last_name: str, email: str, password: str, dob: str):
        self.driver.find_element(*CreateAccountPageLocators.FIRST_NAME).send_keys(first_name)
        self.driver.find_element(*CreateAccountPageLocators.LAST_NAME).send_keys(last_name)
        self.driver.find_element(*CreateAccountPageLocators.EMAIL).send_keys(email)
        self.driver.find_element(*CreateAccountPageLocators.PASSWORD).send_keys(password)
        self.driver.find_element(*CreateAccountPageLocators.DOB).send_keys(dob)

    def check_opt_ins(self, check_data: list):
        element = self.driver.find_elements(*CreateAccountPageLocators.OPT_INS)
        elements = []

        for x in element:
            elements.append(x.find_element(By.TAG_NAME, 'input'))

        for element, checkbox_val in zip(elements, check_data):
            if checkbox_val:
                element.click()

    def send_form(self):
        element = self.driver.find_element(*CreateAccountPageLocators.SUBMIT_BUTTON)
        element.click()
