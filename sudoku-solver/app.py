from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def find_empty(board):
    """Find an empty cell in the board."""
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return i, j
    return None

def is_valid(board, num, pos):
    """Check if a number is valid in the given position."""
    # Check row
    for j in range(9):
        if board[pos[0]][j] == num and pos[1] != j:
            return False
            
    # Check column
    for i in range(9):
        if board[i][pos[1]] == num and pos[0] != i:
            return False
            
    # Check 3x3 box
    box_x, box_y = pos[1] // 3, pos[0] // 3
    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if board[i][j] == num and (i, j) != pos:
                return False
                
    return True

def solve(board):
    """Solve the Sudoku puzzle using backtracking."""
    empty = find_empty(board)
    if not empty:
        return True
        
    row, col = empty
    for num in range(1, 10):
        if is_valid(board, num, (row, col)):
            board[row][col] = num
            if solve(board):
                return True
            board[row][col] = 0
            
    return False

def validate_board(board):
    """Validate the input board."""
    if not isinstance(board, list) or len(board) != 9:
        return False
    for row in board:
        if not isinstance(row, list) or len(row) != 9:
            return False
        for cell in row:
            if not isinstance(cell, int) or cell < 0 or cell > 9:
                return False
    return True

@app.route('/')
def index():
    return render_template('sudoku_solver.html')

@app.route('/solve', methods=['POST'])
def solve_sudoku():
    try:
        data = request.get_json()
        board = data.get('board')
        
        if not validate_board(board):
            return jsonify({'error': 'Invalid board format'}), 400
            
        # Create a copy of the board to avoid modifying the original
        board_copy = [row[:] for row in board]
        
        if solve(board_copy):
            return jsonify({'solved': True, 'board': board_copy})
        else:
            return jsonify({'solved': False, 'error': 'No solution exists'})
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)