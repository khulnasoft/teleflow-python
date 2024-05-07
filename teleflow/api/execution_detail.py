"""
This module is used to define the ``ExecutionDetailApi``, a python wrapper
to interact with ``ExecutionDetails`` in Teleflow.
"""

from typing import Iterator, Optional

import requests

from teleflow.api.base import Api
from teleflow.constants import EXECUTION_DETAILS_ENDPOINT
from teleflow.dto import ExecutionDetailDto


class ExecutionDetailApi(Api):
    """This class aims to handle all API methods around execution details in Teleflow"""

    def __init__(
        self,
        url: Optional[str] = None,
        api_key: Optional[str] = None,
        requests_timeout: Optional[int] = None,
        session: Optional[requests.Session] = None,
    ) -> None:
        super().__init__(url=url, api_key=api_key, requests_timeout=requests_timeout, session=session)

        self._execution_detail_url = f"{self._url}{EXECUTION_DETAILS_ENDPOINT}"

    def list(self, notification_id: str, subscriber_id: str) -> Iterator[ExecutionDetailDto]:
        """List existing execution details using provided notification and subscriber IDs

        Args:
            notification_id: The notification ID in Teleflow
            subscriber_id: The subscriber ID in Teleflow

        Yields:
            Mapped execution detail
        """
        results = self.handle_request(
            "GET",
            self._execution_detail_url,
            payload={"notificationId": notification_id, "subscriberId": subscriber_id},
        )["data"]
        for result in results:
            yield ExecutionDetailDto.from_camel_case(result)
