#! /usr/bin/env python
from ctypes import ArgumentError
import os
import functools
import argparse
from glob import glob

import yaml
from yaml.loader import SafeLoader

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

def build_arg_string(arg_dict):
    return ' '.join([f'-{key} {arg_dict[key]}' if arg_dict[key] is not None or '' else f'-{key}' for key in arg_dict])

def build_list_of_command_line_arguments(config, list_of_gl_paths):
    position = config['position']

    cmd_args_dict_list = [{}]*len(list_of_gl_paths)
    if 'arg' in config:
        for arg_dict in cmd_args_dict_list:
            arg_dict.update(config['arg'])
    for pos_ind in position:
        if 'arg' in position[pos_ind]:
            arg_dict = position[pos_ind]['arg']
            for ind, path in enumerate(list_of_gl_paths):
                pos_string = 'Pos'+ str(pos_ind)
                if pos_string in path:
                    cmd_args_dict_list[ind].update(arg_dict)
                    # cmd_args_list[ind] = build_arg_string(arg_dict)
    return cmd_args_dict_list

def __main__():
    parser = argparse.ArgumentParser()
    group = parser.add_argument_group('required (mutually exclusive) arguments')
    mxgroup = group.add_mutually_exclusive_group(required=True)
    mxgroup.add_argument("-track", "--track", action='store_true',
                    help="perform headless batch-tracking of GLs")
    mxgroup.add_argument("-curate", "--curate", action='store_true',
                    help="perform interactive curation of GLs")
    mxgroup.add_argument("-export", "--export", action='store_true',
                    help="perform headless export of tracking results")
    parser.add_argument("yaml_config_file", type=str,
                    help="path to YAML file with dataset configuration")
    cmd_args = parser.parse_args()

    # Open the file and load the file
    with open(cmd_args.yaml_config_file) as f:
        config = yaml.load(f, Loader=SafeLoader)

    gl_directory_paths = build_list_of_gl_directory_paths(config)
    gl_tiff_paths = build_list_of_gl_tiff_file_paths(gl_directory_paths)
    cmd_args_dict_list = build_list_of_command_line_arguments(config, gl_directory_paths)

    for tiff_path, gl_directory_path, args_dict in zip(gl_tiff_paths, gl_directory_paths, cmd_args_dict_list):
        current_args_dict = args_dict.copy()
        if cmd_args.track:
            current_args_dict.update({'headless':None, 'trackonly':None})
        elif cmd_args.curate:
            analysisName = current_args_dict.pop('analysis', None)
            if not analysisName: raise ArgumentError("Argument 'analysis' is not set for running curation.")
            current_args_dict = {'reload': gl_directory_path, 'analysis': analysisName}  # for running the curation we only need the GL directory path and the name of the analysis
        elif cmd_args.export:
            analysisName = current_args_dict.pop('analysis', None)
            if not analysisName: raise ArgumentError("Argument 'analysis' is not set for running curation.")
            current_args_dict = {'headless':None, 'reload': gl_directory_path, 'analysis': analysisName}  # for running the curation we only need the GL directory path and the name of the analysis
            pass
        args_string = build_arg_string(current_args_dict)
        moma_command = f'moma {args_string} -i {tiff_path}'
        print(moma_command)
        os.system(moma_command)
        # os.system(f"moma --headless -p {mmproperties_path} -i {tiff} -o {output_folder}  2>&1 | tee {moma_log_file}")

    # input_path = config['path']
    # for res in os.walk(input_path):
    #     print(res[0])
    # print("bla1")
    print("Finished.")

if __name__ == "__main__":
    __main__()