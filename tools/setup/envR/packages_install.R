if (TRUE) {
  args      <- commandArgs(TRUE)
  rlibs.dir <- args[1]
} else {
  rlibs.dir <- "/app/tools/condaR/packages/"
}

.libPaths(rlibs.dir)
source("http://bioconductor.org/biocLite.R")

if("Biobase"             %in% rownames(installed.packages()) == FALSE) {
  install.packages("Biobase"             , lib=rlibs.dir,repos=biocinstallRepos())
}
if("BiocManager"             %in% rownames(installed.packages()) == FALSE) {
  install.packages("BiocManager"             , lib=rlibs.dir,repos=biocinstallRepos())
}
if("stringr"             %in% rownames(installed.packages()) == FALSE) {
  install.packages("stringr"             , lib=rlibs.dir,repos=biocinstallRepos())
}
if("AnnotationDbi"             %in% rownames(installed.packages()) == FALSE) {
  install.packages("AnnotationDbi"             , lib=rlibs.dir,repos=biocinstallRepos())
}
#--------------------------------------------#

#--------------------------------------------#
#Plotting and color options packages
if("grid"                %in% rownames(installed.packages()) == FALSE) {
  install.packages("grid"                , lib=rlibs.dir,repos=biocinstallRepos())
}
if("gridExtra"           %in% rownames(installed.packages()) == FALSE) {
  install.packages("gridExtra"           , lib=rlibs.dir,repos=biocinstallRepos())
}
if("ggplot2"             %in% rownames(installed.packages()) == FALSE) {
  install.packages("ggplot2"             , lib=rlibs.dir,repos=biocinstallRepos())
}
if("ggfortify"           %in% rownames(installed.packages()) == FALSE) {
  install.packages("ggfortify"             , lib=rlibs.dir,repos=biocinstallRepos())
}
if("pheatmap"            %in% rownames(installed.packages()) == FALSE) {
  install.packages("pheatmap"             , lib=rlibs.dir,repos=biocinstallRepos())
}
#--------------------------------------------#

#--------------------------------------------#
#Quality control and pre-processing packages
if("affyio"              %in% rownames(installed.packages()) == FALSE) {
  install.packages("affyio"              , lib=rlibs.dir,repos=biocinstallRepos())
}
if("affy"                %in% rownames(installed.packages()) == FALSE) {
  install.packages("affy"                , lib=rlibs.dir,repos=biocinstallRepos())
}
if("oligo"               %in% rownames(installed.packages()) == FALSE) {
  install.packages("oligo"               , lib=rlibs.dir,repos=biocinstallRepos())
}
if("preprocessCore"               %in% rownames(installed.packages()) == FALSE) {
  install.packages("preprocessCore"              , lib=rlibs.dir,repos=biocinstallRepos())
}
#--------------------------------------------#

#--------------------------------------------#
#Statistical filtration
if("limma"               %in% rownames(installed.packages()) == FALSE) {
  install.packages("limma"              , lib=rlibs.dir,repos=biocinstallRepos())
}
#--------------------------------------------#

#--------------------------------------------#
quit(save="no")
#--------------------------------------------#
