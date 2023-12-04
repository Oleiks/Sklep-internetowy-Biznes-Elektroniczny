# Selenium tests

This project contains automated tests for a prestashop application. In order to run the tests successfully, you need to provide pre-made account information in the `main.py` file. Follow the instructions below to set up the required credentials:

## Setup Instructions

1. Open the `main.py` file in your preferred text editor.

2. Locate `PRE_GENERATED_CREDENTIALS`.

3. Input the pre-made account information into the specified variables.

```python
# main.py

# TODO: insert the pre generated account info here
PRE_GENERATED_CREDENTIALS = {
    'email': 'your_email',
    'password': 'your_password'
}