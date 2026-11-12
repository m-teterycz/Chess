#include "Board.hpp"
#include <iostream>


Board::Board(){
    squares.fill('.');
    squares[65] = 'B';
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
