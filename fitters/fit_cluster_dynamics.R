#
# This file includes modifications by Alex
#

calc_bic <- function(fit_output, data_len) {
  bic = fit_output$npars * log(data_len) - 2 * (fit_output$ll)
  return(bic)
}


# This function will fit the three distributions to a tabulated set of change
# sizes (dS).
# dS is the change in size, tabulated data is the number of time each dS
# occurs. They must be vectors of the same length
fit_distrs <- function(dS, tabulated_data) {
  if ( all(diff(tabulated_data) < 0) ) {
    warning("Make sure your data is not the inverse cumulative function, i.e. N(dS>=k) instead of N(dS=k)")
  }
  
  # Create a (very long) vector containing raw occurrences
  raw_occurrences <- unlist(lapply(seq_along(dS), function(i) {
    rep(dS[i], tabulated_data[i])
  }))
  
  print(paste("Length of samples", length(raw_occurrences)))
  
  # Your distributions do not start at 0, so use an xmin here. This is
  # important to get the normalization constants of the distributions right
  xmin <- min(dS)
  
  # Fit exponential, PL, TPL with proper xmin
  expfit <- exp_fit(raw_occurrences, xmin = xmin)
  print("exp fit done")
  
  plfit <- pl_fit(raw_occurrences, xmin = xmin)
  print("pl fit done")
  
  if (fit_tpl) {
    tplfit <- tpl_fit(raw_occurrences, xmin = xmin)
    print("tpl fit done")
  }
  
  # Predict response. Here we use spatialwarnings internal functions, see
  # provided fitpsd.R code if you want to have the details.
  exp_probs <- spatialwarnings:::ddisexp(dS, expfit[["cutoff"]], xmin = xmin)
  exp_cprobs <- spatialwarnings:::ipdisexp(dS, expfit[["cutoff"]], xmin = xmin)
  
  pl_probs <- spatialwarnings:::dpl(dS, plfit[["plexpo"]], xmin = xmin)
  pl_cprobs <- spatialwarnings:::ippl(dS, plfit[["plexpo"]], xmin = xmin)
  
  if (fit_tpl) {
    options(spatialwarnings.constants.maxit = 1e3)
    tpl_probs <- spatialwarnings:::dtpl(dS,tplfit[["plexpo"]], tplfit[["cutoff"]], xmin = xmin)
    tpl_cprobs <- spatialwarnings:::iptpl(dS, tplfit[["plexpo"]], tplfit[["cutoff"]], xmin = xmin)
  }
  
  # Put predictions in df
  # column p contains the probabilities (P(x=k)), ip the inverse cumulative
  # probs (P(x>=k)).
  predictions <- rbind(
    data.frame(psdtype = "pl",  dS = dS, p = pl_probs, ip = pl_cprobs),
    data.frame(psdtype = "exp", dS = dS, p = exp_probs, ip = exp_cprobs)
  )
  if (fit_tpl) {
    predictions <- rbind(predictions, data.frame(psdtype = "tpl", dS = dS, p = tpl_probs, ip = tpl_cprobs))
  }
  
  # Put fits in list object
  if (fit_tpl) {
    fits <- list(exp = expfit, pl = plfit, tpl = tplfit)
  }
  else {
    fits <- list(exp = expfit, pl = plfit)
  }
  
  # Compute observed distribution. p contains the probabilities (P(x=k)),
  # ip the inverse cumulative probs (P(x>=k)).
  obs <- data.frame(dS = dS,
                    p = tabulated_data / sum(tabulated_data),
                    ip = sapply(dS, function(x) sum(tabulated_data[dS >= x]) / sum(tabulated_data) ) )
  
  # Return everything
  list(predictions = predictions,
       fits = fits,
       obs = obs)
}

# Compute the inverse cumulative distribution of a set of values
inv_cumu_distr <- function(xvals, yvals) {
  cdistr <- sapply(xvals, function(x) yvals[xvals >= x] / sum(yvals) )
  # Normalize
  data.frame(x = xvals, y = cdistr)
}

library(ggplot2)
library(reticulate)
library(spatialwarnings)

results_path <- "..//results"

model = "tdp"
# model = "scanlon"

dataset = "256x256_64"
# dataset = "256x256_64_8_24"

fit_tpl = TRUE

# options(spatialwarnings.constants.reltol = 1e-4)

# p_values = c("0p618")
# p_values = c("0p618", "0p62", "0p625", "0p63", "0p64", "0p65", "0p68", "0p7", "0p72", "0p74")
# q_value = "0"

# p_values = c("0p5", "0p505", "0p51", "0p52", "0p53", "0p535", "0p54", "0p55", "0p56")
# q_value = "0q5"

p_values = c("0p282", "0p2825", "0p283", "0p2835", "0p284", "0p2845", "0p285")
q_value = "0q92"

# rainfall_values = c("300")
# rainfall_values = c("300", "400", "500", "600", "700", "770", "800" , "850", "900")

