#!/usr/bin/env python
# -*- coding:utf-8 -*-

#./autobuild.py -p youproject.xcodeproj -s schemename
#./autobuild.py -w youproject.xcworkspace -s schemename

import argparse
import subprocess
import os
import time
import sys
from os import path, access, mknod, R_OK
from biplist import *

import smtplib
from email.mime.text import MIMEText
import email.mime.multipart
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email import Encoders


filePath = "/Users/long/Desktop/000/"
cachePath = filePath + "Archive/Cache/cachePlist.plist"
infoPath  = filePath + "projectName/projectName/Info.plist"

#configuration for iOS build setting
CONFIGURATION = "Release"
CODE_SIGN_IDENTITY = "iPhone Distribution: Weilong Zhao (87MAJJ2CFE)"
PROVISIONING_PROFILE = "23864fdb-9b67-40c3-918e-568907690b88"
ARCHIVE_PATH = filePath + "Archive/Library/"
EXPORT_PATH = filePath + "Archive/Export/"
PROJECT= filePath + "projectName/projectName.xcworkspace"
SCHEME = "projectName"
prefixName = "包名"
bundleName = "APP名称"
bundleID   = "你懂得"
bundleVersion = "版本号"

EXPORT_OPTIONS_PLIST = filePath + "Archive/Document/exportOptions.plist"
cachePlist = {
    'cacheList': []
    }

def readInfo():
    try:
        print infoPath
        infoPlist = readPlist(infoPath)
        global bundleName
        bundleName = infoPlist.CFBundleName
        
        global bundleID
        bundleID = infoPlist.CFBundleIdentifier
        
        global bundleVersion
        bundleVersion = infoPlist.CFBundleVersion.replace(".", "_", 3)
        
        global prefixName
        prefixName = "projectName_" + time.strftime("%Y_%m_%d_%H_%M", time.localtime()) + "_V_" +  bundleVersion
        
        if path.exists(cachePath) and path.isfile(cachePath) and access(cachePath, R_OK):
            print "File exists and is readable"
            global cachePlist
            cachePlist = readPlist(cachePath)
        else:
            print "Either file is missing or is not readable"

    except (InvalidPlistException, NotBinaryPlistException), e:
        print "Not a plist:", e


    print EXPORT_PATH + prefixName + ".ipa" + "33333"
    buildProject()


def createDownloadFile():
    try:
        downPlist = {
        'items': [
                  {
                  'assets': [
                             {
                             'url': "URLADDRESS" + prefixName + ".ipa",
                             'kind': 'software-package'
                             },
                             {
                             'url': 'http: //www.lgstatic.com/thumbnail_300x300/i/image/M00/47/7B/Cgp3O1ePfBSAWEJZAAAdby7zBnk319.jpg',
                             'kind': 'display-image'
                             },
                             {
                             'url': 'http: //www.lgstatic.com/thumbnail_300x300/i/image/M00/47/7B/Cgp3O1ePfBSAWEJZAAAdby7zBnk319.jpg',
                             'kind': 'full-size-image'
                             }
                             ],
                  'metadata': {
                  'kind': 'software',
                  'title': bundleName,
                  'bundle-identifier': bundleID,
                  'bundle-version': bundleVersion
                  }
                  }
                  ]
    }
        tempCachePlist = {
        'cacheList': [prefixName] + cachePlist["cacheList"]
    }
        
        writePlist(downPlist, filePath + "Archive/Export/" + prefixName + ".plist")
        writePlist(tempCachePlist, filePath + "Archive/Cache/cachePlist.plist")
    except (InvalidPlistException, NotBinaryPlistException), e:
        print "Something bad happened:", e

    # 写HTML页面
    firstStr = '<!DOCTYPE html><!-- saved from url=(0091)file:///D:/Users/ZHAOWEILONG565/Desktop/%E5%AE%89%E8%A3%85%E5%8C%85/projectName_download.html --><html lang="en"><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">    <meta charset="UTF-8">    <meta http-equiv="X-UA-Compatible" content="IE=Edge">    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no, minimum-scale=1.0, maximum-scale=1.0">    <meta name="format-detection" content="telephone=no">    <meta name="apple-mobile-web-app-capable" content="yes">    <meta name="apple-mobile-web-app-status-bar-style" content="black">    <meta name="keywords" content="xxxAPP,xxx">    <meta name="description" content="xxxAPP,xxx">    <meta name="WT.pn_sku" content="activitySharedPage">    <meta name="WT.page_name" content="activitySharedPage">    <title>xxxAPP</title>    </head><body>        <div style="margin: 60px 10px;font-size: 20px;">'

    lastStr = '</div></body></html>'

    tempCacheList = tempCachePlist["cacheList"]

    count = int(len(tempCacheList))

    oneStr = '<br><br><br><a href="itms-services://?action=download-manifest&url=https://dmzstg1.pa18.com/padelm/app/ios/%s.plist">点击在线安装xxxAPP测试版' % (tempCacheList[0]) + tempCacheList[0] + '</a>'

    if (count > 1):
        twoStr = '<br><br><br><a href="itms-services://?action=download-manifest&url=https://dmzstg1.pa18.com/padelm/app/ios/%s.plist">点击在线安装xxxAPP测试版' % (tempCacheList[1]) + tempCacheList[1] + '</a>'
    else:
        twoStr = ''

    if (count > 2):
        threeStr = '<br><br><br><a href="itms-services://?action=download-manifest&url=https://dmzstg1.pa18.com/padelm/app/ios/%s.plist">点击在线安装xxxAPP测试版' % (tempCacheList[2]) + tempCacheList[2] + '</a>'
    else:
        threeStr = ''

    if (count > 3):
        fourStr = '<br><br><br><a href="itms-services://?action=download-manifest&url=https://dmzstg1.pa18.com/padelm/app/ios/%s.plist">点击在线安装xxxAPP测试版' % (tempCacheList[3]) + tempCacheList[3] + '</a>'
    else:
        fourStr = ''

    if (count > 4):
        fiveStr = '<br><br><br><a href="itms-services://?action=download-manifest&url=https://dmzstg1.pa18.com/padelm/app/ios/%s.plist">点击在线安装xxxAPP测试版' % (tempCacheList[4]) + tempCacheList[4] + '</a>'
    else:
        fiveStr = ''

    fileContent = firstStr + oneStr + twoStr + threeStr + fourStr + fiveStr + lastStr

    fo = open(filePath + "Archive/Export/projectName_download.html", "wb")

    fo.write(fileContent);

    fo.close()
    postEmail()


