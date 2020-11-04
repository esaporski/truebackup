clean:
	rm -rf ./build
	rm -rf ./dist
	rm -rf ./*.egg-info
generate:
	python3 setup.py sdist bdist_wheel
upload-test:
	python3 -m twine upload --repository testpypi dist/*
