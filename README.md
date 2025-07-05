# MkDocs Merge

This simple tool allows you to merge the source of multiple [MkDocs](http://www.mkdocs.org/) sites
into a single one converting each of the specified sites to a sub-site of the master site.

**Key Features:**

- Merge multiple MkDocs sites into a single master site
- Automatic deduplication: multiple merges replace existing entries (no duplicates)
- Site unification: combine sites with the same name into single navigation sections
- File system updates: content is properly replaced when re-merging sites

## Important Behavior Note (v0.11.0+)

When running merge operations multiple times with the same sites, **existing site entries are replaced, not duplicated**. This allows you to update subsites by simply re-running the merge command with updated source content.

For example:

- First merge: Adds "Project A" to master site
- Second merge with "Project A": Replaces the existing "Project A" entry completely with new content
- Other sites not being merged remain unchanged

This behavior change was introduced in v0.11.0 to fix a bug where multiple merges would create duplicate navigation entries.

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

- `MASTER_SITE`: the path to the MkDocs site where the base `mkdocs.yml` file resides. This is where all other sites
  will be merged into.
- `SITES`: the paths to each of the MkDocs sites that will be merged. Each of these paths is expected to have a
  `mkdocs.yml` file and a `docs` folder.
- `-u` (optional): Unify sites with the same "site_name" into a single sub-site. See [Unification Feature](#unification-feature) below for details.

> **Note:** If you merge the same site multiple times, the existing entry will be replaced with the new content (not duplicated). This allows you to update subsites by re-running the merge command.

## Unification Feature

The `-u` flag enables **site unification**, which combines multiple sites that have the same `site_name` into a single navigation section. This is useful when you have related documentation split across multiple directories but want them to appear as one logical section.

### Without Unification (default behavior)

```bash
$ mkdocs-merge run master-site api-core api-plugins
```

If both `api-core` and `api-plugins` have `site_name: "API Documentation"` in their `mkdocs.yml`, you'll get:

```yaml
nav:
  - Home: index.md
  - API Documentation: # From api-core
      - Core Functions: api_documentation/core.md
  - API Documentation: # From api-plugins (duplicate entry)
      - Plugin System: api_documentation/plugins.md
```

### With Unification

```bash
$ mkdocs-merge run master-site api-core api-plugins -u
```

The same sites will be unified into a single section:

```yaml
nav:
  - Home: index.md
  - API Documentation: # Combined into one section
      - Core Functions: api_documentation/core.md # From api-core
      - Plugin System: api_documentation/plugins.md # From api-plugins
```

### Use Cases

- **Microservices documentation**: Each service has its own docs but you want them grouped under "Services"
- **Multi-repository projects**: Different repos contribute to the same logical documentation section
- **Team-based documentation**: Multiple teams contribute to the same section (e.g., "API Reference")
- **Modular documentation**: Large documentation split across multiple directories for maintainability

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

The publishing process was updated to use GitHub Actions.

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
