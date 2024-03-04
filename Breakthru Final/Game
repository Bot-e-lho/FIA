import tkinter as tk


class Game:
    def __init__(self, game_interface):
        self.game_interface = game_interface

    def make_move_cpu(self):
        print("Computador fazendo movimento...")
        best_score, best_move = self.minimax(self.game_interface, depth=3, maximizing_player=True)
        if best_move:
            x, y = best_move
            print(f"Movimento do computador: {x}, {y}")
            self.game_interface.realizar_movimento(x, y)
        else:
            print("Movimento Invalido")

    def minimax(self, game_interface, depth, maximizing_player, alpha=float('-inf'), beta=float('inf')):
        if depth == 0 or game_interface.is_game_over():
            return self.avaliar(game_interface), None, None

        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            best_piece = None
            for move in game_interface.get_available_moves():
                for piece in ["barcos", "piratas", "flag"]:
                    new_game_interface = game_interface.make_move(move, piece)
                    eval, _, _ = self.minimax(new_game_interface, depth - 1, False, alpha, beta)
                    if eval > max_eval:
                        max_eval = eval
                        best_move = move
                        best_piece = piece
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
            return max_eval, best_move, best_piece
        else:
            min_eval = float('inf')
            best_move = None
            best_piece = None
            for move in game_interface.get_available_moves():
                for piece in ["barcos", "piratas", "flag"]:
                    new_game_interface = game_interface.make_move(move, piece)
                    eval, _, _ = self.minimax(new_game_interface, depth - 1, True, alpha, beta)
                    if eval < min_eval:
                        min_eval = eval
                        best_move = move
                        best_piece = piece
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
            return min_eval, best_move, best_piece

    def avaliar(self, game_interface):
        score_player = self.heuristica_1()
        score_opponent = self.heuristica_2()
        return score_player - score_opponent

    def heuristica_1(self):
        score = 0
        for barco in self.game_interface.barcos:
            distance_to_flag = min(abs(barco[0] - 3), abs(barco[1] - 3))
            score += distance_to_flag
        for pirata in self.game_interface.piratas:
            min_distance_to_adversary = min(
                abs(pirata[0] - advers[0]) + abs(pirata[1] - advers[1]) for advers in self.game_interface.barcos)
            score -= min_distance_to_adversary
        return score

    def heuristica_2(self):
        score = 0
        for pos_pirata in self.get_pos_piratas():
            dist_to_flag = min(abs(pos_pirata[0] - 3), abs(pos_pirata[1] - 3))
            score -= dist_to_flag
        return score

    def get_pos_piratas(self):
        pos_piratas = set()
        for pirata in self.game_interface.piratas:
            if pirata not in self.game_interface.barcos:
                pos_piratas.add(pirata)
        return pos_piratas
