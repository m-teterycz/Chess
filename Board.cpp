#include "Board.hpp"
#include <iostream>
#include <sstream>

Board::Board(std::string FEN){
    squares.fill('.');

    if (FEN == ""){ // Setup the default position.
        FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1";
    }

    std::istringstream fen_stream(FEN);
    std::string piece_positions;
    std::string castling_rights;


    fen_stream >> piece_positions >> turn >> castling_rights >> en_passant_capture_square >> halfmove >> fullmove;
    
    int board_index = 0;
    int row = 1;
    for (auto& letter : piece_positions){ // Iterate over the piece information in the FEN string.
        if (letter == '/'){
            board_index = 16 * row;
            row++;
        }
        else if (isdigit(letter)){
            board_index += letter - '0';
        }
        else{
            squares[board_index] = letter;
            board_index++;
        }
    }
}

void Board::alterCastleValidity(char piece, int from){
    switch (piece) {
        case 'K':
            white_castle_left = false;
            white_castle_right = false;
            break;
        case 'k':
            black_castle_left = false;
            black_castle_right = false;
            break;
        case 'R':
            if (from == 112){
                white_castle_left = false;
            } else if (from == 119){
                white_castle_right = false;
            }
            break;
            
        case 'r':
            if (from == 0){
                black_castle_left = false;
            } else if (from == 7){
                black_castle_right = false;
            }
            break;
    }    
}

void Board::handleCastleMove(int from, int to) {
    char piece = squares[from];

    if (piece == 'k') {
        if (from == 4 && to == 6) {
            squares[7] = '.';
            squares[5] = 'r';
        }
        else if (from == 4 && to == 2) {
            squares[0] = '.';
            squares[3] = 'r';
        }
    }
    else if (piece == 'K') {
        if (from == 116 && to == 118) {
            squares[119] = '.';
            squares[117] = 'R';
        }
        else if (from == 116 && to == 114) {
            squares[112] = '.';
            squares[115] = 'R';
        }
    }
}

void Board::moveTo(int from, int to){
    char piece = squares[from];

    squares[to] = squares[from];
    squares[from] = '.';

    handleCastleMove(from, to);
    alterCastleValidity(piece, from);
}

void Board::display(){
    for (int i = 0; i < 128; i += 16){
        for (int j = 0; j < 8; j++){
            std::cout << squares[i + j] << ' ';
        }
        std::cout << '\n';
    }
}
