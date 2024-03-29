run:  ## run server
	python3 -m dashboard.server


tests: ## Clean and Make unit tests
	python3 -m pytest -v tests --cov=dashboard

test: lint ## run the tests for travis CI
	@ python3 -m pytest -v tests --cov=dashboard

lint: ## run linter
	flake8 dashboard 
	yarn lint

annotate: ## MyPy type annotation check
	mypy -s dashboard

annotate_l: ## MyPy type annotation check - count only
	mypy -s dashboard | wc -l 

clean: ## clean the repository
	find . -name "__pycache__" | xargs  rm -rf 
	find . -name "*.pyc" | xargs rm -rf 
	rm -rf .coverage cover htmlcov logs build dist *.egg-info
	make -C ./docs clean
	rm -rf ./docs/*.*.rst  # generated

js:  ## build the js
	yarn
	yarn build

docs:  ## make documentation
	make -C ./docs html
	open ./docs/_build/html/index.html

install:  ## install to site-packages
	python3 setup.py install

micro:  ## steps before dist, defaults to previous tag + one micro
	. scripts/deploy.sh MICRO

minor:  ## steps before dist, defaults to previous tag + one micro
	. scripts/deploy.sh MINOR

major:  ## steps before dist, defaults to previous tag + one micro
	. scripts/deploy.sh MAJOR

dist:  ## dist to pypi
	python3 setup.py sdist upload -r pypi

# Thanks to Francoise at marmelab.com for this
.DEFAULT_GOAL := help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

print-%:
	@echo '$*=$($*)'

.PHONY: clean test tests help annotate annotate_l docs dist
