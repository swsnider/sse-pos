#!/bin/bash
# A small shell script to package up the app

if [ -z "$1" ]
then
  exit;
fi

if [ -d build_out ]
then
  if [ -d "build_out/$1" ]
  then
    rm -fr build_out/$1;
  fi
else
  rm -fr build_out;
  mkdir build_out;
fi

cp -R "$1" "build_out/$1";

if [ -e "$1/NO_COMMON" ]
then
  rm -fr "build_out/$1/NO_COMMON";
else
  cp -Rn common/ "build_out/$1";
fi
echo "Build complete. Results in build_out/$1";