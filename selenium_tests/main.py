import random
import unittest
import string
from faker import Faker
from selenium import webdriver
import page


class TestCases(unittest.TestCase):
    sing_up_data = {
        'sex': 'male',
        'name': 'name',
        'surname': 'surname',
        'email': ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)) + '@test.com',
        'password': 'chVDaE3mvk3hbnO',
        'dob': '1970-1-1',
        'offers': True,
        'personal_data': True,
        'newsletter': True,
        'TOS': True
    }

    checkout_data = {
        'ALIAS': None,  # None here means optional
        'FIRST_NAME': '',
        'LAST_NAME': '',
        'COMPANY': None,  # None here means optional
        'NIP_UE': None,  # None here means optional
        'ADDRESS': '',
        'ADDRESS_2': None,  # None here means optional
        'POSTCODE': '',
        'CITY': '',
        'COUNTRY': None,  # this is already set by default to Poland
        'PHONE': None,  # None here means optional
        'USE_SAME_ADDRESS': True
    }

    faker = Faker()
    for key in checkout_data.keys():
        if checkout_data[key] is not None and checkout_data[key] not in (True, False):
            if key == 'POSTCODE':
                checkout_data[key] = f"{faker.random_int(10, 99)}-{faker.random_int(100, 999)}"
            else:
                checkout_data[key] = getattr(faker, key.lower())() if hasattr(faker, key.lower()) else faker.word()

    def setUp(self) -> None:
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8080')

    def add_random_to_cart_by_name(self, product_name: str):
        main_page = page.MainPage(self.driver)
        main_page.input_search_box(product_name)

        result_page = page.SearchResultPage(self.driver)
        result_page.click_on_random_product()

        product_page = page.ProductPage(self.driver)
        product_name = product_page.add_product_to_cart()
        product_page.go_to_cart_popup_dialog()
        self.driver.get('http://localhost:8080')  # goes back to home page
        return product_name

    def sing_up(self, sing_up_data: dict):
        self.driver.get('http://localhost:8080')

        main_page = page.MainPage(self.driver)
        main_page.click_log_in()

        my_account_page = page.MyAccountPage(self.driver)
        my_account_page.click_sign_up()

        create_account_page = page.CreateAccountPage(self.driver)
        create_account_page.check_sex_radio(sing_up_data['sex'])
        create_account_page.input_text_fields(
            self.sing_up_data['name'],
            self.sing_up_data['surname'],
            self.sing_up_data['email'],
            self.sing_up_data['password'],
            self.sing_up_data['dob']
        )
        checkbox_values = list(sing_up_data.values())[5:len(sing_up_data)]
        create_account_page.check_opt_ins(checkbox_values)
        create_account_page.send_form()  # goes back to home page

    def test_add_random_to_cart_by_name(self):
        product_name = 'humming'
        self.add_random_to_cart_by_name(product_name)
        main_page = page.MainPage(self.driver)
        main_page.click_go_to_cart()

        cart_page = page.CartPage(self.driver)
        self.assertTrue(cart_page.is_product_name_matching(product_name),
                        'There is no product of given name in the cart.')

    def test_delete_from_cart(self, deletions: int = 3):
        product_names = []
        # this loop is to add different products, if the same product is added this test could potentially fail on
        # its own
        while len(product_names) < 3:
            product_name = self.add_random_to_cart_by_name('hummingbird')
            if product_name not in product_names:
                product_names.append(product_name)

        main_page = page.MainPage(self.driver)
        main_page.click_go_to_cart()

        cart_page = page.CartPage(self.driver)
        no_cart_items_pre: int = cart_page.cart_item_number()
        cart_page.delete_from_cart(deletions=3)
        no_cart_items_post: int = cart_page.cart_item_number()

        self.assertTrue(no_cart_items_pre - no_cart_items_post == deletions)

    def test_sing_up(self):
        self.sing_up(self.sing_up_data)
        main_page = page.MainPage(self.driver)
        self.assertTrue(main_page.is_name_surname_matching(self.sing_up_data['name'], self.sing_up_data['surname']))

    def test_submit_order(self):
        # this test randomly crashes on the delivery part
        # this could be result of the delivery option not being selected by default for some products
        main_page = page.MainPage(self.driver)
        # The test assumes that there will be an account created under 'P182WB89Y1@test.com',
        # and no addresses were previously added
        main_page.click_log_in()
        my_account_page = page.MyAccountPage(self.driver)
        # this is hardcoded and needs to be changed
        my_account_page.login('P182WB89Y1@test.com', self.sing_up_data['password'])

        self.add_random_to_cart_by_name('humming')  # to be changed
        main_page.click_go_to_cart()
        cart_page = page.CartPage(self.driver)
        cart_page.proceed_to_checkout()

        checkout_page = page.CheckoutPage(self.driver)
        checkout_page.fill_in_checkout_info_and_submit(self.checkout_data)

        order_confirmation_page = page.OrderConfirmationPage(self.driver)
        print(f'order_id:{order_confirmation_page.get_order_id()}')
        order_id = order_confirmation_page.get_order_id()

        main_page.click_on_account()
        my_account_page = page.MyAccountPage(self.driver)
        my_account_page.go_to_order_history()
        history_page = page.OrderHistoryPage(self.driver)
        order_ids = history_page.get_order_ids()
        self.assertTrue(order_id in order_ids)

    def test_check_order_status(self):
        main_page = page.MainPage(self.driver)
        main_page.click_log_in()

        my_account_page = page.MyAccountPage(self.driver)
        # this is hardcoded and needs to be changed
        my_account_page.login('P182WB89Y1@test.com', self.sing_up_data['password'])
        my_account_page.go_to_order_history()

        order_history_page = page.OrderHistoryPage(self.driver)
        order_ids = order_history_page.get_order_ids()
        random_order = random.choice(order_ids)
        order_status = order_history_page.get_order_status(random_order)
        print(f'{random_order}_status: {order_status}')
        # there is nothing to check if all goes according to the test
        assert True

    def tearDown(self) -> None:
        self.driver.close()  # this is unnecessary in Selenium 4
