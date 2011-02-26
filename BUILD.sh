#!/bin/bash
# A small shell script to package up the app

if [ -z "$1" ]
then
  exit;
fi

if [ -d build_out ]
then
  rm -fr build_out/*;
else
  rm -fr build_out;
  mkdir build_out;
fi

mkdir "build_out/$1";
cp -R "$1" "build_out/$1";
cp -Rn common/ "build_out/$1";
echo "Build complete. Results in build_out/$1";