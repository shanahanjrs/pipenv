Pipver: Python package versioning the right way
===============================================

Quickly and reliably update version of Python packages using Pipver.
Pipver will automatically find where you version is stored, increment it in place, and create a git tag for you as well, all you have to do is call it!

Easy to use:
------------

    $ pipver
    λ Searching for version string...
    λ Found current version: 0.1.4
    λ New version to be written: 0.1.5
    Keep? [yes]> yes
    λ Done!

Features:
---------

 - Automatically finds the correct file with your package version from a default list of standard locations.
 - Git tag integration for CI and releases
 - Completely customizable if you have a different workflow
 - Promptless run, just use the _--yes_ flag and it can run anywhere
 - Publish your package to Pypi right after running with the _--publish_ flag


 Installation
 ------------

    $ pip install pipenv

Contributing:
-------------

 1. Check for open issues on GitHub
 2. Fork the repo, and make your changes
 3. Write a test we can run to validate
 4. Send us a pull request and you're good to go!
