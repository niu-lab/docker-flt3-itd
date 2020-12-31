# docker-flt3-itd
A Docker image with several *FLT3*-ITD detection tools

## Introduction

A Docker image for *FLT3*-internal tandem duplication (*FLT3*-ITD)  identification in acute myeloid leukaemia (AML). It runs into a [Docker](https://www.docker.com/) container, ready to be downloaded and used on any operating system supported by [Docker](https://www.docker.com/).

We have evaluated the qualitative and quantitative analysis capabilities, result readability, and execution time of six representative tools using simulated and real biological data. To maximize user convenience, we selected several detection tools with effective performance and built a Docker image.

Two *FLT3*-ITD detection softwares and a post-processing script are packaged into the image: [ScanITD](https://github.com/ylab-hi/ScanITD) , [FLT3_ITD_ext](https://github.com/ht50/FLT3_ITD_ext), and PinITD for [Pindel](https://github.com/genome/pindel) results. Users are allowed to choose which to use and change their default settings.

## Install

Download and install the image following the steps below:

1. Install **Docker Community Edition (CE)** in your computer. Instructions and downloading links are here: [macOS](https://hub.docker.com/editions/community/docker-ce-desktop-mac), [Windows](https://hub.docker.com/editions/community/docker-ce-desktop-windows) and [Ubuntu](https://docs.docker.com/install/linux/docker-ce/ubuntu/)

2. Download the *Dockerfile* and packages with this command:

   ```
   git clone http:// 
   ```

3. Build the image:

   ```
   docker bulid -t flt3_itd_detection:1.0 .
   ```

   The image can be built by executing the above command in the *Dockerfile* directory. The `-t` parameter specifies the image name as *flt3_itd_detection*, and `.` represents the current directory.

4. Run the container named `mytest` with the image:

   ```
   docker run -it --name mytest -v /local directory:/container directory flt3_itd_detection:1.0 
   ```

   `-it` used for interactive processes

   `--name` used to name the container

   `-v` used to share the local directory and container directory
   
   **Note**: In case of the container stopped, you have to re-launch the same Docker container that was running before stopping. To do this use the following command:
   
   ```
   # start the container 
   docker start mytest
   
   # run the container
   docker exec -it mytest /bin/bash
   ```

## Instructions

### 1. FLT3_ITD_ext

#### Usage

```
   perl FLT3_ITD_ext.pl -b input_bam_file -o output_path [opts]
```

#### Options

```
   --bam, -b        Input bamfile (either this or fastq1+2 required)
   --typeb, -t      Reads to extract from input bam (defaults to "targeted" [FLT3-aligned]; or can be "loose" or "all")
   --fastq1, -f1    Input fastq1 (either fastq1+2 or bam required)
   --fastq2, -f2    Input fastq2 (either fastq1+2 or bam required)
   --output, -o     Output path (required)
   --ngstype, -n    NGS platform type (defaults to "HC" [hybrid capture]; or can be "amplicon", "NEB", or "Archer")
   --genome, -g     Genome build (defaults to "hg19"; or can be "hg38")
   --adapter, -a    Trim adapters (defaults to true; assumes illumina)
   --web, -w        Create html webpages for each ITD call (defaults to false)
   --umitag, -u     BAM tag holding UMIs in the input bamfile for fgbio (defaults to ""; standard is "RX")
   --strat, -s      Strategy for UMI assignment used in fgbio GroupReadsByUmi (defaults to "adjacency" )
   --probes, -p     Probes/baits file basename (defaults to ""); assumes fasta file, bwa indexfiles
   --minreads, -mr  Minimum number of supporting reads to be included in VCF (umi-based if umitag set)
   --debug, -d      Save all intermediate files (defaults to false)
   --help, -h       Print this help
```

#### Example

Run FLT3_ITD_ext on the test data:

```
   mkdir FLT3_ITD_ext_result
   cd FLT3_ITD_ext_result
   perl /biosoft/FLT3_ITD_ext/FLT3_ITD_ext.pl -b /testdata/ITD.28608018.21.29.9.rmdup.bam -o ./
```

#### Output 

*  ITD.28608018.21.29.9.rmdup_FLT3_ITD.vcf  (the VCF file of FLT3-ITD information)

```
   #CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	ITD.28608018.21.29.9.rmdup_FLT3	
   13	28608018	c.1927_1942+5dup	C	CTGTACCTTTCAGCATTTTGAC	.	.	GENE=FLT3;STRAND=-;SVLEN=21;CDS=c.1927_1942+5dup;AA=;AR=0;AF=0;DP=0;VD=0;AAR=0;AAF=0;RAR=0.3055;RAF=0.234;RDP=179.5;RVD=42;SAMPLE=ITD.28608018.21.29.9.rmdup_FLT3	AR:AF:DP:VD:AAR:AAF:RAR:RAF:RDP:RVD:CR	0:0:0:0:0:0:0.3055:0.234:179.5:42:0,0,0,0,42,0
```

*  ITD.28608018.21.29.9.rmdup_FLT3_ITD_summary.txt  (the TXT file of FLT3-ITD information)

```
   ITD.28608018.21.29.9.rmdup_FLT3	21	c.1927_1942+5dup		0,0,0,0,42,0	0	0	0	0	0	0	0.3055	0.234	42	179.5
```
****
### 2. ScanITD

#### Usage

```
   python3 ScanITD.py -i input_bam_file -r indexed_refenence_genome_fasta -o output_vcf_filename_prefix [opts]
```

#### Options

```
   -h, --help              show this help message and exit
   -i INPUT, --input INPUT
                           BWA-MEM BAM file
   -r REF, --ref REF       reference genome in FASTA format (with fai index)
   -o OUTPUT, --output OUTPUT
                           output prefix
   -m MAPQ, --mapq MAPQ    minimal MAPQ in BAM for calling ITD (default: 15)
   -c AO, --ao AO          minimal observation count for ITD (default: 4)
   -d DP, --depth DP       minimal depth to call ITD (default: 10)
   -f VAF, --vaf VAF       minimal variant allele frequency (default: 0.1)
   -l ITD_LEN, --len ITD_LEN
                           minimal ITD length to report (default: 10)
   -n MISMATCH             maximum allowed mismatch bases of pairwise local alignment  
                           (default: 3)
   -t TARGET, --target TARGET
                           Limit analysis to targets listed in the BED-format file or a samtools region string
   -k, --keep              Keep the ITD build BAM file
   -v, --version           show program's version number and exit
```

#### Example

Run ScanITD on the test data:

```
   mkdir ScanITD_result
   cd ScanITD_result
   python3 /biosoft/ScanITD/ScanITD.py -i /testdata/ITD.28608018.21.29.9.rmdup.bam -r /path/to/ucsc.hg19.fasta -f 0.02 -l 3 -t /biosoft/FLT3.bed -o ITD.28608018.21.29.9
```

**Note:** Mount the directory with the `docker run -v` , then use your local *ucsc.hg19.fasta*.

#### Ouput

ITD.28608018.21.29.9.itd.vcf   (the VCF file of FLT3-ITD information)

```
   #CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	ITD.28608018.21.29.9
   chr13	28608019	.	.	<TDUP>	.	.	NS=1;AO=23;DP=250;AB=0.092;SVLEN=21;SVTYPE=TDUP;SVMETHOD=ScanITD_ALN;CHR2=chr13;END=28608039	GT	1/1
```  
****
### 3. PinITD

#### Usage

```
   python3 pinITD.py -I [input_vcf_file] -O [output_vcf_prefix] -T [bed_file]
```

#### Options

```
   required:
     -I [input.vcf], --input [input.vcf]
                           The VCF file of the Pindel result
     -O [output_vcf], --output [output_vcf]
                           The VCF file of the Pindel post-processing result

   optional:
     -T [bed_file], --target [bed_file]
                           The BED file of FLT3 target is required if it is not provided in the Pindel program
     -h, --help            help message
```

#### Example

*  We recommend running *Pindel* firstly using the following command:

```
   ./pindel -f /path/to/chr13.fa -i /path/to/samplename.config -c chr13 -o samplename -j /path/to/FLT3.bed

   ./pindel2vcf -r /path/to/chr13.fa -R hg19 -d 20110721 -P samplename -G /path/to/gatk -e 5 -he 0.01 -v samplename.vcf
```

*  We provided *ITD.28608018.21.29.9.vcf* to test:

```
   mkdir PinITD_result
   cd PinITD_result
   python3 /biosoft/pinITD.py -I /testdata/ITD.28608018.21.29.9.vcf -O ITD.28608018.21.29.9
```

#### Ouput

ITD.28608018.21.29.9.pro.vcf   (the processed VCF file which only report the *FLT3*-ITD mutations)

```
   #CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	ITD.28608018.21.29.9	
   chr13	28608016	.	T	TACTGTACCTTTCAGCATTTTG	.	PASS	SVLEN=21;SVTYPE=ITD;VAF=0.16216216216216214	GT	0:1
```  

## Contact

If you have any questions, please contact one or more of the following folks: Beifang Niu [bniu@sccas.cn](mailto:bniu@sccas.cn); Danyang Yuan [yuandanyang@cnic.cn](mailto:yuandanyang@cnic.cn); Xiaoyu He [hexy@sccas.cn](mailto:hexy@sccas.cn).
