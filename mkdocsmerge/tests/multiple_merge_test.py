"""
Tests for multiple merge operations to verify deduplication behavior.
"""

import os
import shutil
import tempfile
import unittest

import mkdocsmerge.merge

from .utils import generate_website


class TestMultipleMerge(unittest.TestCase):
    """
    Test class for verifying multiple merge operations don't create duplicates.
    """

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.owd = os.getcwd()
        os.chdir(self.tmpdir)
        print("Test: " + self._testMethodName)

    def tearDown(self):
        # Avoid leaving the temp directory open until program exit (bug in
        # Windows)
        os.chdir(self.owd)
        shutil.rmtree(self.tmpdir)

    def test_multiple_merge_same_sites_without_unify(self):
        """
        Test that merging the same sites multiple times correctly REPLACES
        existing entries instead of creating duplicates.
        This test verifies the fix for the multiple merge bug.
        """
        # Create master site and subsites
        master_yml = {
            "site_name": "Master Website",
            "nav": [{"Home": "index.md"}],
            "docs_dir": "docs",
        }

        subsite_yml = {
            "site_name": "Project A",
            "nav": [{"Home": "index.md"}, {"About": "about.md"}],
        }

        generate_website(self.tmpdir, "master", master_yml)
        generate_website(self.tmpdir, "project_a", subsite_yml)

        # First merge
        result1 = mkdocsmerge.merge.run_merge("master", ["project_a"], False, lambda x: None)

        # Verify first merge worked correctly
        expected_after_first = {
            "site_name": "Master Website",
            "docs_dir": "docs",
            "nav": [
                {"Home": "index.md"},
                {
                    "Project A": [
                        {"Home": "project_a/index.md"},
                        {"About": "project_a/about.md"},
                    ]
                },
            ],
        }
        self.assertEqual(result1, expected_after_first)

        # Second merge of the same site - this should demonstrate the bug
        result2 = mkdocsmerge.merge.run_merge("master", ["project_a"], False, lambda x: None)

        # Debug: Print actual result to see what's happening
        print("Actual result2:", result2)

        # CORRECT behavior after fix: should only have one entry per site
        expected_correct_behavior = {
            "site_name": "Master Website",
            "docs_dir": "docs",
            "nav": [
                {"Home": "index.md"},
                {
                    "Project A": [  # Should only appear ONCE (replaced, not duplicated)
                        {"Home": "project_a/index.md"},
                        {"About": "project_a/about.md"},
                    ]
                },
            ],
        }

        # This assertion now tests the CORRECT behavior
        self.assertEqual(result2, expected_correct_behavior)

    def test_multiple_merge_mixed_sites_without_unify(self):
        """
        Test merging with a mix of existing and new sites.
        Verifies that existing sites are replaced and new sites are added correctly.
        """
        # Create master site and multiple subsites
        master_yml = {
            "site_name": "Master Website",
            "nav": [{"Home": "index.md"}],
        }

        project_a_yml = {
            "site_name": "Project A",
            "nav": [{"Home": "index.md"}],
        }

        project_b_yml = {
            "site_name": "Project B",
            "nav": [{"Home": "index.md"}],
        }

        generate_website(self.tmpdir, "master", master_yml)
        generate_website(self.tmpdir, "project_a", project_a_yml)
        generate_website(self.tmpdir, "project_b", project_b_yml)

        # First merge: add Project A
        mkdocsmerge.merge.run_merge("master", ["project_a"], False, lambda x: None)

        # Second merge: add Project A again + new Project B
        result = mkdocsmerge.merge.run_merge("master", ["project_a", "project_b"], False, lambda x: None)

        # Debug: print the actual result
        print("Actual result:", result)

        # CORRECT behavior after fix: Project A appears only once (replaced),
        # Project B added
        expected_correct = {
            "site_name": "Master Website",
            "nav": [
                {"Home": "index.md"},
                {"Project A": [{"Home": "project_a/index.md"}]},  # Replaced, not duplicated
                {"Project B": [{"Home": "project_b/index.md"}]},  # New site (correct)
            ],
        }

        # This assertion now tests the CORRECT behavior
        self.assertEqual(result, expected_correct)

    def test_multiple_merge_with_unify_sites(self):
        """
        Test multiple merges with unify_sites=True.
        Verifies that the deduplication logic works correctly with the
        existing unification feature.
        """
        # Create master site and subsites
        master_yml = {
            "site_name": "Master Website",
            "nav": [{"Home": "index.md"}],
        }

        project_yml = {"site_name": "Projects", "nav": [{"First": "first.md"}]}

        generate_website(self.tmpdir, "master", master_yml)
        generate_website(self.tmpdir, "project1", project_yml)

        # Create another subsite with same name but different content
        project2_yml = {
            "site_name": "Projects",  # Same name as project1
            "nav": [{"Second": "second.md"}],
        }
        generate_website(self.tmpdir, "project2", project2_yml)

        # First merge with unify_sites=True
        result1 = mkdocsmerge.merge.run_merge("master", ["project1", "project2"], True, lambda x: None)

        expected_after_first = {
            "site_name": "Master Website",
            "nav": [
                {"Home": "index.md"},
                {
                    "Projects": [
                        {"First": "projects/first.md"},
                        {"Second": "projects/second.md"},
                    ]
                },
            ],
        }
        self.assertEqual(result1, expected_after_first)  # Second merge of the same sites with unify_sites=True
        result2 = mkdocsmerge.merge.run_merge("master", ["project1", "project2"], True, lambda x: None)

        # CORRECT behavior after fix: should replace the existing entry, not
        # duplicate
        expected_correct = {
            "site_name": "Master Website",
            "nav": [
                {"Home": "index.md"},
                {
                    "Projects": [  # Should only appear ONCE (replaced)
                        {"First": "projects/first.md"},
                        {"Second": "projects/second.md"},
                    ]
                },
            ],
        }

        # This assertion now tests the CORRECT behavior
        self.assertEqual(result2, expected_correct)

    def test_file_system_consistency_multiple_merges(self):
        """
        Test that file system operations work correctly across multiple merges.
        Verify that files are properly updated/replaced.
        """
        # Create master site
        master_yml = {
            "site_name": "Master Website",
            "nav": [{"Home": "index.md"}],
        }
        generate_website(self.tmpdir, "master", master_yml)

        # Create subsite with initial content
        project_yml = {"site_name": "Project A", "nav": [{"Home": "index.md"}]}
        generate_website(self.tmpdir, "project_a", project_yml)

        # Write initial content to project file
        initial_content = "# Initial Content\nThis is the initial version."
        with open(os.path.join(self.tmpdir, "project_a", "docs", "index.md"), "w") as f:
            f.write(initial_content)

        # First merge
        mkdocsmerge.merge.run_merge("master", ["project_a"], False, lambda x: None)

        # Verify file was copied
        copied_file = os.path.join(self.tmpdir, "master", "docs", "project_a", "index.md")
        self.assertTrue(os.path.exists(copied_file))

        with open(copied_file, "r") as f:
            content = f.read()
        self.assertEqual(content, initial_content)

        # Update the source file content
        updated_content = "# Updated Content\nThis is the updated version."
        with open(os.path.join(self.tmpdir, "project_a", "docs", "index.md"), "w") as f:
            f.write(updated_content)

        # Second merge - should update the file
        mkdocsmerge.merge.run_merge("master", ["project_a"], False, lambda x: None)

        # Verify file content was updated
        with open(copied_file, "r") as f:
            content = f.read()
        self.assertEqual(content, updated_content)

    def test_multiple_merge_should_replace_not_duplicate(self):
        """
        Test that merging the same sites multiple times should REPLACE
        existing entries, not create duplicates.

        This test expects the CORRECT behavior and will FAIL until we fix the bug.
        """
        # Create master site and subsites
        master_yml = {
            "site_name": "Master Website",
            "nav": [{"Home": "index.md"}],
            "docs_dir": "docs",
        }

        subsite_yml = {
            "site_name": "Project A",
            "nav": [{"Home": "index.md"}, {"About": "about.md"}],
        }

        generate_website(self.tmpdir, "master", master_yml)
        generate_website(self.tmpdir, "project_a", subsite_yml)

        # First merge
        mkdocsmerge.merge.run_merge("master", ["project_a"], False, lambda x: None)

        # Second merge of the same site - should REPLACE, not duplicate
        result2 = mkdocsmerge.merge.run_merge("master", ["project_a"], False, lambda x: None)

        # CORRECT behavior: should only have one entry per site
        expected_correct_behavior = {
            "site_name": "Master Website",
            "docs_dir": "docs",
            "nav": [
                {"Home": "index.md"},
                {
                    "Project A": [  # Should only appear ONCE
                        {"Home": "project_a/index.md"},
                        {"About": "project_a/about.md"},
                    ]
                },
            ],
        }

        # This assertion will FAIL until we implement the fix
        self.assertEqual(result2, expected_correct_behavior)


if __name__ == "__main__":
    unittest.main()
