"""This module is used to gather all DTO definitions related to the Topic resource in Teleflow"""

import dataclasses
from typing import List, Optional

from teleflow.dto.base import CamelCaseDto, DtoIterableDescriptor


@dataclasses.dataclass
class TriggerTopicDto(CamelCaseDto["TriggerTopicDto"]):
    """Topic definition for trigger"""

    topic_key: str
    """Topic key"""

    type: str
    """Topic type"""


@dataclasses.dataclass
class TopicDto(CamelCaseDto["TopicDto"]):
    """Topic definition"""

    camel_case_fields = ["key", "name"]
    # Actually, only these fields are editable in Teleflow, so prevent any activity on others

    key: str
    """Topic key"""

    name: Optional[str] = None
    """Name, required during creation"""

    _id: Optional[str] = None
    """Topic ID in Teleflow internal system"""

    _organization_id: Optional[str] = None
    """Organization ID in Teleflow internal storage system"""

    _environment_id: Optional[str] = None
    """Environment ID in Teleflow internal storage system"""

    subscribers: Optional[List[str]] = None
    """List of subscribers in the topic."""


@dataclasses.dataclass
class PaginatedTopicDto(CamelCaseDto["PaginatedTopicDto"]):
    """Paginated topic definition"""

    page: int = 0
    """Page number"""

    total_count: int = 0
    """Total count"""

    page_size: int = 0
    """Page size"""

    data: DtoIterableDescriptor[TopicDto] = DtoIterableDescriptor[TopicDto](default_factory=list, item_cls=TopicDto)
    """Data"""
