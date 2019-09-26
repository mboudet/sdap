####################################################################################
#        Statistical filtration with LIMMA: script                                 #
####################################################################################
#                                                                                  #
# ******************************************************************************** #
# *                                                                              * #
# * This code is distributed under GNU Public License version 2.                 * #
# * Author: Frederic Chalmel                                                     * #
# * Programming language: R (>3.5.1)                                             * #
# * Required R packages: Biobase,                                                * #
# *                      limma                                                   * #
# * Creation date: 31th of October, 2018                                         * #
# * Last update: 31/10/2018                                                      * #
# * Version: 1.0.0                                                               * #
# *                                                                              * #
# ******************************************************************************** #
#                                                                                  #
# ******************************************************************************** #
# *                                                                              * #
# *                                                                              * #
# ******************************************************************************** #
#                                                                                  #
####################################################################################

#--------------------------------------------#
if (TRUE) {
  args        <- commandArgs(TRUE)
  in.dir1     <- args[1]
  in.dir2     <- args[2]
  in.dir3     <- args[3]
  out.dir     <- args[4]
  p.cutoff    <- args[5]
  adjust.meth <- args[6]
}

p.cutoff    <- 0.05
adjust.meth <- c("BH", "holm", "hochberg", "hommel", "bonferroni", "BY", "fdr", "none")[1]
#--------------------------------------------#

#--------------------------------------------#
#.libPaths(rlibs.dir)
source("http://bioconductor.org/biocLite.R")
#--------------------------------------------#

#--------------------------------------------#
#General Bioconductor packages
library(Biobase)
#Statistical filtration
library(limma)
#--------------------------------------------#

#--------------------------------------------#
#--------------------------------------------#
#--------------------------------------------#
# in.dir1 : directory containing the matrix data file
#--------------------------------------------#
matrix.file <- sprintf("%s/matrix.data",in.dir1)
if (file.exists(matrix.file) == FALSE) {
  stop("The matrix data file does not exist!")
  quit(save="no")
}
matrix.data <- as.matrix(read.table(matrix.file,header=TRUE,sep="\t",quote="",check.names=FALSE,row.names=1))

matrix.info.file <- sprintf("%s/matrix.info",in.dir1)
if (file.exists(matrix.info.file) == FALSE) {
  stop("The matrix info data file does not exist!")
  quit(save="no")
}
matrix.info      <- as.matrix(read.table(matrix.info.file,header=TRUE,sep="\t",quote="",check.names=FALSE,row.names=1))
#--------------------------------------------#

#--------------------------------------------#
# in.dir2 : directory containing the design.matrix and contrasts.matrix files
#--------------------------------------------#
design.matrix.file <- sprintf("%s/design.matrix",in.dir2)
if (file.exists(design.matrix.file) == FALSE) {
  stop("The design.matrix file does not exist!")
  quit(save="no")
}
design.matrix <- as.matrix(read.table(design.matrix.file,header=TRUE,sep="\t",quote="",check.names=FALSE,row.names=1))

contrasts.matrix.file <- sprintf("%s/contrasts.matrix",in.dir2)
if (file.exists(contrasts.matrix.file) == FALSE) {
  stop("The contrasts.matrix file does not exist!")
  quit(save="no")
}
contrasts.matrix <- as.matrix(read.table(contrasts.matrix.file,header=TRUE,sep="\t",quote="",check.names=FALSE,row.names=1))
#--------------------------------------------#

#--------------------------------------------#
# in.dir3 : directory containing the entities.list file
#--------------------------------------------#
entities.list.file <- sprintf("%s/entities.list",in.dir3)
if (file.exists(entities.list.file) == FALSE) {
  entities.list <- rownames(matrix.data)
} else {
  entities.list <- as.character(as.vector(as.matrix(read.table(entities.list.file,header=FALSE,sep="\t",quote="",check.names=FALSE))[,1]))
}
#--------------------------------------------#
#--------------------------------------------#
#--------------------------------------------#

