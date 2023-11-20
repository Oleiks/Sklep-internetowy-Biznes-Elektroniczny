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

    def click_on_account(self):
        self.driver.find_element(*MainPageLocators.ACCOUNT).click()

    def is_name_surname_matching(self, name: str, surname: str):
        element = self.driver.find_element(*CreateAccountPageLocators.USER_INFO)
        element = element.find_element(By.TAG_NAME, 'span')
        return ' '.join([name, surname]) == element.text

    def go_to_category(self, category_num: int):
        # category iterates itself by 3 for some reason
        self.driver.find_element(By.ID, f'category-{category_num * 3}').click()


class CategoryPage(MainPage):
    def add_random_products_from_category(self):
        product_names = []

        while len(product_names) < 10:  # this won't work if there is a product that is unavailable
            products = self.driver.find_element(*CategoryProductsLocators.PRODUCT_AREA)
            products = products.find_elements(*CategoryProductsLocators.INDIVIDUAL_PRODUCT)
            for product in products:
                product = product.find_element(*CategoryProductsLocators.PRODUCT_NAME)
                if product.text not in product_names:
                    product_names.append(product.text)
                    product = product.find_element(*CategoryProductsLocators.PRODUCT_NAME_LINK)
                    product.click()
                    product_page = ProductPage(self.driver)

                    product_page.add_product_to_cart(random.randint(1, 4))
                    # Code bellow doesn't work because if there isn't sufficient number of items,
                    # the popup dialog never shows up

                    # WebDriverWait(self.driver, 10).until(
                    #     ec.presence_of_element_located(ProductPageLocators.POPUP_DIALOG)
                    # )

                    # There needs to be some time before the product gets added to cart, this works for now
                    time.sleep(0.5)
                    self.driver.back()
                    break


class SearchResultPage(MainPage):

    def click_on_random_product(self):
        elements = self.driver.find_elements(*SearchPageLocators.PRODUCT)
        random.choice(elements).click()


class ProductPage(MainPage):

    # returns the name of the product
    # TODO: create an exception/ if clause if the product is unavailable
    # def add_product_to_cart(self) -> str:
    #     # quantity = self.driver.find_element(*ProductPageLocators.QUANTITY)
    #     # quantity.clear()
    #     # quantity.send_keys(amount) # amount == param
    #     element = self.driver.find_element(*ProductPageLocators.ADD_TO_CART_BUTTON)
    #     product_name = self.driver.find_element(*ProductPageLocators.PRODUCT_NAME)
    #     element.click()
    #     return product_name.text
    def add_product_to_cart(self, amount: int = 1) -> str:
        # Check if the product is available by looking for a specific element
        # Assuming the availability indicator is present, proceed to add to cart
        add = self.driver.find_element(
            By.CSS_SELECTOR,
            "#add-to-cart-or-refresh > div.product-add-to-cart.js-product-add-to-cart > div > div.qty "
            "> div > span.input-group-btn-vertical > "
            "button.btn.btn-touchspin.js-touchspin.bootstrap-touchspin-up",
        )

        for _ in range(amount - 1):
            add.click()

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

    def proceed_to_checkout(self):
        element = self.driver.find_element(*CartPageLocators.CART_DETAILS)
        element = element.find_element(*CartPageLocators.PROCEED_TO_CHECKOUT_BUTTON)
        element.click()


class CheckoutPage(BasePage):
    # this will fail if there are any addresses previously created
    def fill_in_checkout_info_and_submit(self, info: dict):
        for val in info:
            # text data
            if info[val] is not None and info[val] not in (True, False):
                locator = getattr(CheckoutPageLocators, f'{val}'.upper())
                # element = self.driver.find_element(*locator)
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
        self.driver.find_element(*CheckoutPageLocators.CONFIRM_DELIVERY_BUTTON).click()

        # payment option
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
