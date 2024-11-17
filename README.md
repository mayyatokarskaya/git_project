# Project Title

## Описание

Этот проект предназначен для обработки и анализа данных, включая сортировку записей по дате и фильтрацию записей по статусу. В проекте реализована структура по методологии **GitFlow** для удобной работы с несколькими ветками и совместной разработки. Основные функции реализованы в модуле `processing` внутри директории `src`.

## Функциональность

Проект включает в себя:

1. **Создание и управление ветками Git по GitFlow.**
2. **Загрузка проекта в удалённый репозиторий GitHub** для возможности командной работы.
3. **Реализация функций для обработки данных**:
   - `sort_by_date`: сортирует список словарей по дате.
   - `filter_by_state`: фильтрует список словарей по заданному статусу.

## Установка и настройка

1. **Клонирование репозитория**
   
   Сначала клонируйте репозиторий с GitHub на локальную машину:

   ```bash
   git clone <URL репозитория>
   cd <имя директории>
   ```

2. **Создание веток для работы по GitFlow**

   Для работы над различными частями проекта создайте новые ветки:

   ```bash
   git checkout -b feature/<название фичи>
   ```

3. **Подготовка репозитория**

   После создания локального репозитория добавьте файлы:

   ```bash
   git add .
   ```

   Затем сделайте коммит с описанием изменений:

   ```bash
   git commit -m "Описание изменений"
   ```

   После коммита изменения отправляются в удалённый репозиторий:

   ```bash
   git push origin <имя ветки>
   ```

## Описание модулей

### Модуль `processing`

В модуле `processing`, расположенном в директории `src`, реализованы две основные функции:

- **sort_by_date(data: list, reverse: bool = True) -> list**

  Функция принимает список словарей, каждый из которых содержит ключ `date` (дата записи). Функция сортирует записи по дате в порядке убывания (по умолчанию). Опционально можно изменить порядок сортировки, передав параметр `reverse=False`.

- **filter_by_state(data: list, state: str = 'EXECUTED') -> list**

  Функция принимает список словарей и значение `state` (по умолчанию — `'EXECUTED'`). Она возвращает новый список, содержащий только те записи, у которых поле `state` соответствует заданному значению.

  
## Команды Git для работы над проектом

### Добавление изменений

```bash
git add .
```

### Коммит изменений

```bash
git commit -m "Описание коммита"
```

### Отправка изменений на GitHub

```bash
git push origin <имя ветки>
```