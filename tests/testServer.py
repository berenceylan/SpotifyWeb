import sys
import threading
import urllib.request

import unittest

ServerModule = sys.modules["SpotifyWeb.src.spotify.Server"]

Server = ServerModule.Server

class TestServer(unittest.TestCase):
  def test_roundtrip(self):
    oauth2_url = "some url"
    redirect_port = 1337

    def send_http_request_to_self():
      urllib.request.urlopen("http://localhost:{}/".format(str(redirect_port))).read()

    def send_oauth2_request(url):
      self.assertEqual(url, oauth2_url)

      threading.Timer(2, send_http_request_to_self).start()

    def handle(redirect_response):
      self.assertEqual(redirect_response, "/")

    Server.get_redirect_response(send_oauth2_request, oauth2_url, redirect_port, handle, available_duration_for_login_in_seconds = 5)

  def test_circuit_breaker(self):
    oauth2_url = "some url"
    redirect_port = 1337

    def send_oauth2_request(url):
      self.assertEqual(url, oauth2_url)
      # don't do anything

    def handle(redirect_response):
      self.assertEqual(redirect_response, "/")

    Server.get_redirect_response(send_oauth2_request, oauth2_url, redirect_port, handle, available_duration_for_login_in_seconds = 2)
