# SPDX-FileCopyrightText: 2026 Marcus Baw and Baw Medical Ltd
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Scaffold-level checks.

These exist so CI has something real to run before the first feature lands, and
so a broken package layout fails immediately rather than at first import in a
notebook.
"""

import importlib.metadata

import snomed_widgets


def test_package_imports_without_a_terminology_backend():
    """The package must import with no backend installed.

    Backends are optional extras. If importing the top-level package ever starts
    requiring ``sct_py`` or any other backend, the adapter boundary has leaked.
    """
    assert snomed_widgets.__version__


def test_declared_version_matches_installed_metadata():
    """Catch the usual drift between ``__version__`` and the built distribution."""
    installed = importlib.metadata.version("snomed-widgets")
    assert snomed_widgets.__version__ == installed
