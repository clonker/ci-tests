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

    if [ "$BUILD_LEADER" != "YES" ]
    then
        echo "Was not build leader, exit."
        exit 0
    fi

    if [ "$BUILD_AGGREGATE_STATUS" = "others_failed" ]
    then
        echo "Other builds failed, do not execute make docs."
        exit 0
    fi

    if [ -z ${GH_TOKEN+x} ]
    then
      echo "GH_TOKEN was not set, so this is probably a fork. Exit."
      exit 0
    fi
}

echo "start!"
set_this_up