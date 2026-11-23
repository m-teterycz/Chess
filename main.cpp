#include <iostream>
#include <string>
#include <algorithm>

#include "Board.hpp"
#include "MoveGenerator.hpp"
#include "Move.hpp"
#include "Search.hpp"

bool onBoard(int pos) {
    return pos >= 0 && pos < 128 && (pos & 0x88) == 0;
}

int main() {
    Board board("6Q1/5R2/7k/8/8/8/8/6K1 w - - 0 1");
    MoveGenerator generator;
    Search MoveSearch;

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
            auto moves = generator.generateLegalMoves(
                pos, piece, board
            );

            for (Move move : moves) {
                std::cout << move.to << ' ';
            }
            std::cout << '\n' << std::flush;
        }

        else if (command == "MOVE") {
            int from, to;
            char promotion;

            if (!(std::cin >> from >> to >> promotion)) break;

            // Check that the positions are valid
            if (!onBoard(from) || !onBoard(to) ||
                board.squares[from] == '.') {
                std::cout << "ERR\n" << std::flush;
                continue;
            }

            // Check that the piece belongs to the current player
            if (generator.getPieceColor(from, board) != board.turn) {
                std::cout << "ERR\n" << std::flush;
                continue;
            }

            // Generate legal moves
            auto moves = generator.generateLegalMoves(
                from, board.squares[from], board
            );

            // Find a move matching the requested destination and promotion
            auto it = std::find_if(
                moves.begin(),
                moves.end(),
                [from, to, promotion](const Move& move) {
                    return move.from == from &&
                        move.to == to &&
                        move.promotion == promotion;
                }
            );

            // Check whether the move exists
            if (it == moves.end()) {
                std::cout << "ERR\n" << std::flush;
                continue;
            }

            // Execute the move
            board.moveTo(*it);

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

        else if (command == "PERFT") {
            int depth;

            if (!(std::cin >> depth)) break;

            if (depth < 0 || depth > 6) {
                std::cout << "ERR\n" << std::flush;
                continue;
            }

            auto nodes = generator.perft(depth, board);

            std::cout << nodes << '\n' << std::flush;
        }

        else if (command == "BESTMOVE"){
            int depth;
            std::cin >> depth;

            if (depth < 0 || depth > 6) {
                std::cout << "ERR\n" << std::flush;
                continue;
            }

            auto best_move = MoveSearch.findBestMove(depth, board);
            std::cout << best_move.from << ' ' << best_move.to << ' ' << best_move.promotion << '\n' << std::flush;
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