#--------------------------------------------#
data  <- matrix.data[entities.list,rownames(design.matrix),drop=FALSE]
# Fitting the linear model using the design matrix
fit   <- lmFit(data,design=design.matrix)
# Fitting the linear model for the contrasts
fit2  <- contrasts.fit(fit,contrasts=contrasts.matrix)
# Empirical Bayes statistics
eb    <- eBayes(fit2)
# F-values
F     <- eb$F.p.value
FBH   <- p.adjust(F,method=adjust.meth)
new.list <- rownames(data)[which(FBH <= p.cutoff)]

write.table(matrix(new.list,ncol=1),file=sprintf("%s/entities.list",out.dir),quote=FALSE,col.names=FALSE,row.names=FALSE,sep="\t")
#--------------------------------------------#

#--------------------------------------------#
tt.res <- topTable(eb,number=nrow(data),adjust.method=adjust.meth)

fc.values <- apply(tt.res[,1:4],1, function(x) {if (max(x) >= abs(min(x))) {return(max(x))} else {return(min(x))}})
p.values  <- -log10(tt.res[,ncol(tt.res)])

fc.cutoffs      <- log2(c(1,1.5,2,3))
fc.color.values <- round(seq(0.9,0,(0-0.9)/(length(fc.cutoffs)-1)),digit=3)

p.cutoffs  <- -log10(c(1,0.05,0.01,0.001, 0.00001))
p.color.values <- round(seq(0.9,0,(0-0.9)/(length(p.cutoffs)-1)),digit=3)

minX <- min(c(fc.values,-1*fc.cutoffs))
maxX <- max(c(fc.values,fc.cutoffs))
minY <- min(c(p.values,p.cutoffs))
maxY <- max(c(p.values,p.cutoffs))

pdf(file=sprintf("%s/volcano_plot.pdf",out.dir), width=7, height=7)
plot.new()
plot.window( c(minX,maxX) , c(minY,maxY))

I <- length(fc.cutoffs)
J <- length(p.cutoffs)

for (i in 1:I) {
  fc.min <- fc.cutoffs[i]
  if (i == I) {
    fc.max <- max(abs(fc.values))
  } else {
    fc.max <- fc.cutoffs[i+1]
  }
  fc.color.value <- fc.color.values[i]
  for (j in 1:J) {
    p.min <- p.cutoffs[j]
    if (j == J) {
      p.max <- max(abs(p.values))
    } else {
      p.max <- p.cutoffs[j+1]
    }
    p.color.value <- p.color.values[j]

    indexes <- which(fc.values >= fc.min & fc.values <= fc.max & p.values >= p.min & p.values <= p.max)
    color.value=sqrt((fc.color.value^2+p.color.value^2)/2)
    color=rgb(0.9,color.value,color.value,0.8)
    points(x=fc.values[indexes],y=p.values[indexes],pch=20,col=color)

    indexes <- which(fc.values <= -1*fc.min & fc.values >= -1*fc.max & p.values >= p.min & p.values <= p.max)
    color.value=sqrt((fc.color.value^2+p.color.value^2)/2)
    color=rgb(color.value,color.value,0.9,0.8)
    points(x=fc.values[indexes],y=p.values[indexes],pch=20,col=color)
  }
}
for (fc in fc.cutoffs) {
  lines(x=c(fc,fc),y=c(minY,maxY))
  lines(x=-1*c(fc,fc),y=c(minY,maxY))

  text(x=fc,y=maxY,pos=1,labels=2^fc,cex=0.6)
}
for (p in p.cutoffs) {
  lines(x=c(minX,maxX),y=c(p,p))

  text(x=maxX,y=p,pos=2,labels=10^(p*-1),cex=0.6)
}

axis(1,cex.axis=0.8)
mtext("log2(fold-change)", side=1, line=2, cex=0.8,las=0, col="blue")
axis(2,las=1,cex.axis=0.8)
mtext("-log10(p-value)", side=2, line=2, cex=0.8,las=0, col="blue")
title(main="Volcano plot")
dev.off()
#--------------------------------------------#

#--------------------------------------------#
quit(save="no")
#--------------------------------------------#
