library(ROCR)

values <- read.csv("roc.txt")

png(filename="~/grader/roc.png", height=500, width = 500, bg="white")

plot(values, type="o", xlim = c(0, 1))

abline(a = "0", b = "1", lty=2)

dev.off()


# perd <- prediction(values$TPR, values$FPR)
# perf <- performance(pred, "tpr", "fpr")
# plot(perf)

# data(ROCR.simple)
# pred <- prediction( ROCR.simple$predictions, ROCR.simple$labels)
# perf <- performance(pred,"tpr","fpr")
# plot(perf)
