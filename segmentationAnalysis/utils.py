import copy

# Dict & Ds Keys Adapating ---
def adapt_dict_keys(src_dict:dict, keys_to_adapt:list[str], respective_new_keys:list[str], should_del_other_keys:bool=False):
    adapted_dict = {} if should_del_other_keys else copy.deepcopy(src_dict)
    
    for i, key_to_adapt in enumerate(keys_to_adapt):
        adapted_key = respective_new_keys[i]
        adapted_dict[adapted_key] = src_dict[key_to_adapt]
        
    return adapted_dict

def bubble_sort_dicts_based_on_property(_dict, propertyExpression):
    result = list(zip([*_dict.keys()],[*_dict.values()]))
    
    updates_in_this_iteration = True
    while updates_in_this_iteration:
        updates_in_this_iteration = False
        
        for i in range(len(result)-1):
            if eval(f"result[{i}][1]{propertyExpression}") > eval(f"result[{i+1}][1]{propertyExpression}"):
                updates_in_this_iteration = True
                
                buff = result[i+1]
                result[i+1] = result[i]
                result[i] = buff
                
    return result
    
# Math ---
def divide_smaller_by_larger(x,y):
    larger = max(x, y)
    smaller = min(x, y)
    return smaller / larger