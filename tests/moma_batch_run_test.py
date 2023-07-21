# import unittest
import logging
from pathlib import Path
import sys
import pytest

from moma_batch_run import GlFileManager, MomaSlurmRunner, SlurmHeaderProvider

def setup_function(function):
    print("setting up failed for: ", function)

_default_header_header = """#SBATCH --mem=16G
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --qos=1day
"""

class TestSlurmHeaderProvider():
    def test__init_without_path_argument_uses_default_header_file(self):
        expected = Path.home() / ".moma" / "batch_run_slurm_header.txt"
        sut = SlurmHeaderProvider()
        assert sut.slurm_header_file == expected

    def test__init_with_existing_header_file_path_uses_the_path(self):
        expected = Path("./test_data/temporary_test_batch_run_slurm_header.txt")
        expected.touch()
        sut = SlurmHeaderProvider(expected)
        expected.unlink()
        assert sut.slurm_header_file == expected

    def test__init_with_non_existent_file__raises_argument_error(self):
        expected = Path("./test_data/non_existent_batch_run_slurm_header.txt")
        with pytest.raises(IOError):
            sut = SlurmHeaderProvider(expected)

    def test__slurm_header__return_correct_value(self):
        expected = _default_header_header
        
        sut = SlurmHeaderProvider()
        assert expected == sut.slurm_header

class TestSlurmRunner():
    arg_dict = {'p': '/home/micha/Documents/01_work/15_moma_notes/02_moma_development/feature/20220801-implement-python-batch-processing-script/mm.properties',
                'analysis': 'test_analysis',
                'headless': None,
                'trackonly': None}
    analysisName = 'test_analysis'
    path_to_gl = Path('/home/micha/Documents/01_work/15_moma_notes/02_moma_development/feature/20220801-implement-python-batch-processing-script/test_data/38__bor_20230401/1-Pos000/1-Pos000_GL9')
    gl_file_manager = GlFileManager(path_to_gl, analysisName)

    expected_moma_command = "moma -p /home/micha/Documents/01_work/15_moma_notes/02_moma_development/feature/20220801-implement-python-batch-processing-script/mm.properties -analysis test_analysis -headless -trackonly -i /home/micha/Documents/01_work/15_moma_notes/02_moma_development/feature/20220801-implement-python-batch-processing-script/test_data/38__bor_20230401/1-Pos000/1-Pos000_GL9/20230401_nat_iso_carbon_med3_1_MMStack__1-Pos000_GL9.tif"
    expected_bash_script = "#SBATCH --mem=16G\n#SBATCH --ntasks=1\n#SBATCH --cpus-per-task=4\n#SBATCH --qos=1day\n\nmoma -p /home/micha/Documents/01_work/15_moma_notes/02_moma_development/feature/20220801-implement-python-batch-processing-script/mm.properties -analysis test_analysis -headless -trackonly -i /home/micha/Documents/01_work/15_moma_notes/02_moma_development/feature/20220801-implement-python-batch-processing-script/test_data/38__bor_20230401/1-Pos000/1-Pos000_GL9/20230401_nat_iso_carbon_med3_1_MMStack__1-Pos000_GL9.tif\n"

    def test__build_moma_run_command_returns_correct_command(self):
        sut = MomaSlurmRunner(_default_header_header)
        assert sut.build_moma_run_command(self.gl_file_manager, self.arg_dict) == self.expected_moma_command

    def test__build_slurm_bash_file_string_returns_correct_command(self):
        sut = MomaSlurmRunner(_default_header_header)
        actual = sut.build_slurm_bash_file_string(self.gl_file_manager, self.arg_dict)
        assert self.expected_bash_script == actual

    # def test__write_slurm_bash_script_to_analysis_folder(self):
    #     sut = MomaSlurmRunner(_default_header_header)
    #     actual = sut.write_slurm_bash_script_to_analysis_folder(self.gl_file_manager, self.arg_dict)
        

    def test__bla(self):
        logger = [] # set logger to dummy variable

        sut = MomaSlurmRunner(_default_header_header)

        sut.run(logger, self.gl_file_manager, self.arg_dict)


# class TestFailure():
#     def test__fails(self):
#         assert False
    

