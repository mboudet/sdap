####################################################################################
#        Create design and contrasts matrices: script                              #
####################################################################################
#                                                                                  #
# ******************************************************************************** #
# *                                                                              * #
# * This code is distributed under GNU Public License version 2.                 * #
# * Author: Frederic Chalmel                                                     * #
# * Programming language: R (>3.5.1)                                             * #
# * Required R packages: Biobase,                                                * #
# *                      limma                                                   * #
# * Creation date: 21th of May, 2019                                             * #
# * Last update: 21/05/2019                                                      * #
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
  out.dir     <- args[3]
}
#--------------------------------------------#

#--------------------------------------------#
#--------------------------------------------#
#--------------------------------------------#
# in.dir1 : directory containing the matrix info file (as well as the matrix data file)
#--------------------------------------------#
matrix.info.file <- sprintf("%s/matrix.info",in.dir1)
if (file.exists(matrix.info.file) == FALSE) {
  stop("The matrix info data file does not exist!")
  quit(save="no")
}
matrix.info      <- as.matrix(read.table(matrix.info.file,header=TRUE,sep="\t",quote="",check.names=FALSE,row.names=1))
#--------------------------------------------#

#--------------------------------------------#
# in.dir2 : directory containing the contrasts.data file
#--------------------------------------------#
contrasts.file <- sprintf("%s/contrasts.data",in.dir2)
if (file.exists(contrasts.file) == FALSE) {
  stop("The contrasts.data file does not exist!")
  quit(save="no")
}
contrasts.data <- as.matrix(read.table(contrasts.file,header=FALSE,sep="\t",quote="",check.names=FALSE))
#--------------------------------------------#
#--------------------------------------------#
#--------------------------------------------#

#--------------------------------------------#
Sel.Conds <- unique(as.vector(contrasts.data[,1:2]))

if (length(Sel.Conds) <= 1) {
  stop("The contrasts.data file must contain at least two conditions!")
  quit(save="no")
}
if (length(which((matrix.info[,"conditionNames"] %in% Sel.Conds) == FALSE)) != 0) {
  stop("The contrasts.data file contains conditionNames that are not present in the matrix.info file!")
  quit(save="no")
}
#--------------------------------------------#

#--------------------------------------------#
Sel.Samps <- rownames(matrix.info)[ matrix.info[,"conditionNames"] %in% Sel.Conds]
design.matrix <- matrix(0,nrow=length(Sel.Samps),ncol=length(Sel.Conds),dimnames=list(Sel.Samps,Sel.Conds))

for (Sel.Cond in Sel.Conds) {
  design.matrix [ rownames(matrix.info)[which(matrix.info[,"conditionNames"] == Sel.Cond)] , Sel.Cond ] <- 1
}

write.table(design.matrix,file=sprintf("%s/design.matrix",out.dir),quote=FALSE,col.names=NA,row.names=TRUE,sep="\t")
#--------------------------------------------#

#--------------------------------------------#
contrasts.data
contrasts.matrix <- matrix(0,nrow=length(Sel.Conds),ncol=nrow(contrasts.data), dimnames=list(Sel.Conds, sprintf("%s vs %s",contrasts.data[,1],contrasts.data[,2])))
for (i in 1:nrow(contrasts.data)) {
    Cond1 <- contrasts.data[i,1]
    Cond2 <- contrasts.data[i,2]

    contrasts.matrix[c(Cond1,Cond2),i] <- c(1,-1)
}
write.table(contrasts.matrix,file=sprintf("%s/contrasts.matrix",out.dir),quote=FALSE,col.names=NA,row.names=TRUE,sep="\t")
#--------------------------------------------#

#--------------------------------------------#
quit(save="no")
#--------------------------------------------#
