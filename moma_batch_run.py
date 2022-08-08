#! /usr/bin/env python

from ctypes import ArgumentError
import json
from pathlib import Path
from datetime import datetime
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
    input_path = config['preprocessing_path']
    position = config['pos']

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

class AnalysisMetadata(object):
    def __init__(self, path: Path):
        assert(type(path) is Path, f'path is not of type Path')
        self.__path = path
        if path.exists():
            with open(path, 'r') as fp:
                self.value_dict = json.load(fp)
        else:
            self.value_dict = {'file_version': '0.1.0',
            'created': datetime.now(),
            'tracked': False,
            'curated': False}
            self.save()
        
    @property
    def path(self):
        return self.__path
    
    @property
    def tracked(self):
        return self.value_dict['tracked']

    @tracked.setter
    def tracked(self, val):
        self.value_dict['tracked'] = val
        self.save()

    @property
    def curated(self):
        return self.value_dict['curated']

    @curated.setter
    def curated(self, val):
        self.value_dict['curated'] = val
        self.save()

    def save(self):
        with open(self.path, 'w') as fp:
            json.dump(self.value_dict, fp, default=str)  # default=str is needed for the serialization of datetime object

class GlFileManager(object):
    def __init__(self, gl_directory_path, analysisName):
        self.gl_directory_path = gl_directory_path
        self.analysisName = analysisName

    def get_gl_export_data_path(self) -> Path:
        return Path(os.path.join(self.gl_directory_path, self.analysisName, self.analysisName+'__export_data'))

    def get_gl_track_data_path(self) -> Path:
        path = Path(os.path.join(self.gl_directory_path, self.analysisName, self.analysisName+'__track_data'))
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
        return path

    def get_gl_is_curated(self) -> bool:
        return self.__get_analysis_metadata().curated

    def get_gl_is_tracked(self):
        return self.__get_analysis_metadata().tracked
    
    def set_gl_is_tracked(self):
        self.__get_analysis_metadata().tracked = True
    
    def __get_analysis_metadata(self) -> AnalysisMetadata:
        return AnalysisMetadata(self.get_analysis_meta_data_path())

    def get_analysis_meta_data_path(self) -> Path:
        return Path(os.path.join(self.get_gl_track_data_path(), 'analysis_metadata.json'))

    def get_analysis_name(self):
        return self.analysisName

    def set_gl_is_curated(self):
        self.__get_analysis_metadata().tracked = True  # TODO-MM-20220808: this will be the case, if we were able to curate the GL; I add this here to handle GLs that we tracked, before implementing the use of `analysis_metadata.json`
        self.__get_analysis_metadata().curated = True

def build_list_of_command_line_arguments(config, list_of_gl_paths):
    position = config['pos']

    cmd_args_dict_list = [{}]*len(list_of_gl_paths)
    if 'default_moma_arg' in config:
        for arg_dict in cmd_args_dict_list:
            arg_dict.update(config['default_moma_arg'])
    for pos_ind in position:
        if 'moma_arg' in position[pos_ind]:
            arg_dict = position[pos_ind]['moma_arg']
            for ind, path in enumerate(list_of_gl_paths):
                pos_string = 'Pos'+ str(pos_ind)
                if pos_string in path:
                    cmd_args_dict_list[ind].update(arg_dict)
    return cmd_args_dict_list

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
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('default').addHandler(console)
    logger = logging.getLogger('default')
    sys.stdout = StreamToLogger(logger, logging.INFO)
    sys.stderr = StreamToLogger(logger, logging.ERROR)

    with open(cmd_args.yaml_config_file) as f:
        config = yaml.load(f, Loader=SafeLoader)

    logger.info("START BATCH RUN.")
    batch_operation_type = 'TRACK' if cmd_args.track else 'CURATE' if cmd_args.curate else 'EXPORT' if cmd_args.export else 'UNDEFINED ERROR'
    logger.info(f"Run type: {batch_operation_type}")
    batch_command_string = ' '.join(sys.argv)
    logger.info(f"Command: {batch_command_string}")
    
    gl_directory_paths = build_list_of_gl_directory_paths(config)
    gl_tiff_paths = build_list_of_gl_tiff_file_paths(gl_directory_paths)
    cmd_args_dict_list = build_list_of_command_line_arguments(config, gl_directory_paths)

    for tiff_path, gl_directory_path, args_dict in zip(gl_tiff_paths, gl_directory_paths, cmd_args_dict_list):
        current_args_dict = args_dict.copy()
        
        if 'analysis' not in current_args_dict:
            raise ArgumentError("Value for 'analysis' is not set for running curation.")
        else:
            analysisName = current_args_dict['analysis']

        gl_file_manager = GlFileManager(gl_directory_path, analysisName)

        if gl_file_manager.get_gl_export_data_path().exists():
            logger.warning(f"Will not perform operation {batch_operation_type} for this GL, because it was already exported analysis: {gl_file_manager.get_gl_export_data_path()}")
            continue

        if cmd_args.track:
            current_args_dict.update({'headless':None, 'trackonly':None})
            if not gl_file_manager.get_gl_is_tracked():
                run_moma_and_log(logger, tiff_path, current_args_dict)
                gl_file_manager.set_gl_is_tracked()
            else:
                logger.warning(f"Will not perform operation {batch_operation_type} for this GL, because it was already tracked for this analysis: {gl_file_manager.get_gl_track_data_path()}")
        elif cmd_args.curate:
            current_args_dict = {'reload': gl_directory_path, 'analysis': gl_file_manager.get_analysis_name()}  # for running the curation we only need the GL directory path and the name of the analysis
            if not gl_file_manager.get_gl_is_curated():
                run_moma_and_log(logger, tiff_path, current_args_dict)
                gl_file_manager.set_gl_is_curated()
        elif cmd_args.export:
            current_args_dict = {'headless':None, 'reload': gl_directory_path, 'analysis': gl_file_manager.get_analysis_name()}  # for running the curation we only need the GL directory path and the name of the analysis
            run_moma_and_log(logger, tiff_path, current_args_dict)
    logger.info("FINISHED BATCH RUN.")

def run_moma_and_log(logger, tiff_path, current_args_dict):
    args_string = build_arg_string(current_args_dict)
    moma_command = f'moma {args_string} -i {tiff_path}'
    logger.info("RUN MOMA: " + moma_command)
    os.system(moma_command)
    # os.system(f"moma --headless -p {mmproperties_path} -i {tiff} -o {output_folder}  2>&1 | tee {moma_log_file}")  # this would output also MoMA output to the log file:
    logger.info("FINISHED MOMA.")

if __name__ == "__main__":
    __main__()