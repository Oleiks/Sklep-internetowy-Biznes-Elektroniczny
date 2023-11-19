import random
import unittest
import string

from selenium import webdriver
import page


class TestCases(unittest.TestCase):
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
        while len(product_names) < 5:
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
        main_page = page.MainPage(self.driver)
        main_page.click_log_in()

        my_account_page = page.MyAccountPage(self.driver)
        my_account_page.click_sing_up()

        create_account_page = page.CreateAccountPage(self.driver)
        create_account_page.check_sex_radio(sing_up_data['sex'])
        create_account_page.input_text_fields(
            sing_up_data['name'],
            sing_up_data['surname'],
            sing_up_data['email'],
            sing_up_data['password'],
            sing_up_data['dob']
        )
        checkbox_values = list(sing_up_data.values())[5:len(sing_up_data)]
        create_account_page.check_opt_ins(checkbox_values)
        create_account_page.send_form()

        self.assertTrue(create_account_page.is_name_surname_matching(sing_up_data['name'], sing_up_data['surname']))

    def tearDown(self) -> None:
        self.driver.close()  # this is unnecessary in Selenium 4
