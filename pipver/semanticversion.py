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
        if '+' in self.version_str:
            _ = self.version_str.split('+')
            self.version_str = _[0]
            self.build_num = _[1]

        # Separate the main version from the extension
        # Can be:
        #  -rc
        #  -rc.N
        #  -alpha
        #  -alpha.N
        #  -alpha.beta
        #  -beta
        #  -beta.N
        if '-' in self.version_str:
            _ = self.version_str.split('-')
            self.version_str = _[0]
            self.extension = _[1]

        # Take the main Version string without extension and pull Major, Minor, Patch out
        _ = self.version_str.split('.')
        self.major = int(_[0])
        self.minor = int(_[1])
        self.patch = int(_[2])

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
        return self.__str__()
