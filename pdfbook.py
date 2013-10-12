#! /usr/bin/python2

# pdfbook.c	Rearrange pages in a PDF file into signatures.
#
# Author	Tigran Aivazian <tigran at aivazian.fsnet.co.uk> (original C version)
#               Olivier Aubert <olivier.aubert at liris.cnrs.fr> (python version)
#
# Copyright:	GPLv2
#
# Based on the algorithm from psutils/psbook.c, which was
# written by Angus J. C. Duggan 1991-1995.
#
# For example, to convert a file gnt.pdf into a book with
# signature 32, we can use:
#
# $ pdfbook -s32 gnt.pdf gnt-book.pdf

# FIXME: implement max signature size
# FIXME: try to set the "duplex on short sides" option

import sys
import os
import shutil
import re
import tempfile
from optparse import OptionParser

def check_program(p):
    for d in os.getenv('PATH').split(':'):
	if os.path.exists(os.path.join(d, p)):
	    return True
    return False

def check_dependencies():
    ret=True
    if not check_program('pdflatex'):
	print "pdflatex is not installed. Please install it."
	ret=False
    if not check_program('pdfinfo'):
	print "pdfinfo is not installed. Please install the xpdf-utils package."
	ret=False
    return ret
	
def swap_pairs(array, len):
    """Swap pages for right-to-left typesetting
    """
    for i in range(0, len, 2):
	array[i], array[i+1] = array[i+1], array[i]

def get_number_of_pages(fname):
    """Return the number of pages in the PDF file.
    """
    npages=0
    regexp=re.compile("Pages:\s+(\d+)")
    f=os.popen("pdfinfo '%s'" % fname)
    for l in f:
	m=regexp.search(l)
	if m:
	    npages=m.group(1)
	    break
    return int(npages)

def shuffled_pages(npages, options):
    """Generated the list of page numbers for booklet printing.
    """
    signature=options.signature
    if signature == 0:
	maxpage = npages + (4 - npages % 4) % 4
	signature = maxpage
    else:
	maxpage = npages + (signature - npages % signature) % signature

    actualpg = [ 0 ] * maxpage
    for i in range(0, maxpage):
	actual = i - i % signature
	if i % 4 in (0, 3):
	    actual += signature - 1 - (i % signature) / 2
	else:
	    actual += (i % signature) / 2
	    
	if actual < npages:
	    actualpg[i] = actual + 1

    if options.rtol:
	swap_pairs(actualpg, maxpage)

    return actualpg

def generate_book(inputfile, outputfile, options):
    """Convert input to output, using options.
    """
    npages = get_number_of_pages(inputfile)
    if npages < 1:
	print "invalid number of pages (%d)" % npages
	check_dependencies()
	return

    if options.debug:
	print "Processing %d pages" % npages

    actualpg = shuffled_pages(npages, options)

    def printable(n):
	if n:
	    if not options.quiet:
		print "[%d]" % n,
	    return str(n)
	else:
	    if not options.quiet:
		print "[*]",
	    return "{}"

    compile_dir=tempfile.mkdtemp()

    if options.debug:
	print "Generating files in directory ", compile_dir

    (outbase, ext) = os.path.splitext(os.path.basename(outputfile))
    outtex=".".join( (outbase, 'tex') )
    outpdf=".".join( (outbase, 'pdf') )
    fullouttex=os.path.join( compile_dir, outtex )
    fulloutpdf=os.path.join( compile_dir, outpdf )

    # LaTeX generation
    fout = open(fullouttex, "w")
    fout.write("""\\documentclass[12pt,a4paper,openany]{book}
    \\usepackage{pdfpages}
    \\begin{document}
    \\includepdf[nup=1x2,landscape,pages={%s}]{%s}
    \\end{document}
    """ % (",".join( [ printable(n) for n in actualpg ] ),
	   inputfile ))
    fout.close()

    if not options.quiet:
	print "\nGenerating %s now, please wait..." % outputfile

    cmdline = "pdflatex -output-directory '%s' '%s'" % ( compile_dir, fullouttex )
    if not options.debug:
	cmdline +=  "> /dev/null 2>&1 < /dev/null"
    else:
	print "Executing ", cmdline
    ret=os.system(cmdline)
    if ret:
	print "Failed to generate %s" % outputfile
	check_dependencies()
	return

    if os.path.exists(fulloutpdf):
	shutil.move( fulloutpdf, outputfile )
    else:
	print "Cannot find %s in %s" % (outpdf, compile_dir)
	return 1

    if options.debug < 2:
	# Cleanup
	shutil.rmtree(compile_dir)
    return 0

def main():
    """Option parsing.
    """
    parser=OptionParser(usage="""Rearrange pages in a PDF file into signatures.
%prog [options] input_file.pdf [output_file.pdf]""")
    
    parser.add_option("-s", "--signature", dest="signature", action="store",
		      type="int", default=0, metavar="SIGNATURE",
		      help="Signature of the booklet. It must be positive and divisible by 4.")
    
    parser.add_option("-r", "--right-to-left", dest="rtol", action="store_true",
		      help="Do right-to-left typesetting", default=False)
    
    parser.add_option("-q", "--quiet", dest="quiet", action="store_true",
		      help="Be quiet", default=False)
    
    parser.add_option("-d", "--debug", dest="debug", action="store",
		      help="Debug level (1: display messages, 2: keep intermediary files", 
		      default=0)
    
    (options, args) = parser.parse_args()

    try:
	inputfile=args[0]
    except IndexError:
	print "input file must be specified"
	parser.print_help()
	return

    if not os.path.exists(inputfile):
	print "Cannot read input file", inputfile
	return

    (inputbase, ext) = os.path.splitext(inputfile)
    if ext != '.pdf':
	print "Input file %s should end with .pdf" % inputfile
	return

    try:
	outputfile=args[1]
    except IndexError:
	outbase = os.path.basename(inputbase)
	outputfile=outbase+"-book"+ext

    if options.signature:
	if options.signature < 0 or options.signature % 4:
	    parser.print_help()
	    return

    if options.debug:
	print "Input file :", inputfile
	print "Output file :", outputfile
	print "Signature :", options.signature

    return generate_book(inputfile, outputfile, options)

if __name__ == '__main__':
    main()
