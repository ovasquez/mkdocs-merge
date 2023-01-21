# Changelog
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
