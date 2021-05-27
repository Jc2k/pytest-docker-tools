#! /bin/sh

VERSION=${1:-patch}

poetry version $VERSION
git commit -a -m "Version bump"
git tag -a `poetry version | awk '{ print $2; }'`
git push --tags
git push

