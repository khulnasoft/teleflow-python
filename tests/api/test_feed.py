import types
from unittest import TestCase, mock

import pkg_resources

from teleflow.api import FeedApi
from teleflow.config import TeleflowConfig
from teleflow.dto.feed import FeedDto
from tests.factories import MockResponse

__version__ = pkg_resources.get_distribution("teleflow").version


class FeedApiTests(TestCase):
    api: FeedApi
    response_json = {
        "name": "test",
        "identifier": "test",
        "_organizationId": "63dafed97779f59258e3843f",
        "_environmentId": "63dafed97779f59258e38445",
        "_id": "63e969fcb6729e21337e2360",
        "deleted": None,
        "createdAt": "2023-02-12T22:36:44.611Z",
        "updatedAt": "2023-02-12T22:36:44.611Z",
        "__v": 0,
        "id": "63e969fcb6729e21337e2360",
    }
    expected_dto = FeedDto(
        name="test",
        identifier="test",
        _id="63e969fcb6729e21337e2360",
        _environment_id="63dafed97779f59258e38445",
        _organization_id="63dafed97779f59258e3843f",
        deleted=None,
        created_at="2023-02-12T22:36:44.611Z",
        updated_at="2023-02-12T22:36:44.611Z",
        id="63e969fcb6729e21337e2360",
    )

    @classmethod
    def setUpClass(cls) -> None:
        TeleflowConfig.configure("sample.teleflow.khulnasoft.com", "api-key")
        cls.api = FeedApi()

    @mock.patch("requests.request")
    def test_list_feeds(self, mock_request: mock.MagicMock) -> None:
        mock_request.return_value = MockResponse(200, {"data": [self.response_json]})

        res = self.api.list()
        self.assertIsInstance(res, types.GeneratorType)
        self.assertEqual(list(res), [self.expected_dto])

        mock_request.assert_called_once_with(
            method="GET",
            url="sample.teleflow.khulnasoft.com/v1/feeds",
            headers={"Authorization": "ApiKey api-key", "User-Agent": f"teleflow/python@{__version__}"},
            json=None,
            params=None,
            timeout=5,
        )

    @mock.patch("requests.request")
    def test_create_feed(self, mock_request: mock.MagicMock) -> None:
        mock_request.return_value = MockResponse(201, {"data": self.response_json})

        res = self.api.create("test")
        self.assertIsInstance(res, FeedDto)
        self.assertEqual(res, self.expected_dto)

        mock_request.assert_called_once_with(
            method="POST",
            url="sample.teleflow.khulnasoft.com/v1/feeds",
            headers={"Authorization": "ApiKey api-key", "User-Agent": f"teleflow/python@{__version__}"},
            json={"name": "test"},
            params=None,
            timeout=5,
        )

    @mock.patch("requests.request")
    def test_delete_feed(self, mock_request: mock.MagicMock) -> None:
        mock_request.return_value = MockResponse(204)

        self.assertIsNone(self.api.delete("63e969fcb6729e21337e2360"))  # type: ignore

        mock_request.assert_called_once_with(
            method="DELETE",
            url="sample.teleflow.khulnasoft.com/v1/feeds/63e969fcb6729e21337e2360",
            headers={"Authorization": "ApiKey api-key", "User-Agent": f"teleflow/python@{__version__}"},
            json=None,
            params=None,
            timeout=5,
        )
