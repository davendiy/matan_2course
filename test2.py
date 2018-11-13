#!/usr/bin/env sage
# -*-encoding: utf-8-*-

# by David Zashkol
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com


# -----------------------------------------task 1-----------------------------------------------------------------------

# словник, ключами якого є групи, які треба задати, а значення - відповідний індекс
dict_groups = {DihedralGroup: 10,
               CyclicPermutationGroup: 16,
               AlternatingGroup: 5}


# проходимо циклом по групам
for group, index in dict_groups.items():
    tmp = group(index)              # створюємо групу
    print("Group: " + str(tmp))     # виводимо інфу
    print(tmp.cayley_table())
    print("group's order: " + str(tmp.order()))
    print("is abelian: " + str(tmp.is_abelian()))
    raw_input('\nPress enter to continue...\n')


# -----------------------------------------task 2-----------------------------------------------------------------------

# намагався реалізувати той алгоритм, який розбирали на лабі
# через брак часу (верніш через те, що провтикав дедлайни) я його не додебажив,
# а брати чужий код совість і гордість не дозволяє, тому написав просто перебір

tmp_dict = {}
for group in [SymmetricGroup, AlternatingGroup]:
    print("\nfind orders for all elements of {}...".format(group.__name__))
    for el in group(100):              # так як метод максимально довго працює, перевіряв тільки для 15
        tmp = el.order()
        if tmp in tmp_dict:
            tmp_dict[tmp] += 1
        else:
            tmp_dict[tmp] = 1

    for el, count in tmp_dict.items():
        print("{} : {}".format(el, count))

raw_input("Press enter to continue...")


# -----------------------------------------task 3-----------------------------------------------------------------------
def is_order_in(order, n):
    """
    функція перевірки існування елемента з даним порядком
    в групі підстановок довжини n

    по складності зводиться до складності факторизації порядку
    :param order: порядок
    :param n: довжина підстановок
    :return: bool
    """
    tmp_group = SymmetricGroup(n)

    # спочатку перевіряємо чи ділить шуканий порядок порядок групи
    if tmp_group.order() % order != 0:
        return False

    # у випадку, якщо ділить, то факторизуємо шуканий порядок
    tmp = factor(order)
    s = 0

    # нехай наше число order має розклад p1 ** s1 * p2 ** s2 ... * pm ** sm
    # оскільки p1 ** s1 + p2 ** s2 + ... + pm ** sm - мінімальна можлива сума, нск
    # доданків якої == order (????), то достатньо перевірити чи
    # буде ця сума меншою за n (якщо буде меншою, то ми отримуємо добуток циклів заданих довжин,
    # якщо ж буде більша, то це означає, що не існує такого розкладу n в суму чисел, нск яких == order)
    for devisor in tmp:
        s += devisor[0] ** devisor[1]

    return s <= n


print(is_order_in(12313, 1000))
print(is_order_in(235452, 10000))
ord = int(raw_input("order = "))
test_n = int(input('n = '))
