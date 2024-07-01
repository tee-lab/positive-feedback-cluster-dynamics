library(reticulate)
library(spatialwarnings)

results_path = "C://Code//Github//positive-feedback-cluster-dynamics//results"

# model = "tdp"
model = "scanlon"

# dataset = "256x256_64"
dataset = "256x256_64_8_24"

options(spatialwarnings.constants.reltol = 1e-8)
options(spatialwarnings.constants.maxit = 1e8)

# p_values = c("0p618", "0p62", "0p625", "0p63", "0p64", "0p65", "0p68", "0p7", "0p72", "0p74")
# q_value = "0"

# p_values = c("0p5", "0p505", "0p51", "0p52", "0p53", "0p535", "0p54", "0p55", "0p56")
# q_value = "0q5"

root_path = file.path(results_path, model, dataset)
data_frame = data.frame()

rainfall_values = c("300", "400", "500", "600", "770")
# rainfall_values = c("300", "400", "500", "600", "700", "770", "800", "830", "850", "900")

if (model == "tdp") {
  values = p_values
} else {
  values = rainfall_values
}

root_path = file.path(results_path, model, dataset)

for (p in values) {
  print(paste("<--- Analyzing", p, "--->"))
  
  if (model == "tdp") {
    folder_name = paste(model, p, q_value, sep="_")
  }
  else {
    folder_name = paste(model, p, sep="_")
  }
  
  file_name = paste(folder_name, "lattices.pkl", sep="_")
  file_path = file.path(root_path, folder_name, file_name)
  source_python("lattice_parser.py")
  lattices = load_lattices(file_path)
  
  psd_object = patchdistr_sews(lattices, best_by = "BIC", fit_lnorm = FALSE, merge = TRUE, wrap = TRUE)
  psd_stats = psd_object$psd_type
  
  psd_plot = plot_distr(psd_object, best_only = FALSE)
  
  if (model == "tdp") {
    png(filename=paste(p, "_", q_folder, ".png", sep = ""))
  } else {
    png(filename=paste(p, ".png", sep = ""))
  }
  
  plot(psd_plot)
  dev.off()
  
  pl_bic = psd_stats$BIC[1]
  tpl_bic = psd_stats$BIC[2]
  exp_bic = psd_stats$BIC[3]
  
  pl_expo = psd_stats$plexpo[1]
  exp_trunc = psd_stats$cutoff[3]
  tpl_expo = psd_stats$plexpo[2]
  tpl_trunc = psd_stats$cutoff[2]
  
  print(paste("Power law BIC:", pl_bic))
  print(paste("TPL BIC:", tpl_bic))
  print(paste("Exp BIC:", exp_bic))
  
  if (model == "tdp") {
    p_float = as.double(gsub("p", ".", p))
  } else {
    p_float = as.integer(p)
  }
  
  data_frame = rbind(data_frame, c(p_float, pl_bic, tpl_bic, exp_bic, pl_expo, exp_trunc, tpl_expo, tpl_trunc))
}

if (model == "tdp") {
  colnames(data_frame)[1] = "p"
} else {
  colnames(data_frame)[1] = "rainfall"
}

colnames(data_frame)[2] = "PL"
colnames(data_frame)[3] = "TPL"
colnames(data_frame)[4] = "Exp"
colnames(data_frame)[5] = "PL expo"
colnames(data_frame)[6] = "Exp trunc"
colnames(data_frame)[7] = "TPL expo"
colnames(data_frame)[8] = "TPL trunc"

data_frame[is.na(data_frame)] = 0

if (model == "tdp") {
  write.csv(data_frame, paste(q_value, "_tdp_csd", ".csv", sep=""))
} else {
  write.csv(data_frame, paste("scanlon_csd", ".csv", sep=""))
}
