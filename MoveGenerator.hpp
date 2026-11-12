#pragma once

#include <vector>
#include <span>

class Board;

class MoveGenerator{
    public:
        bool checkEnemy(char piece1, char piece2);
        bool checkValidMove(int pos, int move, const Board &board);
        std::vector<int> generateValidSlidingMoves(int pos, std::span<const int> offsets, const Board &board);
        std::vector<int> generateValidHopMoves(int pos, std::span<const int> offsets, const Board &board);
        std::vector<int> generatePseudoLegalMoves(int pos, char type, const Board &board);
};