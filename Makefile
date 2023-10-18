env:
	python -m venv env
	env/bin/pip install -r requirements.txt

.PHONY: clean-coverage-files
clean-coverage-files:
	rm -rf .coverage .coverage.* coverage.xml htmlcov

coverage: env clean-coverage-files
	env/bin/coverage run -m pytest
	env/bin/coverage report
	env/bin/coverage html
	env/bin/coverage xml

coverage-parallel: env clean-coverage-files
	env/bin/coverage run --parallel-mode -m pytest -n auto
	env/bin/coverage report
	env/bin/coverage html
	env/bin/coverage xml
