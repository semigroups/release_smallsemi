#!/usr/bin/env python
"""
This module contains a script for releasing the SmallSemi GAP package.
"""


import os
import re
import glob
import subprocess

from release import add_checks, exit_abort, exit_error, get_file_contents
from release import main as _main
from release import new_version, rc_branch, stable_branch, today, exec_string


def _check_pkg_info_date():
    """
    Checks if the date in the PackageInfo.g file is today's date.
    """
    regex = re.compile(r'Date\s*:=\s*"(\d\d/\d\d/\d\d\d\d)"')
    match = regex.search(get_file_contents("PackageInfo.g"))
    if match:
        if match.group(1) != today():
            exit_abort(
                f"Date in PackageInfo.g is {match.group(1)} but today is {today()}"
            )
    else:
        exit_error("Cannot determine the date in PackageInfo.g")
    return "ok!"


def _check_pkg_info_version():
    """
    Checks if the version in the PackageInfo.g file is the same as the
    releasing version.
    """
    regex = re.compile(r'Version\s*:=\s*"(\d+\.\d+\.\d+)"')
    match = regex.search(get_file_contents("PackageInfo.g"))
    if match:
        if match.group(1) != new_version():
            exit_abort(
                f"Version in PackageInfo.g is {match.group(1)} but version being released is {new_version()}"
            )
    else:
        exit_error("Cannot determine the date in PackageInfo.g")
    return "ok!"


def _check_change_log():
    """
    Check the date and version number in the CHANGELOG.md file.
    """
    contents = get_file_contents("CHANGELOG")
    regex = re.compile(
        r"Version\s*" + new_version() + r"\s*\((\d\d/\d\d/\d\d)\)"
    )
    match = regex.search(contents)

    if match:
        date_fmt = "%d/%m/%y"
        if match.group(1) != today(fmt=date_fmt):
            exit_abort(
                f"The date in CHANGELOG is {match.group(1)} but today is {today(fmt=date_fmt)}"
            )
    else:
        exit_abort(
            f"The entry for version {new_version()} in CHANGELOG is missing or incorrect"
        )
    return "ok!"


def _check_gh_pages():
    """
    Check if gh-pages dir exists and up to date.
    """
    msg = (
        "\033[31mTry:\ngit clone -b gh-pages --single-branch "
        + "git@github.com:semigroups/Semigroups.git "
        + "gh-pages\033[0m"
    )

    if not os.path.exists("gh-pages"):
        exit_abort("Cannot find the gh-pages directory!\n" + msg)
    elif not os.path.isdir("gh-pages"):
        exit_abort("gh-pages is not a directory! Delete it!\n" + msg)


def _check_trailing_whitespace():
    files = glob.glob("**/*.xml", recursive=True)
    files += glob.glob("**/*.txt", recursive=True)
    files += glob.glob("**/*.rst", recursive=True)
    files += glob.glob("**/*.sh", recursive=True)
    try:
        for file in files:
            exec_string(f'grep -vz " \\+\\n" {file}')
    except subprocess.CalledProcessError:
        if len(get_file_contents(file)) == 0:
            pass
        else:
            exit_abort(f"Found trailing whitespace in file {file}")
    return "ok!"


add_checks(
    ("checking date in PackageInfo.g file", _check_pkg_info_date),
    ("checking version in PackageInfo.g file", _check_pkg_info_version),
    ("checking for entry in changelog file", _check_change_log),
    ("checking gh-pages exists and is up to date", _check_gh_pages),
)


def release_steps():
    "The release steps that will be displayed."
    indent = " " * 4
    return (
        f"git push origin {rc_branch()}",
        f"""open a PR from {rc_branch()} to {stable_branch()} create {stable_branch()} if necessary):
{indent}https://github.com/Semigroups/semigroups/pull/new/{rc_branch()}
{indent}wait for the CI to complete successfully""",
        f"git checkout {stable_branch()} && git merge {rc_branch()}",
        f"""use ReleaseTools `release` script in the smallsemi directory, type:
{indent}~/git/gap/ReleaseTools/release-gap-package
{indent}(ensure that a personal access token is specified using one of the methods described here:
{indent}https://github.com/gap-system/ReleaseTools
{indent}under "GitHub access token")""",
        f"git branch -D {rc_branch()} && git push origin --delete {rc_branch()}",
        f"git checkout main && git merge {stable_branch()} && git push origin main",
    )


def main():
    "Run the release script"
    _main(release_steps, "release_smallsemi")


if __name__ == "__main__":
    main()
