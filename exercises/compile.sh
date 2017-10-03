#/bin/sh

# Compiles the specified TeX file and removes all the undesired files.

function usage {
    echo "A valid path to a TeX file has not been specified."
    echo "Usage: ./compile.sh [path-to-tex-file]"

    exit 1
}

# Check if the required argument is specified, and check the path.
if [ -z "$1" ] || ! [ -f "$1" ]; then
    usage
fi

# Assign the texfile variable to the specified valid path.
ROOTDIR=$(pwd $1)
TEXFILE=$ROOTDIR"/"$1
EXTENSIONLESS=$ROOTDIR"/"${1::-4}
EXTENSIONLESSCLEAN=${1::-4}

# Create a new output folder.
pdflatex $EXTENSIONLESS -halt-on-error -shell-escape
makeindex $EXTENSIONLESS -s nomencl.ist -o $EXTENSIONLESS.nls
bibtex $EXTENSIONLESS
pdflatex $EXTENSIONLESS -halt-on-error -shell-escape
pdflatex $EXTENSIONLESS -halt-on-error -shell-escape

# Remove the undesired files.
rm *.aux &> /dev/null
rm *.aux &> /dev/null
rm *.bcf &> /dev/null
rm *.bib &> /dev/null
rm *.dvi &> /dev/null
rm *.fdb_latexmk &> /dev/null
rm *.fls &> /dev/null
rm *.idx &> /dev/null
rm *.ilg &> /dev/null
rm *.ind &> /dev/null
rm *.log &> /dev/null
rm *.nls &> /dev/null
rm *.out &> /dev/null
rm *.thm &> /dev/null
rm *.toc &> /dev/null
rm *.xml &> /dev/null
