#pragma once
#include <array>
#include <string>
#include "Move.hpp"

class Board{
    private:
        bool checkEnemy(char piece1, char piece2);
        void updateCastleRights(char piece, int from);
        void moveCastlingRook(int from, int to);
        void updateEnPassantSquare(char piece, int from, int to);
        void handleEnPassantCapture(int from, int to);
        int boardCoordsToIndex(std::string char_pos);

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
        void display() const;
        void moveTo(Move move);
};