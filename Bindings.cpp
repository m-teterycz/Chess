#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "Board.hpp"
#include "MoveGenerator.hpp"

namespace py = pybind11;

PYBIND11_MODULE(chess_engine, m) { // tells python that this is a module

    py::class_<Board>(m, "Board")
        .def(py::init<>())
        .def("move_to", &Board::moveTo)
        .def_readwrite("squares", &Board::squares)
        .def("piece_at", [](const Board& board, int pos) {
            if (pos < 0 || (pos & 0x88)) {
                throw py::index_error("Invalid square");
            }
            return board.squares[pos];
        })
        .def("set_piece", [](Board& board, int pos, char piece) {
            if (pos < 0 || (pos & 0x88)) {
                throw py::index_error("Invalid square");
            }
            board.squares[pos] = piece;
        });

    py::class_<MoveGenerator>(m, "MoveGenerator")
        .def(py::init<>())
        .def("generate_moves",
             &MoveGenerator::generatePseudoLegalMoves);
}