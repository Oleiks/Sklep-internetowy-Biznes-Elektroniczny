# Selenium tests

This project contains automated tests for a prestashop application. In order to run the tests successfully, you need to provide pre-made account information in the `main.py` file. Follow the instructions below to set up the required credentials:

## Setup Instructions
1. Install chrome-driver, preferably version 119.0.6045.105.

2. Install packages from requirements.txt

3. Open the `main.py` file in your preferred text editor.

4. Locate `PRE_GENERATED_CREDENTIALS`.

5. Input the pre-made account information into the specified variables.


```python
# main.py

# TODO: insert the pre generated account info here
PRE_GENERATED_CREDENTIALS = {
    'email': 'your_email',
    'password': 'your_password'
}