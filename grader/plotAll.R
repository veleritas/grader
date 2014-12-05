# first version 2014-12-04 toby
# last updated  2014-12-04 toby

# draws ROC curves for all CUIs calculated by grader.py

drawCurve <- function (name)
{
#	make full file path
	loc <- paste(c(rocloc, name), collapse="")
	values <- read.csv(loc)

	pngloc <- "/home/toby/grader/curves/"
	cui <- substr(name, 1, 8)

	print(c("drawing", cui))

	pngname <- paste(c(pngloc, cui, ".png"), collapse="")

	png(filename=pngname, height=500, width=500, bg="white")
	plot(values, main=cui, type="o", xlim=c(0, 1))
	abline(a="0", b="1", lty=2)
	dev.off()
}

rocloc <- "/home/toby/grader/roc/"
fnames <- list.files(rocloc)

temp <- "/home/toby/grader/curves/"
dir.create(temp, showWarnings=TRUE)

work <- lapply(fnames, function (name)
{
	drawCurve(name)
})
