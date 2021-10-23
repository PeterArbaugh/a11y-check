# Automated Accessibility Check with aXe

This tool is intended to run aXe automated accessibility checks on a list of sites input by the user. The script can be run from the terminal and outputs results into a csv file named by the user. Currently, you'll need to enter each URL you want to check -- the script won't crawl sub pages or run at link destinations by itself.

Please note that automated testing will only pick up 20% - 60% of accessibility issues, depending on who you ask. This is meant to be paired with manual testing to provide a full picture of potential issues for remediation.

## Setup

1. Install Python. The script was built and tested in Python 3.8.2.
2. Use pip to install required Python packages: `pip install selenium axe_selenium_python`
3. [Install ChromeDriver.](https://github.com/SeleniumHQ/selenium/wiki/ChromeDriver) Selenium requires ChromeDriver as a bridge between the browser and Selenium.
4. Download the a11y_check.py script.

## Run a11y_check.py

The checker script requires several arguments:

1. File name. What you want to call your csv with test results.
2. Space delimited list of urls. You'll need to include the full URL including the 'https://...'.

From the same directory where you've placed a11y_check.py, run the following in the terminal.
`python3 a11y_check.py filename first_url_to_check [second_url_to_check] [third_url_to_check] [etc]`

For example:
`python3 a11y_check.py test_results.csv https://google.com https://reddit.com https://tanookilabs.com/`
