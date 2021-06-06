#!python
# -*- coding: utf-8 -*-
#
#  TOPPERS ATK2
#      Toyohashi Open Platform for Embedded Real-Time Systems
#      Automotive Kernel Version 2
#
#  Copyright (C) 2013-2014 by Center for Embedded Computing Systems
#              Graduate School of Information Science, Nagoya Univ., JAPAN
#  Copyright (C) 2013-2014 by FUJI SOFT INCORPORATED, JAPAN
#  Copyright (C) 2013-2014 by Panasonic Advanced Technology Development Co., Ltd., JAPAN
#  Copyright (C) 2013-2014 by Renesas Electronics Corporation, JAPAN
#  Copyright (C) 2013-2014 by Sunny Giken Inc., JAPAN
#  Copyright (C) 2013-2014 by TOSHIBA CORPORATION, JAPAN
#  Copyright (C) 2013-2014 by Witz Corporation, JAPAN
#
#  上記著作権者は，以下の(1)～(4)の条件を満たす場合に限り，本ソフトウェ
#  ア（本ソフトウェアを改変したものを含む．以下同じ）を使用・複製・改
#  変・再配布（以下，利用と呼ぶ）することを無償で許諾する．
#  (1) 本ソフトウェアをソースコードの形で利用する場合には，上記の著作
#      権表示，この利用条件および下記の無保証規定が，そのままの形でソー
#      スコード中に含まれていること．
#  (2) 本ソフトウェアを，ライブラリ形式など，他のソフトウェア開発に使
#      用できる形で再配布する場合には，再配布に伴うドキュメント（利用
#      者マニュアルなど）に，上記の著作権表示，この利用条件および下記
#      の無保証規定を掲載すること．
#  (3) 本ソフトウェアを，機器に組み込むなど，他のソフトウェア開発に使
#      用できない形で再配布する場合には，次のいずれかの条件を満たすこ
#      と．
#    (a) 再配布に伴うドキュメント（利用者マニュアルなど）に，上記の著
#        作権表示，この利用条件および下記の無保証規定を掲載すること．
#    (b) 再配布の形態を，別に定める方法によって，TOPPERSプロジェクトに
#        報告すること．
#  (4) 本ソフトウェアの利用により直接的または間接的に生じるいかなる損
#      害からも，上記著作権者およびTOPPERSプロジェクトを免責すること．
#      また，本ソフトウェアのユーザまたはエンドユーザからのいかなる理
#      由に基づく請求からも，上記著作権者およびTOPPERSプロジェクトを
#      免責すること．
#
#  本ソフトウェアは，AUTOSAR（AUTomotive Open System ARchitecture）仕
#  様に基づいている．上記の許諾は，AUTOSARの知的財産権を許諾するもので
#  はない．AUTOSARは，AUTOSAR仕様に基づいたソフトウェアを商用目的で利
#  用する者に対して，AUTOSARパートナーになることを求めている．
#
#  本ソフトウェアは，無保証で提供されているものである．上記著作権者お
#  よびTOPPERSプロジェクトは，本ソフトウェアに関して，特定の使用目的
#  に対する適合性も含めて，いかなる保証も行わない．また，本ソフトウェ
#  アの利用により直接的または間接的に生じたいかなる損害に関しても，そ
#  の責任を負わない．
#
# $Id: post_atk2.py 551 2015-12-30 12:52:19Z ertl-honda $
#

import subprocess
import os
import sys
import re  # for regular expression
import shutil

# set relative path from top proj
proj_rel_dir = ""

# call definition file
common.Source("./def.py")

# path
src_abs_path = os.path.abspath(SRCDIR)

# call common file
common.Source(src_abs_path + "/arch/ccrh/common.py")

#
# convert map file
#
inputfile = open("./DefaultBuild/atk2-sc1.map")
outputfile = open("./DefaultBuild/atk2-sc1.syms", 'w')

r = re.compile("^\s+([0-9a-f]+)\s+[0-9a-f]+\s+\w+\s+,\w+\s+\*\s+")
line = inputfile.readline() 
pre_line = line
while line:
    line = line.replace('\r\n','')   #delete newline
    m = r.search(line)
    if m:
        outputfile.write(m.group(1) + " T " + pre_line + "\n")
    pre_line = line
    line = inputfile.readline()

inputfile.close()
outputfile.close()

#
# copy pass 1 generated files
#
print "Copy pass 1 generated file"
shutil.copy("./cfg/cfg1_out.srec", ".")
shutil.copy("./cfg/cfg1_out.syms", ".")
shutil.copy("./cfg/cfg2_out.tf", ".")

#
# Execute cfg path 3
#
# make command
cfg_command = cfg + " --pass 3 " + "--kernel " + CFG_KERNEL 
cfg_command += " --api-table " + cfg_api_table
cfg_command += " " + cfg_cfg1_def_tables + cfg_includes 
cfg_command += " --rom-image ./DefaultBuild/atk2-sc1.srec --symbol-table ./DefaultBuild/atk2-sc1.syms"
cfg_command += " -T " + cfg_check_tf
cfg_command += " --ini-file " + cfg_ini_file
cfg_command += " " + cfg_input_str

print cfg_command

# Execute 
try:
   output = subprocess.check_output(cfg_command, stderr=subprocess.STDOUT,)
except subprocess.CalledProcessError, e:
    print "ERROR!! : ", e.output
    sys.exit()

output.replace('\r','')
print output

#
# dlete pass 1 generated files
#
print "Delete pass 1 generated file"
os.remove("cfg1_out.srec")
os.remove("cfg1_out.syms")
os.remove("cfg2_out.tf")
