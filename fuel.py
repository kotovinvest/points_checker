import requests
import pandas as pd
from itertools import cycle

def read_wallets(file_path):
    with open(file_path, 'r') as file:
        wallets = [line.strip() for line in file.readlines()]
    return wallets

def read_proxies(file_path):
    with open(file_path, 'r') as file:
        proxies = [line.strip() for line in file.readlines()]
    if not proxies:
        raise ValueError("Файл proxy.txt пуст. Добавьте прокси.")
    return proxies

def get_wallet_data(wallet_address, proxy):
    url = f'https://app.fuel.network/earn-points/api/points/{wallet_address}'
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

def process_data(wallets, proxies):
    data = []
    proxy_cycle = cycle(proxies)

    for wallet in wallets:
        current_proxy = next(proxy_cycle)
        wallet_data = get_wallet_data(wallet, current_proxy)
        if wallet_data:
            wallet_address = wallet_data.get("wallet_address", wallet)
            user_rank = wallet_data.get("user_rank", 0)
            total_points = wallet_data.get("total_points", 0)

            data.append({
                'wallet_address': wallet_address,
                'user_rank': user_rank,
                'total_points': total_points
            })

            print(f"Кошелек: {wallet_address}")
            print(f"Ранг пользователя: {user_rank}")
            print(f"Общее количество очков: {total_points}")
            print(f"Использован прокси: {current_proxy}")
            print("="*30)

    if data:
        df = pd.DataFrame(data)
        df.to_excel('fuel_wallets_data.xlsx', index=False)
        print("Данные успешно сохранены в fuel_wallets_data.xlsx")
    else:
        print("Не удалось получить данные ни для одного кошелька.")
