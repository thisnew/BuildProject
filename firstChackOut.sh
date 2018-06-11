#!/usr/bin/env bash


# updata svn code
svn list https://---/svn/jrbsproweb/trunk --username $1 --password $2

read -p "输入项目名称:" project

svn co https://---/svn/jrbsproweb/trunk/$project --$1 niuzongyuan2016 --password $2
#cd $1
#svn update
# read file path
# build code
# zip
