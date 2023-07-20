# import unittest
import logging
import sys
import pytest

from moma_batch_run import MomaSlurmRunner

def setup_function(function):
    print("setting up failed for: ", function)

class TestMomaSlurmRunner():
    def test_init(self, capsys):
        sut = MomaSlurmRunner()
        with capsys.disabled():
            print("BLA1!")
            print(sut.get_default_slurm_header())
        print("BLA2!")
        
        assert True

# def test_func1(capsys):
#     with capsys.disabled():
#         print("WTF1!!!")
#     assert True


# def test_func2():
#     print("WTF2!!!")
#     assert False

# def f():
#     raise SystemExit(1)

# class TestWithPytest():
#     def test_one(self):
#         x = "this"l
#         print("HELLO WORLD")
#         assert False
#         # assert "h" in x

#     def test_two(self):
#         x = "this"
#         assert "h" in x

    # def test_mytest():
    #     with pytest.raises(SystemExit):
    #         f()

# class TestMomaSlurmRunner(unittest.TestCase):
#     def test_init(self):
#         # log = logging.getLogger( "SomeTest.testSomething" )
#         # log.debug( "this= %r", self.this )
#         sut = MomaSlurmRunner()
#         # print(sut.get_default_slurm_header())
#         print("hello world")
#         # assert False

# # if __name__ == "__main__":
# #     logging.basicConfig( stream=sys.stderr )
# #     logging.getLogger( "SomeTest.testSomething" ).setLevel( logging.DEBUG )
# #     unittest.main()