# Copyright © 2019 Province of British Columbia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests to assure the PayBC service layer.

Test-Suite to ensure that the PayBC Service layer is working as expected.
"""
from unittest.mock import Mock, patch

from pay_api.services.paybc import PayBcService


INVOICE_REQUEST = {
    'entity_name': 'TEST',
    'contact_first_name': 'TEST',
    'contact_last_name': 'TEST',
    'address_line_1': 'TEST',
    'city': 'Victoria',
    'province': 'BC',
    'country': 'CA',
    'postal_code': 'A1A1A1',
    'customer_site_id': '1',
    'total': '10',
    'method_of_payment': 'CC',
    'lineItems': [
        {
            'name': 'TEST',
            'description': 'TEST',
            'amount': '10'
        }
    ]
}

PARTY_NUMBER = '98523'
ACCOUNT_NUMBER = '4099'
SITE_NUMBER = '1234'
INVOICE_NUMBER = '567890'
CONTACT_NUMBER = '123456'

PARTY = {
    'party_number': PARTY_NUMBER,
    'customer_name': 'TEST1',
    'links': [
        {
            'rel': 'collection',
            'href': 'https://heineken.cas.gov.bc.ca:7019/ords/cas/cfs/parties/'
        },
        {
            'rel': 'self',
            'href': 'https://heineken.cas.gov.bc.ca:7019/ords/cas/cfs/parties/98523/'
        },
        {
            'rel': 'accounts',
            'href': 'https://heineken.cas.gov.bc.ca:7019/ords/cas/cfs/parties/98523/accs/'
        }
    ]
}

ACCOUNT = {
    'account_number': ACCOUNT_NUMBER,
    'party_number': '98523',
    'account_description': 'TEST1',
    'links': [
        {
            'rel': 'collection',
            'href': 'https://heineken.cas.gov.bc.ca:7019/ords/cas/cfs/parties/98523/accs/'
        },
        {
            'rel': 'parent',
            'href': 'https://heineken.cas.gov.bc.ca:7019/ords/cas/cfs/parties/98523/'
        },
        {
            'rel': 'self',
            'href': 'https://heineken.cas.gov.bc.ca:7019/ords/cas/cfs/parties/98523/accs/4099/'
        },
        {
            'rel': 'sites',
            'href': 'https://heineken.cas.gov.bc.ca:7019/ords/cas/cfs/parties/98523/accs/4099/sites/ '
        }
    ]
}

SITE = {
    'party_number': PARTY_NUMBER,
    'account_number': ACCOUNT_NUMBER,
    'site_number': SITE_NUMBER
}

CONTACT = {
    'party_number': PARTY_NUMBER,
    'account_number': ACCOUNT_NUMBER,
    'site_number': SITE_NUMBER,
    'contact_number': CONTACT_NUMBER,
    'first_name': 'TEST',
    'last_name': 'TEST'
}

INVOICE = {
    'party_number': PARTY_NUMBER,
    'party_name': 'TEST',
    'account_number': ACCOUNT_NUMBER,
    'account_name': 'TEST',
    'site_number': SITE_NUMBER,
    'invoice_number': INVOICE_NUMBER,
    'total': '10',
    'amount_due': 10,
    'lines': [
        {
            'line_number': '1',
            'description': 'TEST',
            'unit_price': '10',
            'quantity': '1'
        }
    ]
}

ACCESS_TOKEN = 'C284Qa0McwFqPvfKa7pYGw..'


ACCESS_TOKEN_RESPONSE = {
    'access_token': ACCESS_TOKEN,
    'token_type': 'bearer',
    'expires_in': 3600
}


def test_get_token(app):
    """Test generate token for valid credentials."""
    with app.app_context():

        mock_get_token = patch('pay_api.services.oauth_service.requests.post')
        token = ACCESS_TOKEN_RESPONSE
        mock_get = mock_get_token.start()
        mock_get.return_value = Mock(status_code=201)
        mock_get.return_value.json.return_value = token

        get_token_response = PayBcService().get_token()

        mock_get_token.stop()

        assert get_token_response.json().get('access_token') == ACCESS_TOKEN


def test_create_party(app):
    """Test Create party."""
    with app.app_context():
        mock_create_party = patch('pay_api.services.oauth_service.requests.post')
        mock_post = mock_create_party.start()
        mock_post.return_value = Mock(status_code=201)
        mock_post.return_value.json.return_value = PARTY

        create_party_response = PayBcService().create_party(ACCESS_TOKEN, INVOICE_REQUEST)

        mock_create_party.stop()

        assert create_party_response.get('party_number') == PARTY_NUMBER


def test_create_account(app):
    """Test create account."""
    with app.app_context():
        mock_create_account = patch('pay_api.services.oauth_service.requests.post')

        mock_post = mock_create_account.start()
        mock_post.return_value = Mock(status_code=201)
        mock_post.return_value.json.return_value = ACCOUNT

        create_account_response = PayBcService().create_account(ACCESS_TOKEN, PARTY, INVOICE_REQUEST)

        mock_create_account.stop()

        assert create_account_response.get('account_number') == ACCOUNT_NUMBER


def test_create_site(app):
    """Test create site."""
    with app.app_context():
        mock_create_site = patch('pay_api.services.oauth_service.requests.post')

        mock_post = mock_create_site.start()
        mock_post.return_value = Mock(status_code=201)
        mock_post.return_value.json.return_value = SITE

        create_site_response = PayBcService().create_site(ACCESS_TOKEN, ACCOUNT, INVOICE_REQUEST)

        mock_create_site.stop()

        assert create_site_response.get('site_number') == SITE_NUMBER


def test_create_contact(app):
    """Test create contact."""
    with app.app_context():
        mock_create_contact = patch('pay_api.services.oauth_service.requests.post')

        mock_post = mock_create_contact.start()
        mock_post.return_value = Mock(status_code=201)
        mock_post.return_value.json.return_value = CONTACT

        create_contact_response = PayBcService().create_contact(ACCESS_TOKEN, SITE, INVOICE_REQUEST)

        mock_create_contact.stop()

        assert create_contact_response.get('contact_number') == CONTACT_NUMBER


def test_create_invoice(app):
    """Test create invoice."""
    with app.app_context():
        mock_create_invoice = patch('pay_api.services.oauth_service.requests.post')

        mock_post = mock_create_invoice.start()
        mock_post.return_value = Mock(status_code=201)
        mock_post.return_value.json.return_value = INVOICE

        create_invoice_response = PayBcService().create_invoice(ACCESS_TOKEN, SITE, INVOICE_REQUEST)

        mock_create_invoice.stop()

        assert create_invoice_response.get('invoice_number') == INVOICE_NUMBER
