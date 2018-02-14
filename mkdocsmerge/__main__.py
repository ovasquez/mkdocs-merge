"""MkDocs Merge module."""

import click
from mkdocsmerge import __version__
from mkdocsmerge import merge

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

    merge.run_merge(master_site, sites, unify_sites, print_func=click.echo)
