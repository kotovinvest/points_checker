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
    url = f'https://app.ether.fi/api/portfolio/v3/{wallet_address}'
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
    if not proxies:
        print("Список прокси пуст! Проверьте файл proxy.txt.")
        return
    
    data = []
    proxy_cycle = cycle(proxies)

    for wallet in wallets:
        try:
            current_proxy = next(proxy_cycle)
        except StopIteration:
            print("Ошибка: закончились прокси. Проверьте файл proxy.txt.")
            return

        wallet_data = get_wallet_data(wallet, current_proxy)
        if wallet_data:
            points = wallet_data.get("totalLoyaltyPoints", 0)
            eigen_points = wallet_data.get("totalEigenlayerPoints", 0)
            s3_points = wallet_data.get("s3Points", 0)
            s1s2_points = wallet_data.get("s1s2Points", 0)

            data.append({
                'wallet': wallet,
                'totalLoyaltyPoints': points,
                'totalEigenlayerPoints': eigen_points,
                's3Points': s3_points,
                's1S2Points': s1s2_points
            })

            print(f"Кошелек: {wallet}")
            print(f"Total Loyalty Points: {points}")
            print(f"Total Eigenlayer Points: {eigen_points}")
            print(f"S3 Points: {s3_points}")
            print(f"S1S2 Points: {s1s2_points}")
            print(f"Использован прокси: {current_proxy}")
            print("="*30)

    if data:
        df = pd.DataFrame(data)
        df.to_excel('ethfi_wallets_data.xlsx', index=False)
        print("Данные успешно сохранены в ethfi_wallets_data.xlsx")
    else:
        print("Не удалось получить данные ни для одного кошелька.")
