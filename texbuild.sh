#!/bin/bash
# ==============================================================================
# This script compiles the LaTeX files along with any associated bibtex file.
# In case you are fed up with the quirks of various LaTeX editors on linux and
# want to edit your LaTeX files in a simple text editor then this script may be
# useful for you. You are fee to use/modify/share it as you wish :)
#
# DISCLAIMER: IT COMES WITH NO WARRANTY WHATSOEVER.
# ==============================================================================

if [ $# -eq 0 ]; then
	echo Usage: $0 INPUT_LATEX_FILE. For example: $0 my_latex_document.tex
	echo ""
	echo If not already existing, it will create a subdirectory named build\
		to keep intermediatory files.
	echo ""
	exit -1;
fi

F=$1
FN=`basename -s .tex $1`

BD=`pwd`/build
echo Processing $FN.tex. Intermediate generated files and logs will be \
	written to $BD directory.
if [ ! -d $BD ]; then
    echo "Creating build directory ..."
	mkdir $BD
fi

echo Compiling latex file ...
# Compile the LATEX file
latex -interaction=nonstopmode -output-directory=$BD $1 > /dev/null

echo Processing bib file ...
# Generate the bibliography
bibtex $BD/$FN.aux > /dev/null

echo Re-compiling latex file to resolve bib references ...
# Recompile LATEX file to resolve the bibliography references.
latex -interaction=nonstopmode -output-directory=$BD $1 > /dev/null

# Do it again to generate the final dvi output
latex -interaction=nonstopmode -output-directory=$BD $1 > /dev/null

echo Convertin dvi to pdf ...
# Convert dvi file to pdf
dvipdf $BD/$FN.dvi

echo Launching evince to view output file: `pwd`/$FN.pdf ...

evince `pwd`/$FN.pdf

echo Build completed.
