from pmrvc.api import *


def check(requirements: str):
	installed = get_installed_modules()

	for k, v in get_require_modules(requirements).items():
		if k not in installed:
			raise ValueError(f"module `{k}` is not installed")

		if v != installed[k]:
			raise ValueError(f"module `{k}` is wrong version")
