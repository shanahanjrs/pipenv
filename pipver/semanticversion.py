#!/usr/bin/env python
# coding: utf-8
"""
semanticversion.py

custom object to represent a semver and easily modify them.
"""

import re


class SemanticVersion:
    """
    object for manipulating a semver string
    """
    def __init__(self, version_str):
        self.version_str = version_str
        self.build_num = ''
        self.extension = ''
        self.major = 0
        self.minor = 0
        self.patch = 0

        # Grab build data if included
        # Looks like 1.0.0+1234
        if '+' in version_str:
            self.version_str = version_str.split('+')[0]
            self.build_num = version_str.split('+')[1]

        # Separate the main version from the extension
        # Can be:
        #  -rc
        #  -rc.N
        #  -alpha
        #  -alpha.N
        #  -alpha.beta
        #  -beta
        #  -beta.N
        if '-' in version_str:
            self.version = self.version_str.split('-')[0]
            self.extension = self.version_str.split('-')[-1]

        # Take the main Version string without extension and pull Major, Minor, Patch out
        self.version_split = self.version.split('.')
        self.major = int(self.version_split[0])
        self.minor = int(self.version_split[1])
        self.patch = int(self.version_split[2])

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, self.__str__())

    def __str__(self):
        ret = ''
        ver = [
            str(self.major),
            str(self.minor),
            str(self.patch),
        ]
        ret += '.'.join(ver)

        if self.extension:
            ret += '-%s' % self.extension

        if self.build_num:
            ret += '+%s' % self.build_num

        return ret

    def increment_major(self):
        """
        increment Major, reset minor, patch, ext
        """
        self.major += 1
        self.minor = 0
        self.patch = 0
        self.extension = ''
        self.build_num = ''
        return self.__str__()

    def increment_minor(self):
        """
        increment Minor, keep Major, reset Patch and ext
        """
        self.minor += 1
        self.patch = 0
        self.extension = ''
        self.build_num = ''
        return self.__str__()

    def increment_patch(self):
        """
        increment Patch, keep Major and Minor, reset ext
        """
        self.patch += 1
        self.extension = ''
        self.build_num = ''
        return self.__str__()

    def increment_extension(self):
        """
        increment the release candidate iteration
        """
        re_pattern = '(\d+)(?!.*\d)'

        match = re.search(re_pattern, self.extension)

        if not match:
            return

        # If the semver extension had a build/rc/etc number we cast to int, increment, then back to str
        ext_num = str(int(match.group(0)) + 1)

        # Match the pattern
        self.extension = re.sub(re_pattern, ext_num, self.extension)

        self.build_num = ''    # Reset build
