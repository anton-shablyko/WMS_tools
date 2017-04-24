""" This script will format source csv file to the csv that can be accepted by constant Contact  """
import csv
import re


class ConvertForConsantContact:
    def __init__(self, email_type):
        self.email_type = email_type

    # Extract name from the email address like name@test.com
    def generate_name(self, email):
        name = (re.search('^[^@]*', email)).group(0)
        return name.title()

    def clean_emails(self, row):
        # remove commas and empty spaces from email addresses
        clean_row = row[-1].replace(' ', ',').replace(';', ',').split(',')
        clean_row = {i.strip() for i in clean_row}  # remove duplicated emails
        return clean_row

    def convert_emails(self):
        data = {'billing':
                    {'from': 'billing_emails.csv',
                     'to': 'billing_result.csv'},
                'all':
                    {'from': 'notification_emails.csv',
                     'to': 'notification_email_result.csv'}}

        source = data[self.email_type]['from']
        result = data[self.email_type]['to']

        with open(source, 'r', newline='') as original:
            with open(result, 'w', newline='') as result:
                result_emails = csv.writer(result, delimiter=',')
                result_emails.writerow(['Email Address', 'First name', 'Company'])
                original_emails = csv.reader(original)

                for row in original_emails:
                    for email in self.clean_emails(row):
                        if '@' in email:  # check if @ in email address
                            name = self.generate_name(email)
                            print(name, row[-2] + ": " + email.strip())
                            result_emails.writerow([email.strip(), name, row[-2].upper()])


all = ConvertForConsantContact('all')
all.convert_emails()

billing = ConvertForConsantContact('billing')
billing.convert_emails()
