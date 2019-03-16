import csv
import argparse
import subprocess
import sys
import os

def pageRange(pages):
	if len(pages) == 0:
		return ""
	elif len(pages) == 1:
		return str(list(pages)[0])
	else:
		pages = sorted(list(pages))
		page_range = str(pages[0])
		seq = False
		for i in range(1, len(pages[1:])+1):
			if pages[i] - pages[i-1] == 1:
				seq = True
				continue
			else:
				if seq == True:
					page_range = "-".join([page_range, str(pages[i-1])])
					page_range = ", ".join([page_range, str(pages[i])])
					seq = False
					continue
				page_range = ", ".join([page_range, str(pages[i])])
		return page_range	

def parse_args(args):
	parser = argparse.ArgumentParser(description='Outputs pdf metadata')
	parser.add_argument('--textFile', help='filename of the output of ghostscript')
	parser.add_argument('inputPdf', nargs='?', help='filename of the pdf you want to scan')
	return parser.parse_args(args)


def main(args=None):
	if args is None:
		args = sys.argv[1:]
	args = parse_args(args)
	if args.textFile == None:
		print("You didn't add a textfile to the arguments. \nRunning ghostscript. Please Wait.")
		command = "gs -o - -sDEVICE=inkcov " + args.inputPdf + " > pages_stat.txt"
		runCommand = subprocess.call([command], shell=True)
		if runCommand == 0:
			print("Ghostscript finished running." 
				"You can now see the ink details per page of your pdf file at pages_stat.txt")
			args.textFile = 'pages_stat.txt'
		else:
			print("Please install Ghostscript first. (https://www.ghostscript.com/doc/current/Install.htm)")
		
	listOfLines = []
	blackPages = 0
	listOfBlackPages = [] 
	totalNumOfPages = 0
	if os.path.exists(args.textFile):
		with open(args.textFile, 'r') as f:
			try:
				for i in range(4):
					next(f)
				for line in f:
					for line in f:
						line = line.strip().rstrip().replace('  ', ' ').split(' ')
						totalNumOfPages += 1
						if (line[0] == '0.00000' and 
							line[1] == '0.00000' and 
							line[2] == '0.00000'):
							blackPages += 1
							listOfBlackPages.append(totalNumOfPages)
						break

				pages = range(1,totalNumOfPages)
				coloredPages = totalNumOfPages - blackPages
				listOfColoredPages = list(set(pages) - set(listOfBlackPages))
				print("===============================")
				print(f"Book: {args.inputPdf}")
				print(f"Total Number of Pages: {totalNumOfPages}")
				print(f"Total number of pages requiring black ink only: {blackPages}")
				print(f"Pages requiring black ink only: \n{pageRange(listOfBlackPages)}")
				print(f"Total number of pages requiring colored ink (Cyan, Magenta, Yellow): {coloredPages}")
				print(f"Pages requiring colored ink (Cyan, Magenta, Yellow): \n{pageRange(listOfColoredPages)}")
				print("===============================")

			except : 
				print(type(args.textFile))
				print("There's an error with opening the file.")
	else:
		

		print("File does not exist. \n \
			Please run 'gs -o - -sDEVICE=inkcov " + args.inputPdf + " > pages_stat.txt'")

if __name__=="__main__":
	main()