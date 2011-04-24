#!/bin/bash
# A small shell script to clean up after build and test

if [ -z "$1" ]
then
  rm -fr build_out/*;
else
  rm -fr "build_out/$1";
fi