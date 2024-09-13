import requests
import pandas as pd
from itertools import cycle

# Чтение адресов кошельков из файла wallets.txt
def read_wallets(file_path):
    with open(file_path, 'r') as file:
        wallets = [line.strip() for line in file.readlines()]
    return wallets

# Чтение прокси данных из файла proxy.txt
def read_proxies(file_path):
    with open(file_path, 'r') as file:
        proxies = [line.strip() for line in file.readlines()]
    if not proxies:
        raise ValueError("Файл proxy.txt пуст. Добавьте прокси.")
    return proxies

# Получение данных из API Reya с использованием прокси
def get_wallet_data(wallet_address, proxy):
    url = f'https://api.reya.xyz/api/xp/user-leaderboard-v4-data/{wallet_address}'
    proxies = {
        'http': f'http://{proxy}',
        'https': f'http://{proxy}'
    }
    
    try:
        response = requests.get(url, proxies=proxies)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Ошибка при запросе для кошелька {wallet_address}: {response.status_code}")
            return None
    except Exception as e:
        print(f"Ошибка подключения для кошелька {wallet_address} с прокси {proxy}: {str(e)}")
        return None

# Обработка данных и запись в Excel
def process_data(wallets, proxies):
    if not proxies:
        print("Список прокси пуст! Проверьте файл proxy.txt.")
        return
    
    data = []
    proxy_cycle = cycle(proxies)  # Цикл для чередования прокси

    for wallet in wallets:
        try:
            current_proxy = next(proxy_cycle)  # Получаем следующий прокси
        except StopIteration:
            print("Ошибка: закончились прокси. Проверьте файл proxy.txt.")
            return

        wallet_data = get_wallet_data(wallet, current_proxy)
        if wallet_data:
            # Извлечение нужных полей
            value = wallet_data.get("tranchesOG", {}).get("value", 0)
            rank_name = wallet_data.get("rank", {}).get("rankName", "Unknown")
            ranking = wallet_data.get("ranking", 0)
            liquidity_xp = wallet_data.get("liquidityXp", 0)
            trading_xp = wallet_data.get("tradingXp", 0)
            total_xp = liquidity_xp + trading_xp

            # Добавление данных в список
            data.append({
                'wallet': wallet,
                'value': value,
                'rank_name': rank_name,
                'ranking': ranking,
                'liquidity_xp': liquidity_xp,
                'trading_xp': trading_xp,
                'total_xp': total_xp
            })

            # Вывод данных в терминал
            print(f"Кошелек: {wallet}")
            print(f"Value: {value}")
            print(f"Rank Name: {rank_name}")
            print(f"Ranking: {ranking}")
            print(f"Liquidity XP: {liquidity_xp}")
            print(f"Trading XP: {trading_xp}")
            print(f"Total XP: {total_xp}")
            print(f"Использован прокси: {current_proxy}")
            print("="*30)

    # Создание и сохранение Excel файла
    if data:
        df = pd.DataFrame(data)
        df.to_excel('reya_wallets_data.xlsx', index=False)
        print("Данные успешно сохранены в reya_wallets_data.xlsx")
    else:
        print("Не удалось получить данные ни для одного кошелька.")

# Главная функция
def main():
    try:
        wallets = read_wallets('wallets.txt')
        proxies = read_proxies('proxy.txt')

        if not wallets:
            print("Файл wallets.txt пуст или не содержит валидных адресов.")
            return

        process_data(wallets, proxies)
    
    except ValueError as ve:
        print(f"Ошибка: {ve}")
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {str(e)}")

if __name__ == "__main__":
    main()
