BASE_URL = "https://www.saucedemo.com/"
INVENTORY_URL = f"{BASE_URL}inventory.html"
CART_URL = f"{BASE_URL}cart.html"
CHECKOUT_STEP_ONE_URL = f"{BASE_URL}checkout-step-one.html"
CHECKOUT_STEP_TWO_URL = f"{BASE_URL}checkout-step-two.html"
CHECKOUT_COMPLETE_URL = f"{BASE_URL}checkout-complete.html"

VALID_USERS = {
    "standard_user": {
        "username": "standard_user",
        "password": "secret_sauce"
    },
    "locked_out_user": {
        "username": "locked_out_user",
        "password": "secret_sauce"
    },
    "problem_user": {
        "username": "problem_user",
        "password": "secret_sauce"
    },
    "performance_glitch_user": {
        "username": "performance_glitch_user",
        "password": "secret_sauce"
    },
    "error_user": {
        "username": "error_user",
        "password": "secret_sauce"
    },
    "visual_user": {
        "username": "visual_user",
        "password": "secret_sauce"
    }
}

INVALID_CREDENTIALS = [
    {
        "username": "invalid_user",
        "password": "invalid_password",
        "expected_error": "Epic sadface: Username and password do not match any user in this service"
    },
    {
        "username": "",
        "password": "secret_sauce",
        "expected_error": "Epic sadface: Username is required"
    },
    {
        "username": "standard_user",
        "password": "",
        "expected_error": "Epic sadface: Password is required"
    },
    {
        "username": "",
        "password": "",
        "expected_error": "Epic sadface: Username is required"
    }
]

TEST_CHECKOUT_DATA = {
    "valid": {
        "first_name": "Иван",
        "last_name": "Иванов",
        "postal_code": "123456"
    },
    "invalid_first_name": {
        "first_name": "",
        "last_name": "Иванов",
        "postal_code": "123456",
        "expected_error": "Error: First Name is required"
    },
    "invalid_last_name": {
        "first_name": "Иван",
        "last_name": "",
        "postal_code": "123456",
        "expected_error": "Error: Last Name is required"
    },
    "invalid_postal_code": {
        "first_name": "Иван",
        "last_name": "Иванов",
        "postal_code": "",
        "expected_error": "Error: Postal Code is required"
    }
}

PRODUCTS = {
    "backpack": "Sauce Labs Backpack",
    "bike_light": "Sauce Labs Bike Light",
    "bolt_tshirt": "Sauce Labs Bolt T-Shirt",
    "fleece_jacket": "Sauce Labs Fleece Jacket",
    "onesie": "Sauce Labs Onesie",
    "tshirt_red": "Test.allTheThings() T-Shirt (Red)"
}

SORT_OPTIONS = {
    "name_asc": "az",
    "name_desc": "za",
    "price_asc": "lohi",
    "price_desc": "hilo"
}

SUCCESS_MESSAGES = {
    "header": "Thank you for your order!",
    "text": "Your order has been dispatched, and will arrive just as fast as the pony can get there!"
}

TIMEOUTS = {
    "default": 10000,
    "short": 5000,
    "long": 30000
}
