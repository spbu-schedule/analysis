import os

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
df['Day'] = df['День'].apply(time.strptime, args=('%Y-%m-%d',))


def weekNumber(x):
    return time.strftime("%W", time.strptime(x, "%Y-%m-%d"))


df['Номер недели'] = df['День'].apply(weekNumber)
df = df[['Номер группы', 'Факультет', 'Курс', 'Преподаватель', 'Адрес', 'Предмет', 'Вид занятия', 'День', 'День недели',
         'Номер недели', 'Время начала', 'Время окончания']]


# -----------------------------------------------------------------------------------

# Количество занятий по дням недели для учебных групп
def tool_3_1(faculty, group, day):
    name = 'tool_3_1~' + faculty + '~' + group + '~' + day + '.svg'
    if os.path.isfile(name):
        return 0, name
    week = time.strftime("%W", time.strptime(day, "%Y-%m-%d"))
    sns.countplot(
        df[(df['Номер группы'] == group) & (df['Факультет'] == faculty) & (df['Номер недели'] == week)]['День недели'])
    plt.title('Количество пар для определенной группы по дням недели')
    plt.savefig(name)
    return 0, name


# Количество занятий конкретной дисциплины в семестре для учебных групп
def tool_3_2(faculty, group, lesson):
    return 1, df[(df['Номер группы'] == group) & (df['Предмет'] == lesson) & (df['Факультет'] == faculty)][
        'Предмет'].count()


# Количество пар в неделю по дисциплинам
def tool_3_3(faculty, group, day):
    name = 'tool_3_3~' + faculty + '~' + group + '~' + day + '.svg'
    if os.path.isfile(name):
        return 0, name
    week = time.strftime("%W", time.strptime(day, "%Y-%m-%d"))
    sns.countplot(
        df[(df['Номер группы'] == group) & (df['Факультет'] == faculty) & (df['Номер недели'] == week)]['Предмет'])
    plt.title('Сравнение количества занятий по различным дисциплинам')
    plt.xticks(rotation=90)
    plt.savefig(name)
    return 0, name


# Соотношение лекций/практик по дисциплинам учебных групп
def tool_3_4(faculty, group, lesson):
    name = 'tool_3_4~' + faculty + '~' + group + '~' + lesson + '.svg'
    if os.path.isfile(name):
        return 0, name
    sns.countplot(
        df[(df['Номер группы'] == group) & (df['Предмет'] == lesson) & (df['Факультет'] == faculty)]['Вид занятия'])
    plt.title('Количество пар для определенного преподавателя по дням недели')
    plt.savefig(name)
    return 0, name


# Общая занятость факультетов
def tool_3_5(faculty, day):
    name = 'tool_3_5~' + faculty + '~' + day + '.svg'
    if os.path.isfile(name):
        return 0, name
    week = time.strftime("%W", time.strptime(day, "%Y-%m-%d"))
    sns.countplot(df[(df['Факультет'] == faculty) & (df['Номер недели'] == week)]['День недели'])
    plt.ylabel('Количество пар')
    plt.title('Загруженность факультета')
    plt.savefig(name)
    return 0, name


