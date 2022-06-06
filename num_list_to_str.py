def list_to_str(list_data):
    num_to_str = {0: ":zero:",
                  1: ":one:",
                  2: ":two:",
                  3: ":three:",
                  4: ":four:",
                  5: ":five:",
                  6: ":six:",
                  7: ":seven:",
                  8: ":eight:",
                  9: ":nine:"}
    str_from_list = ""
    for i in range(len(list_data)):
        str_from_list += num_to_str[list_data[i]]
    return str_from_list
