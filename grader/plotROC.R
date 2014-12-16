# last updated 2014-12-16 toby

# draws ROC curves for all CUIs calculated by grader.py

library(ROCR)
get_cui <- function (fname)
{
  return(substr(fname, 1, 8))
}

draw_curve <- function (idir, odir, fname)
{
	loc <- paste(c(idir, fname), collapse = "")
	print("location")
	rawdata <- read.csv(loc)

	scores <- rawdata$score
	class <- rawdata$class

	if (length(scores) == 0) {
		print(c("empty file for", idir, fname))


		return()

	}




	print(c("Drawing ROC for", idir, fname))

	# all the same
	if (diff(range(class)) == 0) {
		if (class[1] == 0) {
			print("all zeros")
		} else {
			print("all ones")
		}
		return()
	}

	pred <- prediction(scores, class)
	perf <- performance(pred, measure = "tpr", x.measure = "fpr")

	pngloc <- odir
	cui <- substr(fname, 1, 8)

	pngname <- paste(c(pngloc, cui, ".png"), collapse="")

	png(filename=pngname, height=800, width=800, bg="white")


	plot(perf, main=cui, type="o", col="blue")
	abline(a="0", b="1", lty=2)

	# get AUC
	temp <- performance(pred, "auc")
	auc <- slot(temp, "y.values")[[1]]

	print(c("AUC:", auc))

	mtext(paste(c("auc", auc), collapse=" "))

	dev.off()
}

#-------------------------------------------------------------------------------

inloc <- "/home/toby/grader/data/roc/"
outloc <- "/home/toby/grader/curves/"

dir.create(outloc, showWarnings = FALSE)

# for all directories:
dirs <- list.files(inloc)
traverse <- lapply(dirs, function (dname)
{
#	make output directory
	outdir <- paste(c(outloc, dname, "/"), collapse = "")
	dir.create(outdir, showWarnings=FALSE)

	subdir <- paste(c(inloc, dname, "/"), collapse = "")

	files <- list.files(subdir)
	work <- lapply(files, function (fname)
	{
		draw_curve(subdir, outdir, fname)
	})
})
