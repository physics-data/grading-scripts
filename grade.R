#!/usr/bin/env Rscript

## 输入文件：
## phase1.xls 第一阶段成绩
## phase2.xls 第二阶段成绩
## comments.csv 给 A+ 学生的评语
##
## 输出文件：
## score1.csv 第一阶段分数
## score2.csv 第二阶段分数
## upload1.csv 第一阶段待上传的文件
## upload2.csv 第二阶段待上传的文件

require(plyr)
require(readxl)

args <- commandArgs(trailingOnly=TRUE)
p1 <- read_xls(args[1])
p2 <- read_xls(args[2])

f1 <- setdiff(p1$学号, p2$学号) # 只选了 (1) 的同学
s1 <- p1[p1$学号 %in% f1,]

f2 <- setdiff(p2$学号, p1$学号) # 只选了 (2) 的同学

measure <- data.frame(level=c("A+", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "F"),
                     score=c(98, 94, 89, 80, 70, 64, 60, 52, 46, 40, 30, 0))

s1$等级 <- laply(s1$总分, function(sc) as.character(measure$level[min(which(measure$score < sc))]))

s2 <- merge(p1, p2, by=c("学号", "姓名"))
s2[is.na(s2)] <- 0

s2$合计 <- (s2$总分.x+s2$总分.y)/2
s2$等级 <- laply(s2$合计, function(sc) as.character(measure$level[min(which(measure$score < sc))]))

o2 <- p2[p2$学号 %in% f2,]
o2$等级 <- laply(o2$总分, function(sc) as.character(measure$level[min(which(measure$score < sc))]))

out_fields <- c("学号", "等级")

if (length(args) > 2) {
    comments <- read_xls(args[3])
    s1 <- merge(s1, comments, by="学号", all.x=TRUE)
    s2 <- merge(s2, comments, by="学号", all.x=TRUE)
    o2 <- merge(o2, comments, by="学号", all.x=TRUE)

    # 将无评语的 A+ 降为 A
    Aplus <- subset(s1, 等级=="A+")
    s1[row.names(Aplus[is.na(Aplus$评语),]),]$等级 <- "A"

    out_fields <- c(out_fields, "评语")
}

write.csv(s1, "score1.csv", row.names=FALSE)
write.csv(s2, "score2.csv", row.names=FALSE)
write.csv(o2, "score2o.csv", row.names=FALSE)

print(sprintf("(1) 的 A+ 比例: %f", (sum(s1$等级=="A+") + sum(s2$等级=="A+")) / (nrow(s1)+nrow(s2))))
print(sprintf("(2) 的 A+ 比例: %f", sum(s2$等级=="A+") / nrow(s2)))

upload1 <- rbind(s1[out_fields], s2[out_fields])
write.csv(upload1[upload1$学号 != 2019011717,],
          "upload1.csv", row.names=FALSE, na = "", fileEncoding="UTF-8")
write.csv(rbind(s2[out_fields], o2[out_fields]),
          "upload2.csv", row.names=FALSE, na = "", fileEncoding="UTF-8")
