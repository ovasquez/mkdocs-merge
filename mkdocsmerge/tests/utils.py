import os
from ruamel.yaml import YAML


def generate_website(directory, name, yml=None):
    root = os.path.join(directory, name)
    os.mkdir(root)

    if yml is None:
        yml = make_simple_yaml(name)

    yaml = YAML()
    with open(os.path.join(root, 'mkdocs.yml'), 'w') as f:
        yaml.dump(yml, f)

    docs_folder = yml.get('docs_dir', 'docs')

    docs_dir = os.path.join(root, docs_folder)
    os.mkdir(docs_dir)
    generate_dummy_pages(docs_dir, 'nav', yml['nav'])


def make_simple_yaml(name, docs_dir=None):
    yml = {
        'site_name': '%s Website' % name,
        'nav': [
            {'Home': "index.md"},
        ]
    }

    if docs_dir:
        yml['docs_dir'] = docs_dir
    return yml


def generate_dummy_pages(docs_dir, key, node):
    if isinstance(node, list):
        for item in node:
            generate_dummy_pages(docs_dir, key, item)
    elif isinstance(node, dict):
        for k, v in node.items():
            generate_dummy_pages(docs_dir, k, v)
    else:
        path = os.path.join(docs_dir, str.replace(node, '\\', '/'))
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
        with open(path, 'w') as mdf:
            mdf.write("""
* %s Title
Contents
""" % key)
