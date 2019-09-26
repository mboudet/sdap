####################################################################################
#        Normalisation of Affymetrix microarrays with RMA: install data packages   #
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
# *                                                                              * #
# ******************************************************************************** #
#                                                                                  #
####################################################################################

#--------------------------------------------#
if (TRUE) {
  args       <- commandArgs(TRUE)
  rlibs.dir  <- args[1]
  tmp.dir    <- args[2]
} else {
  rlibs.dir <- "c:/Tools/RLIBS/3.5.1"
  tmp.dir   <- "c:/Projects/Startup/tmp"
}

probetype <- c("entrezg","ensg","refseq","enst")[1]
#--------------------------------------------#

#--------------------------------------------#
.libPaths(rlibs.dir)
#General Bioconductor packages
library(stringr)
library(AnnotationDbi)
#--------------------------------------------#

#--------------------------------------------#
# Extract the current release of brainarray
#--------------------------------------------#
url       = "http://mbni.org/customcdf/"
lines     = readLines(url)
mypattern = '>([0-9]+\\.[0-9]+\\.[0-9]+)/</a>'
lines     = grep(mypattern,lines,value=TRUE)
lines     = str_extract(lines, mypattern)
releases  = sort(gsub(">|/</a>","",lines),decreasing=TRUE)
current.release = releases[1]

if (is.na(current.release) == TRUE) {
  url       = "http://brainarray.mbni.med.umich.edu/Brainarray/Database/CustomCDF/CDF_download.asp"
  lines     = readLines(url)
  mypattern = '<a href=([0-9]+\\.[0-9]+\\.[0-9]+)/version.html>'
  lines     = grep(mypattern,lines,value=TRUE)
  lines     = str_extract(lines, mypattern)
  releases  = sort(gsub("<a href=|/version.html>","",lines),decreasing=TRUE)
  current.release = releases[1]
}
#--------------------------------------------#

#--------------------------------------------#
# Extract all available files in the current
# release of brainarray
#--------------------------------------------#
url      = sprintf("http://brainarray.mbni.med.umich.edu/Brainarray/Database/CustomCDF/%s/%s.asp",current.release,probetype)
lines    = readLines(url)
#--------------------------------------------#
# Download, install and load package
#--------------------------------------------#
pattern  = sprintf('([a-z0-9A-Z]+)%scdf_%s.tar.gz',probetype,current.release)
files    = str_extract(grep(pattern ,lines,value=TRUE),pattern)
urls     = sprintf("http://mbni.org/customcdf/%s/%s.download/%s",current.release,probetype,files)
pkgnames = gsub(sprintf("_%s.tar.gz",current.release),"",files)

n <- length(urls)
for (i in 1:n) {
  file       = files[i]
  url        = urls[i]
  pkgname    = pkgnames[i]
  local.file = sprintf("%s/%s.tar.gz",tmp.dir,pkgname)

  if (is.na(pkgname) == FALSE && (pkgname %in% rownames(installed.packages()) == FALSE)) {
    download.file(url = url, destfile = local.file)
    install.packages(pkgs = local.file, repos = NULL, type = "source",lib=rlibs.dir)
  }
}
#--------------------------------------------#

#--------------------------------------------#
pkgnames <- BiocManager::available(pattern="^pd\\.",include_installed=TRUE)
for (pkgname in pkgnames) {
  if (pkgname %in% rownames(installed.packages()) == FALSE) {
    BiocManager::install(pkgs = pkgname, type = "source",lib=rlibs.dir,update=FALSE)
  }
}
#--------------------------------------------#

#--------------------------------------------#
quit(save="no")
#--------------------------------------------#
