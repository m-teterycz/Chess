#include "MoveGenerator.hpp"
#include "Board.hpp"

#include <vector>
#include <array>
#include <cctype>


bool MoveGenerator::checkEnemy(char piece1, char piece2){
    if (piece1 != '.' && piece2 != '.'){
        return isupper(piece1) != isupper(piece2);
    }
    return false;
}

bool MoveGenerator::checkValidMove(int pos, int move, const Board &board){
    char current_piece = board.squares[pos];
    if ((move & 0x88)){ // check if off board
        return false;
    }
    if (board.squares[move] == '.'){
        return true;
    }
    if (!(checkEnemy(board.squares[move], current_piece))){ // Must be a friendly piece
        return false;
    }
    return true;
}

std::vector<int> MoveGenerator::generateValidSlidingMoves(int pos, std::span<const int> offsets, const Board &board){
    std::vector<int> moves;
    for (const int offset : offsets){
        int move = pos;
        while (true) {
            move += offset;
            if (checkValidMove(pos, move, board)){
                moves.push_back(move);
                if (checkEnemy(board.squares[move], board.squares[pos])){ // If the piece is an enemy add the move then break out since we cant move past it
                    break;
                }
            }else {
                break;
            }
        }
    }
    return moves;
}

std::vector<int> MoveGenerator::generateValidHopMoves(int pos, std::span<const int> offsets, const Board &board){
    std::vector<int> moves;
    for (int offset : offsets){
        int move = pos + offset;
        if (checkValidMove(pos, move, board)){
            moves.push_back(move);
        }
    }
    return moves;
}  

std::vector<int> MoveGenerator::generatePseudoLegalMoves(int pos, char type, const Board &board){
    std::vector<int> temp;
    if (type == 'N' || type == 'n'){ // Knight
        const std::array<int, 8> offsets = { // hardcoded offsets make it easier to implement and faster to generate moves
            14, 18, 31, 33,
            -14, -18, -31, -33
        };      
        return generateValidHopMoves(pos, offsets, board);
    }

    if (type == 'B' || type == 'b'){
        const std::array<int, 4> offsets = {
            15, 17, -15, -17
        };
        return generateValidSlidingMoves(pos, offsets, board);
    }
    if (type == 'R' || type == 'r'){
        const std::array<int, 4> offsets = {
            1, 16, -1, -16
        };
        return generateValidSlidingMoves(pos, offsets, board);
    }
    if (type == 'Q' || type == 'q'){
        const std::array<int, 8> offsets = {
            1, 16, -1, -16, 15, 17, -15, -17
        };
        return generateValidSlidingMoves(pos, offsets, board);
    }
    if (type == 'K' || type == 'k'){
        const std::array<int, 8> offsets = {
            1, 16, -1, -16, 15, 17, -15, -17
        };
        return generateValidHopMoves(pos, offsets, board);
    }
    if (type == 'P' || type == 'p'){
        std::vector<int> moves;
        std::array<int, 2> attacking_squares = {15, 17};
        int direction = (isupper(type)) ? -1 : 1; // also works to determine color later
        int start_row;

        if (pos / 16 == 6){ // must be white
            start_row = 6;
        }else if (pos / 16 == 1){ // must be black
            start_row = 1;
        }
        
        // Normal moves ahead
        if (board.squares[pos + 16 * direction] != '.'){ // looking one square ahead
            moves.push_back(pos + 16 * direction);
            if ((board.squares[pos + 32 * direction] != '.') && (board.squares[pos] / 16 == start_row)){ // looking two squares ahead and checking if the pawn is allowed to do this
                moves.push_back(pos + 32 * direction);
            }
        }

        // Diagonal Captures
        for (const int &attack_square : attacking_squares){
            if ((islower(board.squares[attack_square]) && direction == -1) || (isupper(board.squares[attack_square]) && direction == 1)){ // white capture black piece || black capture white piece
                moves.push_back(attack_square);
            }
        }

    }
    return temp;
}