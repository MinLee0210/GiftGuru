import yaml

def yaml_read(dir): 
    with open(dir) as f:
        my_dict = yaml.safe_load(f)
    return my_dict