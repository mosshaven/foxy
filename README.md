# что это?

фокси - это развлекательный чат-бот для телеграма с экономикой, мини-играми и рп командами.

# установка

## Linux

### зависимости
**Ubuntu / Debian:**
```bash
sudo apt install git python3 python3-pip nano
```

**Arch:**
```bash
sudo pacman -S git python python-pip nano
```

### клонирование и установка
```bash
git clone https://github.com/mosshaven/foxy
cd foxy
pip install uv --break-system-packages
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

### настройка
```bash
mv data/config.py.example data/config.py
nano data/config.py  # заполни токен, api_id, api_hash, admin
```

### запуск
```bash
python main.py
```

---

## Windows

### установка python
1. скачай [python 3.11+](https://www.python.org/downloads/)
2. при установке **обязательно** поставь галочку "Add python.exe to PATH"
3. после установки нажми "Disable path length limit"

### скачивание бота
1. нажми `Code` → `Download ZIP`
2. разархивируй в удобное место

### установка зависимостей
1. открой папку `foxy` в проводнике
2. кликни по адресной строке, напиши `cmd` и нажми Enter
3. в консоли выполни:
```bash
pip install uv
uv pip install -r requirements.txt
```

### настройка
1. переименуй `data\config.py.example` в `data\config.py`
2. открой `data\config.py` блокнотом и заполни:
   - `bot_token` - получи у [@BotFather](https://t.me/BotFather)
   - `api_id` и `api_hash` - получи на [my.telegram.org](https://my.telegram.org)
   - `admin` - твой telegram ID (узнай у [@userinfobot](https://t.me/userinfobot))

### запуск
```bash
py main.py
```

---

## миграция базы данных

если обновляешь бота и появились новые поля в БД:
```bash
python migrate_db.py
```

---

# команды

## экономика
- `/pizza` или `пицца` - сожрать пиццу (кд 15 мин)
- `/case` или `кейс` - открыть кейс (кд 24 часа)
- `/dice [кол-во]` или `кубик [кол-во]` - бросить кубики
- `/casino [ставка]` или `казино [ставка]` - казино (шанс 11%, x3)
- `/shop` или `магазин` - магазин
- `/pay [сумма] [id]` - перевести ФБ
- `/me` или `б` - статистика
- `/top` или `топ` - рейтинг жирдяев

## рп команды (только русский)
- `обнять [юзер]` - обнять
- `привет [юзер]` - поздороваться
- `поцеловать [юзер]` - поцеловать
- `ударить [юзер]` - ударить
- `выебать [юзер]` - выебать
*[юзер] - ответ на сообщение*

## админ команды
- `/give [id] [кол-во]` - выдать ФБ
- `/give_pizzas [id] [кол-во]` - выдать пиццы
- `/give_cubes [id] [кол-во]` - выдать кубики

---

# фичи

- **пиццерия**: при >= 1000 пицц получаешь доход раз в день (пиццы/100 = ФБ/день)
- **глобальный кулдаун**: 3 сек между командами
- **логирование**: раздельные логи (logs.log, errors.log)

---

# лицензия

GPL v3: ты можешь использовать и распространять мой код. **НО**, если ты изменяшь код, ты ОБЯЗАН(-А) открыть исходный код.
