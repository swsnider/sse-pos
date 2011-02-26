#!/bin/bash
# A small shell script to deploy the app

if [ -z "$1" ]
then
  exit;
fi

if [ ! -d "build_out/$1" ]
then
  source scripts/BUILD.sh "$1";
fi

appcfg.py update "build_out/$1" $2;
