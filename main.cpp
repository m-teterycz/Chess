#include <iostream>
#include <array>
#include <vector>
#include <cctype>

#include "Board.hpp"
#include "MoveGenerator.hpp"

using namespace std;


int main(){
    Board board;
    MoveGenerator Gen;
    board.display();

    int pos = 65;
    char type = 'K';
    vector<int> moves = Gen.generatePseudoLegalMoves(pos, type, board);
    cout << "pos " << pos << '\n';
    for (const int &move : moves){
        cout << move << '\n';
    }


    return 0;
}
