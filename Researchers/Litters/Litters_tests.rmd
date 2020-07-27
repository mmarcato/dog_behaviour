posthoc_diff_groups <- function(df_ph){
  # list of variable names to be analysed
  vars = unlist(dc2_ordinal_ph[,1])
  # looping through all variables
  for (n in 1:length(dc2_ordinal_ph[,1])){    
    df_result = dc2_ordinal_ph[,2][1][[1]] 
    var_names = row.names(df_result) <- df_result[,"pval"]!=1.0
    cat(n, vars[n], var_names, "\n")
  }
}
posthoc_diff_groups(dc2_ordinal_ph)