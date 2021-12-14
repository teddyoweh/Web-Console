import re

import sys
sys.path.append('../portal')
from portal import APPEND as a, CLEAR as c, DELETE as d, EXEC as e, write as w, read as r, children
sys.path.append('../altpython')
from altpython import replace_syntax

def run_code(src, context, VALUE=None):
	import string
	import itertools
	import os
	from os import path

	def sum(l):
		value = None
		i = iter(l)
		while True:
			try:
				value = next(i) if value is None else value + next(i)
			except StopIteration:
				break
		return value

	replace = lambda s: re.sub(r'#(\d+)', r'context[\1]', s).replace('#', 'VALUE')
	modified_src = replace_syntax(src, replace, strip_comments=False)
	return eval(modified_src)

def run_command(command, on_type, on_start, context):
	# TODO: kill
	on_start(None)

	if len(command) == 1:
		return run_code(command[0], context)
	else:
		first, *rest = command
		if first.startswith('#'):
			values = context[int(first[1:])]
			src, = rest
			if isinstance(values, dict):
				return {k: run_code(src, context, v) for k, v in values.items()}
			else:
				return {k: run_code(src, context, k) for k in values}
		elif first.startswith('/'):
			return porta.EXEC(first[1:], rest)
		else:
			return globals()[first](*rest)

	raise ValueError("Couldn't interpret command " + repr(command))