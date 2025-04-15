import tkinter as tk

from Game import Game


class GameInterface:
    def __init__(self, window):
        self.num_barcos = 8
        self.num_piratas = 12
        self.tamanho = 7
        self.window = window
        self.window.title("Breakthru")
        self.largura = 800
        self.altura = 600
        self.barcos = {(2, 2), (2, 3), (2, 4), (4, 2), (4, 3), (4, 4), (3, 2), (3, 4)}
        self.flag = {(3, 3)}
        self.piratas = {(2, 0), (3, 0), (4, 0), (6, 2), (6, 3), (6, 4), (0, 2), (0, 3), (0, 4), (2, 6), (3, 6), (4, 6)}
        self.celula = min(self.largura, self.altura) // 7
        self.sel_piratas = None
        self.sel_barcos = None
        self.sel_flag = None
        self.canvas = tk.Canvas(self.window, width=7 * self.celula, height=7 * self.celula, bg="black")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_button_click)
        self.rodada = 1
        self.max_mov = 1
        self.movimentos_restantes = {
            "barcos": self.max_mov,
            "piratas": self.max_mov,
            "flag": self.max_mov
        }
        self.movimento_feito = False
        self.criar_tabuleiro()
        self.criar_pecas()
        self.turn_label = tk.Label(self.window, text="Turno: Jogador 1")
        self.turn_label.pack()
        self.round_label = tk.Label(self.window, text="Rodada: 1")
        self.round_label.pack()

    def criar_tabuleiro(self):
        for i in range(self.tamanho):
            for j in range(self.tamanho):
                x0, y0 = j * self.celula, i * self.celula
                x1, y1 = x0 + self.celula, y0 + self.celula
                self.canvas.create_rectangle(x0, y0, x1, y1, fill="orange", outline="black")

    def realizar_movimento(self, x, y, tipo_peca):
        if tipo_peca:
            if self.sel_piratas in self.piratas:
                self.piratas.remove(self.sel_piratas)
                self.piratas.add((x, y))
                self.movimentos_restantes[tipo_peca] -= 1
            elif self.sel_piratas in self.barcos:
                self.barcos.remove(self.sel_piratas)
                self.barcos.add((x, y))
                self.movimentos_restantes[tipo_peca] -= 1
            elif self.sel_piratas in self.flag:
                self.flag.remove(self.sel_piratas)
                self.flag.add((x, y))
                self.movimentos_restantes[tipo_peca] -= 1
            self.sel_piratas = None
            self.canvas.delete("all")
            self.criar_tabuleiro()
            self.criar_pecas()

    def criar_pecas(self):
        for peca in self.barcos:
            fill = "gold"
            if peca == self.sel_piratas:
                fill = "blue"
            self.criar_peca(peca, fill)
        for peca in self.piratas:
            fill = "black"
            if peca == self.sel_piratas:
                fill = "blue"
            self.criar_peca(peca, fill)
        for peca in self.flag:
            fill = "red"
            if peca == self.sel_piratas:
                fill = "blue"
            self.criar_peca(peca, fill)

    def criar_peca(self, peca, fill):
        x, y = peca
        y_pos = y * self.celula + self.celula // 2
        x_pos = x * self.celula + self.celula // 2
        rad = self.celula // 3
        self.canvas.create_oval(x_pos - rad, y_pos - rad, x_pos + rad, y_pos + rad, fill=fill, outline=fill)

    def avaliar_tabuleiro(self, tipo):
        if tipo == "piratas":
            pecas = self.piratas
        elif tipo == "barcos":
            pecas = self.barcos
        elif tipo == "flag":
            pecas = self.flag
        else:
            return False
        return len(pecas) == 0

    def is_game_over(self):
        return self.num_barcos == 0 or self.num_piratas == 0

    def update_turn_label(self):
        player = "Jogador 1" if self.rodada % 2 != 0 else "Computador"
        self.turn_label.config(text="Turno: {}".format(player))

    def update_round_label(self):
        self.round_label.config(text="Rodada: {}".format(self.rodada))

    def on_button_click(self, event):
        if self.movimento_feito:
            print("Já foi feito um movimento nesta rodada.")
            return
        x, y = event.x // self.celula, event.y // self.celula
        if not self.sel_piratas:
            if (x, y) in self.piratas:
                self.sel_piratas = (x, y)
                self.criar_pecas()
                self.movimentos_restantes["piratas"] -= 1
            elif (x, y) in self.barcos:
                self.sel_piratas = (x, y)
                self.criar_pecas()
                self.movimentos_restantes["barcos"] -= 1
            elif (x, y) in self.flag:
                self.sel_piratas = (x, y)
                self.criar_pecas()
                self.movimentos_restantes["flag"] -= 1
        else:
            if (x, y) in {(self.sel_piratas[0] + 1, self.sel_piratas[1]),
                          (self.sel_piratas[0] - 1, self.sel_piratas[1]),
                          (self.sel_piratas[0], self.sel_piratas[1] + 1),
                          (self.sel_piratas[0], self.sel_piratas[1] - 1)}:
                tipo_peca = self.get_tipo_peca(self.sel_piratas)
                if (x, y) not in self.piratas and (x, y) not in self.barcos and (x, y) not in self.flag:
                    if tipo_peca:
                        self.realizar_movimento(x, y, tipo_peca)
                        self.movimento_feito = True
                        self.rodada += 1
                        self.update_turn_label()
                        self.update_round_label()
                        self.game_loop()
                        self.window.update()
            else:
                print("Movimento inválido")
                self.sel_piratas = None
                self.criar_pecas()

    def get_tipo_peca(self, posicao):
        if posicao in self.piratas:
            return "piratas"
        elif posicao in self.barcos:
            return "barcos"
        elif posicao in self.flag:
            return "flag"
        else:
            return None

    def game_loop(self):
        game = Game(self)
        if self.rodada == 1:
            print("Rodada 1.")
            self.update_round_label()
            self.update_turn_label()
            self.window.mainloop()
        else:
            print("Rodada do computador")
            self.update_round_label()
            game.make_move_cpu()
            self.rodada = 1
            self.window.update()
            self.game_loop()

    def get_available_moves(self):
        available_moves = []
        for x in range(self.tamanho):
            for y in range(self.tamanho):
                if (x, y) not in self.piratas and (x, y) not in self.barcos and (x, y) not in self.flag:
                    available_moves.append((x, y))
        return available_moves

def main():
    interface = tk.Tk()
    interface.title("Breakthru")
    game_interface = GameInterface(interface)
    game = Game(game_interface)

    def make_move_wrapper():
        game.make_move_cpu()
        if not game_interface.is_game_over():
            interface.after(100, make_move_wrapper)

    game_interface.game_loop()

    interface.mainloop()



if __name__ == "__main__":
    main()

