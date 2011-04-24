#!/bin/bash
# A small shell script to package up the app

if [ -z "$1" ]
then
  exit;
fi

if [ `gem list --local | grep "haml" | wc -l` -lt 1 ]
then
  echo "[BUILD] Installing gem for sass";
  sudo gem install haml || (echo "[BUILD] Sass gem installation failed -- exiting..." && exit);
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
echo "[BUILD] Copying complete. Running Sass...";
sass --update --style expanded "build_out/$1" "build_out/$1";
find "build_out/$1" -iname "*.scss" -delete;
echo "[BUILD] Build complete. Results in build_out/$1";