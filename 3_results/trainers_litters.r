library(DescTools)
library(ggplot2)
library(dplyr)
install.packages("languageserver")
# import data
setwd("C://Users//marinara.marcato//Data//Ethogram//Trainers")
data <- read.csv('20-06-23_Ethogram.csv')
# dataframe column names
cols <- colnames(data)

# separate columns by data types
ordinal <- c('Familiarisation.Response..Oriented.to.Handler.',
  'Familiarisation.Response..Exploration.',
  'Familiarisation.Response..Waiting.',
  'Call.Back.Response',
  'Walking.Distractibility',
  'Walking.Pull.on.leash',
  'Walking.Pull.strength',
  'Walking.Initiative',
  'Standing.Response',
  'Sitting.Response',
  'Lying.Response',
  'Lying.Settled',
  'Body.check.Table',
  'Body.check.Response',
  'Distractions.First.Response..Teddy.',
  'Distractions.First.Response..Human.',
  'Distractions.First.Response..Car.',
  'Distractions.First.Response..Food.',
  'Distractions.Second.Response..Teddy.',
  'Distractions.Second.Response..Human.',
  'Distractions.Second.Response..Car.',
  'Distractions.Second.Response..Food.',
  'Distractions.Pull.on.leash',
  'Distractions.Pull.strength',
  'Distractions.Human',
  'Kong.Presentation.Response',
  'Kong.Interaction.Response.to.stimulus',
  'Kong.Interaction.Response.to.handler',
  'Kong.Interaction.Back',
  'Kong.Return.Handler',
  'Dog.Response',
  'Dog.Call.Back.Response',
  'Crate.Entering',
  'Crate.Behaviours..Settled.',
  'Crate.Behaviours..Nudging.Crate.',
  'Crate.Behaviours..Sniffing.Exploring..',
  'Crate.Behaviours..Actively.Seeking.Attention.',
  'Crate.Behaviours..Digging.',
  'Crate.Behaviours..Whining.',
  'Crate.Behaviours..Barking.',
  'Crate.Self.Modulation',
  'Crate.Stress',
  'Petting.Handler.Stimulus',
  'Petting.Handler.Holding.dog',
  'Petting.Confidence.During',
  'Petting.Responsiveness.After',
  'Isolation.Response..Time.oriented.',
  'Isolation.Response..Exploration.',
  'Isolation.Response..Unsettled.Pacing.',
  'Isolation.Response..Whining.', 
  'Isolation.Response..Barking.',
  'Isolation.Urinating',
  'Reunion.Response',
  'Noise.Confidence'
   )

count = c(
  'Short.Barks.Count',
  'Continuous.Barks.Duration',
  'Continuous.Barks.Count',
  'Whines.Duration',
  'Whines.Count',
  'Shakes.Count',
  'Jumps.Count')

categorical = c(
  'Body.check.General..Mouths.', 
  'Body.check.General..Licks.',
  'Tea.Towel.First.Response..Indifferent.', 
  'Tea.Towel.First.Response..Change.from.Neutral.', 
  'Tea.Towel.First.Response..Turns.head.',
  'Tea.Towel.First.Response..Attempts.to.Removes.towel.by.moving.',
  'Tea.Towel.First.Response..Attempts.to.Removes.towel.with.mouth.',
  'Tea.Towel.First.Response..Plays.',
  'Tea.Towel.Second.Response..Indifferent.',
  'Tea.Towel.Second.Response..Change.from.Neutral.', 
  'Tea.Towel.Second.Response..Turns.head.',
  'Tea.Towel.Second.Response..Attempts.to.Removes.towel.by.moving.',
  'Tea.Towel.Second.Response..Attempts.to.Removes.towel.with.mouth.',
  'Tea.Towel.Second.Response..Plays.',
  'Kong.Interaction.Lateralisation',
  'Crate.Urinating',
  'Isolation.Urinating'
)

# removing duplicates considering same dog and same data collection number
# data[,6] is Code
# data[,7] is Data.Collection.Number
data = data[!duplicated(data[,6:7]),]

