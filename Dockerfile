# use the ubuntu base image
FROM ubuntu:18.04

RUN mkdir testdata
WORKDIR /biosoft

# some packages
COPY jdk-8u211-linux-x64.tar.gz /usr/local/java/
COPY testdata /testdata
COPY BBMap_38.16.tar.gz /biosoft
COPY pinITD.py /biosoft
COPY FLT3.bed /biosoft

ADD https://github.com/sbt/sbt/releases/download/v1.4.5/sbt-1.4.5.tgz /usr/local/

# install packages
RUN apt-get update \
    && apt-get install -y apt-utils \
    && apt-get install -y yum vim wget gcc-5 g++-5 make cmake git \
    
    # lib
    && apt-get install -y zlib1g-dev libncurses5-dev libbz2-dev liblzma-dev libcurl4-gnutls-dev \
 
    # python3
    && apt-get install -y python3 python3-pip
   
# java
RUN cd /usr/local/java/ \
&& tar zxvf jdk-8u211-linux-x64.tar.gz \
&& rm jdk-8u211-linux-x64.tar.gz 

ENV JAVA_HOME /usr/local/java/jdk1.8.0_211
ENV CLASSPATH .:${JAVA_HOME}/jre/lib/rt.jar:${JAVA_HOME}/lib/dt.jar:${JAVA_HOME}/lib/tools.jar
ENV PATH ${JAVA_HOME}/bin:$PATH


# samtools
RUN wget https://github.com/samtools/samtools/releases/download/1.11/samtools-1.11.tar.bz2 \
&& tar jxvf samtools-1.11.tar.bz2 \
&& rm samtools-1.11.tar.bz2 \
&& cd samtools-1.11 \
&& ./configure --prefix=/biosoft/samtools-1.11/ \
&& make \
&& make install

ENV SAMTOOLS_HOME /biosoft/samtools-1.11/
ENV PATH ${SAMTOOLS_HOME}/bin:$PATH

# bedtools
RUN wget https://github.com/arq5x/bedtools2/releases/download/v2.18.1/bedtools-2.18.1.tar.gz \
&& tar -zxvf bedtools-2.18.1.tar.gz \
&& rm bedtools-2.18.1.tar.gz \
&& cd bedtools2/ \
&& sed -i '112s/const/constexpr/g' src/utils/fileType/FileRecordTypeChecker.h \
&& make clean \
&& make all 

ENV BEDTOOLS_HOME /biosoft/bedtools2
ENV PATH ${BEDTOOLS_HOME}/bin:$PATH

# bwa
RUN git clone https://github.com/lh3/bwa.git \
&& cd bwa/ \
&& make 

ENV BWA_HOME /biosoft/bwa
ENV PATH ${BWA_HOME}:$PATH

# sumaclust
RUN wget https://git.metabarcoding.org/obitools/sumaclust/uploads/f17c763f8d727621fc92555d7bb52e6f/sumaclust_v1.0.36.tar.gz \
&& tar -xzvf sumaclust_v1.0.36.tar.gz \
&& rm sumaclust_v1.0.36.tar.gz \
&& cd sumaclust_v1.0.36/ \
&& make -C sumalibs install \
&& make install 

ENV SUMACLUST_HOME /biosoft/sumaclust_v1.0.36
ENV PATH ${SUMACLUST_HOME}:$PATH

#sbt
RUN cd /usr/local/ \
&& tar -xzvf sbt-1.4.5.tgz \
&& rm sbt-1.4.5.tgz

ENV SBT_HOME /usr/local/sbt
ENV PATH ${SBT_HOME}/bin:$PATH

# fgbio
RUN git clone https://github.com/fulcrumgenomics/fgbio.git \
&& cd fgbio/ \
&& apt-get install git-lfs \
&& git lfs install \
&& sbt assembly

# bbmap
RUN tar -xzvf BBMap_38.16.tar.gz \
&& rm BBMap_38.16.tar.gz

# picard
RUN wget https://github.com/broadinstitute/picard/releases/download/2.23.0/picard.jar

# ScanITD
RUN git clone https://github.com/ylab-hi/ScanITD.git \
&& pip3 install numpy \
&& pip3 install pandas \
&& pip3 install pyfaidx \
&& pip3 install pysam \
&& pip3 install scikit-bio \
&& cd ScanITD \
&& sed -i "256s/decode('utf-8')/encode('utf-8').decode('utf-8')/g" ScanITD.py

# FLT3_ITD_ext
RUN git clone https://github.com/ht50/FLT3_ITD_ext.git \
&& cd FLT3_ITD_ext/ \
&& bwa index -p FLT3_dna_e14e15 FLT3_dna_e14e15.fa \
&& sed -i '81s/FLT3\_dna\_e14e15/\/biosoft\/FLT3\_ITD\_ext\/FLT3\_dna\_e14e15/g' FLT3_ITD_ext.pl \
&& sed -i '89s/fgbio\.jar/\/biosoft\/fgbio\/target\/scala-2\.13\/fgbio-1\.4\.0-37fbb49-SNAPSHOT\.jar/g' FLT3_ITD_ext.pl \
&& sed -i '90s/bbduk\.sh/\/biosoft\/bbmap\/bbduk\.sh/g' FLT3_ITD_ext.pl \
&& sed -i '91s/picard\.jar/\/biosoft\/picard\.jar/g' FLT3_ITD_ext.pl
