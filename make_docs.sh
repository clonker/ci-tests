#!/usr/bin/env bash

# exit upon failed command and use of undeclared variables
set -e -u

function set_this_up {
    if [ "$TRAVIS_PULL_REQUEST" != "false" ]
    then
        echo "this was a pull request, thus dont build docs."
        exit 0
    fi

    if [ "$TRAVIS_BRANCH" != "master" ]
    then
        echo "This commit was made against the $TRAVIS_BRANCH branch and not the master branch. Exit."
        exit 0
    fi

    if [ "$CONDA_PY" != "27" ]
    then
        echo "Only build documentation for python version 2.7. Exit."
        exit 0
    fi

    if [ -z ${GH_TOKEN+x} ]
    then
      echo "GH_TOKEN was not set, so this is probably a fork. Exit."
      exit 0
    fi
}

echo "start!"
printenv
set_this_up