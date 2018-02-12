"""
Tests for the MkDocs Merge package
"""

import unittest
import mkdocsmerge.merge


class TestSiteMerges(unittest.TestCase):
    """
    Test class for MkDocs Merge. Will be separated when necessary.
    """

    def setUp(self):
        print('Test: ' + self._testMethodName)

    def test_update_pages(self):
        """
        Verifies the function that updates the path to the pages adding the another
        new subroute at the begining of each page's path
        """
        # Create original and expected data structures
        subpage = 'new_root'
        subpage_path = subpage + '/'
        pages = [{'Home': 'index.md'},
                 {'About': 'menu/about.md'},
                 {'Projects': [
                     {'First': 'projects/first.md'},
                     {'Nested': [
                         {'Third': 'projects/nest/third.md'}
                     ]},
                     {'Second': 'projects/second.md'}
                 ]}]

        expected = [{'Home': subpage_path + 'index.md'},
                    {'About': subpage_path + 'menu/about.md'},
                    {'Projects': [
                        {'First': subpage_path + 'projects/first.md'},
                        {'Nested': [
                            {'Third': subpage_path + 'projects/nest/third.md'}
                        ]},
                        {'Second': subpage_path + 'projects/second.md'}
                    ]}]

        mkdocsmerge.merge.update_pages(pages, subpage, lambda x: None)
        self.assertEqual(pages, expected)

    def test_singe_site_merge(self):
        """
        Verifies merging of a single site's pages to the global pages' data without unification.
        """
        site_name = 'Projects'
        # Create original and expected data structures
        global_pages = [{'Home': 'index.md'},
                        {'About': 'menu/about.md'},
                        {site_name: [
                            {'First': 'projects/first.md'},
                            {'Second': 'projects/second.md'}
                        ]}]

        site_pages = [{'Nested': [
            {'Third': 'projects/nest/third.md'},
            {'Fourth': 'projects/nest/fourth.md'}
        ]}]

        expected = [{'Home': 'index.md'},
                    {'About': 'menu/about.md'},
                    {site_name: [
                        {'First': 'projects/first.md'},
                        {'Second': 'projects/second.md'},
                    ]},
                    {site_name: [
                        {'Nested': [
                            {'Third': 'projects/nest/third.md'},
                            {'Fourth': 'projects/nest/fourth.md'}
                        ]},
                    ]}]

        mkdocsmerge.merge.merge_single_site(
            global_pages, site_name, site_pages, False)
        self.assertEqual(global_pages, expected)

    def test_singe_site_merge_unified(self):
        """
        Verifies merging of a single site's pages to the global pages' data with unification
        of the sub-sites with the same site_name
        """
        site_name = 'Projects'
        # Create original and expected data structures
        global_pages = [{'Home': 'index.md'},
                        {'About': 'menu/about.md'},
                        {site_name: [
                            {'First': 'projects/first.md'},
                            {'Second': 'projects/second.md'}
                        ]}]

        site_pages = [{'Nested': [
            {'Third': 'projects/nest/third.md'},
            {'Fourth': 'projects/nest/fourth.md'}
        ]}]

        expected = [{'Home': 'index.md'},
                    {'About': 'menu/about.md'},
                    {site_name: [
                        {'First': 'projects/first.md'},
                        {'Second': 'projects/second.md'},
                        {'Nested': [
                            {'Third': 'projects/nest/third.md'},
                            {'Fourth': 'projects/nest/fourth.md'}
                        ]},
                    ]}]

        mkdocsmerge.merge.merge_single_site(
            global_pages, site_name, site_pages, True)
        self.assertEqual(global_pages, expected)
