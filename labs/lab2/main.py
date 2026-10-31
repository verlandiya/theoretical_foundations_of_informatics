def participant_dict(line):
    if len(line) == 6:
        num, name, group, ex1, ex2, ex3 = line
        participant = {
            'num': int(num.strip()),
            'name': name.strip(),
            'group': group.strip(),
            'ex1': int(ex1.strip()),
            'ex2': int(ex2.strip()),
            'ex3': int(ex3.strip())}
        return participant
    else:
        return {}


def participant_category(score):
    if 240 <= score <= 300:
        return 'Отличный результат'
    elif 180 <= score <= 239:
        return 'Хороший результат'
    if 120 <= score <= 179:
        return 'Удовлетворительный результат'
    if score < 120:
        return 'Требуется подготовка'


participants = []
with open('input.txt', 'r', encoding='utf-8') as file:
    for line in file:
        line = line.split(';')
        participants.append(participant_dict(line))


line_index = 0
nums_list = []
scores = []
correct_participants = []

for participant in participants:
    line_index += 1
    flag = True

    if participant != {}:
        values = participant.values()
        num, name, group, ex1, ex2, ex3 = values

        if num <= 0 or num.is_integer() == False:
            print(f'Строка {line_index}: номер участника должен быть положительным целым числом')
            flag = False
        if name == '':
            print(f'Строка {line_index}: имя пользователя не должно быть пустым')
            flag = False
        if group == '':
            print(f'Строка {line_index}: название группы участника не должно быть пустым')
            flag = False
        if ex1.is_integer() == False or ex2.is_integer() == False or ex3.is_integer() == False:
            print(f'Строка {line_index}: каждый балл должен быть целым числом')
            flag = False
        if ex1 not in range(0, 101) or ex2 not in range(0, 101) or ex3 not in range(0, 101):
            print(f'Строка {line_index}: балл должен находиться в диапазоне от 0 до 100')
            flag = False
        if num in nums_list:
            print(f'Строка {line_index}: повторяющийся номер участника {num}')
            flag = False
        else:
            nums_list.append(num)
    else:
        print(f'Строка {line_index}: строка должна содержать шесть полей')
        flag = False

    if flag:
        values = participant.values()
        num, name, group, ex1, ex2, ex3 = values
        score = ex1 + ex2 + ex3
        average = round((ex1 + ex2 + ex3) / 3, 2)
        category = participant_category(score)
        scores.append([name, group, score, ex1, ex2, ex3])
        correct_participants.append(participant)


rating_scores = sorted(scores, key=lambda x: (-x[2], x[0]))



groups = {}
for person in scores:
    name, group, score, ex1, ex2, ex3 = person
    if group not in groups.keys():
        groups[group] = []
    groups[group].append([name, score])


unique_groups = set()
for person in scores:
    unique_groups.add(person[1])
unique_groups = sorted(unique_groups)


