
k = int(input("k = "))

generator = (str(10 ** i) for i in range(k))   # генератор-вираз, який генерує степінь 10-ки

tmp_str = next(generator)    # 1-ий степінь 10-ки
k -= 1                       # зменшуємо к на 1, оскільки нумерація у python з 0
j = 0                        # індекс елемента всередині n-ого степеня 10-ки
tmp_len = len(tmp_str)       # довжина степеня 10-ки

for i in range(k):       # проходимо циклом до к
    j += 1               # збільшуємо індекс всередині степеня
    if j == tmp_len:     # якщо рядок-степінь закінчився, то генеруємо новий
        tmp_str = next(generator)
        tmp_len = len(tmp_str)
        j = 0                           # а індекс обнуляємо

result = tmp_str[j]
print(result)
