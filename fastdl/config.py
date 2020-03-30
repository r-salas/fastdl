#
#
#   Configuration variables
#
#


def merge(*dicts):
    merged_dict = {}
    for d in dicts:
        for key, val in d.items():
            merged_dict[key] = val

    return merged_dict


default_conf = {
    "default_dir_prefix": "."
}


conf = merge(default_conf)
