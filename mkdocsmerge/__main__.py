"""MkDocs Merge module."""

import os.path
import shutil
import click
from ruamel.yaml import YAML
from mkdocsmerge import __version__

MKDOCS_YML = 'mkdocs.yml'


@click.group(context_settings={'help_option_names': ['-h', '--help']})
@click.version_option(__version__, '-V', '--version')
def cli():
    """
    MkDocs-Merge

    This simple tool allows you to merge the sources of multiple MkDocs sites
    into a single one, converting each of the specified sites to a subpage of
    the master site.

    Basic usage: mkdocs-merge run <MASTER_SITE> <SITES>

    MASTER_SITE: Path to the base site in which all other sites will be merged
    into. The mkdocs.yml file of this site will be preserved as is, except for
    the new pages.

    SITES: Paths to the sites to be merged. Each of this sites will be
    converted to a subpage of the master site. Their mkdocs.yml files
    will be ignored except for the pages data.
    """


@cli.command()
@click.argument('master-site', type=click.Path())
@click.argument('sites', type=click.Path(), nargs=-1)
def run(master_site, sites):
    """
    Executes the site merging. For more info 'mkdocs-merge run -h'

    Usage: mkdocs-merge run MASTER_SITE SITES
    """

    # Custom argument validation instead of an ugly generic error
    if not sites:
        click.echo('Please specify one or more sites to merge to the master '
                   'site.\nUse "mkdocs-merge run -h" for more information.')
        return

    # Read the mkdocs.yml from the master site
    master_yaml = os.path.join(master_site, MKDOCS_YML)
    if not os.path.isfile(master_yaml):
        click.echo('Could not find the master site yml file, '
                   'make sure it exists: ' + master_yaml)
        return

    # Get all site's pages and copy their files
    new_pages = merge_sites(sites, master_site)

    # Round-trip yaml loader to preserve formatting and comments
    yaml = YAML()
    with open(master_yaml) as master_file:
        master_data = yaml.load(master_file)
        master_data['pages'] += new_pages

    # Rewrite the master's mkdocs.yml
    with open(master_yaml, 'w') as master_file:
        yaml.dump(master_data, master_file)


def merge_sites(sites, master_site):
    """
    Adds the sites' "pages" section to the master_data and copies the sites
    content to the master_site.
    """
    new_pages = []
    for site in sites:
        site_yaml = os.path.join(site, MKDOCS_YML)
        if not os.path.isfile(site_yaml):
            click.echo('Could not find the site yml file, this site will be '
                       'skipped: ' + site_yaml)
            continue

        with open(site_yaml) as site_file:
            try:
                yaml = YAML(typ='safe')
                site_data = yaml.load(site_file)
            except Exception:
                click.echo('Error loading the yaml file "' + site_yaml + '". '
                           'This site will be skipped.')
                continue

        try:
            site_name = str(site_data['site_name'])
        except Exception:
            site_name = os.path.basename(site)
            click.echo('Could not find the site_name in the yml file, '
                       'defaulting to the folder name' + site_name)

        site_root = site_name.replace(' ', '_').lower()

        # Copy site's files into the master site's "docs" directory
        new_site_docs = os.path.join(master_site, 'docs' + os.sep + site_root)
        old_site_docs = os.path.join(site, 'docs')

        if not os.path.isdir(old_site_docs):
            click.echo('Could not find the site "docs" folder, this site will '
                       'be skipped: ' + old_site_docs)
            continue

        try:
            shutil.copytree(old_site_docs, new_site_docs)
        except OSError as exc:
            click.echo('Error copying files of site "' +
                       site_name + '". This site will be skipped.')
            click.echo(exc.strerror)
            continue

        # Update the pages data with the new path after files have been copied
        update_pages(site_data['pages'], site_root)
        new_pages.append({site_name: site_data['pages']})
    return new_pages


def update_pages(pages, site_root):
    """
    Recursively traverses the lists of pages (dictionaries) to update the path
    of the pages with the site_name, used as a subsection in the merged site.
    """
    if isinstance(pages, list):
        for page in pages:
            update_pages(page, site_root)
    elif isinstance(pages, dict):
        for name, path in pages.items():
            if isinstance(path, str):
                pages[name] = site_root + '/' + path
            elif isinstance(path, list):
                update_pages(pages[name], site_root)
            else:
                click.echo(
                    'Error merging the "pages" entry in the site: ' + site_root)
    else:
        click.echo('Error merging the "pages" entry in the site: ' + site_root)
