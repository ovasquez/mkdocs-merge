# MkDocs Merge

This simple tool allows you to merge the source of multiple [MkDocs](http://www.mkdocs.org/) sites
into a single one converting each of the specified sites to a sub-site of the master site.

Supports unification of sites with the same `site_name` into a single sub-site.

---
[![PyPI version](https://img.shields.io/pypi/v/mkdocs-merge.svg)](https://pypi.python.org/pypi/mkdocs-merge)
[![Build Status](https://travis-ci.org/ovasquez/mkdocs-merge.svg?branch=master)](https://travis-ci.org/ovasquez/mkdocs-merge)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/10abc652aca046079f4ab069af689163)](https://www.codacy.com/app/oscarv19/mkdocs-merge?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=ovasquez/mkdocs-merge&amp;utm_campaign=Badge_Grade)
[![Codacy Badge](https://api.codacy.com/project/badge/Coverage/10abc652aca046079f4ab069af689163)](https://www.codacy.com/app/oscarv19/mkdocs-merge?utm_source=github.com&utm_medium=referral&utm_content=ovasquez/mkdocs-merge&utm_campaign=Badge_Coverage)

MkDocs-Merge supports Python versions 2.7, 3.3, 3.4, 3.5, 3.6 and pypy.

Support for Python 2.6 (MkDocs does support 2.6) was removed due to the use of `ruamel.yaml`. More details
[here](https://yaml.readthedocs.io/en/latest/pyyaml.html#py2-py3-reintegration).

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
pages:
  - Home: index.md
  - About: about.md
```

**Merged `root/mypath/mysite/mkdocs.yml`**

```yaml
...
pages:
  - Home: index.md
  - About: about.md
  - new-site: new-site/home/another.md # Page merged from /another/path/new-site
  - website: website/index.md # Page merged from /newpath/website
```

## Development

### Dev Install

Clone the repository and specify the `dev` dependencies on the install command.

Check this [StackOverflow answer](https://stackoverflow.com/a/28842733/2313246) for more details about the `dev`
dependencies

```bash
$ pip install -e .[dev]
```

### Test

The tests can be run using `tox` from the root directory. `tox` is part of the development dependencies:
```bash
$ tox
```

## Project Status

Very basic implementation. The code works but doesn't allow to specify options for the merging.

### Pending work

- [ ] Refactoring of large functions.
- [x] Travis CI build.
- [x] Publish pip package.
- [ ] Better error handling.
- [x] Merge configuration via CLI options.
- [x] Unit testing (work in progress).
- [ ] Consider more complex cases.
- [x] Make MkDocs Merge module friendly: thanks to [mihaipopescu](https://github.com/mihaipopescu)
