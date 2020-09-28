# install libraries for plotting data
# install.packages('ggplot2')
# install.packages('dplyr')
# install.packages('DescTools')

# import libraries 
library(DescTools)
library(ggplot2)
library(dplyr)

# import data
setwd("E://Study//Ethogram")
data <- read.csv('20-02-26_Ethogram.csv')

# --------------------------------------------------------------------#
#                       COLUMNS PER DATA TYPE                         #
# --------------------------------------------------------------------#
# dataframe column names
cols = colnames(data)

# separate columns by data types
ordinal = c(
  'Familiarisation.Response..Oriented.to.Handler.',
  'Familiarisation.Response..Exploration.',
  'Familiarisation.Response..Waiting.',
  'Call.Back.Response',
  'Walking.Distractibility',
  'Walking.Pull.on.leash',
  'Walking.Pull.strength',
  'Walking.Initiative',
  'Sitting.Attempts',
  'Sitting.Response',
  'Lying.Attempts',
  'Lying.Response',
  'Lying.Settled',
  'Body.check.Response',
  'Distractions.First.Response..Object.',
  'Distractions.First.Response..Human.',
  'Distractions.First.Response..Car.',
  'Distractions.First.Response..Food.',
  'Distractions.Second.Response..Object.',
  'Distractions.Second.Response..Human.',
  'Distractions.Second.Response..Car.',
  'Distractions.Second.Response..Food.',
  'Distractions.Pull.on.leash',
  'Distractions.Pull.strength',
  'Kong.Concentration.Response',
  'Kong.Retrieve.Response.to.stimulus',
  'Kong.Retrieve.Response.to.assessor',
  'Kong.Retrieve.Back',
  'Dog.Response',
  'Dog.Call.Back.Response',
  'Crate.Entering',
  'Crate.Behaviours..Relaxing.',
  'Crate.Behaviours..Sniffing.Exploring..',
  'Crate.Behaviours..Attention.Seeking.',
  'Crate.Behaviours..Digging.',
  'Crate.Behaviours..Licking.Mouthing.',
  'Crate.Behaviours..Whining.',
  'Crate.Behaviours..Barking.',
  'Crate.Response')

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
  'Tea.Towel.First.Response..Turns.head.',
  'Tea.Towel.First.Response..Attempts.to.Removes.towel.by.moving.',
  'Tea.Towel.First.Response..Attempts.to.Removes.towel.with.mouth.',
  'Tea.Towel.First.Response..Plays.',
  'Tea.towel.Second.Response..Indifferent.',
  'Tea.towel.Second.Response..Turns.head.',
  'Tea.towel.Second.Response..Attempts.to.Removes.towel.by.moving.',
  'Tea.towel.Second.Response..Attempts.to.Removes.towel.with.mouth.',
  'Tea.towel.Second.Response..Plays.',
  'Kong.Retrieve.Lateralisation'
  # eliminate 'Crate.Urinating' because only has No
)

all = c(ordinal, count, categorical)

length(ordinal)       # 39 variables
length(count)         # 7 variables
length(categorical)   # 13 variables
length(all)           # 60 variables in total

# --------------------------------------------------------------------#
#                         EXPLORING DATASET                           #
# --------------------------------------------------------------------#
# removing duplicates, 105 examples left
data = data[!duplicated(data[,3:4]),]

# checking how many males and females in dataset
table(data[!duplicated(data[,1]), "Sex"])

# METHOD 1: checking how many dogs in each data collection
dog_dc = aggregate(data$Data.Collection.Number, by = list(Category = data$Name), FUN = sum)
dogs_dc1 = dog_dc[dog_dc$x ==1, 'Category']
print(dogs_dc1)
length(dogs_dc1)
dogs_dc2 = dog_dc[dog_dc$x ==2, 'Category']
print(dogs_dc2)
length(dogs_dc2)
dogs_dcs = dog_dc[dog_dc$x ==3, 'Category']
print(dogs_dcs)
length(dogs_dcs)

# METHOD 2: checking how many data collection 1 and 2 there are
table(data$Data.Collection.Number)

#                            EXPLORING DC1                            #

# creating new dataframe dc1 containing data collection 1 
dc1 <- data[data$Data.Collection.Number == 1, ]
nrow(dc1) # 57 examples
table(dc1$Litter)
# removing litter with only one dog
dc1 = dc1[!(dc1$Litter == 'L' | dc1$Litter == 'T' | dc1$Litter == 'Z'),]


#                            EXPLORING DC2                            #

# creating new dataframe dc2 containing data collection 2 
dc2 <- data[data$Data.Collection.Number == 2, ]
print(dc2$Data.Collection.Number) 
nrow(dc2) # 48 examples
table(dc2$Litter)
# removing litter with only one dog
dc2 = dc2[!(dc2$Litter == 'L' | dc2$Litter == 'T' |  dc2$Litter == 'Z'),]




#                         EXPLORING DC1 AND DC2                       #

# filtering out dogs that DO NOT HAVE both dc1 and dc2
dcs = data %>% filter( Name %in% dogs_dcs)

