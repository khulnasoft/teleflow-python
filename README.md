# Python Teleflow SDK

[![PyPI](https://img.shields.io/pypi/v/teleflow.khulnasoft.comlor=blue)](https://pypi.org/project/teleflow/)
![Tests Status](https://github.com/khulnasoft/teleflow-python/actions/workflows/.github/workflows/tests.yml/badge.svg)
[![codecov](https://codecov.io/gh/khulnasoft/teleflow-python/branch/main/graph/badge.svg?token=RON7F8QTZX)](https://codecov.io/gh/khulnasoft/teleflow-python)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/teleflow)
![PyPI - License](https://img.shields.io/pypi/l/teleflow)
[![semantic-release: angular](https://img.shields.io/badge/semantic--release-angular-e10079?logo=semantic-release)](https://github.com/semantic-release/semantic-release)

---

The [Python Teleflow](https://teleflow.khulnasoft.com) SDK and package provides a fluent and expressive interface for interacting with [Teleflow's API](https://api-teleflow.khulnasoft.com/api) and managing notifications.

## Install

To install this package

```shell
# Via pip
pip install teleflow

# Via poetry
poetry add teleflow
```

## Contents

- [Install](#install)
- [Quick start](#quick-start)
- [Code Snippet Examples](#code-snippet-examples)
  - [Events](#events)
  - [Subscribers](#subscribers)
  - [Topics](#topics)
  - [Feeds](#feeds)
  - [Environments](#environments)
- [Go further](#go-further)
- [Development](#development)

## Quick start

This package is a wrapper of all the resources offered by Teleflow, we will just start by triggering an event on Teleflow.

To do this, you will need to:

1. Create your first notification workflow and keep in mind the identifier to trigger the workflow: https://docs-teleflow.khulnasoft.com/overview/quickstart/general-quickstart#create-a-workflow
2. Retrieve your API key from the Teleflow dashboard directly in the settings section: https://web.teleflow.khulnasoft.com/settings
3. Write code to trigger your first event:

```python
from teleflow.api import EventApi

event_api = EventApi("https://api-teleflow.khulnasoft.com", "<TELEFLOW_API_KEY>")
event_api.trigger(
    name="<YOUR_WORKFLOW_ID>",  # The workflow ID is the slug of the workflow name. It can be found on the workflow page.
    recipients="<YOUR_SUBSCRIBER_ID>",
    payload={},  # Your Teleflow payload goes here
)
```

This will trigger a notification to the subscribers.

## Code Snippet Examples

### Events

Firstly, make imports and declare the needed variables this way:

```python
from teleflow.api import EventApi

url = "https://api-teleflow.khulnasoft.com"
api_key = "<TELEFLOW_API_KEY>"

# You can sign up on https://web.teleflow.khulnasoft.com to get your API key from https://web.teleflow.khulnasoft.com/settings
```

**Trigger an event** - Send notification to subscribers:

```python
from teleflow.api import EventApi

teleflow = EventApi(url, api_key).trigger(
    name="digest-workflow-example",  # This is the Workflow ID. It can be found on the workflow page.
    recipients="<SUBSCRIBER_IDENTIFIER>", # The subscriber ID can be gotten from the dashboard.
    payload={},  # Your custom Teleflow payload goes here
)
```

**Bulk Trigger events** - Trigger multiple events at once:

```python
from teleflow.dto.event import InputEventDto
from teleflow.api import EventApi

url = "https://api-teleflow.khulnasoft.com"
api_key = "<TELEFLOW_API_KEY>"

event_1 = InputEventDto(
    name="digest-workflow-example",  # The workflow ID is the slug of the workflow name. It can be found on the workflow page.
    recipients="<SUBSCRIBER_IDENTIFIER>",
    payload={},  # Your custom Teleflow payload goes here
)
event_2 = InputEventDto(
    name="digest-workflow-example",
    recipients="<SUBSCRIBER_IDENTIFIER>",
    payload={},
)

teleflow = EventApi("https://api-teleflow.khulnasoft.com", api_key).trigger_bulk(events=[event1, event2])
```

**Include actor field:**

```python
from teleflow.api import EventApi

teleflow = EventApi(url, api_key).trigger(
    name="workflow_trigger_identifier",
    recipients="subscriber_id",
    actor={
        "subscriberId": "subscriber_id_actor"
    },
    payload={
        "key":"value"
    },
)
```

**Broadcast to all current subscribers:**

```python
teleflow = EventApi(url, api_key).broadcast(
    name="digest-workflow-example",
    payload={"customVariable": "value"},  # Optional
)
```

### Subscribers

```python
from teleflow.dto.subscriber import SubscriberDto
from teleflow.api.subscriber import SubscriberApi

url = "https://api-teleflow.khulnasoft.com"
api_key = "<TELEFLOW_API_KEY>"

# Define a subscriber instance
subscriber = SubscriberDto(
    email="teleflow_user@mail.com",
    subscriber_id="82a48af6ac82b3cc2157b57f", #This is what the subscriber_id looks like
    first_name="",  # Optional
    last_name="",  # Optional
    phone="",  # Optional
    avatar="",  # Optional
)

# Create a subscriber
teleflow = SubscriberApi(url, api_key).create(subscriber)

# Get a subscriber
teleflow = SubscriberApi(url, api_key).get(subscriber_id)

# Get list of subscribers
teleflow = SubscriberApi(url, api_key).list()
```

### Topics

```python
from teleflow.api import TopicApi

url = "<TELEFLOW_URL>"
api_key = "<TELEFLOW_API_KEY>"

# Create a topic
teleflow = TopicApi(url, api_key).create(
    key="new-customers", name="New business customers"
)

# Get a topic
teleflow = TopicApi(url, api_key).get(key="new-customers")

# List topics
teleflow = TopicApi(url, api_key).list()

# Rename a topic
teleflow = TopicApi(url, api_key).rename(key="new-customers", name="New business customers")

# Subscribe a list of subscribers to a topic
teleflow = TopicApi(url, api_key).subscribe(key="old-customers", subscribers="<LIST_OF_SUBSCRIBER_IDs>")

# Unsubscribe a list of subscribers from a topic
teleflow = TopicApi(url, api_key).unsubscribe(key="old-customers", subscribers="<LIST_OF_SUBSCRIBER_IDs>")

```

### Feeds

```python
from teleflow.api.feed import FeedApi

url = "<TELEFLOW_URL>"
api_key = "<TELEFLOW_API_KEY>"

# Create a Feed
teleflow = FeedApi(url, api_key).create(name="<SUPPLY_NAME_FOR_FEED>")

# Delete a Feed
FeedApi(url, api_key).delete(feed_id="<FEED_TELEFLOW_INTERNAL_ID>")

# List feeds
teleflow = FeedApi(url, api_key).list()
```

### Environments

```python
from teleflow.api.environment import EnvironmentApi

url = "<TELEFLOW_URL>"
api_key = "<TELEFLOW_API_KEY>"

# Create an Environment
teleflow = EnvironmentApi(url, api_key).create(
    name="<INSERT_NAME>",
    parent_id="<INSERT_PARENT_ID>" # Optional. Defaults to None
)

# # List existing environments
teleflow = EnvironmentApi(url, api_key).list()

# # Get the current environment
teleflow = EnvironmentApi(url, api_key).current()

# # Retrieve an environment's API_KEY
teleflow = EnvironmentApi(url, api_key).api_keys()

```

### Tenants

```python
from teleflow.api.tenant import TenantApi

url = "<TELEFLOW_URL>"
api_key = "<TELEFLOW_API_KEY>"

# Create an Environment
tenant = TenantApi(url, api_key).create(
    identifier="<INSERT_UNIQUE_TENANT_ID>",
    name="<INSERT_NAME>",
    data={} # Optional. Defaults to {}
)

# List existing tenants
tenants = TenantApi(url, api_key).list()
tenants = TenantApi(url, api_key).list(page=1, limit=10)

# Get a tenant
tenant = TenantApi(url, api_key).get("<TENANT-IDENTIFIER>")

# Patch some field of a tenant
tenant = TenantApi(url, api_key).patch(
    "<CURRENT-TENANT-IDENTIFIER>",
    identifier="<NEW-IDENTIFIER>",
    name="<NEW-NAME>",
    data="<NEW-DATA>"
)

# Delete a tenant
TenantApi(url, api_key).delete("<TENANT-IDENTIFIER>")
```

## Go further

After a quick start with the SDK, you'll quickly get to grips with the advanced use of the SDK and the other APIs available.

For this purpose, documentation is available here: https://teleflow-python.readthedocs.io/

## Development

```bash
# install deps
poetry install

# pre-commit
poetry run pre-commit install --install-hook
poetry run pre-commit install --install-hooks --hook-type commit-msg
```

## Contributing

Feature requests, bug reports and pull requests are welcome. Please create an [issue](https://github.com/khulnasoft/teleflow-python/issues).

## Support and Feedback

Be sure to visit the Teleflow official [documentation website](https://docs-teleflow.khulnasoft.com/docs) for additional information about our SDK.
If you need additional assistance, join our Discord server [here](https://discord.teleflow.khulnasoft.com).

## License

Teleflow Python SDK is licensed under the MIT License - see the [LICENSE](https://github.com/khulnasoft/teleflow-python/blob/main/LICENSE) file for details.
