import os  # Импорт библиотеки для работы с файлами
import math

files = os.listdir("Сваи")  # Составляем список из имён файлов в папке "Сваи"
for file in files:
    file_open = open("Сваи/" + file, encoding='utf-8')  # Поочерёдно открываем файлы в папке "Сваи"
    file_list = file_open.readlines()  # Составляем список состоящий из строк файла
    file_list = file_list[3:]  # Срезом списка удаляем первые три ненужные строки

    # Создаём пустые списки для ключевых данных
    tiefe_list = []  # Глубина бурения
    bohrtisch_list = []  # Давление на двигатель бурильной головы в процессе бурения
    drehzahl_list = []  # Cкорость вращения
    beton_list = []  # Давление подачи бетонного раствора
    durchfluss_list = []  # Текущая скорость прокачки бетонного раствора
    gesamtmenge_list = []  # Общее количество уже поданного раствора
    stufenmenge_list = []  # Показывает сколько литров залито на каждый метр. Каждая следующая цифра это суммма
    # текущего значения и предыдущего на каждом отдельном метре
    tiefenstufe_list = []  # Показывает текущую глубину откидывая всё после запятой. Данный список используется
    # только как дополнительная информация необходимая для расчёта stufenmenge

    for line in file_list:
        broken_line = line.split(';')  # Разбиваем каждую строку по разделителю «;»
        # Далее записываем в каждй из ключевых списков свои данные
        tiefe_list.append(float(broken_line[1]))
        # 1-ый условный оператор для исключения нулей в bohrtisch_list
        if broken_line[2] == 0:
            pass
        else:
            bohrtisch_list.append(int(broken_line[2]))
        # 2-ой условный оператор для исключения нулей в drehzahl_list
        if broken_line[3] == 0:
            pass
        else:
            drehzahl_list.append(int(broken_line[3]))
        # 3-ий условный оператор для исключения нулей в beton_list
        if broken_line[4] == 0:
            pass
        else:
            beton_list.append(float(broken_line[4]))
        # 4-ый условный оператор для исключения нулей в durchfluss_list
        if broken_line[5] == 0:
            pass
        else:
            durchfluss_list.append(int(broken_line[5]))
        gesamtmenge_list.append(int(broken_line[6]))
        stufenmenge_list.append(int(broken_line[7]))
        tiefenstufe_list.append(int(broken_line[8]))

    # Далее происходит вычисление тех значений, ради которых был написан весь код
    # 1 - Ищем самую глубокую отметку до которой добурили
    max_tiefe = min(tiefe_list)
    # 2 - Ищем среднеарифметическое значение без учёта нулевых элементов
    mittig_value_bohrtisch = round((sum(bohrtisch_list) / len(bohrtisch_list)), 1)
    # 3 - Ищем среднеарифметическое значение без учёта нулевых элементов
    mittig_value_drehzahl = round((sum(drehzahl_list) / len(drehzahl_list)), 1)
    # 4 - Ищем среднеарифметическое значение без учёта нулевых элементов
    mittig_value_beton = round((sum(beton_list) / len(beton_list)), 1)
    # 5 - Ищем среднеарифметическое значение без учёта нулевых элементов
    mittig_value_durchfluss = round((sum(durchfluss_list) / len(durchfluss_list)), 1)
    # 6 - Ищем максимальное значение
    max_gesamtmenge = gesamtmenge_list[-1]
    # 7 - Ищем максимальное значение поданного раствора на каждый метр скважины
    max_stufenmenge_list = []  # Список заполнится после выполнения ниже цикла While
    modified_max_tiefe = math.ceil(abs(max_tiefe))  # Это модуль максимальной глубины округлённый вверх до целого числа
    zero_meter = 0  # Создадим переменную с нулевым метром на котором начинается бурение
    while zero_meter < modified_max_tiefe:
        i_empty_list = []  # Из tiefenstufe_list вытащим сюда индексы всех элементов равных текущему значению zero_meter
        for i_id, i_item in enumerate(tiefenstufe_list):
            if i_item == zero_meter:
                i_empty_list.append(i_id)
        j_empty_list = []  # Из stufenmenge_list вытащим сюда все элементов индексы которых есть в i_empty_list
        for j_id, j_item in enumerate(stufenmenge_list):
            if j_id in i_empty_list:
                j_empty_list.append(j_item)
        # Также два цикла выше можно было написать более коротко через генераторы списков сократив код на 6 строчек
        # i_empty_list = [i_id for i_id, i_item in enumerate(tiefenstufe_list) if i_item == zero_meter]
        # j_empty_list = [j_item for j_id, j_item in enumerate(stufenmenge_list) if j_id in i_empty_list]
        max_stufenmenge = max(j_empty_list)  # Ищем максимум раствора для текущего zero_meter
        max_stufenmenge_list.append(max_stufenmenge)  # Добавляем сюда максимумы для каждого метра
        zero_meter += 1  # Перед началом новой итерации цикла While увеличим zero_meter на 1 метр

    print('Маскимальняа глубина:', max_tiefe)
    print('Среднее давление:', mittig_value_bohrtisch)
    print('Средняя скорость вращения:', mittig_value_drehzahl)
    print('Среднее давление раствора:', mittig_value_beton)
    print('Максимальная скорость подачи раствора:', mittig_value_durchfluss)
    print('Всего подано раствора:', max_gesamtmenge)
    print('20 максималок одним списком:', max_stufenmenge_list)
