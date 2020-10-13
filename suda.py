from random import Random
import copy


# class with backtracking algorithm for finding possible values
class SudokuSolver:
    def solve(puzzle):
        solution = copy.deepcopy(puzzle)
        if SudokuSolver.solveHelper(solution):
            return solution
        return None

    #solving sudoku matrix
    def solveHelper(solution):
        minPossibleValueCountCell = None
        while True:
            minPossibleValueCountCell = None
            for rowIndex in range(9):
                for columnIndex in range(9):
                    if solution[rowIndex][columnIndex] != 0:
                        continue
                    possibleValues = SudokuSolver.findPossibleValues(rowIndex, columnIndex, solution)
                    possibleValueCount = len(possibleValues)
                    if possibleValueCount == 0:
                        return False
                    if possibleValueCount == 1:
                        solution[rowIndex][columnIndex] = possibleValues.pop()
                    if not (minPossibleValueCountCell and not (possibleValueCount < len(minPossibleValueCountCell[1]))):
                        minPossibleValueCountCell = ((rowIndex, columnIndex), possibleValues)
            if not minPossibleValueCountCell:
                return True
            elif 1 < len(minPossibleValueCountCell[1]):
                break
        r, c = minPossibleValueCountCell[0]
        for v in minPossibleValueCountCell[1]:
            solutionCopy = copy.deepcopy(solution)
            solutionCopy[r][c] = v
            if SudokuSolver.solveHelper(solutionCopy):
                for r in range(9):
                    for c in range(9):
                        solution[r][c] = solutionCopy[r][c]
                return True
        return False

    def findPossibleValues(rowIndex, columnIndex, puzzle):
        values = {v for v in range(1, 10)}
        values -= SudokuSolver.getRowValues(rowIndex, puzzle)
        values -= SudokuSolver.getColumnValues(columnIndex, puzzle)
        values -= SudokuSolver.getBlockValues(rowIndex, columnIndex, puzzle)
        return values

    def getRowValues(rowIndex, puzzle):
        return set(puzzle[rowIndex][:])

    def getColumnValues(columnIndex, puzzle):
        return {puzzle[r][columnIndex] for r in range(9)}

    def getBlockValues(rowIndex, columnIndex, puzzle):
        blockRowStart = 3 * (rowIndex // 3)
        blockColumnStart = 3 * (columnIndex // 3)
        return {
            puzzle[blockRowStart + r][blockColumnStart + c]
            for r in range(3)
            for c in range(3)
        }


def printPuzzle(puzzle):
    num = '   y  0  1  2  3  4  5  6  7  8'
    print(num)
    print('x')
    k = 0
    for row in puzzle:
        print(k, '  ', row)
        k += 1


#sudoku generation
class Sudoku:

    def sudoku_gen(self):
        sudoku = Sudoku.matrix_gen(row=9, col=9)
        for row in range(9):
            for col in range(9):
                random_number = Random.randrange(Random(), 0, 8) + 1
                if sudoku[row][col] == 0 and self.no_conflict(sudoku, row, col, random_number):
                    sudoku[row][col] = random_number
        return sudoku

    @staticmethod
    def matrix_gen(row, col):
        array = [0] * col
        for i in range(col):
            array[i] = [0] * row
        return array

    @staticmethod
    def no_conflict(array, row, col, random_number):
        for x in range(9):
            if array[row][x] == random_number:
                return False
            if array[x][col] == random_number:
                return False

        dig_max = row - (row % 3)
        dig_min = col - (col % 3)
        for k in range(dig_max, dig_max + 3):
            for p in range(dig_min, dig_min + 3):
                if array[k][p] == random_number:
                    return False
        return True


def game(sudoku_update):
    gen = input("Choose level |easy|medium|hard|:")
    if gen == 'easy':
        for n in range(400):
            r = Random.randrange(Random(), 0, 9)
            c = Random.randrange(Random(), 0, 9)
            sudoku_update[r][c] = 0
    elif gen == 'medium':
        for n in range(600):
            r = Random.randrange(Random(), 0, 9)
            c = Random.randrange(Random(), 0, 9)
            sudoku_update[r][c] = 0

    elif gen == 'hard':
        for n in range(800):
            r = Random.randrange(Random(), 0, 9)
            c = Random.randrange(Random(), 0, 9)
            sudoku_update[r][c] = 0
    else:
        print('Invalid level')

    return sudoku_update


def get_sudoku():
    sud = Sudoku()
    sudoku = sud.sudoku_gen()
    solution = SudokuSolver.solve(sudoku)
    origin_board = SudokuSolver.solve(sudoku)
    update_sudoku = game(origin_board)
    count = 10
    while True:
        if count == 0:
            print("You lose")
            break
        print("Your lives", "❤"*count)
        printPuzzle(update_sudoku)
        x = int(input('Enter x pos: '))
        y = int(input('Enter y pos: '))
        if update_sudoku[x][y] != 0:
            print("Field is full")
        elif update_sudoku == solution:
            print("You win!!!!")
            break
        else:
            num = input("Enter number: ")
            if int(num) == solution[x][y]:
                update_sudoku[x][y] = int(num)
            else:
                print('Wrong number')
                count -= 1


if __name__ == '__main__':
    get_sudoku()


