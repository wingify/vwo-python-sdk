# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
