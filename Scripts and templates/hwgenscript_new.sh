mkdir hwpdf
#hwgen for all files
sort hw*.roster | cut -c1-8 | sed 's/^/lookat\ /' | sed 's/cs70-\([a-z][a-z]\)/&; mv LOOK\/hw*.pdf hwpdf\/\1.pdf;/' > hwgen.sh
#check wc hw*roster before you do these two
#sort hw*roster | head -150 | cut -c1-8 | sed 's/^/lookat\ /' | sed 's/cs70-\([a-z][a-z]\)/&; mv LOOK\/hw*.pdf hwpdf\/\1.pdf;/' > hwgen1.sh
#sort hw*roster | tail -150 | cut -c1-8 | sed 's/^/lookat\ /' | sed 's/cs70-\([a-z][a-z]\)/&; mv LOOK\/hw*.pdf hwpdf\/\1.pdf;/' > hwgen2.sh
