####################################################################################
#        Quantile normalization of matrix data file: script                        #
####################################################################################
#                                                                                  #
# ******************************************************************************** #
# *                                                                              * #
# * This code is distributed under GNU Public License version 2.                 * #
# * Author: Frederic Chalmel                                                     * #
# * Programming language: R (>3.5.1)                                             * #
# * Required R packages: Biobase,                                                * #
# *                      grid, gridExtra, ggplot2,                               * #
# *                      preprocessCore                                          * #
# * Creation date: 31th of October, 2018                                         * #
# * Last update: 31/10/2018                                                      * #
# * Version: 1.0.0                                                               * #
# *                                                                              * #
# ******************************************************************************** #
#                                                                                  #
# ******************************************************************************** #
# *                                                                              * #
# * http://web.mit.edu/~r/current/arch/i386_linux26/lib/R/library/preprocessCore/html/normalize.quantiles.html                                                                             * #
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
#--------------------------------------------#

#--------------------------------------------#
setwd(in.dir)
source("http://bioconductor.org/biocLite.R")
#--------------------------------------------#

#--------------------------------------------#
#General Bioconductor packages
library(Biobase)
#Plotting and color options packages
library(ggplot2)
library(grid)
library(gridExtra)
library(ggfortify)
library(pheatmap)
#Limma package
library(preprocessCore)
library(oligo)
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
#--------------------------------------------#

#--------------------------------------------#
qq.data     <- as.matrix(normalize.quantiles(matrix.data))
colnames(qq.data) <- colnames(matrix.data)
rownames(qq.data) <- rownames(matrix.data)

write.table(round(qq.data,digit=3),file=sprintf("%s/matrix.data",out.dir),quote=FALSE,col.names=NA,row.names=TRUE,sep="\t")
#--------------------------------------------#

#--------------------------------------------#
# Copy the matrix.info file
#--------------------------------------------#
write.table(matrix.info,file=sprintf("%s/matrix.info",out.dir),quote=FALSE,col.names=NA,row.names=TRUE,sep="\t")
#--------------------------------------------#

#--------------------------------------------#
# Density plot of log2-transformed intensity signals
#--------------------------------------------#
p1 <- ggplot2::ggplot(stack(as.data.frame(matrix.data)), aes(x = values, fill = ind )) +
  geom_density(alpha=.1) +
  ggtitle("Raw data") +
  xlab("Log2(intensity signals)")
p2 <- ggplot2::ggplot(stack(as.data.frame(qq.data)), aes(x = values, fill = ind )) +
  geom_density(alpha=.1) +
  ggtitle("Quantile normalized data") +
  xlab("Log2(intensity signals)")

pdf(sprintf("%s/density_plot.pdf",out.dir), width=10, height=5)
grid.arrange(p1,p2, top="Density plot of intensity signals", nrow=1)
dev.off()
#--------------------------------------------#

#--------------------------------------------#
# Boxplot of log2-transformed intensity signals
#--------------------------------------------#
p1 <- ggplot2::ggplot(stack(as.data.frame(matrix.data)), aes(x = ind, y = values)) +
  xlab("Samples") +
  ylab("Log2(intensity signals)") +
  geom_boxplot(outlier.shape = NA) +
  ggtitle("Raw data") +
  theme(plot.title = element_text(size = 10), axis.text.x = element_text(colour = "aquamarine4", angle = 60, size = 6.5, hjust = 1 , face = "bold"))
p2 <- ggplot2::ggplot(stack(as.data.frame(qq.data)), aes(x = ind, y = values)) +
  xlab("Samples") +
  ylab("Log2(intensity signals)") +
  geom_boxplot(outlier.shape = NA) +
  ggtitle("Quantile normalized data") +
  theme(plot.title = element_text(size = 10), axis.text.x = element_text(colour = "aquamarine4", angle = 60, size = 6.5, hjust = 1 , face = "bold"))

pdf(sprintf("%s/box_plot.pdf",out.dir), width=10, height=5)
grid.arrange(p1,p2, top="Boxplot of intensity signals", nrow=1)
dev.off()
#--------------------------------------------#

#--------------------------------------------#
# MA plots of log2-transformed intensity signals
#--------------------------------------------#
# M is the difference between the intensity of a probe on the array and the median intensity of that probe over all arrays
# A is the average of the intensity of a probe on that array and the median intesity of that probe over all arrays
#
# Ideally, the cloud of data points in the MA-plot should be centered
# around M=0 (blue line). This is because we assume that the majority
# of the genes is not DE and that the number of upregulated genes is
# similar to the number of downregulated genes. Additionally, the
# variability of the M values should be similar across different
# array-medianarray combinations. You see that the spread of the point
# cloud increases with the average intensity: the loess curve (red line)
# moves further and further away from M=0 when A increases. To remove
# (some of this) dependency, we will normalize the data.
#--------------------------------------------#
pdf(sprintf("%s/MA_plots.pdf",out.dir), width=10, height=5)
for (i in 1:ncol(qq.data)) {
  layout(matrix(c(1:2), 1, 2, byrow = TRUE), respect = FALSE)
  MAplot(matrix.data,which=i)
  MAplot(qq.data,which=i)
}
dev.off()
#--------------------------------------------#

#--------------------------------------------#
# PCA plots of log2-transformed intensity signals
#--------------------------------------------#
# http://rstudio-pubs-static.s3.amazonaws.com/53162_cd16ee63c24747459ccd180f69f07810.html
#--------------------------------------------#
data <- qq.data
if (nrow(data) > 1000) {n <- 1000} else {n <- nrow(data)}
data <- data[sort(apply(data,1,sd),decreasing=TRUE,index.return=TRUE)$ix[1:n],,drop=FALSE]
pca.res = prcomp(t(data),scale.=TRUE)

pdf(sprintf("%s/PCA_plot.pdf",out.dir), width=7, height=7)
p <- autoplot(pca.res,label=TRUE,label.size=3,title="Principal component analysis of normalized data")
p + ggtitle("Principal component analysis of normalized data")

dev.off()
#--------------------------------------------#

#--------------------------------------------#
# Heatmap of the correlaton matrix
#--------------------------------------------#
cor.res <- as.matrix(1-cor(qq.data))
#diag(dist.res) <- NA
colors  <- grey(seq(0,1,0.05))
MinV    <- round(min(cor.res, na.rm = TRUE),digit=3)
MaxV    <- round(max(cor.res, na.rm = TRUE),digit=3)

pdf(sprintf("%s/correlation_matrix.pdf",out.dir), width=7, height=7)
pheatmap(cor.res, col = colors, legend = TRUE, treeheight_row = 0,
legend_labels = (c("High","Low")),
legend_breaks = c(MinV, MaxV),
main = "Clustering heatmap for the correlation matrix")
dev.off()
#--------------------------------------------#

#--------------------------------------------#
quit(save="no")
#--------------------------------------------#