if (model == "tdp") {
  values = p_values
} else {
  values = rainfall_values
}

root_path = file.path(results_path, model, dataset)
data_frame = data.frame()

for (p in values) {
  if (model == "tdp") {
    p_float = as.double(gsub("p", ".", p))
  } else {
    p_float = as.integer(p)
  }
  
  print(paste("<--- Analyzing", p, "--->"))
  
  # load data
  
  if (model == "tdp") {
    folder_name = paste(model, p, q_value, sep="_")
  } else {
    folder_name = paste(model, p, sep="_")
  }
  
  file_name = paste(folder_name, "_cd.txt", sep="")
  file_path = file.path(root_path, folder_name, file_name)
  source_python("dynamics_parser.py")
  changes_distr = load_changes(file_path)
  
  # format data
  x_start = 3 # remove first two points corresponding to ds = 0, and ds = +/- 1
  x_range = x_start:length(changes_distr)
  changes_distr = changes_distr[x_start:length(changes_distr)]
  data_len = length(changes_distr)
  
  # What to the changes in changes_icdf correspond to?
  dS <- x_range - 1 # the true dS values corresponding to observations
  # it starts at 2 because we remove 0 and +/- 1 (?)
  
  print("Load complete")
  
  # Fit distributions
  distribs <- fit_distrs(dS, changes_distr)
  
  # Display
  require(ggplot2)
  
  # Show inverse cumulative distribution
  ggplot(NULL) +
    geom_point(aes(x = dS, y = ip),
               data = subset(distribs[["obs"]], ip > 0)) +
    geom_line(aes(x = dS, y = ip, color = psdtype),
              data = distribs[["predictions"]]) +
    scale_y_continuous(trans = "log10") + # comment to remove log scale
    scale_x_continuous(trans = "log10") +
    labs(x = "dS", y = "P(x>=dS)")
  
  if (model == "tdp") {
    ggsave(filename=paste("..//outputs//", folder_name  ,"_icdf.png", sep=""))
  } else {
    ggsave(filename=paste("..//outputs//", p, "_icdf.png", sep=""))
  }
  
  # Show probability distribution
  ggplot(NULL) +
    geom_point(aes(x = dS, y = p),
               data = subset(distribs[["obs"]], p > 0)) +
    geom_line(aes(x = dS, y = p, color = psdtype),
              data = distribs[["predictions"]]) +
    scale_y_continuous(trans = "log10") +
    scale_x_continuous(trans = "log10") +
    labs(x = "dS", y = "P(x=dS)")
  
  if (model == "tdp") {
    ggsave(filename=paste("..//outputs//", folder_name, "_pdf.png", sep=""))
  } else {
    ggsave(filename=paste("..//outputs//", p, "_pdf.png", sep=""))
  }
  
  # Extract bic for every fit. Note that the BIC takes the number of
  # observations, not the length of the vector in which you stored the
  # number of obs for each dS.
  n_obs <- sum(changes_distr)
  BICs <- c(p_float, 
            calc_bic(distribs[["fits"]][["pl"]], n_obs),
            calc_bic(distribs[["fits"]][["exp"]], n_obs)
  )
  if (fit_tpl) {
    BICs = append(BICs, calc_bic(distribs[["fits"]][["tpl"]], n_obs))
  }
  
  params <- c(distribs[["fits"]][["pl"]]$plexpo,
              distribs[["fits"]][["exp"]]$cutoff
  )
  if (fit_tpl) {
    tpl_fit_data = distribs[["fits"]][["tpl"]]
    params = append(params, c(tpl_fit_data$plexpo, tpl_fit_data$cutoff))
  }
  all_data = append(BICs, params)
  
  if (fit_tpl) {
    print(paste("BICs (pl/exp/tpl): ", BICs[2], BICs[3], BICs[4]))
  }
  else {
    print(paste("BICs (pl/exp): ", BICs[2], BICs[3]))
  }
  
  # append to data frame
  data_frame <- rbind(data_frame, all_data)
}

if (model == "tdp") {
  colnames(data_frame)[1] = "p"
} else {
  colnames(data_frame)[1] = "rainfall"
}

colnames(data_frame)[2] = "PL BIC"
colnames(data_frame)[3] = "Exp BIC"

if (fit_tpl) {
  colnames(data_frame)[4] = "TPL BIC"
  next_index = 5
} else {
  next_index = 4
}

colnames(data_frame)[next_index] = "PL expo"
colnames(data_frame)[next_index + 1] = "Exp trunc"
if (fit_tpl) {
  colnames(data_frame)[next_index + 2] = "TPL expo"
  colnames(data_frame)[next_index + 3] = "TPL trunc"
}

# save BIC values as CSV
if (model == "tdp") {
  write.csv(data_frame, paste("..//outputs//", q_value, "_cd", ".csv", sep=""))
} else {
  write.csv(data_frame, paste("..//outputs//", "scanlon_cd", ".csv", sep=""))
}

