import re

def isCUI(cui):
	match = re.search(r'^C\d{7}$', cui)
	if match:
		return True
	else:
		return False
