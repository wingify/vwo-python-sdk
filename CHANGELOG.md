# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.14.0] - 2021-04-29

### Added

- Sending stats which are used for launching the SDK like storage service, logger, and integrations, etc. in tracking calls(track-user and batch-event). This is solely for debugging purpose. We are only sending whether a particular key is used not the actual value of the key.

### Changed

- Removed sending user-id, that is provided in the various APIs, in the tracking calls to VWO server as it might contain sensitive PII data.
- SDK Key will not be logged in any log message, for example, tracking call logs.

## [1.13.0] - 2021-03-16

### Added

- Exposed lifecycle hook events. This feature allows sending VWO data to third party integrations.

### Changed

- Introduced `integrations` param in `launch` API to enable receiving hooks for the third party integrations.

```py
class Integrations(object):
    def __init__(self):
        pass

    def callback(self, properties):
        print(properties)

vwo_instance = vwo.launch(settings_file, integrations=Integrations())
```

## [1.12.0] - 2021-03-16

### Changed

- If User Storage Service is provided, do not track same visitor multiple times.

You can pass `should_track_returning_user` as `True` in case you prefer to track duplicate visitors.

```py
vwo_client_instance.activate(campaign_key, user_id, should_track_returning_user=True)
```

Or, you can also pass `should_track_returning_user` at the time of instantiating VWO SDK client. This will avoid passing the flag in different API calls.

```py
vwo_client_instance = vwo.launch(
    settings_file=settings_file,
    user_storage_service = user_storage_service,
    should_track_returning_user=True
)
```

If `should_track_returning_user` param is passed at the time of instantiating the SDK as well as in the API options as mentioned above, then the API options value will be considered.

- If User Storage Service is provided, campaign activation is mandatory before tracking any goal, getting variation of a campaign, and getting value of the feature's variable.

**Correct Usage**

```py
vwo_client_instance.activate(campaign_key, user_id, custom_variables = custom_variables, variation_targeting_variables = variation_targeting_variables)
vwo_client_instance.track(campaign_key, user_id, goal_identifier, custom_variables = custom_variables, variation_targeting_variables = variation_targeting_variables)
```

**Wrong Usage**

```py
# Calling track API before activate API
# This will not track goal as campaign has not been activated yet.
vwo_client_instance.track(campaign_key, user_id, goal_identifier, custom_variables = custom_variables, variation_targeting_variables = variation_targeting_variables)

# After calling track API
vwo_client_instance.activate(campaign_key, user_id, custom_variables = custom_variables, variation_targeting_variables = variation_targeting_variables)
```

## [1.11.0] - 2021-02-20
### Added
- Added support for batching of events sent to VWO server
- Intoduced `batch_events` config in launch API for setting when to send bulk events
- Added `flush_events` API to manually flush the batch events queue when `batch_events` config is passed. Note: `batch_events` config i.e. `events_per_request` and `request_time_interval` won't be considered while manually flushing
- If `request_time_interval` is passed, it will only set the timer when the first event will arrive
- If `request_time_interval` is provided, after flushing of events, new interval will be registered when the first event will arrive

```py
def flush_callback(err, events):
  print(err)
  print(events)

settings_file = vwo.get_settings_file(account_id, sdk_key)
vwo_client_instance = vwo.launch(
    settings_file=settings_file,
    batch_events={
        'events_per_request': 1000, # specify the number of events
         'request_time_interval': 10000, # specify the time limit fordraining the events (in seconds)
        'flush_callback': flush_callback # optional callback to execute when queue events are flushed
    }
)

# (optional): Manually flush the batch events queue to send impressions to VWO server.
vwo_client_instance.flush_events(mode='sync'); // two modes are available sync and async
```

## [1.10.0] - 2021-02-15
### Added
- Webhooks support
- Introduced `get_and_update_settings_file` API to fetch and update settings-file in case of webhook-trigger

## [1.8.2] - 2021-02-10

### Changed

