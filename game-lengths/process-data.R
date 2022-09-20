library(ggplot2)
files <- list.files("data")
data <- data.frame(variant=character(), moves=integer())
setwd("data")
for (file in files) {
    variant <- sub("\\.target", "", file) 
    moves <- c(sapply(readLines(file), strtoi))
    df <- data.frame(
        variant=rep(variant, length(moves)),
        moves=moves
    )
    ggplot(df) + aes(x=moves) + geom_density() + xlim(0, 100)
    ggsave(paste("../plots/",variant,".svg", sep=""), width=30, height=20, units="cm")
    data <- rbind(data, df)
    print(paste(variant, median(moves)))
}

ggplot(data) + aes(x=moves, color=variant) + geom_density() + xlim(0, 100)
ggsave("../plots/all.svg", width=30, height=20, units="cm")
