library(DescTools)
library(ggplot2)
library(dplyr)
library(plyr)
library(tidyverse)
library(ggplot2)


setwd("C://Users//marinara.marcato//Data//Ethogram//Trainers")
data <- read.csv('dcs.csv', stringsAsFactors=FALSE)
vars <- read.csv('Variables_Trainers.csv', stringsAsFactors=FALSE)

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


stats <- function(test, var){
        if (!is.na(test)){
        if (test == 'Wilcoxon'){
        cat('\nWilcox', var)
        r = wilcox.test(dcs[dcs$Data.Collection.Number == 1 , var],  dcs[dcs$Data.Collection.Number == 2, var], paired = TRUE)
        return(r$p.value)
        } else if (test == 'Chisq'){            
        cat('\nChisq', var)
        dc1 = dcs[dcs$Data.Collection.Number == 1 , as.character(var)]
        dc2 = dcs[dcs$Data.Collection.Number == 2, as.character(var)]
        #cat(dc1,"\n", dc2,"\n")
        #cat(unique(dc1),"\n", unique(dc2),"\n")
        if ((unique(dc1) == unique(dc2)) & (length(unique(dc1))>1) & (length(unique(dc2))>1)){
                r = chisq.test(dc1, dc2)
                return(r$p.value)
        }
        }
        return(NA)
        }
        return(NA)
        }

vars = vars %>% mutate(Result = mapply(FUN = stats, test = vars$Test, var = vars$Variable))


vars$Result = as.numeric(vars$Result)
vars$Sign = ifelse(vars$Result<0.05, 1, 0)
unique(vars[vars$Sign == 1, 'Variable'])
write.csv(vars,"Results_Trainers_dcs.csv")

sign_vars <- vars %>% select('Variable') %>% filter( vars$Sign == 1, vars$Type == 'ordinal')

ggplot(dcs, aes(x =Data.Collection.Number, fill=Tea.towel.Second.Response..Plays.)) +  geom_bar(position = "dodge")
ggplot(dcs, aes(x = Data.Collection.Number, fill= factor(Tea.towel.Second.Response..Plays.)))+ geom_bar(position = "fill") + labs(y = "Proportion")
ggplot(dcs, aes(x = Data.Collection.Number, fill= factor(Tea.Towel.First.Response..Plays.)))+ geom_bar(position = "fill") + labs(y = "Proportion")


ggplot(dcs, aes(x = Data.Collection.Number, fill= factor(Walking.Initiative)))+ geom_bar(position = "fill") + labs(y = "Proportion")

dcs$Tea.towel.Second.Response..Plays.
plot(dcs$Data.Collection.Number, names.arg = dcs$Tea.Towel.First.Response..Turns.head.)
, xlab = 'Training Outcome', ylab = 'Scoring')