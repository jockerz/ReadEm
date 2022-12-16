build:
	rm -rf dist/ build/
	python3 setup.py sdist bdist_wheel

clean:
	rm -rf dist/ build/

upload:
	twine upload dist/*
