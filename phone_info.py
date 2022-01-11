import phonenumbers
from phonenumbers import timezone, geocoder, carrier
from opencage.geocoder import OpenCageGeocode
import requests
import json

import restricted

CARRIER_EMAIL_SUFFIX = {
    'verizon': '@vtext.com'
}

KEY = restricted.API_Key


class Phone:

    def __init__(self, number, country_code='+1', mobile_carrier=None):
        self.number = number
        self.country_code = country_code
        self.full_number = self.country_code+self.number
        self.coded_number = phonenumbers.parse(self.full_number)

        self.time_zone = timezone.time_zones_for_number(self.coded_number)
        if mobile_carrier is not None:
            self.carrier = mobile_carrier.lower()
        else:
            self.carrier = self.get_carrier()


        self.textable_number = self.get_textable_number()
        self.beeg_location = geocoder.description_for_number(self.coded_number, 'en')
        self.show_info()
        #self.geocoder = OpenCageGeocode(KEY)

    # Returning different results. Table for now.
    def get_carrier(self):
        if self.country_code == '+1':
            url = 'https://api.telnyx.com/v1/phone_number/1' + self.number
            html = requests.get(url).text
            data = json.loads(html)
            result = data["carrier"]["name"].split(' ')
            return result[-1].lower()
        else:
            return carrier.name_for_number(self.coded_number, 'en')


    def get_textable_number(self):
        if self.carrier in CARRIER_EMAIL_SUFFIX:
            return self.number + CARRIER_EMAIL_SUFFIX[self.carrier]
        else:
            return None

    def show_info(self):
        attributes = vars(self)
        for info in attributes:
            print(attributes[info])


