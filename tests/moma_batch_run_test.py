# import unittest
import logging
from pathlib import Path
import sys
import pytest

from moma_batch_run import GlFileManager, MomaSlurmRunner

def setup_function(function):
    print("setting up failed for: ", function)

class TestMomaSlurmRunner():
    def test__init_without_path_argument_uses_default_header_file(self):
        expected = Path.home() / ".moma" / "batch_run_slurm_header.txt"
        sut = MomaSlurmRunner()
        assert sut.slurm_header_file == expected

    def test__init_with_existing_header_file_path_uses_the_path(self):
        expected = Path("./test_data/temporary_test_batch_run_slurm_header.txt")
        expected.touch()
        sut = MomaSlurmRunner(expected)
        expected.unlink()
        assert sut.slurm_header_file == expected

    def test__init_with_non_existent_file__raises_argument_error(self):
        expected = Path("./test_data/non_existent_batch_run_slurm_header.txt")
        with pytest.raises(IOError):
            sut = MomaSlurmRunner(expected)

    def test__calling_run__does_something(self):
        arg_dict = {'p': '/home/micha/Documents/01_work/15_moma_notes/02_moma_development/feature/20220801-implement-python-batch-processing-script/mm.properties',
                    'analysis': 'test_analysis',
                    'headless': None,
                    'trackonly': None}
        analysisName = 'test_analysis'
        path_to_gl = Path('/home/micha/Documents/01_work/15_moma_notes/02_moma_development/feature/20220801-implement-python-batch-processing-script/test_data/38__bor_20230401/1-Pos000/1-Pos000_GL9')
        glFileManager = GlFileManager(path_to_gl, analysisName)
        expected = Path("./test_data/temporary_test_batch_run_slurm_header.txt")
        expected.touch()
        sut = MomaSlurmRunner(expected)
        raise NotImplementedError()
