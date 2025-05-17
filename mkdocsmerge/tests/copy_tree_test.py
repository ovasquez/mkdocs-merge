#!/usr/bin/env python3
import os
import shutil
import tempfile
import unittest

from mkdocsmerge.merge import merge_sites


class TestCopyTreeWhenModuleImportMerge(unittest.TestCase):
    """
    This test is needed because there was a bug where subsequent calls to distutil.copy_tree
    would fail when mkdocs-merge was used as a module (https://stackoverflow.com/a/28055993/920464)
    Even though the code was updated to use shutil.copytree, this test remains valuable to prevent
    a similar bug from happening again.
    """

    def setUp(self):
        # Create an isolated temp directory and cd into it
        self.tmpdir = tempfile.mkdtemp()
        self.old_cwd = os.getcwd()
        os.chdir(self.tmpdir)

        # --- Set up a fake siteA with mkdocs.yml + docs/index.md ---
        os.makedirs("siteA/docs", exist_ok=True)
        with open("siteA/mkdocs.yml", "w") as f:
            f.write("site_name: siteA\n" "nav:\n" "  - Home: index.md\n")
        with open("siteA/docs/index.md", "w") as f:
            f.write("# Hello from siteA\n")

        # --- Prepare the master/docs folder ---
        os.makedirs("master/docs", exist_ok=True)

    def tearDown(self):
        # Cleanup
        os.chdir(self.old_cwd)
        shutil.rmtree(self.tmpdir)

    def test_merge_twice_with_deletion(self):
        master_docs = os.path.join("master", "docs")
        # First merge should always succeed
        merge_sites(["siteA"], master_docs, unify_sites=False, print_func=print)
        first_copy = os.path.join(master_docs, "sitea", "index.md")
        self.assertTrue(
            os.path.isfile(first_copy),
            f"After first merge, expected {first_copy} to exist",
        )

        # Remove the merged folder to trigger the old distutils cache bug
        shutil.rmtree(os.path.join(master_docs, "sitea"))

        # Second merge should *not* raise and should recreate the files
        # This failed with dir_util but succeeded with shutil
        merge_sites(["siteA"], master_docs, unify_sites=False, print_func=print)
        second_copy = os.path.join(master_docs, "sitea", "index.md")
        self.assertTrue(
            os.path.isfile(second_copy),
            f"After second merge, expected {second_copy} to exist",
        )


if __name__ == "__main__":
    unittest.main()
