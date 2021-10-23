from selenium import webdriver
from axe_selenium_python import Axe
import csv
import sys

# Get filename from args and check format is correct
if str(sys.argv[1]).endswith('.csv'):
    filename = str(sys.argv[1])
else:
    filename = str(sys.argv[1]) + '.csv'

# Make a list of URLs
url_list = []
for arg in sys.argv[2:]:
    url_list.append(str(arg))

print('Checking ' + str(len(url_list)) +
      ' URLs for accessibility issues with aXe...')

# Create and/or open the file to run the a11y check
# Arguments: filename for the csv, list of urls to check


def a11y_check(fn, urls):

    # Define count for feedback to user
    count = 0

    # Create CSV file
    with open(fn, 'w', newline='') as file:
        writer = csv.writer(file)
        # Write header row
        writer.writerow(["URL", "Description", "Help", "Help Link", "Issue Id",
                        "Impact", "Failure Summary", "HTML", "Selector", "Tags"])

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
                        writer.writerow([
                            url,
                            v['description'],
                            v['help'],
                            v['helpUrl'],
                            v['id'],
                            v['impact'],
                            v['nodes'][n]['failureSummary'],
                            v['nodes'][n]['html'],
                            str(v['nodes'][n]['target']).strip("''[]"),
                            str(v['tags']).strip("''[]")
                        ])
    print('Check complete. All results saved to ' + filename)


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
a11y_check(filename, url_list)
