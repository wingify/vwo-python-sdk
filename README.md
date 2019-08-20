# VWO Python SDK

[![PyPI version](https://badge.fury.io/py/vwo-python-sdk.svg)](https://pypi.org/project/optimizely-sdk) [![Build Status](http://img.shields.io/travis/wingify/vwo-python-sdk/master.svg?style=flat)](http://travis-ci.org/wingify/vwo-python-sdk) [![Coverage Status](https://coveralls.io/repos/github/wingify/vwo-python-sdk/badge.svg?branch=master)](https://coveralls.io/github/wingify/vwo-python-sdk?branch=master)

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
vwo_client_instance = vwo.VWO(settings_file)
```

**API usage**

```python
# activate API
variation_name = vwo_client_instance.activate(ab_campaign_test_key, user_id)

# getVariation API
variation_name = vwo_client_instance.getVariation(ab_campaign_test_key, user_id)

# track API
vwo_client_instance.track(ab_campaign_test_key, user_id, ab_campaign_goal_identifeir, revenue_value)
```

**Custom Logger** - change log level only

```python
import vwo
from vwo import logger

custom_logger = logger.DefaultLogger(logger.DEBUG)

settings_file = vwo.get_settings_file(account_id, sdk_key)
vwo_client_instance = vwo.VWO(settings_file, logger = custom_logger)
```

**Custom Logger** - implement your own logger method

```python
import vwo
from vwo import logger

class CustomLogger:
   def log(self, level, message):
      print(level, message)
      # ...write to file or database or integrate with any third-party service

settings_file = vwo.get_settings_file(account_id, sdk_key)
vwo_client_instance = vwo.VWO(settings_file, logger = CustomLogger())
```

**User Profile Service**

```python
import vwo
from vwo import logger

class user_profile_service(UserProfileService):
  def lookup(self, user_id):
    # ...code here for getting data
    # return data

  def save(self, user_profile_obj):
    # ...code to persist data

ups = user_profile_service()

settings_file = vwo.get_settings_file(account_id, sdk_key)
vwo_client_instance = vwo.VWO(settings_file, user_profile_service = ups)
```

## Documentation

Refer [Official VWO Documentation](https://developers.vwo.com/reference#server-side-introduction)

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

## Credits

We use the following open-source projects which are published under MIT License. Thanks to the authors and maintainers of the corresponding projects.

* [mmh3](https://pypi.org/project/mmh3/) by Hajime Senuma
* [requests](https://github.com/psf/requests) by [@psf](https://github.com/psf)
* [jsonschema](https://github.com/Julian/jsonschema) by [@Julian](https://github.com/Julian)


## Authors

* Main Contributor - [Shravan Chaudhary](https://github.com/shravanchaudhary)
* Repo health maintainer - [Varun Malhotra](https://github.com/softvar)([@s0ftvar](https://twitter.com/s0ftvar))

## Contributing

Please go through our [contributing guidelines](https://github.com/wingify/vwo-python-sdk/blob/master/CONTRIBUTING.md)

## Code of Conduct

[Code of Conduct](https://github.com/wingify/vwo-python-sdk/blob/master/CODE_OF_CONDUCT.md)

## License

```text
    MIT License

    Copyright (c) 2019 Wingify Software Pvt. Ltd.

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
```
