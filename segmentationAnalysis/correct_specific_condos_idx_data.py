import json

# Cofig
idxs_to_replace = [1, 2]

data_to_update_f_name = "all_trees_Optimal_Kmeans_K_search_3"
data_to_update_f_path = r"C:\Users\lince\Documents\Projects\Analista_De_Aborizacao\Analista V.6\News\program" + "\\" + data_to_update_f_name + ".txt"

data_to_replace_f_name = "..."
data_to_replace_f_path = r"C:\Users\lince\Documents\Projects\Analista_De_Aborizacao\Analista V.6\News\program" + "\\" + data_to_replace_f_name + ".txt"

f_to_save_changes_name = data_to_update_f_name + "_corrected_data.txt"




# Data To Update ---
# data_to_update_f = open(data_to_update_f_name, "r")
# data = eval(data_to_update_f.read())
# data_to_update_f.close()

data_to_update = {
    "a": [0, 1, 2],
    "b": [0, 1, 2]
}


# Data To Replace ---
# data_to_replace_f = open(data_to_replace_f_path, "r")
# data = eval(data_to_replace_f.read())
# data_to_replace_f.close()

data_to_replace = {
    "a": [100, 200],
    "b": [50, 666]
}


# Replacing ---
for key in data_to_update.keys():
    for idx, idx_to_replace in enumerate(idxs_to_replace):
        data_to_update[key][idx_to_replace] = data_to_replace[key][idx]
        

# Saving ---
file_to_save = open(f_to_save_changes_name, "w")

file_to_save.write(json.dumps(data_to_update, indent=1))
file_to_save.close()