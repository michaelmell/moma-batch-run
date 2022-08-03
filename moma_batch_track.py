from glob import glob
import yaml
from yaml.loader import SafeLoader
import os

def build_list_of_gl_directory_paths(config):
    input_path = config['path']
    position = config['position']

    gl_paths=[]
    for pos in position:
        get_gl_paths_for_position(input_path, position, gl_paths, pos)
    return gl_paths

"""
This method caluclates the paths to the GL directories.
"""
def get_gl_paths_for_position(input_path, position, gl_paths, pos):
    if position[pos]: # GLs are defined for this position; iterate over them to generate list of paths
        for gl in position[pos]['gl']:
            gl_path=input_path
            gl_path+=("/Pos"+str(pos))
            gl_path+="/Pos"+str(pos)+"_"+"GL"+str(gl)
            gl_paths.append(gl_path)

def build_list_of_gl_tiff_file_paths(gl_directory_paths: list):
    gl_tiff_paths = []
    for path in gl_directory_paths:
        tiff_path = glob(path+'/*[0-9].tif')[0]
        gl_tiff_paths.append(tiff_path)
    return gl_tiff_paths

def build_arg_string(arg_dicts):
    return ' '.join([f'-{key} {arg_dict[key]}' for arg_dict in arg_dicts for key in arg_dict])

def build_list_of_command_line_arguments(config, list_of_gl_paths):
    position = config['position']

    cmd_args_list = ['']*len(list_of_gl_paths)
    for pos_ind in position:
        if 'arg' in position[pos_ind]:
            arg_dict = position[pos_ind]['arg']
            for ind, path in enumerate(list_of_gl_paths):
                pos_string = 'Pos'+ str(pos_ind)
                if pos_string in path:
                    cmd_args_list[ind] = build_arg_string(arg_dict)
    return cmd_args_list

def __main__():
    # Open the file and load the file
    with open('tracking_config_test_1.yaml') as f:
        config = yaml.load(f, Loader=SafeLoader)
        # print(config)

    gl_directory_paths = build_list_of_gl_directory_paths(config)
    gl_tiff_paths = build_list_of_gl_tiff_file_paths(gl_directory_paths)
    cmd_arguments = build_list_of_command_line_arguments(config, gl_directory_paths)

    # [print(path) for path in gl_directory_paths]
    # [print(path) for path in gl_tiff_paths]

    for tiff_path, args in zip(gl_tiff_paths, cmd_arguments):
        print(f'moma {args} -i {tiff_path}')

    # input_path = config['path']
    # for res in os.walk(input_path):
    #     print(res[0])
    # print("bla1")
    print("Finished.")

__main__()