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


def __main__():
    # Open the file and load the file
    with open('tracking_config_test_1.yaml') as f:
        config = yaml.load(f, Loader=SafeLoader)
        # print(config)

    gl_directory_paths = build_list_of_gl_directory_paths(config)
    gl_tiff_paths = build_list_of_gl_tiff_file_paths(gl_directory_paths)

    # [print(path) for path in gl_directory_paths]
    [print(path) for path in gl_tiff_paths]

    # input_path = config['path']
    # for res in os.walk(input_path):
    #     print(res[0])
    # print("bla1")
    print("Finished.")

__main__()