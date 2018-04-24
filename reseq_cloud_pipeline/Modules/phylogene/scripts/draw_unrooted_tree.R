library(getopt)

h <- function(x) {
    cat("Usage: Rscript --vanilla draw_unrooted_tree.R -i Newick_file_name [-o Prefix_of_output_files (output)] [-h]\n\n")
    quit(save="no", status=x)
}

opt <- getopt(matrix(c(
    'help',   'h', 0, "logical",
    'prefix', 'o', 1, "character",
    'newick', 'i', 1, "character"
), ncol=4, byrow=TRUE));

if (! is.null(opt$help)) { h(0) }

file.prefix <- ifelse(is.null(opt$prefix), "output", opt$prefix)

if (! is.null(opt$newick)) {
    newick.file <- opt$newick
    if (! file.exists(newick.file)) { cat(sprintf("Newick file (%s) was not found!\n", newick.file)); h(1) }
} else {
    h(1)
}

library(ape)
#library(phangorn)

image_file.name <- paste(file.prefix, ".ml.pdf", sep = "")

#image_file.name <- paste(file.prefix, ".ml.png", sep = "")

tree.newick <- read.tree(newick.file)
#png(filename=image_file.name, width = 1000, height = 1000)
pdf(image_file.name, width = 10, height = 10)
plot(tree.newick, type="unrooted", edge.width=2, cex=1)
plot(tree.newick, type="fan", edge.width=2, cex=1)
plot(tree.newick, edge.width=2, cex=1)
dev.off()
