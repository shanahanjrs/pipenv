#!/usr/bin/env python
# coding: utf-8
"""
pipver
author: John Shanahan <shanahan.jrs@gmail.com>

TODO:
  - Fix giant run-on main()
  - git support
  - TESTS
  - add a license
  - update readme
"""

from pipver.lib import *
from pipver.semanticversion import SemanticVersion

import click
from git import Repo
from colorama import Fore, Style

import sys

# lambda print
f = '%s[Pipver]%s ' % (Fore.GREEN, Style.RESET_ALL)


def bye(message='%sExiting...' % f, exit_code=1):
    print(message)
    sys.exit(exit_code)


@click.command()
@click.option('--filepath',
              default=False,
              help='Name of file containing the version variable/string.')
@click.option('--version',
              default=False,
              help='SemVer string of the new version to use.')
@click.option('--major', default=False, help='Increment the version Major.')
@click.option('--minor', default=False, help='Increment the version Minor.')
@click.option('--patch',
              default=True,
              help='Increment the version Patch (This is the default).')
@click.option('--extension',
              default=True,
              help='Increment the version Extension.')
@click.option('--build', default=True, help='Increment the version Build.')
@click.option('--from-git',
              default=False,
              help='Check the latest git tag for the version string.')
@click.option('--dont-tag',
              is_flag=True,
              default=False,
              help='Skip tagging the commit with the generated version.')
@click.option('--git-push',
              is_flag=True,
              default=False,
              help='Also perform a `git push` after tagging.')
@click.option('--yes',
              is_flag=True,
              default=False,
              help='Always answer Yes when prompted with a Y/n question.')
def main(filepath, version, major, minor, patch, extension, build, from_git,
         dont_tag, git_push, yes):
    """
    main
    """
    # init git
    _git = Repo()

    # Make sure they know git repo isnt clean
    if _git.is_dirty():
        if not yes:
            # if --yes was not specified prompt for an answer
            if input('%sGit repo not clean, continue? %s[y/*]>%s ' %
                     (f, Fore.YELLOW, Style.RESET_ALL)).lower() != 'y':
                bye()

    # Find current version
    print('%sSearching for version string...' % f)
    if filepath:
        old_version_str = search_file_for_valid_semver(filepath)
        if not old_version_str:
            raise ValueError('No valid semver string found in file %s' %
                             filepath)
    else:
        old_version_str, filepath = search_each_existing_file(
            search_for_possible_files())

    old_version = SemanticVersion(old_version_str)
    print('%sFound current version: %s%s%s in %s%s%s' %
          (f, Fore.CYAN, old_version, Style.RESET_ALL, Fore.CYAN, filepath,
           Style.RESET_ALL))

    # Now bump the version...
    if version:
        # If a --version string was specified use that
        if not is_valid_semver(version):
            if not yes:
                # if --yes was not specified prompt for an answer
                print('%sWARNING: %s%s%s is not valid, use anyway?' %
                      (f, Fore.RED, version, Style.RESET_ALL))
                if input(
                        'Keep? %s[y/*]>%s ' %
                    (Fore.YELLOW, Style.RESET_ALL)).lower() != 'y' or not yes:
                    bye()
        new_version = version
    else:
        # If a --version was not specified then use one of these
        if major:
            new_version = old_version.increment_major()
        elif minor:
            new_version = old_version.increment_minor()
        elif patch:
            new_version = old_version.increment_patch()
        elif extension:
            new_version = old_version.increment_extension()
        elif build:
            new_version = old_version.increment_build()
        else:
            new_version = old_version.inc()

    # New version string Ok?
    print('%sNew version to be written: %s%s%s' %
          (f, Fore.CYAN, new_version, Style.RESET_ALL))

    if not yes:
        # Ask to use the new version string if they havent specified --yes
        if input('Keep? %s[y/*]>%s ' %
                 (Fore.YELLOW, Style.RESET_ALL)).lower() != 'y':
            bye()

    modify_file_with_new_version_string(filepath, old_version_str, new_version)

    # add/commit/tag updated file to git
    if dont_tag:
        # Skip the git tagging process
        if git_push:
            print(
                '%s Skipping `git push` since we aren\'t tagging the commit...'
            )
    else:
        _git.git.add(filepath)
        _git.git.commit('-m [Pipver] Updated version to %s' % new_version)
        _git.create_tag(new_version)

        if git_push:
            _git.git.push('-u origin %s --tags' % _git.active_branch.name)

    # Done
    bye('%sDone!' % f, 0)


if __name__ == '__main__':
    main()