# METHOD 1: checking how many dogs in each data collection
dog_dc = aggregate(data$Data.Collection.Number, by = list(Category = data$Name), FUN = sum)
## dogs with dc1 only
cat('Dogs with dc1 only: ', length(as.list(dogs_dc1)), '\n') 
print(dogs_dc1)
## dogs with dc2 only
dogs_dc2 = dog_dc[dog_dc$x ==2, 'Category']
cat('Dogs with dc2 only: ', length(as.list(dogs_dc2)), '\n')
print(dogs_dc2)
## dogs with dc1 & dc2 
dogs_dcs = dog_dc[dog_dc$x ==3, 'Category']
cat('Dogs with dc1 & dc2: ', length(as.list(dogs_dcs)), '\n')
print(dogs_dcs)

# CREATING THE DATAFRAMES FOR ANALYSIS

# creating new dataframe dc1 containing data collection 1 
dc1 <- data[data$Data.Collection.Number == 1, ]
# removing litter with only one dog
dc1 = dc1[!(dc1$Litter == 'L' | dc1$Litter == 'T' | dc1$Litter == 'Z'),]
# resetting levels
dc1$Name = factor(dc1$Name)
dc1$Litter = factor(dc1$Litter)
# printing out information
cat("DC1:", length(dc1$Name), "\n", paste(sort(dc1$Name), collapse = ","))



# creating new dataframe dc2 containing data collection 2 
dc2 <- data[data$Data.Collection.Number == 2, ]
# removing litter with only one dog
dc2 = dc2[!(dc2$Litter == 'L' | dc2$Litter == 'T' | dc2$Litter == 'Z'),]
# resetting levels
dc2$Name = factor(dc2$Name)
dc2$Litter = factor(dc2$Litter)
# printing out information
cat("DC2:", length(dc2$Name), "\n", paste(sort(dc2$Name), collapse = ","))


# retrieving name of dogs with dc1 and dc2
dog_dc = aggregate(data$Data.Collection.Number, by = list(Category = data$Name), FUN = sum)
dogs_dcs = dog_dc[dog_dc$x ==3, 'Category']
dcs = data %>% filter( Name %in% dogs_dcs)
# removing litter with only one dog
dcs_litter = subset(dcs,  !Litter %in%  c('L','T', 'Z'))
dcs_litter$Litter = factor(dcs_litter$Litter)
dcs_litter$Name = factor(dcs_litter$Name)


## investigating ordinal variables

ordinal_between_groups <- function(df){
  result = c()
  for (variable in ordinal){
      print(variable)
      r = kruskal.test(df[, variable], df$Litter)
      result = rbind(result, c(variable, r[1], r[2], r[3]))
  }
  return (result)
}



# saves results for ALL ORDINAL-scored behaviours between litters
dc1_ordinal = ordinal_between_groups(dc1)
dc2_ordinal = ordinal_between_groups(dc2)

dc1_ordinal_sign = dc1_ordinal[dc1_ordinal[,4]<0.05, ]
dc2_ordinal_sign = dc2_ordinal[dc2_ordinal[,4]<0.05, ]

# prints outputs to file
cat('Ordinal - DC 1 - Difference between litters')
print(dc1_ordinal_sign)
cat('Ordinal - DC 2 - Difference between litters')
print(dc2_ordinal_sign)


### CATEGORICAL DATA
categorical_between_groups <- function(df){
  result = c()
  for (variable in categorical){
    print(variable)
    if (length(unique(df[,variable]))>1){
      r = chisq.test(df[, variable], df$Litter, simulate.p.value=TRUE)
      #print(c(variable, r[3]))
      result = rbind(result, c(variable, r[1], r[2], r[3]))
    }
  }
  return (result)
}

dc1_categorical = categorical_between_groups(dc1)
dc2_categorical = categorical_between_groups(dc2)
dc1_categorical_sign = dc1_categorical[dc1_categorical[,4]<0.05, ]
dc2_categorical_sign = dc2_categorical[dc2_categorical[,4]<0.05, ]
cat('Categorical - DC 1 - Difference between litters')
print(dc1_categorical_sign)
cat('Categorical - DC 2 - Difference between litters')
print(dc2_categorical_sign)