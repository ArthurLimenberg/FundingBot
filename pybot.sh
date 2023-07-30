#!/bin/bash

BOLD="$(tput bold)"
YELLOW="$(tput setaf 3)"
GREEN="$(tput setaf 2)"
NC="$(tput sgr0)"

if [ "$1" == "tests" ]; then
    echo "${GREEN}Running tests...${NC}"
    python -m unittest tests/*
else
    echo "${YELLOW}Unknown command : \"$1\".${NC}"
fi