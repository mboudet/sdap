####################################################################################
#        Average replicate experiments with matrix data file: script               #
####################################################################################
#                                                                                  #
# ******************************************************************************** #
# *                                                                              * #
# * This code is distributed under GNU Public License version 2.                 * #
# * Author: Frederic Chalmel                                                     * #
# * Programming language: R (>3.5.1)                                             * #
# * Required R packages: Biobase                                                 * #
# * Creation date: 31th of October, 2018                                         * #
# * Last update: 31/10/2018                                                      * #
# * Version: 1.0.0                                                               * #
# *                                                                              * #
# ******************************************************************************** #
#                                                                                  #
# ******************************************************************************** #
# *                                                                              * #
# *                                                                              * #
# *                                                                              * #
# ******************************************************************************** #
#                                                                                  #
####################################################################################

#--------------------------------------------#
if (TRUE) {
  args       <- commandArgs(TRUE)
  in.dir     <- args[1]
  out.dir    <- args[2]
}
method    <- c("mean","median")[1]
#--------------------------------------------#

#--------------------------------------------#
setwd(in.dir)
source("http://bioconductor.org/biocLite.R")
#--------------------------------------------#

#--------------------------------------------#
#General Bioconductor packages
library(Biobase)
#--------------------------------------------#

#--------------------------------------------#
matrix.file <- sprintf("%s/matrix.data",in.dir)
if (file.exists(matrix.file) == FALSE) {
  stop("The matrix data file does not exist!")
  quit(save="no")
}
matrix.data <- as.matrix(read.table(matrix.file,header=TRUE,sep="\t",quote="",check.names=TRUE,row.names=1))

matrix.info.file <- sprintf("%s/matrix.info",in.dir)
if (file.exists(matrix.info.file) == FALSE) {
  stop("The matrix info data file does not exist!")
  quit(save="no")
}
matrix.info      <- as.matrix(read.table(matrix.info.file,header=TRUE,sep="\t",quote="",check.names=TRUE,row.names=1))

if (length(which(colnames(matrix.info) == "conditionNames")) != 1) {
  stop("The matrix info data file does not contain a conditionNames column!")
  quit(save="no")
}
#--------------------------------------------#

#--------------------------------------------#
cnames <- unique(matrix.info[,"conditionNames"])
data   <- matrix(NA,ncol=length(cnames),nrow=nrow(matrix.data),dimnames=list(rownames(matrix.data),cnames))

for (cname in cnames) {
  snames <- rownames(matrix.info)[which(matrix.info[,"conditionNames"] == cname)]

  if (method == "mean") {
    data[,cname] <- apply(matrix.data[,snames,drop=FALSE],1,median)
  } else {
    data[,cname] <- apply(matrix.data[,snames,drop=FALSE],1,mean)
  }
}
write.table(round(data,digit=3),file=sprintf("%s/matrix_final.data",out.dir),quote=FALSE,col.names=NA,row.names=TRUE,sep="\t")
#--------------------------------------------#

#--------------------------------------------#
# Copy the matrix.info file
#--------------------------------------------#
data.info <- matrix(nrow=length(cnames),ncol=ncol(matrix.info),dimnames=list(cnames,colnames(matrix.info)))
for (cname in cnames) {
  for (cond in colnames(matrix.info)) {
    snames <- rownames(matrix.info)[which(matrix.info[,"conditionNames"] == cname)]
    data.info[cname,cond] <- paste(unique(matrix.info[snames,cond]), collapse="|")
  }
}
write.table(data.info,file=sprintf("%s/matrix_final.info",out.dir),quote=FALSE,col.names=NA,row.names=TRUE,sep="\t")
#--------------------------------------------#

#--------------------------------------------#
quit(save="no")
#--------------------------------------------#
