#include "Board.hpp"
#include <iostream>
#include <sstream>

Board::Board(std::string FEN){
    squares.fill('.');
    white_castle_left = false;
    white_castle_right = false;
    black_castle_left = false;
    black_castle_right = false;

    if (FEN == ""){ // Setup the default position.
        FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1";
    }

    std::istringstream fen_stream(FEN);
    std::string piece_positions;
    std::string castling_rights;
    std::string test_en_passant_capture_square;


    fen_stream >> piece_positions >> turn >> castling_rights >> test_en_passant_capture_square >> halfmove >> fullmove;
    
    int board_index = 0;
    int row = 1;
    for (char letter : piece_positions){ // Iterate over the piece information in the FEN string.
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

    for (auto& letter : castling_rights){
        switch (letter){
            case 'K':
                white_castle_right = true;
                break;
            case 'Q':
                white_castle_left = true;
                break;
            case 'k':
                black_castle_right = true;
                break;
            case 'q':
                black_castle_left = true;
                break;
        }
    }

    if (test_en_passant_capture_square[0] == '-'){
        en_passant_capture_square = -1;
    } else{
        en_passant_capture_square = boardCoordsToIndex(test_en_passant_capture_square);
    }

    if (turn == 'w'){
        turn = 'W';
    }
}

int Board::boardCoordsToIndex(std::string char_pos){
    int col = char_pos[0] - 'a';
    int row = 8 - (char_pos[1] - '0');

    return row * 16 + col;;
}

bool Board::checkEnemy(char piece1, char piece2){
    if (piece1 != '.' && piece2 != '.'){
        return isupper(piece1) != isupper(piece2);
    }
    return false;
}

void Board::updateCastleRights(char piece, int from){
    if (squares[112] != 'R'){
        white_castle_left = false;
    }
    if (squares[119] != 'R'){
        white_castle_right = false;
    }
    if (squares[0] != 'r'){
        black_castle_left = false;
    }
    if (squares[7] != 'r'){
        black_castle_right = false;
    }
    switch (piece) {
        case 'K':
            white_castle_left = false;
            white_castle_right = false;
            break;
        case 'k':
            black_castle_left = false;
            black_castle_right = false;
            break;
    }    
}

void Board::moveCastlingRook(int from, int to) {
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

void Board::updateEnPassantSquare(char piece, int from, int to){
    int direction = (isupper(piece)) ? -1 : 1;

    if (abs(to - from) == 32 && (piece == 'p' || piece == 'P')){
        en_passant_capture_square = from + 16 * direction;
    }else {
        en_passant_capture_square = -1;
    }
}

void Board::handleEnPassantCapture(int from, int to){
    char piece = squares[from];
    int direction = (isupper(piece)) ? -1 : 1;
    if (piece == 'p' || piece == 'P'){
        if (to == en_passant_capture_square){
            squares[to - 16 * direction] = '.';
        }
    }
}

void Board::moveTo(Move move){
    char piece = squares[move.from];

    moveCastlingRook(move.from, move.to);
    handleEnPassantCapture(move.from, move.to);

    if (move.promotion != '.'){
        squares[move.to] = move.promotion;
    }else{
        squares[move.to] = squares[move.from];
    }
    squares[move.from] = '.';

    updateCastleRights(piece, move.from);
    updateEnPassantSquare(piece, move.from, move.to);

    turn = (turn == 'W') ? 'b' : 'W';
}

void Board::display() const{
    for (int i = 0; i < 128; i += 16){
        for (int j = 0; j < 8; j++){
            std::cout << squares[i + j] << ' ';
        }
        std::cout << '\n';
    }
}
