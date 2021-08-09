import json
import os
import sys


def get_installed_modules():
	txt = []
	for line in os.popen(f"'{sys.executable}' -m pip list --format json"):
		txt.append(line)

	if not txt:
		return {}

	data = {}
	for (name, version) in map(lambda x: x.values(), json.loads("".join(txt))):
		data[name.lower()] = version
	return data


def get_require_modules(fp: str):
	try:
		# pip >=20
		from pip._internal.network.session import PipSession  # noqa
		from pip._internal.req import parse_requirements  # noqa
	except ImportError:
		try:
			# 10.0.0 <= pip <= 19.3.1
			from pip._internal.download import PipSession  # noqa
			from pip._internal.req import parse_requirements  # noqa
		except ImportError:
			# pip <= 9.0.3
			try:
				from pip.download import PipSession
				from pip.req import parse_requirements
			except ImportError:
				print("you should to upgrade your pip, `python -m pip install --upgrade pip`")
				raise SystemExit

	data = {}
	session = PipSession()
	for r in parse_requirements(fp, session):
		if "://" in r.requirement:
			continue
		if "==" not in r.requirement:  # must equals
			raise ValueError("bad requirements")
		(k, v) = r.requirement.split("==")
		data[str(k.strip()).lower()] = v.strip()
	return data
