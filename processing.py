import asyncio
import json
import aiofiles
from collections import defaultdict

async def process_transactions(file_name):
    category_sum = defaultdict(float)

    async with aiofiles.open(file_name, mode='r') as f:
        async for line in f:
            line = line.strip()  
            if not line:  
                continue
            try:
                # Загружаем данные
                transactions_data = json.loads(line)
                for transaction in transactions_data['transactions']:
                    category = transaction['category']
                    amount = transaction['amount']
                    category_sum[category] += amount
            except json.JSONDecodeError as e:
                print(f"Ошибка декодирования JSON: {e} для строки: {line}")

    return category_sum

async def processing_expenses(category_sum, all_sum):
    for category, total in category_sum.items():
        if total > all_sum:
            print(f'Превышены траты по категории "{category}": {total:.2f}₽')  # Вывод суммы 

async def main():
    file_name = 'transactions.json'
    all_sum = 68000 
    category_sum = await process_transactions(file_name)
    await processing_expenses(category_sum, all_sum)

if __name__ == "__main__":
    asyncio.run(main())



