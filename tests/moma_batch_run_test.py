# import unittest
import logging
from pathlib import Path
import sys
import pytest

from moma_batch_run import MomaSlurmRunner

def setup_function(function):
    print("setting up failed for: ", function)

class TestMomaSlurmRunner():
    def test__init_without_path_argument__returns__path_to_home_directory(self):
        expected = Path.home() / ".moma" / "batch_run_slurm_header.txt"
        sut = MomaSlurmRunner()
        assert sut.slurm_header_file == expected

    def test__init_with_path__returns__path(self):
        expected = Path("./test_data/temporary_test_batch_run_slurm_header.txt")
        expected.touch()
        sut = MomaSlurmRunner(expected)
        expected.unlink()
        assert sut.slurm_header_file == expected

    def test__init_with_non_existent_file__raises_argument_error(self):
        expected = Path("./test_data/non_existent_batch_run_slurm_header.txt")
        with pytest.raises(IOError):
            sut = MomaSlurmRunner(expected)