def postEmail():

    print "success============="
#    mailto_list=["mailAddress", "mailAddress"]
#    mail_host= "smtp.163.com"
#    mail_user= "18221009215"
#    mail_pass= "long1009"
#    mail_postfix="163.com"

#    mailto_list=["mailAddress", "mailAddress"]
#    mail_host= "smtp.qq.com"
#    mail_user= "912838021"
#    mail_pass= "bjhcaroujzombcjb"
#    mail_postfix="qq.com"
#
#    me = "xxxAPP安装包" + "<" + mail_user + "@" + mail_postfix + ">"
#
#    content = prefixName
#
#    msg = MIMEMultipart()
#    body = MIMEText(content, _subtype='html', _charset='gb2312')
#
#    msg.attach(body)
#    msg['Subject'] = prefixName
#    msg['From'] = me
#    msg['To'] = ";".join(mailto_list)
#
#    partIPA = MIMEBase('application', 'octet-stream')
#    partIPA.set_payload(open(EXPORT_PATH + prefixName + ".ipa",'rb').read())
#    Encoders.encode_base64(partIPA)
#    partIPA.add_header('Content-Disposition', 'attachment; filename=%s' % (prefixName + ".ipa"))
#    msg.attach(partIPA)
#
#    partList = MIMEBase('application', 'octet-stream')
#    partList.set_payload(open(EXPORT_PATH + prefixName + ".plist",'rb').read())
#    Encoders.encode_base64(partList)
#    partList.add_header('Content-Disposition', 'attachment; filename=%s' % (prefixName + ".plist"))
#    msg.attach(partList)
#    
#    partHTML = MIMEBase('application', 'octet-stream')
#    partHTML.set_payload(open(EXPORT_PATH + "projectName_download.html",'rb').read())
#    Encoders.encode_base64(partHTML)
#    partHTML.add_header('Content-Disposition', 'attachment; filename=projectName_download.html')
#    msg.attach(partHTML)
#
#    try:
#        s = smtplib.SMTP_SSL()
#        s.connect(mail_host, 465)
#        s.login(mail_user, mail_pass)
#        s.sendmail(me, mailto_list, msg.as_string())
#        s.close()
#        print 'send mail sucess'
#
#    except Exception, e:
#        print 'send mail failed' + e



def cleanArchiveFile():
    cleanCmd = "rm -r %s" %(ARCHIVE_PATH + "Temp.xcarchive")
    process = subprocess.Popen(cleanCmd, shell = True)
    process.wait()
    print "cleaned archiveFile success"

def exportArchive():
	exportCmd = "xcodebuild -exportArchive -archivePath %s -exportPath %s -exportOptionsPlist %s" %(ARCHIVE_PATH + "Temp.xcarchive", EXPORT_PATH, EXPORT_OPTIONS_PLIST)
	process = subprocess.Popen(exportCmd, shell=True)
	(stdoutdata, stderrdata) = process.communicate()

	signReturnCode = process.returncode
	if signReturnCode != 0:
		print "export failed"
	else:
		print "export success"
        print EXPORT_PATH + prefixName + ".ipa"
        os.rename(EXPORT_PATH + SCHEME + ".ipa", EXPORT_PATH + prefixName + ".ipa")
        createDownloadFile()


def buildProject():
	
	archiveCmd = 'xcodebuild -workspace %s -scheme %s -configuration %s archive -archivePath %s -destination generic/platform=iOS build CODE_SIGN_IDENTITY="%s" PROVISIONING_PROFILE="%s"' %(PROJECT, SCHEME, CONFIGURATION, ARCHIVE_PATH + "Temp", CODE_SIGN_IDENTITY, PROVISIONING_PROFILE)
	process = subprocess.Popen(archiveCmd, shell=True)
	process.wait()

	archiveReturnCode = process.returncode
	if archiveReturnCode != 0:
		print "archive workspace failed"
		cleanArchiveFile()
	else:
		exportDirectory = exportArchive()
		cleanArchiveFile()

def updateSVN():
    updateCmd = 'svn update %s' % (filePath)
    process = subprocess.Popen(updateCmd, shell=True)
    process.wait()

    readInfo()


if __name__ == '__main__':
    updateSVN()

