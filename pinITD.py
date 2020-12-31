import os
import argparse
import pandas as pd
import sys

parser = argparse.ArgumentParser(description='\nThis Python script is a post-processing program for Pindel results to identify FLT3_ITD signals in AML',
                                 add_help=False,
                                 usage='\npython3 pinITD.py -I [input_vcf_file] -O [output_vcf_prefix] -T [bed_file]'
                                 )
required = parser.add_argument_group('required')
optional = parser.add_argument_group('optional')
required.add_argument('-I', '--input', metavar='[input.vcf]', help='The VCF file of the Pindel result', required=True)
required.add_argument('-O', '--output', metavar='[output_vcf]', help='The VCF file of the Pindel post-processing result', required=True)
optional.add_argument('-T', '--target', metavar='[bed_file]', help='The BED file of FLT3 target is required if it is not provided in the Pindel program', required=False)
optional.add_argument('-h', '--help', action='help', help='help message')
args = parser.parse_args()

input_file = args.input
samplename = input_file.split("/")[-1].split(".vcf")[0]
temp_file = samplename + ".csv"
output_file = args.output + ".pro.vcf"

if args.target:
    os.system("bedtools intersect -a {} -b {} -header > {}.target.vcf".format(args.input,args.target,samplename))
    input_file = samplename + ".target.vcf"


fo = open(temp_file,"w")
fo.write("Samplename\tChr\tPos\tLength\tRef\tAlt\ttype\tPindel_var\n")
with open(input_file,"r") as f1:
    for line in f1:
        if line.startswith("#"):continue
        arr = line.strip().split()
        if len(arr[4]) < 3:continue
        sub = arr[7].split(";")
        info = {}
        for i in range(len(sub)):
            key,value = sub[i].split("=")
            info[key] = value
        vtype = info["SVTYPE"]
        key = "\t".join([arr[0],str(int(arr[1])),str(len(arr[4])-len(arr[3])),arr[3],arr[4],vtype])
        ref,alt = map(int,arr[-1].split(":")[-1].split(","))
        var = str(float(alt)/(ref+alt))
        fo.write(samplename+"\t"+key+"\t"+var+"\n")
fo.close()

pindel_result = pd.read_csv(temp_file,sep='\t')
if pindel_result.empty:
    with open(output_file,'w') as f:
    	f.write('##fileformat=VCFv4.0\n')
    	f.write('##source=pindel_process\n')
    	f.write('##INFO=<ID=SVLEN,Number=1,Type=Integer,Description="Difference in length between REF and ALT alleles">\n')
    	f.write('##INFO=<ID=SVTYPE,Number=1,Type=String,Description="Type of structural variant">\n')
    	f.write('##INFO=<ID=VAF,Number=1,Type=Float,Description="FLT3-ITD allele fraction">\n')
    	f.write('##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">\n')
    	f.write("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\t"+ samplename + "\t\n")
    f.close()
else:
    pindel_result1 = pindel_result[(pindel_result['type'].isin(['INS','DUP:TANDEM']))]
    vaf_max = pindel_result1['Pindel_var'].groupby(pindel_result1['Length']).max().reset_index()
    pindel_result2 = pd.merge(pindel_result1,vaf_max,on=['Length','Pindel_var'])[["Chr","Length","Ref","Alt","type"]]    

    vaf_merge = pindel_result1['Pindel_var'].groupby(pindel_result1['Length']).sum().reset_index()
    pos_min = pindel_result1['Pos'].groupby(pindel_result1['Length']).min().reset_index()
    vaf_merge1 = vaf_merge[vaf_merge['Pindel_var'] >= 0.026]
    result = pd.merge(pos_min,vaf_merge1, on=['Length'])
    result2 = pd.merge(result,pindel_result2,on=['Length'])

    with open(output_file,'w') as f:
    	f.write('##fileformat=VCFv4.0\n')
    	f.write('##source=pindel_process\n')
    	f.write('##INFO=<ID=SVLEN,Number=1,Type=Integer,Description="Difference in length between REF and ALT alleles">\n')
    	f.write('##INFO=<ID=SVTYPE,Number=1,Type=String,Description="Type of structural variant">\n')
    	f.write('##INFO=<ID=VAF,Number=1,Type=Float,Description="FLT3-ITD allele fraction">\n')
    	f.write('##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">\n')
    	f.write("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\t"+ samplename + "\t\n")
    	for indexs in result2.index:
            Chr = result2.loc[indexs]['Chr']
            Pos = str(result2.loc[indexs]['Pos'])
            Ref = result2.loc[indexs]['Ref']
            Alt = result2.loc[indexs]['Alt']
            Length = str(result2.loc[indexs]['Length'])
            Vaf = str(result2.loc[indexs]['Pindel_var'])
            f.write(Chr+"\t"+ Pos+"\t"+"."+"\t"+Ref+"\t"+Alt+"\t"+"."+"\t"+"PASS\t"+"SVLEN="+Length+";SVTYPE=ITD;"+"VAF="+Vaf+"\tGT\t"+"0:1\n")

    f.close()

os.remove(temp_file)
