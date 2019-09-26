####################################################################################
#        Normalisation of Affymetrix microarrays with RMA: script                  #
####################################################################################
#                                                                                  #
# ******************************************************************************** #
# *                                                                              * #
# * This code is distributed under GNU Public License version 2.                 * #
# * Author: Frederic Chalmel                                                     * #
# * Programming language: R (>3.5.1)                                             * #
# * Required R packages: Biobase,                                                * #
# *                      grid, gridExtra, ggplot2,                               * #
# *                      affyio, affy, oligo                                     * #
# * Creation date: 31th of October, 2018                                         * #
# * Last update: 31/10/2018                                                      * #
# * Version: 1.0.0                                                               * #
# *                                                                              * #
# ******************************************************************************** #
#                                                                                  #
# ******************************************************************************** #
# *                                                                              * #
# * https://www.bioconductor.org/packages/devel/workflows/vignettes/maEndToEnd/inst/doc/MA-Workflow.html
# * https://github.com/AEBilgrau/DLBCLdata/blob/master/R/preprocessCELFiles.R    * #
# * https://wiki.bits.vib.be/index.php/Analyze_your_own_microarray_data_in_R/Bioconductor
# * http://rstudio-pubs-static.s3.amazonaws.com/53162_cd16ee63c24747459ccd180f69f07810.html
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

probetype <- c("entrezg","ensg","refseq","enst")[1]
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
#Quality control and pre-processing packages
library(affyio)
library(affy)
library(oligo)
#--------------------------------------------#

#--------------------------------------------#
samples.info.file <- sprintf("%s/samples.info",in.dir)
if (file.exists(samples.info.file) == FALSE) {
  stop("The sample info data file does not exist!")
  quit(save="no")
}
samples.info      <- read.table(samples.info.file,header=TRUE,sep="\t",quote="",check.names=FALSE)

cel.files         <- normalizePath(sprintf("%s/%s",in.dir,samples.info[,"sampleFiles"]))
sample.names      <- samples.info[,"sampleNames"]
rownames(samples.info) <- sample.names
#--------------------------------------------#

#--------------------------------------------#
if (length(which(file.exists(cel.files)==FALSE)) > 0) {
  stop("Some raw data files do not exist!")
  quit(save="no")
}
#--------------------------------------------#

#--------------------------------------------#
array.type <- unique(sapply(cel.files, function(x) return(read.celfile.header(x)$cdfName)))

if (length(array.type) != 1) {
  stop("The raw data files should be from one array platform to be preprocess!")
  quit(save="no")
}
#--------------------------------------------#

#--------------------------------------------#
platform = cleancdfname(array.type)
platform = sub("cdf", "", platform)
platform = sub("stv1", "st", platform)
platform = sub("stv2", "st", platform)
#--------------------------------------------#

#--------------------------------------------#
pkgname1 <- sprintf("pd.%s",gsub("([^a-z0-9]+)",".",tolower(array.type)))
if(pkgname1 %in% rownames(installed.packages()) == FALSE) {
  stop("The annotation package for preprocessing those raw data files does not exist!")
  quit(save="no")
}
require(pkgname1, character.only = TRUE)
#--------------------------------------------#

#--------------------------------------------#
pattern = sprintf('%s[a-z][a-z]%scdf',platform,probetype)
pkgname2 = grep(pattern ,rownames(installed.packages()),value=TRUE)

if (length(pkgname2) > 1) {
  stop("Several annotation packages for preprocessing those raw data files exist!")
  quit(save="no")
} else if (length(pkgname2) == 0) {
  stop("The annotation package for preprocessing those raw data files does not exist!")
  quit(save="no")
}
require(pkgname2, character.only = TRUE)
#--------------------------------------------#

#--------------------------------------------#
# Microarray pictures: Chip pseudo-images
# Microarray pictures can show large inconsistencies on individual arrays.
# https://wiki.bits.vib.be/index.php/How_to_create_chip_pseudo-images
#--------------------------------------------#
raw.data <- oligo::read.celfiles(filenames = cel.files, sampleNames=sample.names,verbose = FALSE,pkgname=pkgname1)
if (validObject(raw.data) == FALSE) {
  stop("The loaded raw data do not pass the tests of validy!")
}
raw.data$sample <- sample.names
pset.data       <- fitProbeLevelModel(raw.data)
rm(raw.data)

