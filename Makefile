
#package specific stuff
PACKNAME=visla
TESTDIR=tests

#useful general variables
VENV=test_venv
ACTIVATE=$(VENV)/bin/activate
VENVPIP=$(VENV)/bin/pip
SANDBOX=sbox/sandbox.py

#create/update virtual environment for testing
update-venv:
	@#operations in order:
	@#make virtual environment
	@#activate virtual environment
	@#install package to be tested in editable form (automatically gets dependencies)
	@#deactivate virtual environment
	@#all above directed to shell (necessary)
	@(\
	virtualenv $(VENV); \
	source $(ACTIVATE); \
	$(VENVPIP) install -e .; \
	deactivate; \
	)

#test using virtual environment
test:
	@#operations in order:
	@#activate virtual environment
	@#run all scripts in $(TESTDIR) directory 
	@#deactivate virtual environment
	@#all directed to shell (necessary)
	@(\
	source $(ACTIVATE); \
	for f in $(TESTDIR)/*.py; do python "$$f"; done; \
	deactivate; \
	)

#development sandbox for on the fly testing
sandbox:
	@(\
	source $(ACTIVATE); \
	python $(SANDBOX); \
	deactivate; \
	)

#install package locally (user/non-venv environment) in editable form
local-install:
	@pip uninstall $(PACKNAME)
	@pip install -e .

#uninstall editable package from user/non-venv environment
local-uninstall:
	@pip uninstall $(PACKNAME)

#print TODO notes to terminal
todo:
	grep -r -i "todo" $(PACKNAME) $(TESTDIR)

#remove virtual environment
clean:
	@\rm -rf test_venv

#STEPS TO CREATE PYTHON PACKAGE
#(for full guide see DZone's "Build your first pip package")
# 0.  create setup.py file (already included, just fill appropriately)
# 0.1 address bin/<PACKAGE_NAME> executable (just rename)
# 1. python setup.py bdist_wheel
# 2. ensure ~/.pyirc file exists
# 3. $ python -m twine upload dist/*
# if updating, before step 1: bump version number
#                             clear dist/* of old versions

