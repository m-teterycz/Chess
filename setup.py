from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension, build_ext

setup(
    name="chess_engine",
    ext_modules=[
        Pybind11Extension(
            "chess_engine",
            [
                "bindings.cpp",
                "Board.cpp",
                "MoveGenerator.cpp"
            ],
            cxx_std=20
        )
    ],
    cmdclass={"build_ext": build_ext}
)