while True:
    print()
    print('МЕНЮ')
    print('1. Показать всех участников')
    print('2. Показать общий рейтинг')
    print('3. Найти участников по группе')
    print('4. Найти участников по части имени')
    print('5. Показать участников, прошедших отбор')
    print('6. Показать статистику')
    print('7. Сохранить отчёт')
    print('0. Завершить программу')

    choice = input('Выберите пункт меню')
    if choice == '1':
        for participant in correct_participants:
            values = participant.values()
            num, name, group, ex1, ex2, ex3 = values
            score = ex1 + ex2 + ex3
            average = round(score / 3, 2)
            category = participant_category(score)

            print(str(num) + ' ' + name + ' ' + str(group))
            print('балл за 3 задачи:', ex1, ex2, ex3)
            print('итоговый балл:', score)
            print('средний балл:', average)
            print('категория участника:', category)
            print()

    elif choice == '2':
        print('Рейтинг по итоговому баллу:')
        for el in rating_scores:
            print(str(el[0]) + ' ' + str(el[1]) + ': ' + str(el[2]))

    elif choice == '3':
        print('Введите название группы для поиска участников')
        need_group = input().lower().strip()
        for participant in correct_participants:
            if participant['group'].lower() == need_group:
                print(participant['num'], participant['name'])

    elif choice == '4':
        print('Введите часть имени участника для поиска')
        need_str = input().lower().strip()
        for participant in correct_participants:
            if need_str in participant['name'].lower():
                print(participant['name'])

    elif choice == '5':
        print('Участники прошедшие отбор')
        for person in scores:
            if person[2] >= 180:
                if person[3] >= 50 and person[4] >= 50 and person[5] >= 50:
                    print(person[0] + ' ' + person[1])

    elif choice == '6':
        print()
        print('Статистика по группам')
        for group in groups:
            group_scores = groups[group]

            count = len(group_scores)
            average = round(sum(person[1] for person in group_scores) / count, 2)
            max_score = max(person[1] for person in group_scores)

            best_participants = []

            for person in group_scores:
                if person[1] == max_score:
                    best_participants.append(person[0])

            print()
            print('Группа:', group)
            print('Количество участников:', count)
            print('Средний итоговый балл:', average)
            print('Максимальный итоговый балл:', max_score)
            print('Участники с максимальным результатом:', ', '.join(best_participants))

        print()

        print('Статистика по задачам')
        for i in range(3):
            task_scores = []

            for person in scores:
                task_scores.append(person[i + 3])

            if len(task_scores)>0:
                average = round(sum(task_scores)/len(task_scores), 2)
                min_score = min(task_scores)
                max_score = max(task_scores)

                print()
                print('Средний балл:', average)
                print('Минимальный балл:', min_score)
                print('Максимальный балл:', max_score)

        print()

        print('Уникальные группы')
        for group in unique_groups:
            print(group)


    elif choice == '7':
        with open('tournament_report.txt', 'w', encoding='utf-8') as file:
            file.write('Количество корректных записей: ' + str(len(scores)) + '\n')

            file.write('\nперечь уникальных групп:\n')
            for group in unique_groups:
                file.write(group + '\n')

            file.write('\nобщий рейтинг:\n')
            for person in rating_scores:
                file.write(person[0] + ' ' + person[1] + ': ' + str(person[2]) + '\n')

            file.write('\nучастники прошедшие отбор:\n')
            for person in scores:
                if person[2] >= 180:
                    if person[3] >= 50 and person[4] >= 50 and person[5] >= 50:
                        file.write(person[0] + ' ' + person[1] + '\n')

            file.write('\nстатистика по группам\n')

            for group in groups:
                group_scores = groups[group]
                count = len(group_scores)
                average = round(sum(person[1] for person in group_scores) / count, 2)
                max_score = max(person[1] for person in group_scores)
                best_participants = []

                for person in group_scores:
                    if person[1] == max_score:
                        best_participants.append(person[0])

                file.write('\nГруппа: ' + group + '\n')
                file.write('Количество участников: ' + str(count) + '\n')
                file.write('Средний балл: ' + str(average) + '\n')
                file.write('Максимальный балл: ' + str(max_score) + '\n')
                file.write('Лучшие участники: ' + ', '.join(best_participants) + '\n')

            file.write('\nстатистика по задачам\n')

            for i in range(3):
                task_scores = []

                for person in scores:
                    task_scores.append(person[i + 3])

                if len(task_scores) > 0:
                    file.write('\nЗадача ' + str(i + 1) + '\n')
                    file.write('Средний балл: ' + str(round(sum(task_scores) / len(task_scores), 2)) + '\n')
                    file.write('Минимальный балл: ' + str(min(task_scores)) + '\n')
                    file.write('Максимальный балл: ' + str(max(task_scores)) + '\n')

    elif choice == '0':
        print('Программа завершена')
        break

