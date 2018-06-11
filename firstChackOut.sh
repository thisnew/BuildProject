#!/usr/bin/env bash


# updata svn code
svn list https://10.129.33.214:8443/svn/jrbsproweb/trunk --username $1 --password $2

read -p "输入项目名称:" project

svn co https://10.129.33.214:8443/svn/jrbsproweb/trunk/$project --$1 niuzongyuan2016 --password $2
#cd $1
#svn update
# read file path
# build code
# zip
#https://DESKTOP-TVO89QL/svn/allpro/trunk/jrbs_report
#https://jrbspro.jinrongboshi.com:8443/svn/jrbsproweb/trunk/jrbs_standard_v4.0