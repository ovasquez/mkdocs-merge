import os
import shutil
import tempfile
import unittest

import mkdocsmerge.merge

from .utils import generate_website, make_simple_yaml


class TestRunMerge(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.owd = os.getcwd()
        os.chdir(self.tmpdir)

    def test_run_merge(self):

        docs_dir_map = {
            '__master__': 'master_docs',
            'Test': 'test_docs'
        }

        site_names = ['__master__', 'Foo', 'Bar', 'Test']
        for site_name in site_names:
            docs_dir = docs_dir_map.get(site_name, None)
            yml = make_simple_yaml(site_name, docs_dir)
            generate_website(self.tmpdir, site_name, yml)

        merged_pages = mkdocsmerge.merge.run_merge(
            site_names[0], site_names[1:], True, lambda x: None)

        for site_name in site_names[1:]:
            index_path = os.path.join(
                site_name, docs_dir_map.get(site_name, 'docs'), 'index.md')
            self.assertTrue(os.path.exists(index_path))

            docs_dir_path = os.path.join(
                site_names[0], docs_dir_map.get(site_names[0], 'docs'),
                '%s_website' % site_name.lower())
            self.assertTrue(os.path.exists(docs_dir_path))

        self.assertEqual(merged_pages, {
            'site_name': '__master__ Website',
            'nav': [
                {'Home': "index.md"},
                {'Foo Website': [
                    {'Home': 'foo_website/index.md'}
                ]},
                {'Bar Website': [
                    {'Home': 'bar_website/index.md'}
                ]},
                {'Test Website': [
                    {'Home': 'test_website/index.md'}
                ]}
            ],
            'docs_dir': 'master_docs'
        })

    def tearDown(self):
        # Avoid leaving the temp directory open until program exit (bug in Windows)
        os.chdir(self.owd)
        shutil.rmtree(self.tmpdir)
