#include <iostream>
#include <string>
#include <algorithm>

#include "Board.hpp"
#include "MoveGenerator.hpp"

bool onBoard(int pos) {
    return pos >= 0 && pos < 128 && (pos & 0x88) == 0;
}

int main() {
    Board board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1");
    MoveGenerator generator;

    std::string command;

    while (std::cin >> command) {

        if (command == "BOARD") {
            for (int row = 0; row < 8; row++) {
                for (int col = 0; col < 8; col++) {
                    std::cout << board.squares[row * 16 + col];
                }
            }
            std::cout << '\n' << std::flush;
        }

        else if (command == "MOVES") {
            int pos;
            if (!(std::cin >> pos)) break;

            if (!onBoard(pos) || board.squares[pos] == '.') {
                std::cout << "ERR\n" << std::flush;
                continue;
            }

            char piece = board.squares[pos];
            auto moves = generator.generatePseudoLegalMoves(
                pos, piece, board
            );

            for (int move : moves) {
                std::cout << move << ' ';
            }
            std::cout << '\n' << std::flush;
        }

        else if (command == "MOVE") {
            int from, to;
            if (!(std::cin >> from >> to)) break;

            if (!onBoard(from) || !onBoard(to) ||
                board.squares[from] == '.') {
                std::cout << "ERR\n" << std::flush;
                continue;
            }

            auto moves = generator.generatePseudoLegalMoves(
                from, board.squares[from], board
            );

            if (std::find(moves.begin(), moves.end(), to)
                == moves.end()) {
                std::cout << "ERR\n" << std::flush;
                continue;
            }

            board.moveTo(from, to);
            std::cout << "OK\n" << std::flush;
        }

        else if (command == "GETATTACKEDSQUARES") {
            int pos;
            char attacking_color;

            if (!(std::cin >> pos >> attacking_color)) break;

            if (!onBoard(pos) ||
                (attacking_color != 'W' && attacking_color != 'b')) {
                std::cout << "ERR\n" << std::flush;
                continue;
            }

            bool attacked = generator.isSquareAttacked(
                pos, attacking_color, board
            );

            std::cout << (attacked ? "1" : "0") << '\n' << std::flush;
        }

        else if (command == "QUIT") {
            std::cout << "BYE\n" << std::flush;
            break;
        }

        else {
            std::cout << "ERR\n" << std::flush;
        }
    }

    return 0;
}