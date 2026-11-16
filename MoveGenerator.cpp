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

bool MoveGenerator::checkValidBounds(int destination){
    return destination >= 0 && destination < 128 && (destination & 0x88) == 0;
}

bool MoveGenerator::checkValidMove(int pos, int move, const Board &board){
    if (!checkValidBounds(pos) || !checkValidBounds(move)){
        return false;
    }

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

char MoveGenerator::getPieceColor(int pos, const Board& board){
    if (checkValidBounds(pos)){
        if (isupper(board.squares[pos])){
            return 'W';
        }else if(islower(board.squares[pos])){
            return 'b';
        }
    }
    return false;
}

bool MoveGenerator::isSquareAttacked(int pos, char attacking_color, const Board& board){
    std::array<int, 8> king_offsets = {1, 16, -1, -16, 15, 17, -15, -17};
    std::array<int, 4> bishop_offsets = {15, 17, -15, -17};
    std::array<int, 4> rook_offsets = {1, 16, -1, -16};
    std::array<int, 2> pawn_offsets = {15, 17};
    std::array<int, 8> knight_offsets = {14, 18, 31, 33, -14, -18, -31, -33};

    for (const int offset : bishop_offsets){
        int current_square = pos;
        while(true){
            current_square += offset;
            if (checkValidBounds(current_square)){
                char piece_at_square = board.squares[current_square];
                char piece_at_square_color = getPieceColor(current_square, board);
                piece_at_square = std::tolower(static_cast<unsigned char>(piece_at_square)); // dont have to check as many conditions since the text is lower case.
                
                if (piece_at_square_color == attacking_color && (piece_at_square == 'b' || piece_at_square == 'q')){ // enemy piece found
                    return true;
                } else if (piece_at_square != '.'){ // another piece which would block any attack
                    break;
                }
            }else{
                break;
            }
        }
    }

    for (const int offset : rook_offsets){
        int current_square = pos;
        while (true){
            current_square += offset;
            if (checkValidBounds(current_square)){
                char piece_at_square = board.squares[current_square];
                char piece_at_square_color = getPieceColor(current_square, board);
                piece_at_square = std::tolower(static_cast<unsigned char>(piece_at_square));

                if (piece_at_square_color == attacking_color && (piece_at_square == 'r' || piece_at_square == 'q')){
                    return true;
                } else if (piece_at_square != '.'){
                    break;
                }
            } else {
                break;
            }
        }
    }
    
    int direction = (attacking_color == 'W') ? 1 : -1;
    for (const int offset : pawn_offsets){
        int current_square = pos + offset * direction;

        if (checkValidBounds(current_square)){
            char piece_at_square = board.squares[current_square];
            char piece_at_square_color = getPieceColor(current_square, board);
            
            if ((piece_at_square == 'p' || piece_at_square == 'P') && attacking_color == piece_at_square_color){
                return true;
            }
        }
    }

    for (const int offset : knight_offsets){
        int current_square = pos + offset;
        if (checkValidBounds(current_square)){
            char piece_at_square = board.squares[current_square];
            char piece_at_square_color = getPieceColor(current_square, board);

            if ((piece_at_square == 'N' || piece_at_square == 'n') && attacking_color == piece_at_square_color){
                return true;
            }
        }
    }

    for (const int offset : king_offsets){
        int current_square = pos + offset;
        if (checkValidBounds(current_square)){
            char piece_at_square = board.squares[current_square];
            char piece_at_square_color = getPieceColor(current_square, board);
            if (piece_at_square_color == attacking_color && (piece_at_square == 'K' || piece_at_square == 'k')){
                return true;
            }
        }
    }
    return false;
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

std::vector<int> MoveGenerator::generateCastlingMoves(int pos, const Board &board){
    std::vector<int> moves;

    char king_color = getPieceColor(pos, board);
    char attacking_color = (king_color == 'b') ? 'W' : 'b';

    if (king_color == 'b' && pos == 4 && board.squares[4] == 'k') {

        if (board.black_castle_right &&
            board.squares[7] == 'r' &&
            board.squares[5] == '.' &&
            board.squares[6] == '.' &&
            !isSquareAttacked(4, attacking_color, board) &&
            !isSquareAttacked(5, attacking_color, board) &&
            !isSquareAttacked(6, attacking_color, board)) {

            moves.push_back(6);
        }

        if (board.black_castle_left &&
            board.squares[0] == 'r' &&
            board.squares[1] == '.' &&
            board.squares[2] == '.' &&
            board.squares[3] == '.' &&
            !isSquareAttacked(4, attacking_color, board) &&
            !isSquareAttacked(3, attacking_color, board) &&
            !isSquareAttacked(2, attacking_color, board)) {

            moves.push_back(2);
        }
    }

    else if (king_color == 'W' && pos == 116 && board.squares[116] == 'K') {

        if (board.white_castle_right &&
            board.squares[119] == 'R' &&
            board.squares[117] == '.' &&
            board.squares[118] == '.' &&
            !isSquareAttacked(116, attacking_color, board) &&
            !isSquareAttacked(117, attacking_color, board) &&
            !isSquareAttacked(118, attacking_color, board)) {

            moves.push_back(118);
        }

        if (board.white_castle_left &&
            board.squares[112] == 'R' &&
            board.squares[113] == '.' &&
            board.squares[114] == '.' &&
            board.squares[115] == '.' &&
            !isSquareAttacked(116, attacking_color, board) &&
            !isSquareAttacked(115, attacking_color, board) &&
            !isSquareAttacked(114, attacking_color, board)) {

            moves.push_back(114);
        }
    }

    return moves;
}

std::vector<int> MoveGenerator::generatePseudoLegalMoves(int pos, char type, const Board &board){
    std::vector<int> moves;
    if (type == 'N' || type == 'n'){
        const std::array<int, 8> offsets = {
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
        
        std::vector<int> moves = generateValidHopMoves(pos, offsets, board);
        std::vector<int> castling = generateCastlingMoves(pos, board);
        moves.insert(moves.end(), castling.begin(), castling.end());

        return moves;

        
    }
    if (type == 'P' || type == 'p'){
        std::vector<int> moves;
        std::array<int, 2> attacking_offsets = {15, 17};
        int destination;
        int direction = (isupper(type)) ? -1 : 1; // works to determine color later
        int start_row = (direction == -1) ? 6 : 1;
        
        // Normal moves ahead
        destination = pos + 16 * direction;
        if (checkValidBounds(destination) && board.squares[destination] == '.'){
            moves.push_back(destination);
            destination = pos + 32 * direction;
            if (checkValidBounds(destination) && ((pos / 16 == start_row) && (board.squares[destination] == '.'))){
                moves.push_back(destination);
            }
        }

        for (const int &attack_offset : attacking_offsets){
            destination = pos + attack_offset * direction;
            if (checkValidBounds(destination) && ((islower(board.squares[destination]) && direction == -1) || (isupper(board.squares[destination]) && direction == 1))){
                moves.push_back(destination);
            }
        }
        return moves;
    }
    return moves;
}