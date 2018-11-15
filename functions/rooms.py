import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
import warnings

warnings.simplefilter('ignore')
from pylab import rcParams

rcParams['figure.figsize'] = 8, 5

import time

df = pd.read_csv('data.csv', sep='~', encoding='utf-8',
                 usecols=['ContingentUnitCourse', 'ContingentUnitName', 'DivisionsString', 'DivisionName', 'Start',
                          'End', 'EducatorAssignment', 'LocationsDisplayText', 'Subject'])
df.columns = ['Start', 'End', 'Курс', 'Номер группы', 'Факультет1', 'Факультет2', 'Преподаватель', 'Адрес', 'Предмет']
df['Вид занятия'] = df['Предмет'].str.split(',').str.get(1)
df['Предмет'] = df['Предмет'].str.split(',').str.get(0)
df['День'] = df['Start'].str.split(' ').str.get(0)
df['Время начала'] = df['Start'].str.split(' ').str.get(1)
df['Время окончания'] = df['End'].str.split(' ').str.get(1)
df['Факультет'] = df['Факультет1'].fillna(df['Факультет2'])
df['Аудитория'] = df['Адрес'].str.split(',').str.get(-1)
df['Корпус'] = df['Адрес'].str.split(',').str.get(0) + df['Адрес'].str.split(',').str.get(1)


def timeConvert(x):
    return int(x[0] + x[1]) * 60 + int(x[3] + x[4])


df['Начало(мин)'] = df['Время начала'].apply(timeConvert)
df['Окончание(мин)'] = df['Время окончания'].apply(timeConvert)


def convert(x):
    x = x.tm_wday
    if x == 0:
        return 'пн'
    elif x == 1:
        return 'вт'
    elif x == 2:
        return 'ср'
    elif x == 3:
        return 'чт'
    elif x == 4:
        return 'пт'
    elif x == 5:
        return 'сб'


df['День недели'] = (df['День'].apply(time.strptime, args=('%Y-%m-%d',))).apply(convert)
df = pd.concat([df[df['День недели'] == 'пн'], df[df['День недели'] == 'вт'], df[df['День недели'] == 'ср'],
                df[df['День недели'] == 'чт'], df[df['День недели'] == 'пт'], df[df['День недели'] == 'сб']],
               ignore_index=True)
df['Day'] = df['День'].apply(time.strptime, args=('%Y-%m-%d',))


def weekNumber(x):
    return time.strftime("%W", time.strptime(x, "%Y-%m-%d"))


def dayNumber(x):
    return time.strftime("%j", time.strptime(x, "%Y-%m-%d"))


df['Номер недели'] = df['День'].apply(weekNumber)
df['Номер дня'] = df['День'].apply(dayNumber)
df = df[['Номер группы', 'Факультет', 'Курс', 'Преподаватель', 'Адрес', 'Корпус', 'Аудитория', 'Предмет', 'Вид занятия',
         'День', 'День недели', 'Номер дня', 'Номер недели', 'Время начала', 'Начало(мин)', 'Время окончания',
         'Окончание(мин)']]

df['Номер дня'] = df['Номер дня'].apply(int)


# -----------------------------------------------------------------------------------------


# Список свободных аудиторий в определенный промежуток времени на факультете
def tool_1_2(corp, startDay, startTime, stopDay, stopTime):
    dff = df[df['Корпус'] == corp]

    begin = int(startTime[0] + startTime[1]) * 60 + int(startTime[3] + startTime[4])
    end = int(stopTime[0] + stopTime[1]) * 60 + int(stopTime[3] + stopTime[4])

    startDayNumber = int(time.strftime("%j", time.strptime(startDay, "%Y-%m-%d")))
    stopDayNumber = int(time.strftime("%j", time.strptime(stopDay, "%Y-%m-%d")))

    classroomList = pd.unique(dff['Адрес'])
    result = np.zeros(len(classroomList))

    dff = dff[(dff['Номер дня'] >= startDayNumber) & (dff['Номер дня'] < stopDayNumber)]

    def isEmpty(row):
        for j, room in enumerate(classroomList):
            if row['Адрес'] == room:
                if row['Номер дня'] == startDayNumber:
                    if begin < row['Окончание(мин)']:
                        result[j] += 1
                elif row['Номер дня'] == stopDayNumber - 1:
                    if end > row['Начало(мин)']:
                        result[j] += 1
                else:
                    result[j] += 1

    dff.apply(lambda row: isEmpty(row), axis=1)

    print('Свободные аудитории с ', startTime, startDay, ' до ', stopTime, stopDay)
    x = np.array([])
    for i, room in enumerate(classroomList):
        if result[i] == 0:
            x = np.append(x, room)

    return 1, x

# Расписание аудитории
def tool_1_3(number):
    x = df[(df['Адрес'] == number)]
    x = x.sort_values(by=['Номер дня', 'Начало(мин)'], ascending=[True, True])
    return 1, x

