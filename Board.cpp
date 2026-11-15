#include "Board.hpp"
#include <iostream>
#include <ranges>

Board::Board(std::string FEN){
    squares.fill('.');

    if (FEN == ""){ // Setup the default position.
        FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1";
    }

    auto parsed_FEN = std::views::split(FEN, ' ');
    auto it = parsed_FEN.begin();
    
    int board_index = 0;
    int row = 1;
    for (auto& letter : *it){ // Iterate over the piece information in the FEN string.
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

void Board::moveTo(int from, int to){
    squares[to] = squares[from];
    squares[from] = '.';
}

void Board::display(){
    for (int i = 0; i < 128; i += 16){
        for (int j = 0; j < 8; j++){
            std::cout << squares[i + j] << ' ';
        }
        std::cout << '\n';
    }
}
