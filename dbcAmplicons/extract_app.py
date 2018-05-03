import sys, os

class extractApp():

	def __init__(self):
		self.verbose = False

	def start(self, taxon, fixrank, fastq, threshold, output):
		#Format inputs:
		tax_target = str(taxon)
		print("taxon target is: "+tax_target)
		fixrank_file = open(fixrank, "r")
		vsequences = open(fastq, "r")
		minBs = float(threshold)
		out_prefix = output

		#generate list of fasta headers to be extracted:
		headers = []
		sampleIDs = []
		with fixrank_file as f:
			for line in f.readlines():
		 		if tax_target in line:
		 			if line.split("\t",26)[25] >= minBs:
		 				headers.append(line.split("|")[0])
		 				sampleIDs.append(line.split('|')[1].split(':')[0])
		 			else:
		 				continue

		#Extract selected reads from fasta
		if os.path.isfile(out_prefix+"."+tax_target+".fasta"):
			open(out_prefix+"."+tax_target+".fasta", "w").close()
		vOutput = open(out_prefix+"."+tax_target+".fasta", "a")

		with vsequences as file:
			vReads = file.read().replace('\n','')
		vReadList = vReads.split('@M')

		n = 0
		with vOutput as myfile:
			for header in headers:
				for read in vReadList:
					if ('M'+read[:len(headers[n])-1]) == headers[n]:
						myfile.write('>' + sampleIDs[n] + '~' + read.split()[0] + '\n' + read.split()[3].split('|')[3].split('+')[0] + '\n')
				n +=1
