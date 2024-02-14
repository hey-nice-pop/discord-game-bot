import discord

class OthelloGame:
    def __init__(self):
        self.board = [[' ' for _ in range(6)] for _ in range(6)]  # 6x6の盤面に変更
        self.board[2][2], self.board[3][3] = ':white_circle:', ':white_circle:'  # 中央の位置を調整
        self.board[2][3], self.board[3][2] = ':black_circle:', ':black_circle:'  # 中央の位置を調整
        self.current_player = ':black_circle:'
        self.last_message_id = None  # last_message_idを初期化

    def is_valid_move(self, row, col):
        if self.board[row][col] != ' ' or not (0 <= row < 6 and 0 <= col < 6):
            return False
        opponent = ':white_circle:' if self.current_player == ':black_circle:' else ':black_circle:'
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            while 0 <= r < 6 and 0 <= c < 6 and self.board[r][c] == opponent:
                r += dr
                c += dc
                if 0 <= r < 6 and 0 <= c < 6 and self.board[r][c] == self.current_player:
                    return True
        return False

    def flip_pieces(self, row, col):
        opponent = ':white_circle:' if self.current_player == ':black_circle:' else ':black_circle:'
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dr, dc in directions:
            pieces_to_flip = []
            r, c = row + dr, col + dc
            while 0 <= r < 6 and 0 <= c < 6 and self.board[r][c] == opponent:
                pieces_to_flip.append((r, c))
                r += dr
                c += dc
            if 0 <= r < 6 and 0 <= c < 6 and self.board[r][c] == self.current_player:
                for fr, fc in pieces_to_flip:
                    self.board[fr][fc] = self.current_player

    def switch_player(self):
        self.current_player = ':white_circle:' if self.current_player == ':black_circle:' else ':black_circle:'

    def count_pieces(self, player):
        return sum(row.count(player) for row in self.board)

    def is_board_full(self):
        return all(cell != ' ' for row in self.board for cell in row)

    def is_game_over(self):
        return self.is_board_full() or all(not self.is_valid_move(i, j) for i in range(6) for j in range(6))

    def get_valid_moves(self):
        valid_moves = []
        for i in range(6):
            for j in range(6):
                if self.is_valid_move(i, j):
                    valid_moves.append((i, j))
        return valid_moves

games = {}  # ゲーム状態を保持するための辞書

def render_board(board, game):
    current_player_str = f"現在のターン: {game.current_player}"
    letters = [':regional_indicator_a:', ':regional_indicator_b:', ':regional_indicator_c:', ':regional_indicator_d:', ':regional_indicator_e:', ':regional_indicator_f:']
    
    result = current_player_str + '\n' + ':white_medium_square: ' + ' '.join(letters) + '\n'
    for i, row in enumerate(board):
        result += letters[i] + ' '
        for cell in row:
            if cell == ' ':
                result += ':white_medium_square: '
            else:
                result += cell + ' '
        result += '\n'
    return result

def setup(bot):
    @bot.tree.command(name='othello_start', description='新しいオセロを始めます')
    async def start_game(interaction: discord.Interaction):
        channel_id = interaction.channel_id
        if channel_id in games:
            await interaction.response.send_message('このチャンネルで既にゲームが進行中です。', ephemeral=True)
            return

        await interaction.response.defer()  # 応答を保留にする
        game = OthelloGame()
        message = await interaction.followup.send('新しいゲームを開始しました。\n' + render_board(game.board, game))  # メッセージを送信し、戻り値を取得
        game.last_message_id = message.id  # 初期盤面メッセージのIDを記録
        games[channel_id] = game

    @bot.tree.command(name='othello_place', description='指定した位置にコマを置きます')
    async def place_piece(interaction: discord.Interaction, col: str, row: str):
        channel_id = interaction.channel_id
        if channel_id not in games:
            await interaction.response.defer(ephemeral=True)  # 応答を保留にし、ephemeralをTrueに設定
            await interaction.followup.send('このチャンネルでゲームが開始されていません。', ephemeral=True)
            return

        game = games[channel_id]

        col = col.lower()
        row = row.lower()
        if len(col) != 1 or len(row) != 1 or col < 'a' or col > 'f' or row < 'a' or row > 'f':
            await interaction.response.defer(ephemeral=True)  # 応答を保留にし、ephemeralをTrueに設定
            await interaction.followup.send('無効な列または行です。列と行はa-fの一文字で指定してください。', ephemeral=True)
            return

        col_index = ord(col) - ord('a')
        row_index = ord(row) - ord('a')

        if not game.is_valid_move(row_index, col_index):
            await interaction.response.defer(ephemeral=True)  # 応答を保留にし、ephemeralをTrueに設定
            await interaction.followup.send('無効な移動です。', ephemeral=True)
            return

        game.board[row_index][col_index] = game.current_player
        game.flip_pieces(row_index, col_index)
        game.switch_player()

        # 盤面を全員に表示する通常のメッセージとして送信
        await interaction.response.defer(ephemeral=False)  # 応答を保留にし、ephemeralをFalseに設定
        new_message = await interaction.followup.send(render_board(game.board, game))
        game.last_message_id = new_message.id

        if game.is_game_over():
            winner = ':black_circle:' if game.count_pieces(':black_circle:') > game.count_pieces(':white_circle:') else ':white_circle:'
            await interaction.channel.send(f'ゲーム終了！ 勝者: {winner}')
            del games[channel_id]

    @bot.tree.command(name='othello_pass', description='手番をパスします')
    async def pass_turn(interaction: discord.Interaction):
        channel_id = interaction.channel_id
        if channel_id not in games:
            await interaction.response.send_message('このチャンネルでゲームが開始されていません。', ephemeral=True)
            return

        game = games[channel_id]

        # 手番を次のプレイヤーに渡す
        game.switch_player()

        # 応答の保留を解除
        await interaction.response.defer()

        # 盤面を全員に表示する通常のメッセージとして送信
        new_message = await interaction.followup.send(render_board(game.board, game))
        game.last_message_id = new_message.id

    @bot.tree.command(name='othello_end', description='オセロを強制終了します')
    async def end_game(interaction: discord.Interaction):
        channel_id = interaction.channel_id
        if channel_id in games:
            del games[channel_id]
            await interaction.response.send_message('ゲームを強制終了しました。')
        else:
            await interaction.response.send_message('アクティブなゲームが見つかりません。')

    @bot.tree.command(name='othello_show', description='現在のオセロの盤面を表示します')
    async def show_board(interaction: discord.Interaction):
        channel_id = interaction.channel_id
        if channel_id not in games:
            await interaction.response.send_message('このチャンネルでゲームが開始されていません。', ephemeral=True)
            return

        game = games[channel_id]
        await interaction.response.send_message(render_board(game.board, game))
