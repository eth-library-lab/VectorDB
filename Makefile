format:
	autoflake -i **/*.py
	isort -i **/*.py
	yapf -i **/*.py