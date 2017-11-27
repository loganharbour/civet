
# Copyright 2016 Battelle Energy Alliance, LLC
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

from django.test import TestCase, RequestFactory, Client
from django.contrib.messages.storage.fallback import FallbackStorage
from django.core.urlresolvers import reverse
from django.conf import settings
from mock import patch
from requests_oauthlib import OAuth2Session
from ci import bitbucket, oauth_api
from ci.tests import utils
import json

class OAuthTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        utils.create_git_server(host_type=settings.GITSERVER_BITBUCKET)

    def request_post_json(self, data):
        jdata = json.dumps(data)
        request = self.factory.post('/', jdata, content_type='application/json')
        # to allow for the messages framework to work
        setattr(request, 'session', {})
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        return request

    def test_sign_in(self):
        url = reverse('ci:bitbucket:sign_in')
        response = self.client.get(url)
        self.assertIn('bitbucket_state', self.client.session)
        state = self.client.session['bitbucket_state']
        self.assertIn(state, response.url)
        self.assertIn('state', response.url)

        # already signed in
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302) # redirect

        session = self.client.session
        session['bitbucket_token'] = {'access_token': '1234', 'token_type': 'bearer', 'scope': 'repo'}
        session.save()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302) # redirect

    def test_update_user(self):
        user = utils.get_test_user()
        session = {'bitbucket_token': json.loads(user.token), 'bitbucket_user': user.name}
        auth = bitbucket.oauth.BitBucketAuth()
        auth.update_user(session)
        user2 = utils.create_user()
        session['bitbucket_user'] = user2.name
        auth.update_user(session)

    class dummy_json_request(object):
        def json(self):
            return {'name': 'value'}

    def test_get_json_value(self):
        with self.assertRaises(Exception):
            bitbucket.oauth.get_json_value(None, 'name')

        dummy_request = self.dummy_json_request()
        with self.assertRaises(oauth_api.OAuthException):
            auth = bitbucket.oauth.BitBucketAuth()
            auth.get_json_value(dummy_request, 'foo')

        val = auth.get_json_value(dummy_request, 'name')
        self.assertEqual(val, 'value')


    class JsonResponse(object):
        def __init__(self, data):
            self.data = data
        def json(self):
            return self.data

    @patch.object(OAuth2Session, 'fetch_token')
    @patch.object(OAuth2Session, 'get')
    def test_callback(self, mock_get, mock_fetch_token):
        user = utils.get_test_user()
        auth = bitbucket.oauth.BitBucketAuth()
        mock_fetch_token.return_value = {'access_token': '1234', 'token_type': 'bearer', 'scope': 'repo'}
        mock_get.return_value = self.JsonResponse({auth._callback_user_key: user.name})

        session = self.client.session
        session[auth._state_key] = 'state'
        session.save()
        url = reverse('ci:bitbucket:callback')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)

        mock_fetch_token.side_effect = Exception('Side effect')
        url = reverse('ci:bitbucket:callback')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)


    def test_sign_out(self):
        session = self.client.session
        session['bitbucket_token'] = 'token'
        session['bitbucket_state'] = 'state'
        session['bitbucket_user'] = 'user'
        session.save()
        url = reverse('ci:bitbucket:sign_out')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302) # redirect
        # make sure the session variables are gone
        self.assertNotIn('bitbucket_token', self.client.session)
        self.assertNotIn('bitbucket_state', self.client.session)
        self.assertNotIn('bitbucket_user', self.client.session)

        data = {'source_url': reverse('ci:main')}
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, 302) # redirect

    def test_session(self):
        user = utils.get_test_user()
        oauth = bitbucket.oauth.BitBucketAuth()
        self.assertEqual(oauth.start_session(self.client.session), None)

        session = self.client.session
        self.assertFalse(oauth.is_signed_in(session))
        session['bitbucket_user'] = 'no_user'
        session.save()
        self.assertFalse(oauth.is_signed_in(session))
        session['bitbucket_token'] = 'token'
        session.save()
        self.assertTrue(oauth.is_signed_in(session))
        self.assertEqual(oauth.signed_in_user(user.server, session), None)
        self.assertNotEqual(oauth.start_session(session), None)

        session['bitbucket_user'] = user.name
        session.save()
        self.assertEqual(oauth.signed_in_user(user.server, session), user)
        self.assertNotEqual(oauth.user_token_to_oauth_token(user), None)
        user2 = utils.create_user()
        self.assertEqual(oauth.user_token_to_oauth_token(user2), None)

        self.assertNotEqual(oauth.start_session_for_user(user), None)

        oauth.set_browser_session_from_user(session, user)
        session.save()
        self.assertEqual(session['bitbucket_user'], user.name)
