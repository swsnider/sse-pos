#!/bin/bash
# A small shell script to package up the app

if [ -z "$1" ]
then
  exit;
fi

if [ 0 -ne `gem list --local | grep "haml" | wc -l`]
then
  echo "Installing gem for sass";
  sudo gem install haml || (echo "Install failed -- exiting..." && exit);
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
echo "Copying complete. Running Sass...";
sass --update "build_out/$1" "build_out/$1";
find "build_out/$1" -iname "*.scss" -delete;
echo "Build complete. Results in build_out/$1";