# latexmk configuration for radicals poster
# use xelatex for full Unicode support (Chinese + accents)
$pdf_mode = 5;            # generate PDF
$pdflatex = 'xelatex %O --halt-on-error -output-directory=build %S';
$success_cmd = 'mkdir -p pdf && cp build/%R.pdf pdf/';

# Output directories to keep root clean
$out_dir = 'build';       # auxiliary files (aux, log, etc)
$pdf_dir = 'pdf';         # PDF output

# Watch these files as dependencies that trigger rebuilds
@extra_input_files = ( 'Radicals.csv', 'generate_radicals.py' );

# custom rule: regenerate .tex from .csv using the python script
add_cus_dep('csv','tex',0,'genradicals');
sub genradicals {
    system('python3 generate_radicals.py');
}

$clean_ext = 'aux bbl blg log out toc fdb_latexmk fls dvi ps';
$clean_full_ext = 'pdf';

# For user: 
# latexmk -c   : clean intermediate files (keeps PDFs)
# latexmk -C   : clean all including PDFs and build/pdf directories
# latexmk      : build normally
# run: latexmk -e '$print_mode="yale"' for Yale variant
# PDFs will be in pdf/, build artifacts in build/
