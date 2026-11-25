#include "Search.hpp"

#include <unordered_map>

int Search::to64(int pos){
    return (pos / 16) * 8 + pos % 16;
}

int Search::evaluate(const Board &board){
    int evaluation = 0;
    
    for (int i = 0; i < board.squares.size(); i++){
        if (i & 0x88){
            continue;
        }

        char piece = board.squares[i];
        if (piece != '.'){
            evaluation += piece_values.at(piece) + positionalEvaluation(piece, i);
        }
    }
    return evaluation;
}

int Search::positionalEvaluation(char piece_type, int pos){
    pos = to64(pos);
    switch (piece_type){
        case 'P':
        case 'p':
        {
            if (piece_type == 'P'){
                return white_pawn_position_table[pos];
            }
            int mirrored_pos = pos ^ 56;
            return -white_pawn_position_table[mirrored_pos];
        }

        case 'N': 
        case 'n':
        {
            if (piece_type == 'N'){
                return white_knight_position_table[pos];
            }
            int mirrored_pos = pos ^ 56;
            return -white_knight_position_table[mirrored_pos];
        }

        case 'B':
        case 'b':
        {
            if (piece_type == 'B'){
                return white_bishop_position_table[pos];
            }
            int mirrored_pos = pos ^ 56;
            return -white_bishop_position_table[mirrored_pos];            
        }
        
        case 'R':
        case 'r':
        {
            if (piece_type == 'R'){
                return white_rook_position_table[pos];
            }
            int mirrored_pos = pos ^ 56;
            return -white_rook_position_table[mirrored_pos];                
        }

        case 'Q':
        case 'q':
        {
            if (piece_type == 'Q'){
                return white_queen_position_table[pos];
            }
            int mirrored_pos = pos ^ 56;
            return -white_queen_position_table[mirrored_pos];            
        }

        case 'K':
        case 'k':
        {
            if (piece_type == 'K'){
                return white_king_position_table[pos];
            }
            int mirrored_pos = pos ^ 56;
            return -white_king_position_table[mirrored_pos];            
        }
    }
    return 0;
}

int Search::negamax(int depth, int alpha, int beta, const Board &board){ // Alpha is the best score initial player can get and beta is the best score the other player can get
    constexpr int INF = 2000000;
    constexpr int MATE = 1000000;

    int score = -INF;
    int best_score = -INF;
    bool has_legal_moves = false;  

    for (int i = 0; i < board.squares.size(); i++){
        char piece = board.squares[i];
        if (piece == '.' || i & 0X88 || board.turn != generator.getPieceColor(i, board)){ // checks if the square is valid, the piece is the player's and its not an empty square
            continue;
        }

        auto moves = generator.generateLegalMoves(i, piece, board);
        if (moves.size() != 0){
            has_legal_moves = true;
        }

        if (depth == 0){
            continue;
        }

        for (auto move : moves){
            Board simulated = generator.simulateMove(i, move, board);
            score = -negamax(depth - 1, -beta, -alpha, simulated);

            best_score = std::max(score, best_score);
            alpha = std::max(alpha, score);

            if (alpha >= beta){
                break;
            }
        }
    }
    if (!has_legal_moves){
        char color = (board.turn == 'W') ? 'b' : 'W';
        int king_pos = generator.getKingPos(board.turn, board);
        if (generator.isSquareAttacked(king_pos, color, board)){
            return -MATE;
        }else{
            return 0;
        }
    }
    if (depth == 0){
        int color = (board.turn == 'W') ? 1 : -1;
        return color * evaluate(board);
    }
    return best_score;
}

Move Search::findBestMove(int depth, const Board &board){
    constexpr int INF = 2000000;

    int best_score = -INF;
    Move best_move;

    for (int i = 0; i < board.squares.size(); i++){
        char piece = board.squares[i];
        if (piece == '.' || i & 0X88 || board.turn != generator.getPieceColor(i, board)){
            continue;
        }

        auto moves = generator.generateLegalMoves(i, piece, board);
        for (auto move : moves){
            Board simulated = generator.simulateMove(i, move, board);
            int score = -negamax(depth - 1, -INF, INF, simulated);

            if (score > best_score){
                best_move = move;
                best_score = score;
            }
        }    
    }
    return best_move;
}