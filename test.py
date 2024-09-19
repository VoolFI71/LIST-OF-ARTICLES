def maximalSquare(matrix):
    if not matrix:
        return 0, (-1, -1)  # Возвращаем 0 и недопустимые координаты

    m, n = len(matrix), len(matrix[0])
    dp = [[0] * n for _ in range(m)]
    max_side = 0
    max_coords = (-1, -1)  # Координаты левого верхнего угла

    for i in range(m):
        for j in range(n):
            if matrix[i][j] == '1':  # Проверяем на '1'
                if i == 0 or j == 0:
                    dp[i][j] = 1
                else:
                    dp[i][j] = min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) + 1
                
                # Обновляем максимальную сторону и координаты
                if dp[i][j] > max_side:
                    max_side = dp[i][j]
                    max_coords = (i - max_side + 1, j - max_side + 1)  # Левый верхний угол

    return max_side, max_coords  # Возвращаем длину стороны и координаты


m, n = map(int, input().split())
matrix = []
for i in range(m):
    row = input().strip()
    matrix.append(row)

side_length, top_left_coords = maximalSquare(matrix)

if side_length > 0:
    print(f"{side_length}")
    print(top_left_coords[0]+1, top_left_coords[1]+1)
