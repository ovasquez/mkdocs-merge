"""MkDocs Merge module."""

import os.path
from distutils.dir_util import copy_tree
import click
from ruamel.yaml import YAML
from mkdocsmerge import __version__

MKDOCS_YML = 'mkdocs.yml'
UNIFY_HELP = ('Unify sites with the same "site_name" into a single sub-site. Contents of unified '
              'sub-sites will be stored in the same subsite folder.')


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
@click.option('-u', '--unify-sites', is_flag=True, help=UNIFY_HELP)
def run(master_site, sites, unify_sites):
    """
    Executes the site merging.\n
    MASTER_SITE: base site of the merge.\n
    SITES: sites to merge into the base site.
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
    new_pages = merge_sites(sites, master_site, unify_sites)

    # Round-trip yaml loader to preserve formatting and comments
    yaml = YAML()
    with open(master_yaml) as master_file:
        master_data = yaml.load(master_file)
        master_data['pages'] += new_pages

    # Rewrite the master's mkdocs.yml
    with open(master_yaml, 'w') as master_file:
        yaml.dump(master_data, master_file)


def merge_sites(sites, master_site, unify_sites):
    """
    Adds the sites' "pages" section to the master_data and copies the sites
    content to the master_site.
    """
    new_pages = []
    for site in sites:
        click.echo('\nAttempting to merge site: ' + site)
        site_yaml = os.path.join(site, MKDOCS_YML)
        if not os.path.isfile(site_yaml):
            click.echo('Could not find the site yaml file, this site will be '
                       'skipped: "' + site_yaml + '"')
            continue

        with open(site_yaml) as site_file:
            try:
                yaml = YAML(typ='safe')
                site_data = yaml.load(site_file)
            except Exception:
                click.echo('Error loading the yaml file "' + site_yaml + '". '
                           'This site will be skipped.')
                continue

        # Check 'site_data' has the 'pages' mapping
        if not site_data['pages']:
            click.echo('Could not find the "pages" entry in the yaml file: "' + site_yaml + '", '
                       'this site will be skipped.')

        try:
            site_name = str(site_data['site_name'])
        except Exception:
            site_name = os.path.basename(site)
            click.echo('Could not find the "site_name" property in the yaml file. '
                       'Defaulting the site folder name to: "' + site_name + '"')

        site_root = site_name.replace(' ', '_').lower()

        # Copy site's files into the master site's "docs" directory
        new_site_docs = os.path.join(master_site, 'docs' + os.sep + site_root)
        old_site_docs = os.path.join(site, 'docs')

        if not os.path.isdir(old_site_docs):
            click.echo('Could not find the site "docs" folder. This site will '
                       'be skipped: ' + old_site_docs)
            continue

        try:
            # Update if the directory already exists to allow site unification
            copy_tree(old_site_docs, new_site_docs, update=1)
        except OSError as exc:
            click.echo('Error copying files of site "' +
                       site_name + '". This site will be skipped.')
            click.echo(exc.strerror)
            continue

        # Update the pages data with the new path after files have been copied
        update_pages(site_data['pages'], site_root)
        merge_single_site(new_pages, site_name,
                          site_data['pages'], unify_sites)

        # Inform the user
        click.echo('Successfully merged site located in "' + site +
                   '" as sub-site "' + site_name + '"\n')
    return new_pages


def merge_single_site(global_pages, site_name, site_pages, unify_sites):
    """
    Merges a single site's pages to the global pages' data. Supports unification
    of sub-sites with the same site_name.
    """
    unified = False
    if unify_sites:
        # Check if the site_name already exists in the global_pages
        for page in global_pages:
            if site_name in page:
                # Combine the new site's pages to the existing entry
                page[site_name] = page[site_name] + site_pages
                unified = True
                break
    # Append to the global list if no unification was requested or it didn't exist.
    if (not unify_sites) or (not unified):
        global_pages.append({site_name: site_pages})


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
