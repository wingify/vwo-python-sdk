# VWO Python SDK

[![PyPI version](https://badge.fury.io/py/vwo-python-sdk.svg)](https://pypi.org/project/vwo-python-sdk)
[![CI](https://github.com/wingify/vwo-python-sdk/workflows/CI/badge.svg?branch=master)](https://github.com/wingify/vwo-python-sdk/actions?query=workflow%3ACI)
[![codecov](https://codecov.io/gh/wingify/vwo-python-sdk/branch/master/graph/badge.svg?token=813UYYMWGM)](https://codecov.io/gh/wingify/vwo-python-sdk)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](http://www.apache.org/licenses/LICENSE-2.0)

This open source library allows you to A/B Test your Website at server-side.

## Requirements

* Works with Python: 2.7 onwards. Python 3 is also supported.

## Installation

It's recommended you use [virtualenv](https://virtualenv.pypa.io/en/latest/) to create isolated Python environments.

```bash
pip install vwo-python-sdk
```

## Basic usage

**Importing and Instantiation**

```python
import vwo

settings_file = vwo.get_settings_file(account_id, sdk_key)
vwo_client_instance = vwo.launch(settings_file)
```

**API usage**

```python
# activate API
variation_name = vwo_client_instance.activate(ab_campaign_key, user_id)

# get_variation_name API
variation_name = vwo_client_instance.get_variation_name(ab_campaign_key, user_id)

# track API
vwo_client_instance.track(ab_campaign_key, user_id, ab_campaign_goal_identifeir, revenue_value)
```

**Log Level** - pass log_level to SDK

```python
import vwo
from vwo import LogLevels

settings_file = vwo.get_settings_file(account_id, sdk_key)
vwo_client_instance = vwo.launch(settings_file, log_level=LogLevels.DEBUG)
```

**Custom Logger** - implement your own logger method

```python
import vwo

class CustomLogger:
   def log(self, level, message):
      print(level, message)
      # ...write to file or database or integrate with any third-party service

settings_file = vwo.get_settings_file(account_id, sdk_key)
vwo_client_instance = vwo.launch(settings_file, logger = CustomLogger())
```

**User Storage Service**

```python
import vwo
from vwo import logger

class user_storage(UserStorage):
  def get(self, user_id, campaign_key):
    # ...code here for getting data
    # return data

  def set(self, user_storage_data):
    # ...code to persist data

us = user_storage()

settings_file = vwo.get_settings_file(account_id, sdk_key)
vwo_client_instance = vwo.launch(settings_file, user_storage = us)
```

## Documentation

Refer [Official VWO Documentation](https://developers.vwo.com/docs/fullstack-overview)

## Local development

```bash
python setup.py develop
```

## Running Unit Tests

```bash
python setup.py test
```

## Demo Python application

[vwo-python-sdk-example](https://github.com/wingify/vwo-python-sdk-example)

## Third-party Resources and Credits

Refer [third-party-attributions.txt](https://github.com/wingify/vwo-python-sdk/blob/master/third-party-attributions.txt)

## Authors

* Main Contributor - [Shravan Chaudhary](https://github.com/shravanchaudhary)
* Repo health maintainer - [Varun Malhotra](https://github.com/softvar)([@s0ftvar](https://twitter.com/s0ftvar))

## Changelog

Refer [CHANGELOG.md](https://github.com/wingify/vwo-python-sdk/blob/master/CHANGELOG.md)

## Contributing

Please go through our [contributing guidelines](https://github.com/wingify/vwo-python-sdk/blob/master/CONTRIBUTING.md)


## Code of Conduct

[Code of Conduct](https://github.com/wingify/vwo-python-sdk/blob/master/CODE_OF_CONDUCT.md)

## License

[Apache License, Version 2.0](https://github.com/wingify/vwo-python-sdk/blob/master/LICENSE)

Copyright 2019-2021 Wingify Software Pvt. Ltd.
