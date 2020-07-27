
library(DescTools)
library(ggplot2)
library(dplyr)
library(plyr)


setwd("C://Users//marinara.marcato//Data//Ethogram//Researchers")
data <- read.csv('20-05-20_Ethogram.csv')
vars <- read.csv('variables.csv')

# Adding a column to df vars for Test 
vars = vars %>% mutate(Test = case_when(
        Type == "count" ~ "Wilcoxon",
        Type == "ordinal" ~ "Wilcoxon", 
        Type == "categorical" ~ "Chisq"))

# print the number of variables per data type
print(table(vars$Type))

# removing duplicates, down from 116 to 105 examples left
data = data[!duplicated(data[,3:4]),]
# data collection number per dog
dog_dc = aggregate(data$Data.Collection.Number, by = list(Category = data$Name), FUN = sum)
# retrieving name of dogs with dc1 and dc2
dogs_dcs = dog_dc[dog_dc$x ==3, 'Category']
# selecting dogs with dc1 and dc2 only
dcs = data %>% filter( Name %in% dogs_dcs)
# ordering the df by Name and DC
dcs = dcs[order(dcs$Name, dcs$Data.Collection.Number),]
dcs$Name = factor(dcs$Name)
cat("Number of dogs with DC1 and DC2: ", length(unique(dcs$Name)))