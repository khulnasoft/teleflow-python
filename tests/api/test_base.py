from unittest import TestCase, mock

import pkg_resources
from requests.exceptions import HTTPError

from teleflow.api.base import Api
from teleflow.config import TeleflowConfig
from tests.factories import MockResponse

__version__ = pkg_resources.get_distribution("teleflow").version


class ApiTests(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        TeleflowConfig.configure("sample.teleflow.com", "api-key")
        cls.api = Api()

    @mock.patch("requests.request")
    def test_handle_request_with_header_override(self, mock_request: mock.MagicMock) -> None:
        mock_request.return_value = MockResponse(200, {})

        res = self.api.handle_request("GET", self.api._url, headers={"MyHeader": "value"})
        self.assertEqual(res, {})

        mock_request.assert_called_once_with(
            method="GET",
            url="sample.teleflow.com",
            headers={
                "Authorization": "ApiKey api-key",
                "User-Agent": f"teleflow/python@{__version__}",
                "MyHeader": "value",
            },
            json=None,
            params=None,
            timeout=5,
        )

    @mock.patch("requests.request")
    def test_handle_request_raise_with_details(self, mock_request: mock.MagicMock) -> None:
        mock_request.return_value = MockResponse(500, {"details": "my-detail"})

        self.assertRaises(
            HTTPError, lambda: self.api.handle_request("GET", self.api._url, headers={"MyHeader": "value"})
        )

        mock_request.assert_called_once_with(
            method="GET",
            url="sample.teleflow.com",
            headers={
                "Authorization": "ApiKey api-key",
                "User-Agent": f"teleflow/python@{__version__}",
                "MyHeader": "value",
            },
            json=None,
            params=None,
            timeout=5,
        )

    @mock.patch("requests.request")
    def test_handle_request_raise_without_details(self, mock_request: mock.MagicMock) -> None:
        mock_request.return_value = MockResponse(500, raise_on_json_decode=True)

        self.assertRaises(
            HTTPError, lambda: self.api.handle_request("GET", self.api._url, headers={"MyHeader": "value"})
        )

        mock_request.assert_called_once_with(
            method="GET",
            url="sample.teleflow.com",
            headers={
                "Authorization": "ApiKey api-key",
                "User-Agent": f"teleflow/python@{__version__}",
                "MyHeader": "value",
            },
            json=None,
            params=None,
            timeout=5,
        )

    @mock.patch("requests.request")
    def test_override_requests_timeout(self, mock_request: mock.MagicMock) -> None:
        mock_request.return_value = MockResponse(500, raise_on_json_decode=True)

        api = Api(requests_timeout=60)

        self.assertRaises(HTTPError, lambda: api.handle_request("GET", api._url, headers={"MyHeader": "value"}))

        mock_request.assert_called_once_with(
            method="GET",
            url="sample.teleflow.com",
            headers={
                "Authorization": "ApiKey api-key",
                "User-Agent": f"teleflow/python@{__version__}",
                "MyHeader": "value",
            },
            json=None,
            params=None,
            timeout=60,
        )

    @mock.patch("requests.request")
    def test_use_requests_session(self, mock_request: mock.MagicMock) -> None:
        session_mock = mock.MagicMock()
        session_mock.request.return_value = MockResponse(200, {})
        api = Api(session=session_mock)

        res = api.handle_request("GET", api._url, headers={"MyHeader": "value"})
        self.assertEqual(res, {})

        mock_request.assert_not_called()
        session_mock.request.assert_called_once_with(
            method="GET",
            url="sample.teleflow.com",
            headers={
                "Authorization": "ApiKey api-key",
                "User-Agent": f"teleflow/python@{__version__}",
                "MyHeader": "value",
            },
            json=None,
            params=None,
            timeout=5,
        )
