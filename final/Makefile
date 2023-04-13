SHELL := /usr/bin/env bash

SCRIPTS_DIR  = ./tests
TESTS_DIR    = ./tests
N_VALUES_DIR = ./tests/n-values
P_VALUES_DIR = ./tests/p-values
DIST_DIR     = ./dist

TEST_SINGLE  = $(SCRIPTS_DIR)/single.sh
TEST_MULTI   = $(SCRIPTS_DIR)/multi.sh
RENDER_PLOT  = $(SCRIPTS_DIR)/render.py

N_VALUES     = $(wildcard $(N_VALUES_DIR)/*)
P_VALUES     = $(wildcard $(P_VALUES_DIR)/*)

RESULTS_DIR  = $(TESTS_DIR)/results

SINGLE_DIR   = $(RESULTS_DIR)/single
SINGLE_FILES = $(patsubst $(N_VALUES_DIR)/%, $(SINGLE_DIR)/%.txt, $(N_VALUES))

MULTI_DIR    = $(RESULTS_DIR)/multi
MULTI_DIRS   = $(patsubst $(P_VALUES_DIR)/%, $(MULTI_DIR)/%, $(P_VALUES))
MULTI_FILES  = $(foreach multi_dir, $(MULTI_DIRS), $(patsubst $(N_VALUES_DIR)/%, $(multi_dir)/%.txt, $(N_VALUES))) 

PLOT_FILE    = $(DIST_DIR)/plot.png


all: $(PLOT_FILE)

$(PLOT_FILE): $(RENDER_PLOT) $(DIST_DIR) $(SINGLE_DIR) $(SINGLE_FILES) $(MULTI_DIRS) $(MULTI_FILES)
	$(RENDER_PLOT) $(N_VALUES_DIR) $(SINGLE_DIR) $(MULTI_DIR) $@

$(DIST_DIR):
	mkdir -p $(DIST_DIR)

$(SINGLE_DIR):
	mkdir -p $(SINGLE_DIR)

$(MULTI_DIR)/%: $(P_VALUES_DIR)/%
	mkdir -p $(MULTI_DIR)/$(<F)

$(SINGLE_DIR)/%.txt: $(N_VALUES_DIR)/% $(TEST_SINGLE) 
	$(TEST_SINGLE) $(<F) > $@

$(MULTI_FILES): $(TEST_MULTI)
	$(TEST_MULTI) $(lastword $(subst /, , $(@D))) $(firstword $(subst ., , $(@F))) > $@
