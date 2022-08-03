import yaml
from yaml.loader import SafeLoader
import os

def get_tiff_filename(gl_path):
    pass

def build_list_of_gls(config):
    input_path = config['path']
    position = config['position']

    gls=[]
    for pos in position:
        gl_path=input_path
        # print(pos)
        print(position[pos])
        gl_path+=("/Pos"+str(pos))
        # pos_name=f"Pos{position[pos]}"
        # print(pos_name)
        if position[pos]:
            for gl in position[pos]['gl']:
                gl_path+=("/Pos"+str(pos)+"_"+"GL"+str(gl))
                # print(gl_path)
                filename = get_tiff_filename(gl_path)
                # print(gl)
    pass

def __main__():
    # Open the file and load the file
    with open('tracking_config_1.yaml') as f:
        config = yaml.load(f, Loader=SafeLoader)
        print(config)

    gl_list = build_list_of_gls(config)

    # input_path = config['path']
    # for res in os.walk(input_path):
    #     print(res[0])
    # print("bla1")
    print("Finished.")

__main__()