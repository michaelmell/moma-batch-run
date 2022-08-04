#! /usr/bin/env python

from ctypes import ArgumentError
from pathlib import Path
import os
import sys
import argparse
from glob import glob
import logging

import yaml
from yaml.loader import SafeLoader

"""
This class was taken from here: https://stackoverflow.com/a/39215961
"""
class StreamToLogger(object):
    """
    Fake file-like stream object that redirects writes to a logger instance.
    """
    def __init__(self, logger, level):
       self.logger = logger
       self.level = level
       self.linebuf = ''

    def write(self, buf):
       for line in buf.rstrip().splitlines():
          self.logger.log(self.level, line.rstrip())

    def flush(self):
        pass

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

def build_arg_string(arg_list):
    return ' '.join([f'-{list(entry.keys())[0]} {list(entry.values())[0]}' if type(entry) is dict else f'-{entry}' if type(entry) is str else '' for entry in arg_list])

def add_to_or_update_arg_list(args_to_update: list, new_args: list):
    for new_arg in new_args:
        if type(new_arg) is str and new_arg not in args_to_update:
            args_to_update.append(new_arg)
        elif type(new_arg) is dict:
            new_key = list(new_arg.keys())[0]
            new_val = list(new_arg.values())[0]
            existing_keys = [list(arg.keys())[0] if type(arg) is dict else None for arg in args_to_update]
            if new_key in existing_keys:
                index = existing_keys.index(new_key)
                args_to_update[index].update({new_key: new_val})
            else:
                args_to_update.append({new_key: new_val})
    return args_to_update

def build_list_of_command_line_arguments(config, list_of_gl_paths):
    position = config['position']

    cmd_arg_lists = [list()]*len(list_of_gl_paths)
    if 'arg' in config:
        for cmd_arg_list in cmd_arg_lists:
            cmd_arg_list = add_to_or_update_arg_list(cmd_arg_list, config['arg'])
    for pos_ind in position:
        if 'arg' in position[pos_ind]:
            cmd_arg_list = position[pos_ind]['arg']
            for ind, path in enumerate(list_of_gl_paths):
                pos_string = 'Pos'+ str(pos_ind)
                if pos_string in path:
                    cmd_arg_lists[ind] = add_to_or_update_arg_list(cmd_arg_lists[ind], cmd_arg_list)
    return cmd_arg_lists

def calculate_log_file_path(yaml_config_file_path: Path):
    return Path(os.path.join(yaml_config_file_path.parent,yaml_config_file_path.stem + '.log'))

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
    parser.add_argument("-l", "--log", type=str,
                    help="path to the log-file for this batch-run; derived from 'yaml_config_file' and stored next to it, if not specified")
    parser.add_argument("yaml_config_file", type=str,
                    help="path to YAML file with dataset configuration")
    cmd_args = parser.parse_args()

    yaml_config_file_path = Path(cmd_args.yaml_config_file)
    
    if not yaml_config_file_path.exists():
        print("ERROR: Check argument 'yaml_config_file'; file not found at: {yaml_config_file_path}")
        exit(-1)

    if cmd_args.log is not None:
        log_file = Path(cmd_args.log)
    else:
        log_file = calculate_log_file_path(yaml_config_file_path)
    
    with open(log_file, 'a') as f:
        if not f.writable():
            if cmd_args.log is not None:
                print("ERROR: Check argument '-log'; cannot write to the log-file at: {cmd_args.log}")
                exit(-1)
            else:
                print("ERROR: Cannot write to the file log-file at: {cmd_args.log}")
                exit(-1)

    # instructions how to setup the logger to write to terminal can be found here:
    # https://docs.python.org/3.8/howto/logging-cookbook.html
    # and
    # https://stackoverflow.com/a/38394903
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        filename=log_file,
                        filemode='a')
    # define a new Handler to log to console as well
    console = logging.StreamHandler()
    # optional, set the logging level
    console.setLevel(logging.INFO)
    # set a format which is the same for console use
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    # tell the handler to use this format
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger('default').addHandler(console)
    logger = logging.getLogger('default')

    sys.stdout = StreamToLogger(logger, logging.INFO)
    sys.stderr = StreamToLogger(logger, logging.ERROR)
    
    with open(cmd_args.yaml_config_file) as f:
        config = yaml.load(f, Loader=SafeLoader)

    gl_directory_paths = build_list_of_gl_directory_paths(config)
    gl_tiff_paths = build_list_of_gl_tiff_file_paths(gl_directory_paths)
    cmd_arg_lists = build_list_of_command_line_arguments(config, gl_directory_paths)

    print("START BATCH RUN.")
    for tiff_path, gl_directory_path, arg_list in zip(gl_tiff_paths, gl_directory_paths, cmd_arg_lists):
        current_arg_list = arg_list.copy()
        if cmd_args.track:
            current_arg_list.append('headless')
            current_arg_list.append('trackonly')
        elif cmd_args.curate:
            analysisName = current_arg_list.pop('analysis', None)
            if not analysisName: raise ArgumentError("Argument 'analysis' is not set for running curation.")
            current_arg_list = {'reload': gl_directory_path, 'analysis': analysisName}  # for running the curation we only need the GL directory path and the name of the analysis
        elif cmd_args.export:
            analysisName = current_arg_list.pop('analysis', None)
            if not analysisName: raise ArgumentError("Argument 'analysis' is not set for running curation.")
            current_arg_list = {'headless':None, 'reload': gl_directory_path, 'analysis': analysisName}  # for running the curation we only need the GL directory path and the name of the analysis
            pass
        args_string = build_arg_string(current_arg_list)
        moma_command = f'moma {args_string} -i {tiff_path}'
        print("RUN MOMA: " + moma_command)
        os.system(moma_command)
        # os.system(f"moma --headless -p {mmproperties_path} -i {tiff} -o {output_folder}  2>&1 | tee {moma_log_file}")  # this would output also MoMA output to the log file:
        print("FINISHED MOMA.")
    print("FINISHED BATCH RUN.")

if __name__ == "__main__":
    __main__()