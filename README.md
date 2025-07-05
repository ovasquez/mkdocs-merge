# MkDocs Merge

This simple tool allows you to merge the source of multiple [MkDocs](http://www.mkdocs.org/) sites
into a single one converting each of the specified sites to a sub-site of the master site.

**Key Features:**

- Merge multiple MkDocs sites into a single master site
- Automatic deduplication: multiple merges replace existing entries (no duplicates)
- Site unification: combine sites with the same name into single navigation sections
- File system updates: content is properly replaced when re-merging sites

## Important Behavior Note (v0.11.0+)

When merging the same site multiple times, existing entries are **replaced** (not duplicated). This allows you to update subsites by re-running the merge command.

## Changelog

Access the changelog here: https://ovasquez.github.io/mkdocs-merge/changelog/

> Note: Since version 0.6 MkDocs Merge added support for MkDocs 1.0 and dropped
> support for earlier versions.
> See here for more details about the changes in [MkDocs 1.0](https://www.mkdocs.org/about/release-notes/#version-10-2018-08-03).

---

[![PyPI version](https://img.shields.io/pypi/v/mkdocs-merge.svg)](https://pypi.python.org/pypi/mkdocs-merge)
[![MkDocs Merge Validation Build](https://github.com/ovasquez/mkdocs-merge/actions/workflows/build.yml/badge.svg)](https://github.com/ovasquez/mkdocs-merge/actions/workflows/build.yml)

MkDocs-Merge officially supports Python versions 3.8, 3.9 and 3.10. It has been tested to work correctly in previous 3.X versions, but those are no longer officially supported.

## Install

```bash
$ pip install mkdocs-merge
```

## Usage

```bash
$ mkdocs-merge run MASTER_SITE SITES [-u]...
```

### Parameters

- `MASTER_SITE`: Path to the main MkDocs site (contains `mkdocs.yml`)
- `SITES`: Paths to MkDocs sites to merge (each needs `mkdocs.yml` and `docs/` folder)
- `-u` (optional): Unify sites with the same name into one section

> **Note:** Re-merging the same site replaces the existing content (enables updates).

## Unification Feature

The `-u` flag combines multiple sites with the same `site_name` into a single navigation section.

**Without `-u`:** Sites with the same name create duplicate navigation entries.  
**With `-u`:** Sites with the same name are merged into one section.

**Use Cases:**

- Microservices documentation grouped under "Services"
- Multi-repository projects in the same logical section
- Team-based documentation contributions

### Example

```bash
$ mkdocs-merge run root/mypath/mysite /another/path/new-site /newpath/website
```

A single MkDocs site will be created in `root/mypath/mysite`, and the sites in
`/another/path/new-site` and `/newpath/website` will be added as sub-pages.

**Original `root/mypath/mysite/mkdocs.yml`**

```yaml
---
nav:
  - Home: index.md
  - About: about.md
```

**Merged `root/mypath/mysite/mkdocs.yml`**

```yaml
---
nav:
  - Home: index.md
  - About: about.md
  - new-site: new-site/home/another.md # Page merged from /another/path/new-site
  - website: website/index.md # Page merged from /newpath/website
```

## Development

### Dev Install

Clone the repository and specify the `dev` dependencies on the install command.
Project has been updated to use `pyproject.toml` so the version has to be manually synchronized in both `__init__.py` and `pyproject.toml`.

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

Package publishing uses GitHub Actions. Documentation is published manually from main branch via Actions tab.

## Project Status

Very basic implementation. The code works but doesn't allow to specify options for the merging.

### Pending work

- [ ] Refactoring of large functions.
- [x] GitHub Actions build.
- [x] Publish pip package.
- [ ] Better error handling.
- [x] Merge configuration via CLI options.
- [x] Unit testing (work in progress).
- [ ] CLI integration testing.
- [ ] Consider more complex cases.
- [x] Make MkDocs Merge module friendly: thanks to [mihaipopescu](https://github.com/mihaipopescu)