# removing litter with only one dog
dcs_litter = subset(dcs,  !Litter %in%  c('L','M','T'))

#resetting levels in subset dataframe
dc1$Name = factor(dc1$Name)
dc1$Litter = factor(dc1$Litter)
dc2$Name = factor(dc2$Name)
dc2$Litter = factor(dc2$Litter)
dcs$Name = factor(dcs$Name)
dcs$Litter = factor(dcs$Litter)
dcs_litter$Litter = factor(dcs_litter$Litter)
dcs_litter$Name = factor(dcs_litter$Name)

fs = '20-03-10_Ethogram-Results-Significant.txt'

write('Student Ethogram Data Analysis - Statistically Significant Results' , file = fs)

write('\nSUBJECTS INCLUDED' , fs, append = T)

write('\nData Collection 1' , fs, append = T)
write(length(dc1$Name), fs, append = T)

write('\nData Collection 2' , fs, append = T)
write(nrow(dc1),fs, append = T)
write('\nSex Distribution' , fs, append = T)
write.table(table(dc1$Sex),  fs, append = T)
      
 # 55 dogs
write.table(table(dc2$Sex),fs, append = T )
table(dc1$Sex)
table(dc1$Litter)

nrow(dc2) # 46 dogs
table(dc2$Sex)
table(dc2$Litter)

# --------------------------------------------------------------------#
# --------------------------------------------------------------------#
#                 BETWEEN GROUPS/LITTER ANALYSIS                      #
# --------------------------------------------------------------------#
# --------------------------------------------------------------------#


# plot a histogram of all the variable
for (variable in ordinal){
  print(variable)
  hist(dc1[,variable], main = variable)
} 


# --------------------------------------------------------------------#
#             ORDINAL VARIABLES - HYPOTHESIS TESTING                  #
# --------------------------------------------------------------------#

# Kruskal-Wallis Test:
# testing significant differences between multiple groups 
ordinal_between_groups <- function(df){
  result = c()
  for (variable in ordinal){
      print(variable)
      r = kruskal.test(df[, variable], df$Litter)
      result = rbind(result, c(variable, r[1], r[2], r[3]))
  }
  return (result)
}

# POST-HOC Test for Kruskal-Wallis Test: 
#   pairwise comparison of groups which showed statistically significant difference
posthoc_between_groups <- function(df, variables){
  results = c()
  for (variable in variables){
    r = DunnTest(df[,variable], df$Litter, method = "bonferroni")
    results = rbind(results, c(variable,  r))
  }
  return(results)
}

write('ORDINAL VARIABLES' , file = fs, append = T)
# saves results for ALL ORDINAL-scored behaviours between litters
dc1_ordinal = ordinal_between_groups(dc1)
dc2_ordinal = ordinal_between_groups(dc2)
# saves results for SIGNIFICANTLY DIFFERENT ORDINAL-scored behaviours between litters 
dc1_ordinal_sign = dc1_ordinal[dc1_ordinal[,4]<0.05, ]
dc2_ordinal_sign = dc2_ordinal[dc2_ordinal[,4]<0.05, ]

# performs posthoc on SIGNIFICANTLY DIFFERENT ORDINAL variables
dc1_ordinal_ph = posthoc_between_groups(dc1, unlist(dc1_ordinal_sign[,1]))
dc2_ordinal_ph = posthoc_between_groups(dc2, unlist(dc2_ordinal_sign[,1]))

# saves outputs to file
write('\n\nData Collection 1 - Difference between litters', file = fs, append = T)
write.table(dc1_ordinal_sign,fs, append = T)
write('\n\nData Collection 2', file = fs, append = T)
write.table(dc2_ordinal_sign,fs, append = T )







# --------------------------------------------------------------------#
#             ORDINAL VARIABLES - FURTHER ANALYSIS                    #
# --------------------------------------------------------------------#

# Creating an overall distraction mean 
dc1$Distractions <- rowMeans(dc1[50:57])

# Average Distraction score per litter
dc1 %>% group_by(Litter) %>% summarise_at(vars(Distractions), funs(mean))

# Average Pull Strengh score per Litter
dc1 %>% group_by(Litter) %>% summarise_at(vars(Distractions.Pull.strength), funs(mean))

# Average Kong.Concentration.Response score per Litter
dc1 %>% group_by(Litter) %>% summarise_at(vars(Kong.Concentration.Response), funs(mean))



plot_ordinal <- function(df, var){
  # returns bar plot of @var in df per 'Litter'
  df = df %>% group_by(Litter) %>% summarise_at(var, funs(mean))
  barplot(df[[var]], names.arg = df[['Litter']], ylab = 'Mean score', xlab= 'Litter', main = var)
}

for (var in unlist(dc2_ordinal_sign[,1])){
  print (var)
  plot_ordinal(dc2, var)   
}


#               Visualise results from Post Hoc test using
#                       dc1_ordinal_ph[1,]
#     The vales in the result do not seem to be signficantly different
#       maybe because there are a lot of ties as the data is ordinal 
    

