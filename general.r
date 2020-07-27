library(ggplot2)
vars <- read.csv('Variables.csv')
train <- read.csv('Training.csv')



### EXPLORATORY DATA ANALYSIS
barplot(table(vars$Type), col = rainbow(6))
barplot(table(vars$Subset), col = rainbow(length(unique(vars$Subset))), xlab = "Subtest in Behaviour Test", ylab = "Number of Variables Analysed")

barplot(table(train$Status),col = rainbow(5) )
barplot(c(16,16,19), names.arg = c('AD', 'GD', 'W'), col = rainbow(3))
barplot(c(32/51*100,19/51*100), names.arg = c('AD/GD', 'W'), col = rainbow(4),
xlab = "Outcome", ylab = "No of Dogs")

