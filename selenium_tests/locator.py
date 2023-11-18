from selenium.webdriver.common.by import By


class MainPageLocators(object):
    SEARCH_BOX = (By.NAME, 's')
    LOGIN_AREA = (By.CLASS_NAME, 'user-info')
    GO_TO_CART_BUTTON = (By.CLASS_NAME, 'cart-products-count')
    USER_INFO = (By.CLASS_NAME, 'user-info')


class SearchPageLocators(object):
    PRODUCT = (By.CLASS_NAME, 'thumbnail-top')


class ProductPageLocators(object):
    ADD_TO_CART_BUTTON = (By.CLASS_NAME, 'btn-primary.add-to-cart')  # '.' instead of ' ' is needed
    POPUP_DIALOG = (By.CLASS_NAME, 'cart-content')
    POPUP_DIALOG_CART_BUTTON = (By.CLASS_NAME, 'btn.btn-primary')
    PRODUCT_NAME = (By.CLASS_NAME, 'h1')


class CartPageLocators(object):
    CART_OVERVIEW = (By.CLASS_NAME, 'cart-overview.js-cart')  # '.' instead of ' ' is needed
    TOP_PRODUCT_NAME = (By.CLASS_NAME, 'product-line-info')
    DELETE_BUTTON = (By.CLASS_NAME, 'remove-from-cart')


class MyAccountLocators(object):
    SIGN_UP = (By.CLASS_NAME, 'no-account')


class CreateAccountLocators(MainPageLocators):
    MALE_RADIO = (By.ID, 'field-id_gender-1')
    FEMALE_RADIO = (By.ID, 'field-id_gender-2')
    FIRST_NAME = (By.ID, 'field-firstname')
    LAST_NAME = (By.ID, 'field-lastname')
    EMAIL = (By.ID, 'field-email')
    PASSWORD = (By.ID, 'field-password')
    DOB = (By.ID, 'field-birthday')
    OPT_INS = (By.CLASS_NAME, 'custom-checkbox')  # will have to go further and find input tag
    SUBMIT_BUTTON = (
        By.CLASS_NAME, 'btn.btn-primary.form-control-submit.float-xs-right'
    )  # '.' instead of ' ' is needed