# --------------------------------------------------------------------#
#                            COUNT VARIABLES                          #
# --------------------------------------------------------------------#

# plot a histogram of all the variable
for (variable in count){
  print(variable)
  hist(dc1[,variable], main = variable)
} 

# HAZEL kruskal.test(data$feature, data$control)
# Testing significance of all ORDINAL variables considering GROUPS
# saves results for significantly different behaviours between litters for each dc
count_between_groups <- function(df){
  result = c()
  for (variable in count){
    r = kruskal.test(df[, variable], df$Litter)
    print(c(variable, r[3]))
    result = rbind(result, c(variable, r[1], r[2], r[3]))
  }
  return (result)
}
dc1_count = count_between_groups(dc1)
dc2_count = count_between_groups(dc2)
dc1_count_sign = dc1_count[dc1_count[,4]<0.05, ]
dc2_count_sign = dc2_count[dc2_count[,4]<0.05, ]
 
# no need to perform Post Hoc because NO variable was significantly different 

# --------------------------------------------------------------------#
#                        CATEGORICAL VARIABLES                        #
# --------------------------------------------------------------------#
# visualising barchart for categorical data
for (variable in categorical)
{
  print(variable)
  ggplot(dc1, aes(x = factor(variable)))
}

# HAZEL chiq.test(table(data$feature, data$control)
# Testing significance of all CATEGORICAL variables considering GROUPS
# saves results for significantly different behaviours between litters for each dc
categorical_between_groups <- function(df){
  result = c()
  for (variable in categorical){
    if (length(unique(df[,variable]))>1){
      r = chisq.test(df[, variable], df$Litter)
      print(c(variable, r[3]))
      result = rbind(result, c(variable, r[1], r[2], r[3]))
    }
  }
  return (result)
}

dc1_categorical = categorical_between_groups(dc1)
dc2_categorical = categorical_between_groups(dc2)
dc1_categorical_sign = dc1_categorical[dc1_categorical[,4]<0.05, ]
dc2_categorical_sign = dc2_categorical[dc2_categorical[,4]<0.05, ]


# --------------------------------------------------------------------#
#   MIXED DESIGN BETWEEN GROUPS (LITTER) AND WITHIN (DC1 VS. DC2)     #
# --------------------------------------------------------------------#
# HAZEL DC1 vs. DC2; example code I sent her
# aov_behaviour_time <- aov(behaviour ~ litter*DC + Error(dog/DC), data= your_dataset)
# using mixed design ANOVA (AOV) even though I know the data may not be appropriate... 

ordinal_within_groups <- function(df){
  r_all = c()
  r_sig = c()
  for (variable in ordinal){
    print(variable)
    r = summary(aov(df[, variable] ~ Litter*Data.Collection.Number + Error(Name/Data.Collection.Number), data = df))
    r_all = rbind(r_all, c(variable, r[[1]], r[[2]]))
    pvalues = c(unlist(r[[1]])["Pr(>F)1"],unlist(r[[2]])["Pr(>F)1"], unlist(r[[2]])["Pr(>F)2"])
    if (any(pvalues < 0.05)){
      r_sig = rbind(r_sig, c(variable, r[[1]], r[[2]]))
    }
  }
  return (r_sig)
}
ord_dcs_sig = ordinal_within_groups(dcs)

# UNDERSTAND THE OUTPU AND UNDERSTAND THE FOLLOWING:
# most of the variable result in a model with 1 factor
# while, some of them result in a model with 2 factors


# barplot of behaviour per DC
for (variable in ordinal){
  par(mfrow = c(1, 3))
  for(i in unique(dcs$Data.Collection.Number)) {
    print (i)
    barplot(table(dcs[dcs$Data.Collection.Number == i, variable]), space = 1,
         xlab = "",
         col = "gray50",
         main = paste("DC", i, variable)) 
  }
  boxplot(dcs[dcs$Data.Collection.Number == 1,variable], dcs[dcs$Data.Collection.Number == 2,variable], names = unique(dcs$Data.Collection.Number))
  #title(strwrap(descriptive, width=60), cex.main=1, font.main=1)
}


# HAZEL dunnTest(data$feature, data$control, method = 'bonferroni')
dunnTest(dc1$Familiarisation.Response..Oriented.to.Handler., dc1$Litter, method = 'bonferroni')
dc1$Body.check.General..Mouths.
dc1_ordinal <- dc1 %>% select("Litter", "Body.check.General..Mouths.", "Body.check.General..Licks.")
barplot(dc1_ordinal.data)
ggplot(data, aes(x = factor("Body.check.General..Mouths.")))

# CONGHAL 


# --------------------------------------------------------------------#
# --------------------------------------------------------------------#
#                     WITHING SUBJECT ANALYSIS                        #
# --------------------------------------------------------------------#
# --------------------------------------------------------------------#

# double check his data by regrouping dc1 and dc2 per dog side by side
# check how many dogs, what the dogs were,

# run wilcoxon for ordinal data
dcs$Data.Collection.Number
groupby(dcs, Data.Collection.Number)
# run chi-squared for categorical data

#