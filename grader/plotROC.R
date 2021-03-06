# last updated 2014-12-12 toby

# draws ROC curves for all CUIs calculated by grader.py

library(ROCR)

getCUI <- function (name)
{
  return(substr(name, 1, 8))
}

drawCurve <- function (name)
{
	loc <- paste(c(rocloc, name), collapse="")
	rawdata <- read.csv(loc)

	scores <- rawdata$score
	class <- rawdata$class

	print(c("Drawing ROC for", name))

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

	pngloc <- "/home/toby/grader/curves/"
	cui <- substr(name, 1, 8)

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

rocloc <- "/home/toby/grader/data/roc/"
fnames <- list.files(rocloc)

temp <- "/home/toby/grader/curves/"
dir.create(temp, showWarnings=TRUE)

work <- lapply(fnames, function (name)
{
	drawCurve(name)
})
