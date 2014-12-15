# last updated 2014-12-12 toby

import re
import os
import shutil

def move_and_replace(file, dest):
	if os.path.exists(dest + file):
		os.remove(dest + file)
	shutil.move(file, dest)

def is_cui(cui):
	return re.match(r'C\w\d{6}$', cui) is not None
