import asyncio
import json
import aiofiles
import random
from datetime import datetime

CATEGORIES = ["Food", "Transport", "Utilities", "Education", "Health", "Agenda"]

async def generate_transactions(num_transactions):
    transactions = []
    for _ in range(num_transactions):
        transaction = {
            "timestamp": datetime.now().isoformat(),
            "category": random.choice(CATEGORIES),
            "amount": round(random.uniform(1, 150000), 2) 
        }
        transactions.append(transaction)

        # Сохраняем каждые 10 записей в файл
        if len(transactions) == 10:
            await save_to_file(transactions)
            transactions.clear()  

    # Сохраняем оставшиеся транзакции
    if transactions:
        await save_to_file(transactions)

async def save_to_file(transactions):
    file_name = 'transactions.json'
    
    # Записываем транзакции в файл асинхронно
    try:
        async with aiofiles.open(file_name, 'a') as f:
            # Группируем записи, оборачивая их в массив JSON
            group = {"transactions": transactions}
            await f.write(json.dumps(group) + '\n') 
        print(f'Сохранено {len(transactions)} транзакций в файл {file_name}')
    except Exception as e:
        print(f'Ошибка сохранения: {e}')

async def main(num_transactions):
    await generate_transactions(num_transactions)

if __name__ == "__main__":
    num_transactions = int(input("Сколько нужно сгенерить транзакций(введите значение): "))
    asyncio.run(main(num_transactions))


