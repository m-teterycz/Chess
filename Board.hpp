#pragma once
#include <array>
#include <string>

class Board{
    public:
        std::array<char, 128> squares;
        char turn;
        int en_passant_capture_square;
        int halfmove;
        int fullmove;
        bool white_castle_left;
        bool white_castle_right;
        bool black_castle_left;
        bool black_castle_right;

        Board(std::string Fen);
        void display();
        void moveTo(int from, int to);
        void alterCastleValidity(char piece, int from);
        void handleCastleMove(int from, int to);
};