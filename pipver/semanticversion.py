#!/usr/bin/env python
# coding: utf-8


class SemanticVersion():
    """
    object for manipulating a semver string
    """
    def __init__(self, version_str):
        self.version_str = version_str

        # Grab build data if included
        # Looks like <...>+<build_data>
        if '+' in version_str:
            self.version_str = version_str.split('+')[0]
            self.build_num = version_str.split('+')[-1]
        else:
            self.build_num = None

        # Separate the main version from the extension
        if '-' in version_str:
            # extension present: split on '-' and take second half
            # *Can only increment the last number in the extension if it is a digit
            # Can be:
            #  -rc
            #  -rc.N
            #  -alpha
            #  -alpha.N
            #  -alpha.beta
            #  -beta
            #  -beta.N
            self.version = version_str.split('-')[0]
            self.extension = version_str.split('-')[-1]
        else:
            # No extension found, no need to split it off
            self.version = version_str
            self.extension = None

        # Take the main Version string without extension and pull Major, Minor, Patch out
        self.version_split = self.version.split('.')
        self.major = int(self.version_split[0])
        self.minor = int(self.version_split[1])
        self.patch = int(self.version_split[2])

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, self.__str__())

    def __str__(self):
        ret = ''
        # todo: support extension
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
        increment Major, reset minor and patch to zero
        """
        self.major += 1
        self.minor = 0
        self.patch = 0
        self.extension = None  # Reset ext
        return self.__str__()

    def increment_minor(self):
        """
        increment Minor, keep Major, reset Patch
        """
        self.minor += 1
        self.patch = 0
        self.extension = None  # Reset ext
        return self.__str__()

    def increment_patch(self):
        """
        increment Patch, keep Major and Minor
        """
        self.patch += 1
        self.extension = None  # Reset ext
        return self.__str__()

    def increment_rc(self):
        """
        increment the release candidate iteration
        """
        pass
