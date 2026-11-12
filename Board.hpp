#pragma once
#include <array>

class Board{
    public:
        std::array<char, 128> squares;

        Board();
        void display();
        void moveTo(int from, int to);
};