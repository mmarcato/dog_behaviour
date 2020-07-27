# THIS FILE IN R, BUT SHOULD BE TRANSLATED TO PYTHON AND INCLUDED IN THE MAIN.PY
# ALL WE DO IS TO REMOVE DUPLICATES 
# FILTER OUT LITTERS WITH ONLY ONE DOG -> DC1, DC2
# FILTER OUT DOGS WITH ONLY ONE DC -> DCS

library(DescTools)
library(ggplot2)
library(dplyr)
library(plyr)

setwd("C://Users//marinara.marcato//Data//Ethogram//Researchers")
data <- read.csv('20-05-20_Ethogram.csv', stringsAsFactors=FALSE)

# removing duplicates, 105 examples left
data = data[!duplicated(data[,3:4]),]
print(nrow(data))


# creating new dataframe dc1 containing data collection 1 
dc1 <- data[data$Data.Collection.Number == 1, ]
# removing litter with only one dog
dc1 = dc1[!(dc1$Litter == 'L' | dc1$Litter == 'T' | dc1$Litter == 'Z'),]
write.csv(dc1, 'dc1.csv')

# creating new dataframe dc2 containing data collection 2 
dc2 <- data[data$Data.Collection.Number == 2, ]
print(nrow(dc2))
# removing litter with only one dog
dc2 = dc2[!(dc2$Litter == 'L' | dc2$Litter == 'T' | dc2$Litter == 'Z'),]
write.csv(dc2, 'dc2.csv')

# retrieving name of dogs with dc1 and dc2
dog_dc = aggregate(data$Data.Collection.Number, by = list(Category = data$Name), FUN = sum)
# retrieving name of dogs with dc1 and dc2
dogs_dcs = dog_dc[dog_dc$x ==3, 'Category']
dcs = data %>% filter( Name %in% dogs_dcs )
print(nrow(dcs))
write.csv(dcs, 'dcs.csv')
