#!/usr/bin/env python3

print("""
# multitail behaves like "tail -f" on the most recent file
# in the given glob pattern, and regularly checks which is the most
# recent file. This is useful when some kind of build process is
# sequentialy generating several log files.
# please comment/suggest/request/contribute changes at:
# https://github.com/ThomasGeroudet/scripts
#
# Copyright (C) 2024 Thomas GEROUDET
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
""")


import argparse
import glob
import os
import time


# handle command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('directory')
arguments = parser.parse_args()


current_file_name = ""
file_handle = None
while True:
	# find the most recent file matching the glob pattern from command line
	file_list = glob.glob(arguments.directory, recursive=True)
	file_list = [x for x in file_list if not os.path.isdir(x)]
	if len(file_list) == 0:
		print("no matching file, exiting")
		exit()
	latest_file_name = max(file_list, key=os.path.getctime)
	#print(latest_file_name)

	# if newest file has changed, close the previous and open the new one
	if (latest_file_name != current_file_name):
		if file_handle != None:
			file_handle.close()
		file_handle = open(latest_file_name, "r")
		current_file_name = latest_file_name

	# print file contents, if wait is too long, go check newest file again
	i = 0
	while i < 5:
		line = file_handle.readline()
		if line is not None and line != "":
			print(current_file_name + ": " + line, end="")
		else:
			time.sleep(1)
			i += 1