pdf(file=sprintf("%s/pseudo_images.pdf",out.dir), width=7, height=7)
colors <- grey(seq(0,1,0.01))
N = length(sample.names)
n = 2
m = 2
for (i in 0:(ceiling(N/(n*m))-1)) {
  from <- (i*n*m)+1
  to   <- from+(n*m)-1
  if (to > N) {to = N}

  v = rep(0,n*m)
  v[(from-i*(n*m)):(to-i*(n*m))] = (from-i*(n*m)):(to-i*(n*m))
  mat = matrix(v,nrow=n,ncol=m,byrow=TRUE)

  layout(mat, widths = rep(1,m), heights = rep(1,n), respect = FALSE)
  for (j in from:to) {
    image(pset.data,which=j,type="residuals",main=sample.names[j])
  }
}
dev.off()
rm(pset.data)
#--------------------------------------------#

#--------------------------------------------#
# Normalization with RMA
#--------------------------------------------#
# raw data
rma.data1           <- exprs(just.rma(filenames = cel.files, verbose = TRUE, cdfname = pkgname2, background=FALSE, normalize=FALSE))
colnames(rma.data1) <- sample.names
rownames(rma.data1) <- gsub("_at","",rownames(rma.data1))
# data after background correction
rma.data2           <- exprs(just.rma(filenames = cel.files, verbose = TRUE, cdfname = pkgname2, background=TRUE, normalize=FALSE))
colnames(rma.data2) <- sample.names
rownames(rma.data2) <- gsub("_at","",rownames(rma.data2))
# normalized data
rma.data3           <- exprs(just.rma(filenames = cel.files, verbose = TRUE, cdfname = pkgname2, background=TRUE, normalize=TRUE))
colnames(rma.data3) <- sample.names
rownames(rma.data3) <- gsub("_at","",rownames(rma.data3))

write.table(round(rma.data3,digit=3),file=sprintf("%s/matrix.data",out.dir),quote=FALSE,col.names=NA,row.names=TRUE,sep="\t")
#--------------------------------------------#

#--------------------------------------------#
# Copy the samples.info file
#--------------------------------------------#
write.table(samples.info,file=sprintf("%s/matrix.info",out.dir),quote=FALSE,col.names=NA,row.names=TRUE,sep="\t")
#--------------------------------------------#

#--------------------------------------------#
# Density plot of log2-transformed intensity signals
#--------------------------------------------#
p1 <- ggplot2::ggplot(stack(as.data.frame(rma.data1)), aes(x = values, fill = ind )) +
  geom_density(alpha=.1) +
  ggtitle("Raw data") +
  xlab("Log2(intensity signals)")
p2 <- ggplot2::ggplot(stack(as.data.frame(rma.data2)), aes(x = values, fill = ind )) +
  geom_density(alpha=.1) +
  ggtitle("Data after background correction") +
  xlab("Log2(intensity signals)")
p3 <- ggplot2::ggplot(stack(as.data.frame(rma.data3)), aes(x = values, fill = ind )) +
  geom_density(alpha=.1) +
  ggtitle("Normalized data") +
  xlab("Log2(intensity signals)")

pdf(sprintf("%s/density_plot.pdf",out.dir), width=15, height=5)
grid.arrange(p1,p2,p3, top="Density plot of intensity signals", nrow=1)
dev.off()
#--------------------------------------------#

#--------------------------------------------#
# Boxplot of log2-transformed intensity signals
#--------------------------------------------#
p1 <- ggplot2::ggplot(stack(as.data.frame(rma.data1)), aes(x = ind, y = values)) +
  xlab("Samples") +
  ylab("Log2(intensity signals)") +
  geom_boxplot(outlier.shape = NA) +
  ggtitle("Raw data") +
  theme(plot.title = element_text(size = 10), axis.text.x = element_text(colour = "aquamarine4", angle = 60, size = 6.5, hjust = 1 , face = "bold"))
