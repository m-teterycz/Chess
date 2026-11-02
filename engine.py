import random, torch, math, copy, pandas
import numpy as np

class ChessNetwork(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.layer1 = torch.nn.Linear(773, 256)
        self.layer2 = torch.nn.Linear(256, 128)
        self.layer3 = torch.nn.Linear(128, 1)

    def forward(self, x):
        self.activation = torch.nn.ReLU()
        output1 = self.layer1(x)
        output1R = self.activation(output1)

        output2 = self.layer2(output1R)
        output2R = self.activation(output2)

        output3 = self.layer3(output2R)
        return output3


class Engine:
    def __init__(self, engine_color, WIDTH, HEIGHT):
        self.engine_color = engine_color
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.batch_size = 2048
        self.piece_value = {"Q" : 9,
                "R" : 5,
                "B" : 3,
                "N" : 3,
                "P" : 1,
                "K" : 0
                }
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.smallest_MAE = 100
        self.load()

    def get_best_move(self, board):
        while True:
            piece = random.choice(self.engine_pieces)
            board.get_legal_moves(self.engine_color, piece)
            if len(piece.moves) != 0:
                break
        return piece, random.choice(piece.moves)

    def get_all_pieces(self, board):
        self.engine_pieces = []
        for piece in board.pieces:
            if piece.color == self.engine_color:
                self.engine_pieces.append(piece)

    def evaluate_position(self, board, turn):
        self.network.eval()
        with torch.inference_mode():
            number_turn = [1] if turn == "W" else [0]
            board, castling_rights, white_value, black_value = self.board_to_tensor_boards(board)
            T = torch.tensor(board)
            T = T.flatten()
            T = torch.cat((torch.tensor(number_turn) ,T))
            T = torch.cat((torch.tensor(castling_rights) ,T))
            T = T.to(self.device)
            
            return self.network(T.float()) + white_value - black_value

    def board_to_tensor_boards(self, board):
            empty_boards = []
            castling_rights = [0, 0, 0, 0]
            white_value = 0
            black_value = 0
            for i in range(12):
                empty_boards.append([[0 for _ in range(8)]for _ in range(8)])

            for i in range(1, 13): # bitboards
                wrapped_index = i % 6
                color = "W" if i > 6 else "B"
                searching_piece = list(self.piece_value.keys())[wrapped_index]
                for piece in board.pieces:
                    if piece.piece_type == searching_piece and piece.color == color:
                        row, col = board.get_piece_pos(piece)
                        empty_boards[i - 1][row][col] = 1


            # CASTLING RIGHTS LOGIC AND COLLECTING VALUE OF EACH SIDE
            for piece in board.pieces:
                if piece != ".":
                    if piece.color == "W":
                        white_value += self.piece_value[piece.piece_type]
                        if piece.piece_type == "K":
                            wk = piece
                    else:
                        black_value += self.piece_value[piece.piece_type]
                        if piece.piece_type == "K":
                            bk = piece

            if wk.move_count == 0:
                if board.WKR is not None and board.WKR.move_count == 0 and board.positions[7][7] == board.WKR:
                    castling_rights[0] = 1
                if board.WQR is not None and board.WQR.move_count == 0 and board.positions[7][0] == board.WQR:
                    castling_rights[1] = 1
            if bk.move_count == 0:
                if board.BKR is not None and board.BKR.move_count == 0 and board.positions[0][7] == board.BKR:
                    castling_rights[2] = 1
                if board.BQR is not None and board.BQR.move_count == 0 and board.positions[0][0] == board.BQR:
                    castling_rights[3] = 1

            return empty_boards, castling_rights, white_value, black_value

    def get_data(self, row_count, validation_count):
        data = pandas.read_csv("C:/Users/user/Downloads/chessData.csv/chessData.csv", memory_map = True, header = None, nrows = row_count)
        eval_col = data.iloc[:, 1]
        data = data[~eval_col.str.contains("#", na = False)].dropna()
        data = data.sample(frac = 1)
        data[1] = (pandas.to_numeric(data.iloc[:, 1]) / 100).astype("float32")
        self.validation_data = data.iloc[0:validation_count]
        self.training_data = data.iloc[validation_count:]


    def data_to_validation_tensors(self):
        self.validation_tensors = []
        self.validation_eval_tensors = []

        for i in range(self.validation_positions):
            Board1, turn, castling_rights, white_value, black_value = self.FEN_to_Board(self.validation_FENS[i])
            number_turn = [1] if turn == "W" else [0]

            T = torch.tensor(Board1).float()
            T = T.flatten()
            T = torch.cat((torch.tensor(number_turn).float() ,T))
            T = torch.cat((torch.tensor(castling_rights).float(), T))
            self.validation_tensors.append(T)

            T = torch.tensor(self.validation_evals[i] - (white_value - black_value)).float()
            self.validation_eval_tensors.append(T)

        del self.validation_FENS
        del self.validation_evals

        self.validation_tensors = torch.stack(self.validation_tensors).to(self.device)
        self.validation_eval_tensors = torch.stack(self.validation_eval_tensors).to(self.device)


    def data_to_training_tensors(self, batch_size, pos):
        self.training_board_tensors = []
        self.training_eval_tensors = []

        start_index = pos *  batch_size
        remaining_positions = len(self.training_FENS) - start_index
        actual_chunk_size = min(remaining_positions, batch_size)
        for i in range(actual_chunk_size): # creates all the tensors in batches so RAM isnt filled.
            Board1, turn, castling_rights, white_value, black_value = self.board_info[i + start_index]
            number_turn = [1] if turn == "W" else [0]

            T = torch.tensor(Board1).float()
            T = T.flatten()
            T = torch.cat((torch.tensor(number_turn).float() ,T))
            T = torch.cat((torch.tensor(castling_rights).float(), T))
            self.training_board_tensors.append(T)

            T = torch.tensor(self.training_evals[i + pos * batch_size] - (white_value - black_value)).float()
            T = T.flatten()
            self.training_eval_tensors.append(T)

        self.training_board_tensors = torch.stack(self.training_board_tensors).to(self.device)
        self.training_eval_tensors = torch.stack(self.training_eval_tensors).to(self.device)

            
    def train(self):
        self.network.train()
        loss_function = torch.nn.HuberLoss(delta = 1.0)
        batch_count = 0

        for i in range(math.ceil(len(self.training_board_tensors) / self.batch_size)):
            pos_batch = self.training_board_tensors[i * self.batch_size: self.batch_size + (i * self.batch_size)]
            eval_batch = self.training_eval_tensors[i * self.batch_size: self.batch_size + (i * self.batch_size)]

            prediction = self.network(pos_batch.float())

            loss = loss_function(prediction, eval_batch)

            if batch_count % 100 == 0:
                print(batch_count, loss)

            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()
            batch_count += 1

    def load(self):
        self.network = ChessNetwork()
        try:
            weights = torch.load("ChessEval")
            self.network.load_state_dict(weights)
            self.network.eval()
        except:
            pass
        self.network.to(self.device)
        self.optimizer = torch.optim.Adam(self.network.parameters(), lr=0.001)

    def save(self):
        weights = self.network.state_dict()
        torch.save(weights, "ChessEval")

    def validation(self):
        self.network.eval() # put network into eval mode
        differences_sumed = 0
        with torch.inference_mode(): # stop calculating weights
            for i in range(math.ceil(self.validation_positions / self.batch_size)):
                validation_stack = self.validation_tensors[i * self.batch_size: self.batch_size + (i * self.batch_size)]
                target_stack = self.validation_eval_tensors[i * self.batch_size: self.batch_size + (i * self.batch_size)]
                result = self.network(validation_stack.float())

                differences_tensor = torch.abs(target_stack - result.squeeze(-1))
                differences_sumed += differences_tensor.sum()

            MAE = (differences_sumed / self.validation_positions).item()
            if abs(MAE) < self.smallest_MAE:
                self.smallest_MAE = MAE
                self.best_weights = copy.deepcopy(self.network.state_dict())
                print(f"Smallest MAE: {self.smallest_MAE}")
            print(MAE)

    def save_best_weights(self):
        torch.save(self.best_weights, "ChessEval")

    def FEN_to_flatboard(self, FEN):
        FEN = FEN.split(" ")
        formatted_data = np.zeros(shape = 773, dtype= "uint8")
        row = col = 0
        piece_board_scalars = {"P" : 0, "N" : 64, "B" : 128, "R" : 192, "Q" : 256, "K" : 320}
        for char in FEN[0]:
            if char == "/":
                row += 1
                col = 0
            elif char.isnumeric():
                col += int(char)
            elif char.isupper(): # must be a white piece
                index = piece_board_scalars[char] + row * 8 + col
                formatted_data[index] = 1
                col += 1
            elif char.islower():
                index = piece_board_scalars[char.upper()] + row * 8 + col + 384
                formatted_data[index] = 1
                col += 1

        for char in FEN[2]:
            if char == "K":
                formatted_data[768] = 1
            elif char == "Q":
                formatted_data[769] = 1
            elif char == "k":
                formatted_data[770] = 1
            elif char == "q":
                formatted_data[771] = 1


        if FEN[1] == "w":
            formatted_data[772] = 1

        return formatted_data

    def bulkFEN_to_flatboard(self):
        training_length = len(self.training_data.index)
        validation_length = len(self.validation_data.index)
        self.training_boards = np.zeros(shape = (training_length, 773), dtype= "uint8")
        self.validation_boards = np.zeros(shape = (validation_length, 773), dtype= "uint8")

        for i,fen in enumerate(self.training_data.iloc[:, 0].tolist()):
            self.training_boards[i] = self.FEN_to_flatboard(fen)
        for i,fen in enumerate(self.validation_data.iloc[:, 0].tolist()):
            self.validation_boards[i] = self.FEN_to_flatboard(fen)

    def extract_evals(self):
        self.training_evals = self.training_data[1].to_numpy(copy = True)
        self.validation_evals = self.validation_data[1].to_numpy(copy = True)

        del self.training_data
        del self.validation_data


    def shuffle(self):
        combined = list(zip(self.training_FENS, self.training_evals))
        random.shuffle(combined)
        self.training_FENS, self.training_evals = zip(*combined)