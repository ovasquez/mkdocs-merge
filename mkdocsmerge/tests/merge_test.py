"""
Tests for the MkDocs Merge package
"""

import unittest
from mkdocsmerge.__main__ import update_pages


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
        # Create original and expected data structure
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

        # Call updatepages
        update_pages(pages, subpage)
        # Verify expected data structure
        self.assertEqual(pages, expected)
