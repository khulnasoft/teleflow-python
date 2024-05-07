from unittest import TestCase, mock

import pkg_resources

from teleflow.api import InboundParseApi
from teleflow.config import TeleflowConfig
from tests.factories import MockResponse

__version__ = pkg_resources.get_distribution("teleflow").version


class InboundParseApiTests(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        TeleflowConfig.configure("sample.teleflow.khulnasoft.com", "api-key")
        cls.api = InboundParseApi()

    @mock.patch("requests.request")
    def test_validate_mx_record_setup(self, mock_request: mock.MagicMock) -> None:
        mock_request.return_value = MockResponse(200, {"data": {"mxRecordConfigured": True}})

        self.assertTrue(self.api.validate_mx_record_setup())

        mock_request.assert_called_once_with(
            method="GET",
            url="sample.teleflow.khulnasoft.com/v1/inbound-parse/mx/status",
            headers={"Authorization": "ApiKey api-key", "User-Agent": f"teleflow/python@{__version__}"},
            json=None,
            params=None,
            timeout=5,
        )
