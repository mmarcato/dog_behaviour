# cols by subtests in the behaviour test

info = c(
  'Dog.code', 
  'Data.Collection.Date', 
  'Data.Collection.Number', 
  'Sex', 
  'Litter', 
  'Status', 
  'Assessor')
familiarisation = c(
  'Familiarisation-Response [Oriented to Handler]', 
  'Familiarisation-Response [Exploration]',
  'Familiarisation-Response [Waiting]')
callback = c('Call Back Response')
walking = c(
  'Walking-Distractibility',
  'Walking-Pull on leash',
  'Walking-Pull strength',
  'Walking-Initiative')
standing = c(
  'Standing-Attempts ', 
  'Standing-Response')
sitting = c(
  'Sitting-Attempts', 
  'Sitting-Response')
lying = c(
  'Lying-Attempts', 
  'Lying-Response', 
  'Lying-Settled')
bodycheck = c(
  'Body check-Response', 
  'Body check-General [Mouths]', 
  'Body check-General [Licks]')
teatowel = c(
  'Tea Towel-First Response [Indifferent]', 
  'Tea Towel-First Response [Turns head]',
  'Tea Towel-First Response [Attempts to/Removes towel by moving]',
  'Tea Towel-First Response [Attempts to/Removes towel with mouth]',
  'Tea Towel-First Response [Plays]',
  'Tea towel-Second Response [Indifferent]',
  'Tea towel-Second Response [Turns head]',
  'Tea towel-Second Response [Attempts to/Removes towel by moving]',
  'Tea towel-Second Response [Attempts to/Removes towel with mouth]',
  'Tea towel-Second Response [Plays]')
distractions = c(
  'Distractions-First Response [Object]',
  'Distractions-First Response [Human]',
  'Distractions-First Response [Car]',
  'Distractions-First Response [Food]',
  'Distractions-Second Response [Object]',
  'Distractions-Second Response [Human]',
  'Distractions-Second Response [Car]',
  'Distractions-Second Response [Food]',
  'Distractions-Pull on leash',
  'Distractions-Pull strength')
kong = c(
  'Kong-Concentration-Response ',
  'Kong-Retrieve-Lateralisation',
  'Kong-Retrieve-Response to stimulus',
  'Kong-Retrieve-Response to assessor',
  'Kong-Retrieve-Back')
dogdist = c(
  'Dog-Response',
  'Dog-Call Back Response')
crate = c(
  'Crate-Entering',
  'Crate-Behaviours [Relaxing]',
  'Crate-Behaviours [Sniffing/Exploring ]',
  'Crate-Behaviours [Attention Seeking]',
  'Crate-Behaviours [Digging]',
  'Crate-Behaviours [Licking/Mouthing]',
  'Crate-Behaviours [Whining]',
  'Crate-Behaviours [Barking]',
  'Crate-Response',
  'Crate-Urinating')
# this only evaluates the trainers
petting = c(
  'Petting-Stimulus',
  'Petting-Holding dog')
isolation = c(
  'Isolation-Response [Time oriented]',
  'Isolation-Response [Exploration]',
  'Isolation-Response [Unsettled/Locomotion]',
  'Isolation-Response [Whining]',
  'Isolation-Response [Barking]',
  'Isolation-Urinating')
behaviours = c(
  'Short.Barks.Count',
  'Continuous.Barks.Duration',
  'Continuous.Barks.Count',
  'Whines.Duration',
  'Whines.Count',
  'Shakes.Count',
  'Jumps.Count')


all = c(info, familiarisation, walking, standing, sitting, lying, 
        bodycheck, teatowel, distractions, kong, dogdist, crate, petting, isolation,behaviours)