p2 <- ggplot2::ggplot(stack(as.data.frame(rma.data2)), aes(x = ind, y = values)) +
  xlab("Samples") +
  ylab("Log2(intensity signals)") +
  geom_boxplot(outlier.shape = NA) +
  ggtitle("Data after background correction") +
  theme(plot.title = element_text(size = 10), axis.text.x = element_text(colour = "aquamarine4", angle = 60, size = 6.5, hjust = 1 , face = "bold"))
p3 <- ggplot2::ggplot(stack(as.data.frame(rma.data3)), aes(x = ind, y = values)) +
  xlab("Samples") +
  ylab("Log2(intensity signals)") +
  geom_boxplot(outlier.shape = NA) +
  ggtitle("Normalized data") +
  theme(plot.title = element_text(size = 10), axis.text.x = element_text(colour = "aquamarine4", angle = 60, size = 6.5, hjust = 1 , face = "bold"))

pdf(sprintf("%s/box_plot.pdf",out.dir), width=15, height=5)
grid.arrange(p1,p2,p3, top="Boxplot of intensity signals", nrow=1)
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
pdf(sprintf("%s/MA_plots.pdf",out.dir), width=15, height=5)
for (i in 1:ncol(rma.data1)) {
  layout(matrix(c(1:3), 1, 3, byrow = TRUE), respect = FALSE)
  MAplot(rma.data1,which=i)
  MAplot(rma.data2,which=i)
  MAplot(rma.data3,which=i)
}
dev.off()
#--------------------------------------------#

#--------------------------------------------#
# PCA plots of log2-transformed intensity signals
#--------------------------------------------#
# http://rstudio-pubs-static.s3.amazonaws.com/53162_cd16ee63c24747459ccd180f69f07810.html
#--------------------------------------------#
data <- rma.data3
if (nrow(data) > 1000) {n <- 1000} else {n <- nrow(data)}
data <- data[sort(apply(data,1,sd),decreasing=TRUE,index.return=TRUE)$ix[1:n],,drop=FALSE]
pca.res = prcomp(t(data),scale.=TRUE)

pdf(sprintf("%s/PCA_plot.pdf",out.dir), width=7, height=7)
if (length(which(colnames(samples.info) == "conditionNames")) > 0) {
  p <- autoplot(pca.res,label=TRUE,label.size=3,data=samples.info,colour="conditionNames",title="Principal component analysis of normalized data")
} else {
  p <- autoplot(pca.res,label=TRUE,label.size=3,title="Principal component analysis of normalized data")
}
p + ggtitle("Principal component analysis of normalized data")

dev.off()
#--------------------------------------------#

#--------------------------------------------#
# Heatmap of the correlaton matrix
#--------------------------------------------#
cor.res <- as.matrix(1-cor(rma.data3))
#diag(dist.res) <- NA
colors  <- grey(seq(0,1,0.05))
MinV    <- round(min(cor.res, na.rm = TRUE),digit=3)
MaxV    <- round(max(cor.res, na.rm = TRUE),digit=3)

pdf(sprintf("%s/correlation_matrix.pdf",out.dir), width=7, height=7)
if (ncol(samples.info) > 2) {
  annotation.data <- as.data.frame(samples.info[,3:ncol(samples.info)])
  rownames(annotation.data) <- samples.info[,2]

  pheatmap(cor.res, col = colors, legend = TRUE, treeheight_row = 0,
    legend_labels = (c("High","Low")),
    legend_breaks = c(MinV, MaxV),
    main = "Clustering heatmap for the correlation matrix",
    annotation_row = annotation.data
  )
} else {
  pheatmap(cor.res, col = colors, legend = TRUE, treeheight_row = 0,
    legend_labels = (c("High","Low")),
    legend_breaks = c(MinV, MaxV),
    main = "Clustering heatmap for the correlation matrix"
  )
}
dev.off()
#--------------------------------------------#

#--------------------------------------------#
quit(save="no")
#--------------------------------------------#
