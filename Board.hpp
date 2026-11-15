#pragma once
#include <array>
#include <string>

class Board{
    public:
        std::array<char, 128> squares;

        Board(std::string Fen);
        void display();
        void moveTo(int from, int to);
};