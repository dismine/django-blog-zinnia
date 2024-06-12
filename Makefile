# Makefile for Zinnia
#
# Aim to simplify development and release process
# Be sure you have run the buildout, before using this Makefile

NO_COLOR	= \033[0m
COLOR	 	= \033[32;01m
SUCCESS_COLOR	= \033[35;01m

all: kwalitee test docs clean package ensure_virtual_env requirements sync-requirements

# most of the commands can only be used inside of the virtual environment
ensure_virtual_env:
	@if [ -z $$VIRTUAL_ENV ]; then \
		echo "You don't have a virtualenv enabled."; \
		echo "Please enable the virtualenv first!"; \
		exit 1; \
	fi

package: ensure_virtual_env
	@echo "$(COLOR)* Creating source package for Zinnia$(NO_COLOR)"
	@python -m build

test:
	@echo "$(COLOR)* Launching the tests suite$(NO_COLOR)"
	@./bin/test

coverage:
	@echo "$(COLOR)* Generating coverage report$(NO_COLOR)"
	@./bin/cover

sphinx:
	@echo "$(COLOR)* Generating Sphinx documentation$(NO_COLOR)"
	@./bin/docs

docs: coverage sphinx

kwalitee: ensure_virtual_env
	@echo "$(COLOR)* Running flake8$(NO_COLOR)"
	@./bin/flake8 --show-source --statistics zinnia
	@echo "$(SUCCESS_COLOR)* No kwalitee errors, Congratulations ! :)$(NO_COLOR)"

push-translations:
	@echo "$(COLOR)* Generating english translation$(NO_COLOR)"
	@cd zinnia && ../bin/demo makemessages --extension=html,xml,txt,py -l en
	@echo "$(COLOR)* Pushing source translation to Transifex$(NO_COLOR)"
	@tx push -s
	@echo "$(COLOR)* Removing source translation$(NO_COLOR)"
	@rm -rf zinnia/locale/en/

pull-translations:
	@echo "$(COLOR)* Pulling translations from Transifex$(NO_COLOR)"
	@tx pull -a -f --minimum-perc=50
	@echo "$(COLOR)* Compiling translations$(NO_COLOR)"
	@cd zinnia && ../bin/demo compilemessages

2to3:
	@echo "$(COLOR)* Checking Py3 code$(NO_COLOR)"
	@2to3 -x future -x dict -x map -x xrange -x imports -x import -x urllib -x print -x input zinnia/

clean:
	@echo "$(COLOR)* Removing useless files$(NO_COLOR)"
	@find demo zinnia docs -type f \( -name "*.pyc" -o -name "\#*" -o -name "*~" \) -exec rm -f {} \;
	@rm -f \#* *~
	@rm -rf uploads

mrproper: clean
	@rm -rf docs/build/doctrees
	@rm -rf docs/build/html
	@rm -rf docs/coverage

# compile requirements.txt. Requires GITLAB_PIP_USERNAME and GITLAB_PIP_TOKEN environment variables
requirements: ensure_virtual_env
	pip-compile -v --index-url 'https://${GITLAB_PIP_USERNAME}:${GITLAB_PIP_TOKEN}@gitlab.com/api/v4/projects/14215913/packages/pypi/simple' --generate-hashes requirements.in -o requirements.txt --allow-unsafe --no-emit-index-url --resolver=backtracking --strip-extras

# install requirements for development. Requires GITLAB_PIP_USERNAME and GITLAB_PIP_TOKEN environment variables
sync-requirements: ensure_virtual_env
	pip-sync requirements.txt --index-url 'https://${GITLAB_PIP_USERNAME}:${GITLAB_PIP_TOKEN}@gitlab.com/api/v4/projects/14215913/packages/pypi/simple'
