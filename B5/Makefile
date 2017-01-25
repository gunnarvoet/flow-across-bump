# Makefile for model with remote build and data directory

RUN = B5
USER = gunnar
REMOTE_DIR = /Volumes/svalbard/mitgcm/bump/
CURRENT_DIR = @pwd

MITGCM_DIR = /Users/gunnar/Projects/model/MITgcm
OPTFILE = /Users/gunnar/Projects/model/upolu_mitgcm_optfile

.PHONY: all link build

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  all           to run all processing steps"
	@echo "  link          to generate directories and link files"
	@echo "  build         to build the model"


# Group some processing steps
all: link build
link: make_dirs link_input
build: make_dirs genmake buildmodel

###########################
# LINK INPUT FILES TO RUN #
###########################

# set up directories
make_dirs:
	@echo "generating directories on scratch drive"
	@mkdir -p $(REMOTE_DIR)$(RUN)/build
	@mkdir -p $(REMOTE_DIR)$(RUN)/run
	@mkdir -p $(REMOTE_DIR)$(RUN)/run/allmnc

# link input files and utils
DATA_FILES = $(abspath $(wildcard input/data*))
MORE_FILES = $(abspath $(wildcard input/OB*) input/Tref input/V.init $(wildcard input/del*) input/topo.bin)
link_input:
	@echo "linking input files to run directory"
	@ln -fs $(DATA_FILES) input/eedata $(REMOTE_DIR)$(RUN)/run
	@ln -fs $(MORE_FILES) input/eedata $(REMOTE_DIR)$(RUN)/run
	@echo "linking utility script"
	@ln -fs $(abspath ../utils/glueall.sh) $(REMOTE_DIR)$(RUN)/run/allmnc

# generate the makefile
genmake:
	@echo "running genmake"
	@$(MITGCM_DIR)/tools/./genmake2 -rootdir=$(MITGCM_DIR) -mpi -of=$(OPTFILE)  -mods=code -mf=$(REMOTE_DIR)/$(RUN)/build/Makefile
	@echo "moving files"
	@mv AD_CONFIG.h PACKAGES_CONFIG.h genmake.log $(REMOTE_DIR)/$(RUN)/build

# build the model
buildmodel:
	@echo "building model"
	@cd $(REMOTE_DIR)/$(RUN)/build/ && make depend && make
	@echo "link executable to run directory"
	@ln -s $(REMOTE_DIR)/$(RUN)/build/mitgcmuv $(REMOTE_DIR)/$(RUN)/run/


# MATLAB SCRIPTS
# to run a matlab script include it like this:
# matlabnographics -r "run('/full/path/script.m')"
