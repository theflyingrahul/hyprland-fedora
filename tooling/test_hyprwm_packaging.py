#!/usr/bin/python3

import runpy
import tempfile
import unittest
from contextlib import redirect_stdout
from argparse import Namespace
from io import StringIO
from unittest import mock
from pathlib import Path


MODULE = runpy.run_path(
    str(Path(__file__).with_name("hyprwm-packaging"))
)


class PackagingToolTests(unittest.TestCase):
    def test_repository_manifest_is_valid(self):
        data = MODULE["load_manifest"]()
        self.assertEqual(MODULE["validate_manifest"](data), [])

    def test_meta_requirement_drift_is_rejected(self):
        data = MODULE["load_manifest"]()
        package = data["packages"]["hyprwm-meta"]
        spec = MODULE["spec_path"]("hyprwm-meta", package).read_text()
        drifted = spec.replace(
            "hyprland = 0.55.4-3%{?dist}",
            "hyprland = 0.55.4-99%{?dist}",
        )
        self.assertTrue(
            MODULE["validate_meta_requirements"](data, drifted)
        )

    def test_plugin_evr_drift_is_rejected(self):
        data = MODULE["load_manifest"]()
        package = data["packages"]["hyprland-plugins"]
        spec = MODULE["spec_path"]("hyprland-plugins", package).read_text()
        drifted = spec.replace(
            "%global hyprland_evr 0.55.4-3%{?dist}",
            "%global hyprland_evr 0.55.4-99%{?dist}",
        )
        self.assertTrue(
            MODULE["validate_plugin_coupling"](data, drifted)
        )

    def test_revision_epoch_is_release_midnight_utc(self):
        self.assertEqual(
            MODULE["revision_epoch"]("2026.07.15-1"),
            1784073600,
        )
        self.assertEqual(
            MODULE["revision_epoch"]("2026.07.15-2"),
            1784073601,
        )

    def test_github_tag_archive_is_detected(self):
        source = {
            "url": (
                "https://github.com/hyprwm/hyprutils/"
                "archive/refs/tags/v0.13.1.tar.gz"
            )
        }
        self.assertEqual(
            MODULE["github_tag_source"](source),
            ("hyprwm", "hyprutils", "v0.13.1"),
        )

    def test_github_release_asset_is_detected(self):
        source = {
            "url": (
                "https://github.com/hyprwm/Hyprland/releases/download/"
                "v0.55.4/source-v0.55.4.tar.gz"
            )
        }
        self.assertEqual(
            MODULE["github_tag_source"](source),
            ("hyprwm", "Hyprland", "v0.55.4"),
        )

    def test_commit_archive_requires_manual_update(self):
        source = {
            "url": (
                "https://github.com/hyprwm/hyprland-plugins/archive/"
                "3aa21f2e0ca72412f1b434c3126f8f1fec3c716c.tar.gz"
            )
        }
        self.assertIsNone(MODULE["github_tag_source"](source))

    def test_unapproved_upstream_is_rejected(self):
        self.assertFalse(
            MODULE["official_upstream_allowed"](
                "hyprutils",
                "https://github.com/example/hyprutils/archive/v1.tar.gz",
            )
        )

    def test_upstream_path_traversal_is_rejected(self):
        for url in (
            "https://github.com/hyprwm/hyprutils/../../evil/repo/archive.tar.gz",
            "https://github.com/hyprwm/hyprutils/%2e%2e/%2e%2e/evil/archive.tar.gz",
        ):
            self.assertFalse(
                MODULE["official_upstream_allowed"]("hyprutils", url)
            )

    def test_unsigned_repo_config_has_no_active_key(self):
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "hyprwm.repo"
            MODULE["render_repo_config"](
                destination,
                fedora_release=44,
                baseurl="file:///srv/hyprwm",
                signed=False,
            )
            rendered = destination.read_text()
        self.assertIn("pkg_gpgcheck=0", rendered)
        self.assertNotIn("\ngpgkey=", rendered)

    def test_github_token_uses_curl_bearer_option(self):
        captured = []
        function = MODULE["github_json"]
        original_output = function.__globals__["output"]
        function.__globals__["output"] = lambda command: (
            captured.append(command) or '{"tag_name":"v1"}'
        )
        try:
            with mock.patch.dict("os.environ", {"GITHUB_TOKEN": "test-token"}):
                self.assertEqual(
                    function("https://api.github.com/example"),
                    {"tag_name": "v1"},
                )
        finally:
            function.__globals__["output"] = original_output
        self.assertIn("--oauth2-bearer", captured[0])
        self.assertIn("test-token", captured[0])

    def test_unsigned_rpm_is_rejected(self):
        function = MODULE["require_rpm_header_signature"]
        original_output = function.__globals__["output"]
        function.__globals__["output"] = lambda _command: (
            "(none)\n(none)\n(none)\n"
        )
        try:
            with self.assertRaises(MODULE["PackagingError"]):
                function(Path("unsigned.rpm"))
        finally:
            function.__globals__["output"] = original_output

    def test_affected_graph_includes_dependents_and_prerequisites(self):
        data = {
            "packages": {
                "base": {
                    "enabled": True,
                    "build_after": [],
                },
                "library": {
                    "enabled": True,
                    "build_after": ["base"],
                },
                "application": {
                    "enabled": True,
                    "build_after": ["library"],
                },
                "unrelated": {
                    "enabled": True,
                    "build_after": [],
                },
            }
        }
        self.assertEqual(
            MODULE["affected_package_names"](data, {"library"}),
            {"base", "library", "application"},
        )

    def test_partial_snapshot_is_rejected(self):
        args = Namespace(
            config_name=["fedora-44-x86_64"],
            output="unused",
            input="results",
            signing_key=None,
            public_key=None,
            baseurl="file:///unused",
            activate=False,
        )
        with self.assertRaises(MODULE["PackagingError"]):
            MODULE["snapshot_command"](args)

    def test_snapshot_activation_cannot_regress(self):
        with tempfile.TemporaryDirectory() as temporary:
            release_root = Path(temporary)
            releases = release_root / "releases"
            old = releases / "2026.07.15-1"
            new = releases / "2026.07.16-1"
            old.mkdir(parents=True)
            new.mkdir()
            (release_root / "current").symlink_to(
                Path("releases") / new.name
            )
            with self.assertRaises(MODULE["PackagingError"]):
                MODULE["activate_snapshot"](release_root, old.name)

    def test_explicit_rollback_can_regress_current(self):
        with tempfile.TemporaryDirectory() as temporary:
            release_root = Path(temporary)
            releases = release_root / "releases"
            old = releases / "2026.07.15-1"
            new = releases / "2026.07.16-1"
            old.mkdir(parents=True)
            new.mkdir()
            current = release_root / "current"
            current.symlink_to(Path("releases") / new.name)
            MODULE["activate_snapshot"](
                release_root,
                old.name,
                allow_regression=True,
            )
            self.assertEqual(current.resolve(), old)

    def test_rollback_verifies_snapshot_before_activation(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            release_root = output / "fedora" / "44"
            old = release_root / "releases" / "2026.07.15-1"
            new = release_root / "releases" / "2026.07.16-1"
            new.mkdir(parents=True)
            (release_root / "current").symlink_to(
                Path("releases") / new.name
            )
            key = old / "RPM-GPG-KEY-hyprwm-fedora"
            key.parent.mkdir(parents=True)
            key.write_text("test key")

            calls = []
            function = MODULE["rollback_command"]
            original = function.__globals__["verify_snapshot"]
            function.__globals__["verify_snapshot"] = (
                lambda data, snapshot, **options:
                calls.append((snapshot, options))
            )
            try:
                with redirect_stdout(StringIO()):
                    function(
                        Namespace(
                            output=str(output),
                            revision=old.name,
                            public_key=str(key),
                            check_only=False,
                        )
                    )
            finally:
                function.__globals__["verify_snapshot"] = original
            self.assertEqual(len(calls), 1)
            self.assertEqual(calls[0][0], old)
            self.assertTrue(calls[0][1]["require_signatures"])
            self.assertEqual(calls[0][1]["public_key"], key.resolve())
            self.assertEqual((release_root / "current").resolve(), old)

    def test_hyprland_automatic_update_is_prohibited(self):
        with self.assertRaises(MODULE["PackagingError"]):
            MODULE["prepare_update_command"](
                Namespace(
                    package="hyprland",
                    force=True,
                    tag="v0.56.0",
                    version=None,
                    apply=False,
                    date=None,
                    maintainer="Test <test@example.invalid>",
                    change=None,
                )
            )

if __name__ == "__main__":
    unittest.main()
