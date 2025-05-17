# MkDocs Merge

This simple tool allows you to merge the source of multiple [MkDocs](http://www.mkdocs.org/) sites
into a single one converting each of the specified sites to a sub-site of the master site.

Supports unification of sites with the same `site_name` into a single sub-site.

> Note: Since version 0.6 MkDocs Merge added support for MkDocs 1.0 and dropped
> support for earlier versions.
> See here for more details about the changes in [MkDocs 1.0](https://www.mkdocs.org/about/release-notes/#version-10-2018-08-03).

---
[![PyPI version](https://img.shields.io/pypi/v/mkdocs-merge.svg)](https://pypi.python.org/pypi/mkdocs-merge)
[![MkDocs Merge Validation Build](https://github.com/ovasquez/mkdocs-merge/actions/workflows/build.yml/badge.svg)](https://github.com/ovasquez/mkdocs-merge/actions/workflows/build.yml)

MkDocs-Merge supports Python versions 3.5+ and pypy.

## Install

```bash
$ pip install mkdocs-merge
```

## Usage

```bash
$ mkdocs-merge run MASTER_SITE SITES [-u]...
```

### Parameters

- `MASTER_SITE`: the path to the MkDocs site where the base `mkdocs.yml` file resides. This is where all other sites
    will be merged into.
- `SITES`: the paths to each of the MkDocs sites that will be merged. Each of these paths is expected to have a
    `mkdocs.yml` file and a `docs` folder.
- `-u` (optional): Unify sites with the same "site_name" into a single sub-site.  

### Example

```bash
$ mkdocs-merge run root/mypath/mysite /another/path/new-site /newpath/website
```

A single MkDocs site will be created in `root/mypath/mysite`, and the sites in
`/another/path/new-site` and `/newpath/website` will be added as sub-pages.

**Original `root/mypath/mysite/mkdocs.yml`**

```yaml
...
nav:
  - Home: index.md
  - About: about.md
```

**Merged `root/mypath/mysite/mkdocs.yml`**

```yaml
...
nav:
  - Home: index.md
  - About: about.md
  - new-site: new-site/home/another.md # Page merged from /another/path/new-site
  - website: website/index.md # Page merged from /newpath/website
```

## Development

### Dev Install

Clone the repository and specify the `dev` dependencies on the install command.
Project has been updated to use `pyproject.toml` so the version has to be manually synchronized.

#### Setup Virtual Environment

Before installing the package, create and activate a virtual environment in the root directory of the repo:

```bash
cd <root of the cloned repo>
python -m venv .venv
source .venv/bin/activate
```

#### Install the package for development mode

```bash
# Using quotes for zsh compatibility
$ pip install -e '.[dev]'
```

### Test

The tests can be run using `tox` from the root directory. `tox` is part of the development dependencies:

```bash
$ tox
```

### Publishing

The publishing process was updated to use GitHub Actions.

## Project Status

Very basic implementation. The code works but doesn't allow to specify options for the merging.

### Pending work

- [ ] Refactoring of large functions.
- [x] GitHub Actions build.
- [x] GitHub Actions release automation.
- [x] Publish pip package.
- [ ] Better error handling.
- [x] Merge configuration via CLI options.
- [x] Unit testing (work in progress).
- [ ] CLI integration testing.
- [ ] Consider more complex cases.
- [x] Make MkDocs Merge module friendly: thanks to [mihaipopescu](https://github.com/mihaipopescu)
