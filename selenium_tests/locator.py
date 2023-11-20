from selenium.webdriver.common.by import By


class MainPageLocators(object):
    SEARCH_BOX = (By.NAME, 's')
    LOGIN_AREA = (By.CLASS_NAME, 'user-info')
    GO_TO_CART_BUTTON = (By.CLASS_NAME, 'cart-products-count')
    USER_INFO = (By.CLASS_NAME, 'user-info')
    ACCOUNT = (By.CLASS_NAME, 'account')


class SearchPageLocators(MainPageLocators):
    PRODUCT = (By.CLASS_NAME, 'thumbnail-top')


class ProductPageLocators(MainPageLocators):
    ADD_TO_CART_BUTTON = (By.CLASS_NAME, 'btn-primary.add-to-cart')  # '.' instead of ' ' is needed
    POPUP_DIALOG = (By.CLASS_NAME, 'cart-content')
    POPUP_DIALOG_CART_BUTTON = (By.CLASS_NAME, 'btn.btn-primary')
    PRODUCT_NAME = (By.CLASS_NAME, 'h1')
    QUANTITY = (By.ID, 'quantity_wanted')


class CartPageLocators(MainPageLocators):
    CART_OVERVIEW = (By.CLASS_NAME, 'cart-overview.js-cart')  # '.' instead of ' ' is needed
    TOP_PRODUCT_NAME = (By.CLASS_NAME, 'product-line-info')
    DELETE_BUTTON = (By.CLASS_NAME, 'remove-from-cart')
    CART_DETAILS = (By.CLASS_NAME, 'card.cart-summary')
    PROCEED_TO_CHECKOUT_BUTTON = (By.CLASS_NAME, 'text-sm-center')


class MyAccountLocators(MainPageLocators):
    SIGN_UP = (By.CLASS_NAME, 'no-account')
    EMAIL = (By.ID, 'field-email')
    PASSWORD = (By.ID, 'field-password')
    SUBMIT_LOGIN = (By.ID, 'submit-login')
    IDENTITY = (By.ID, 'identity-link')
    ORDER_HISTORY = (By.ID, 'history-link')
    ADDRESSES = (By.ID, 'addresses-link')
    ORDER_SLIPS = (By.ID, 'order-slips-link')
    WISHLIST = (By.ID, 'wishlist-link')


class OrderHistoryLocators(MainPageLocators):
    ORDERS = (By.TAG_NAME, 'tbody')
    ORDER_ID = (By.TAG_NAME, 'th')


class CreateAccountPageLocators(MainPageLocators):
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


class CheckoutPageLocators(object):
    ALIAS = (By.ID, 'field-alias')
    FIRST_NAME = (By.ID, 'field-firstname')
    LAST_NAME = (By.ID, 'field-lastname')
    COMPANY = (By.ID, 'field-company')
    EMAIL = (By.ID, 'field-email')
    NIP_UE = (By.ID, 'field-vat_number')
    ADDRESS = (By.ID, 'field-address1')
    ADDRESS_2 = (By.ID, 'field-address2')
    POSTCODE = (By.ID, 'field-postcode')
    CITY = (By.ID, 'field-city')
    COUNTRY = (By.ID, 'field-id_country')
    PHONE = (By.ID, 'field-phone')
    USE_SAME_ADDRESS = (By.ID, 'use_same_address')
    SUBMIT_DATA_AREA = (By.CLASS_NAME, 'form-footer.clearfix')
    SUBMIT_DATA_BUTTON = (By.CLASS_NAME, 'continue.btn.btn-primary.float-xs-right')
    DELIVERY_OPTIONS_AREA = (By.CLASS_NAME, 'delivery-options-list')
    DELIVERY_OPTION_1 = (By.ID, 'delivery_option_1')  # will have to inject int value later
    CONFIRM_DELIVERY_BUTTON = (By.NAME, 'confirmDeliveryOption')
    PAYMENT_OPTION = (By.ID, 'payment-option-1')  # will have to inject int value later
    TOS = (By.ID, 'conditions_to_approve[terms-and-conditions]')
    SUBMIT_ORDER_AREA = (By.ID, 'payment-confirmation')
    SUBMIT_ORDER_BUTTON = (By.CLASS_NAME, 'btn.btn-primary.center-block')


class OrderConfirmationLocators(MainPageLocators):
    ORDER_ID = (By.ID, 'order-reference-value')


class CategoryProductsLocators(MainPageLocators):
    PRODUCT_AREA = (By.CLASS_NAME, 'products.row')
    INDIVIDUAL_PRODUCT = (By.TAG_NAME, 'article')
    PRODUCT_NAME_LINK = (By.TAG_NAME, 'a')
