test:
	python -m unittest tests

build:
	python -m pip install --upgrade build
	python -m build

upload: build
	python -m pip install --upgrade twine
	python -m twine upload --repository perfectconfig dist/*