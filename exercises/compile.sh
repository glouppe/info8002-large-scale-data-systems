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
echo $EXTENSIONLESS

# Remove the old output directory, and old generated pdf.
rm -r output &> /dev/null

# Create a new output folder.
mkdir output
cd output
pdflatex $EXTENSIONLESS -shell-escape
makeindex $EXTENSIONLESS -s nomencl.ist -o $EXTENSIONLESS.nls
bibtex $EXTENSIONLESS
pdflatex $EXTENSIONLESS -shell-escape
pdflatex $EXTENSIONLESS -shell-escape

# Move the generated pdf to the parent directory.
mv $ROOTDIR"/output/"$EXTENSIONLESSCLEAN".pdf" $ROOTDIR
cd ..
rm -r output
