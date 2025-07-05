# Changelog

## 0.11.0 - July 4, 2025

- **Breaking change:** Fixed multiple merge duplication bug where running merge operations multiple times would create duplicate site entries in the master navigation.
- **Behavior change:** When the same site is merged multiple times, existing entries are now replaced (not duplicated) to allow for site updates.
- **Documentation pipeline:** Changed documentation publishing to manual trigger only.
- Added comprehensive test suite for multiple merge scenarios including mixed existing/new sites and interaction with the unify_sites feature.
- Formatting all code with black formatter.

## 0.10.0 - May 17, 2025

- Permanent fix for [#20](https://github.com/ovasquez/mkdocs-merge/issues/20): replaced `dir_util.copy_tree` with `shutil.copytree` to use a built-in and maintained API in the directory merge functionality.
- Added a test to verify the scenario of deleting paths and merging them again when using mkdocs-merge as a module.

## 0.9.0 - July 30, 2024

- Fixed bug of `dir_util.copy_tree` caused by setuptools moving to 70.2.0 (fixes [#20](https://github.com/ovasquez/mkdocs-merge/issues/20)).
- Updated dependency on deprecated distutils package to use setuptools version.
- Updated project to use `pyproject.toml` instead of `setup.py` (package version now has to be manually kept in sync).

## 0.8.0 - January 20, 2023

- Added support for section index pages
  [feature from MkDocs Material](https://squidfunk.github.io/mkdocs-material/setup/setting-up-navigation/#section-index-pages)
  (thanks to [@Acerinth](https://github.com/Acerinth)).

## 0.7.0 - November 16, 2022

- **Breaking change:** removed support for Python 2 and Python 3.4.
- Updated several dependencies.
- DEV: migrated tests from nose to pytest.

## 0.6.0 - August 29, 2018

- **Breaking change:** added support for added support for MkDocs 1.0 and dropped support for earlier versions.

## 0.5.0 - June 1, 2018

- Fixed the merge process ignoring the `docs` folder in the `mkdocs.yml` of the
  sites to merge.
- Removed support for Python 3.3 due to pip removing support for it.

## 0.4.2 - February 14, 2018

- Fixed import error in `merge.py` when used in Windows.

## 0.4.1 - February 14, 2018

- Fixed import error when used from CLI.

## 0.4.0 - February 2, 2018

- Separate CLI functionality from the Merge logic for a more module friendly package.