- Changed copyright header year from 2020 to 2021
- Added `long_description_content_type` in setup.py so that `long_description` can be rendered properly on [PyPI](https://pypi.org/project/vwo-python-sdk/).

## [1.8.1] - 2020-05-19
### Added
- Introduced launch API to initialize the VWO instance
- Integrated black formatter and doc_checker pre-push hook for development

#### Before
```py
from vwo import VWO
vwo_client_instance = VWO(settings_file)
```
#### After
```py
from vwo import launch
vwo_client_instance = launch(settings_file)
```

## [1.8.0] - 2020-04-29
### Changed
- Update track API to handle duplicate and unique conversions and corresponding changes in VWO `init` method
- Update track API to track a goal globally across campaigns with the same `goal_identifier` and corresponding changes in VWO `init` method
```python
# it will track goal having `goal_identifier` of campaign having `campaign_key` for the user having `user_id` as id.
vwo_client_instance.track(campaign_key, user_id, goal_identifier)
# it will track goal having `goal_identifier` of campaigns having `campaign_key1` and `campaign_key2` for the user having `user_id` as id.
vwo_client_instance.track([campaign_key1, campaign_key2], user_id, goal_identifier)
# it will track goal having `goal_identifier` of all the campaigns
vwo_client_instance.track(None, user_id, goal_identifier)
```

## [1.6.3] - 2020-02-03
### Changed
- Updated year in Apache-2.0 Copyright header in all source, tests and scripts files.

## [1.6.2] - 2020-01-27
### Changed
- Fixed test case data files to remove ambiguity while running test cases in python 3.5

## [1.6.0] - 2020-01-15
### Breaking Changes
To prevent ordered arguments and increasing use-cases, we are moving all optional arguments to be passed via `kwargs`.

- customVariables argument in APIs: `activate`, `get_variation`, `track`, `is_feature_enabled`, and `get_feature_variable_value` will now be passed via `kwargs`.
- `revenueValue` parameter in `track` API via `kwargs`

#### Before
```py
# activae API
vwo_client_instance.activate(campaign_key, user_id)
# getVariation API
vwo_client_instance.get_variation(campaign_key, user_id)
# track API
vwo_client_instance.track(campaign_key, user_id, goalIdentifier, revenueValue)
# isFeatureEnabled API
vwo_client_instance.is_feature_enabled(campaign_key, user_id)
# getFeatureVariableValue API
vwo_client_instance.get_feature_variable_value(campaign_key, variableKey, user_id)
```
#### After
```py
custom_variables = {}
variation_targeting_variables = {}

# activae API
vwo_client_instance.activate(campaign_key, user_id, custom_variables = custom_variables, variation_targeting_variables = variation_targeting_variables)
# getVariation API
vwo_client_instance.get_variation(campaign_key, user_id, custom_variables = custom_variables, variation_targeting_variables = variation_targeting_variables)
# track API
vwo_client_instance.track(campaign_key, user_id, goalIdentifier, revenue_value = revenue_value, custom_variables = custom_variables, variation_targeting_variables = variation_targeting_variables)
# isFeatureEnabled API
vwo_client_instance.is_feature_enabled(campaign_key, user_id, custom_variables = custom_variables, variation_targeting_variables = variation_targeting_variables)
# getFeatureVariableValue API
vwo_client_instance.get_feature_variable_value(campaign_key, variableKey, user_id, custom_variables = custom_variables, variation_targeting_variables = variation_targeting_variables)
```
### Added
Forced Variation capabilites
- Introduced `Forced Variation` to force certain users into specific variation. Forcing can be based on User IDs or custom variables defined.
### Changed
- All existing APIs to handle variation-targeting-variables as an option for forcing variation
- Code refactored to support Whitelisting.


## [1.5.0] - 2019-11-29
### Added
Pre and Post segmentation capabilites
- Introduced new Segmentation service to evaluate whether user is eligible for campaign based on campaign pre-segmentation conditions and passed custom-variables
### Changed
- All existing APIs to handle custom-variables for tageting audience
- Code refactored to support campaign tageting and post segmentation


## [1.4.1] - 2019-11-28
### Changed
- Fix case when no call was made when Control was returned for feature-test in `isFeatureEnabled` API and feature is not enabled for it.


## [1.4.0] - 2019-11-28
### Added
Feature Rollout and Feature Test capabilities
- Introduced two new APIs i.e. `isFeatureEnabled` and `getFeatureVariableValue`
### Changed
- Existing APIs to handle new type of campaigns i.e. feature-rollout and feature-test
- Code refactored to support feature-rollout and feature-test capabilites


## [1.3.0] - 2019-11-21
### Changed
- Change MIT License to Apache-2.0
- Added apache copyright-header in each file
- Add NOTICE.txt file complying with Apache LICENSE
- Give attribution to the third-party libraries being used and mention StackOverflow


## [1.2.0] - 2019-10-15
### Changed
- Fix reusing Singleton class instance by creating new instance on re-initialization of SDK


## [1.0.0] - 2019-10-15
### Added
- First release with Server-side A/B capabilities
