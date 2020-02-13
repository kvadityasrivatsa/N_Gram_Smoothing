import sys
import kneser as kn
import witten as wb

n = int(sys.argv[1])
s_type = sys.argv[2]
path = sys.argv[3]

if(s_type=="k"):
	kn.fetchNclean(path)
	kn.prep_ds(n)
	kn.run()

elif(s_type=="w"):
	wb.fetchNclean(path)
	wb.prep_ds(n)
	wb.run()