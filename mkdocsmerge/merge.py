import os.path
from ruamel.yaml import YAML
# Both imports are needed to avoid errors in Windows
import distutils
from distutils import dir_util

MKDOCS_YML = 'mkdocs.yml'


def run_merge(master_site, sites, unify_sites, print_func):

    # Custom argument validation instead of an ugly generic error
    if not sites:
        print_func('Please specify one or more sites to merge to the master '
                   'site.\nUse "mkdocs-merge run -h" for more information.')
        return

    # Read the mkdocs.yml from the master site
    master_yaml = os.path.join(master_site, MKDOCS_YML)
    if not os.path.isfile(master_yaml):
        print_func('Could not find the master site yml file, '
                   'make sure it exists: ' + master_yaml)
        return None

    # Round-trip yaml loader to preserve formatting and comments
    yaml = YAML()
    with open(master_yaml) as master_file:
        master_data = yaml.load(master_file)

    master_docs_dir = master_data.get('docs_dir', 'docs')
    master_docs_root = os.path.join(master_site, master_docs_dir)

    # Get all site's pages and copy their files
    new_pages = merge_sites(sites, master_docs_root, unify_sites, print_func)

    # then add them to the master pages
    master_data['pages'] += new_pages

    # Rewrite the master's mkdocs.yml
    with open(master_yaml, 'w') as master_file:
        yaml.dump(master_data, master_file)

    return master_data


def merge_sites(sites, master_docs_root, unify_sites, print_func):
    """
    Copies the sites content to the master_docs_root and returns
    the new merged "pages" to be added to the master yaml.
    """

    # NOTE: need to do this otherwise subsequent distutil.copy_tree will fail if
    # mkdocs-merge is used as a module (https://stackoverflow.com/a/28055993/920464)
    distutils.dir_util._path_created = {}

    new_pages = []
    for site in sites:
        print_func('\nAttempting to merge site: ' + site)
        site_yaml = os.path.join(site, MKDOCS_YML)
        if not os.path.isfile(site_yaml):
            print_func('Could not find the site yaml file, this site will be '
                       'skipped: "' + site_yaml + '"')
            continue

        with open(site_yaml) as site_file:
            try:
                yaml = YAML(typ='safe')
                site_data = yaml.load(site_file)
            except Exception:
                print_func('Error loading the yaml file "' + site_yaml + '". '
                           'This site will be skipped.')
                continue

        # Check 'site_data' has the 'pages' mapping
        if not site_data['pages']:
            print_func('Could not find the "pages" entry in the yaml file: "' +
                       site_yaml + '", this site will be skipped.')

        try:
            site_name = str(site_data['site_name'])
        except Exception:
            site_name = os.path.basename(site)
            print_func('Could not find the "site_name" property in the yaml file. '
                       'Defaulting the site folder name to: "' + site_name + '"')

        site_root = site_name.replace(' ', '_').lower()
        site_docs_dir = site_data.get('docs_dir', 'docs')

        # Copy site's files into the master site's "docs" directory
        old_site_docs = os.path.join(site, site_docs_dir)
        new_site_docs = os.path.join(master_docs_root, site_root)

        if not os.path.isdir(old_site_docs):
            print_func('Could not find the site "docs_dir" folder. This site will '
                       'be skipped: ' + old_site_docs)
            continue

        try:
            # Update if the directory already exists to allow site unification
            dir_util.copy_tree(old_site_docs, new_site_docs, update=1)
        except OSError as exc:
            print_func('Error copying files of site "' +
                       site_name + '". This site will be skipped.')
            print_func(exc.strerror)
            continue

        # Update the pages data with the new path after files have been copied
        update_pages(site_data['pages'], site_root, print_func=print_func)
        merge_single_site(new_pages, site_name,
                          site_data['pages'], unify_sites)

        # Inform the user
        print_func('Successfully merged site located in "' + site +
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


def update_pages(pages, site_root, print_func):
    """
    Recursively traverses the lists of pages (dictionaries) to update the path
    of the pages with the site_name, used as a subsection in the merged site.
    """
    if isinstance(pages, list):
        for page in pages:
            update_pages(page, site_root, print_func)
    elif isinstance(pages, dict):
        for name, path in pages.items():
            if isinstance(path, str):
                pages[name] = site_root + '/' + path
            elif isinstance(path, list):
                update_pages(pages[name], site_root, print_func)
            else:
                print_func(
                    'Error merging the "pages" entry in the site: ' + site_root)
    else:
        print_func('Error merging the "pages" entry in the site: ' + site_root)
