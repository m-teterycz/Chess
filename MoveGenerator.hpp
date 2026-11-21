#pragma once

#include <vector>
#include <span>
#include "Move.hpp"

class Board;

class MoveGenerator{
    public:
        bool checkEnemy(char piece1, char piece2);
        bool checkValidMove(int pos, int move, const Board &board);
        bool checkValidBounds(int destination);
        bool isSquareAttacked(int king_pos, char attacking_color, const Board &board);
        char getPieceColor(int pos, const Board& board);
        
        int perft(int depth, const Board &board);
        int getKingPos(char color, const Board &board);
        std::vector<Move> generateValidSlidingMoves(int pos, std::span<const int> offsets, const Board &board);
        std::vector<Move> generateValidHopMoves(int pos, std::span<const int> offsets, const Board &board);
        std::vector<Move> generateCastlingMoves(int pos, const Board &board);
        std::vector<Move> generatePseudoLegalMoves(int pos, char type, const Board &board);
        std::vector<Move> generateLegalMoves(int pos, char type, const Board &board);
        Board simulateMove(int pos, Move move, const Board &board);
};