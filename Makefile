format:
	autoflake -i **/*.py
	isort -i **/*.py
	yapf -i **/*.py

build:
	python3 setup.py sdist bdist_wheel

publish:
	twine upload dist/*

clean:
	rm -rf build dist *.egg-info