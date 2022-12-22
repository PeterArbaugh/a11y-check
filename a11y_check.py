from selenium import webdriver
from axe_selenium_python import Axe
import csv
import sys
import os
from dotenv import load_dotenv
from pyairtable import Base, Table
import datetime
import json

# Load Airtable API key
load_dotenv()
api_key = os.getenv('AIRTABLE_API_KEY')

# Connect to Airtable Base
base = Base(api_key, 'appAVJZA9TfkNWn6c')
issues_table = base.get_table('All issues')
pages_table = base.get_table('Pages')
properties_table = base.get_table('Properties')
scans_table = base.get_table('Scans')

# Make a list of properties to check
prop_list = []
for arg in sys.argv[1:]:
    prop_list.append(str(arg))

# Lookup each property and retrieve record ID
prop_records = []
# print(properties_table.all())
for prop in prop_list:
    for item in properties_table.all():
        try:
            if item['fields']['Name'] == prop:
                prop_records.append(item['id'])
                print(item['id'])
        except KeyError:
            continue
print(prop_records)

# Make a list of URLs from the Pages table that matches property id
url_list = []
for record in prop_records:
    for page in pages_table.all():
        print(page)
        try:
            if record in page['fields']['Property']:
                url_list.append(page['fields']['URL'])
            else:
                continue
        except KeyError:
            continue
print(url_list)

# Create a scan record on the scan table
# Link the property(s)
current = scans_table.create({
    'Property': prop_records
})

# Get the scan ID to associate with new issues
current_scan = []
current_scan.append(current['id']) # Airtable needs an array

print('Checking ' + str(len(url_list)) +
      ' URLs for accessibility issues with aXe...')

# Create and/or open the file to run the a11y check
def a11y_check(urls):

    # Define count for feedback to user
    count = 0
    # Create a single timestamp for the scan
    timestamp = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())

    for url in urls:
        count = count + 1
        print('Checking location ' + str(count) +
                ' of ' + str(len(urls)) + ': ' + url)
        # Get a list of violations from the aXe audit run in selenium with audit_url
        violations_list = audit_url(url)['violations']
        # Check the list is not empty
        if (len(violations_list) > 0):
            # Iterate through each recorded violation
            for v in violations_list:
                # Iterate through each instance of a violation and write to CSV.
                # This creates a new row for each instance of violation.
                for n in range(len(v['nodes'])):
                    issues_table.create({
                        'url': url,
                        'description': v['description'],
                        'help': v['help'],
                        'helpurl': v['helpUrl'],
                        'wcag_id': v['id'],
                        'impact': v['impact'],
                        'failureSummary': v['nodes'][n]['failureSummary'],
                        'html': v['nodes'][n]['html'],
                        'selector': str(v['nodes'][n]['target']).strip("''[]"),
                        'tags': str(v['tags']).strip("''[]"),
                        'timestamp': timestamp,
                        'Scans': current_scan
                    })
    print('Check complete. All results saved.')


def audit_url(site_url):
    driver = webdriver.Chrome()
    driver.get(site_url)
    axe = Axe(driver)
    # Inject axe-core javascript into page.
    axe.inject()
    # Run axe accessibility checks.
    results = axe.run()
    # OPTIONAL: Write results to file in JSON
    # axe.write_results(results, 'a11y.json')
    driver.close()
    return results


# Run the checks
a11y_check(url_list)
