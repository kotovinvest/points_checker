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

# Получение данных из API
def get_wallet_data(wallet_address, proxy):
    url = f'https://app.usual.money/api/points/{wallet_address}'
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
        current_proxy = next(proxy_cycle)  # Получаем следующий прокси
        wallet_data = get_wallet_data(wallet, current_proxy)
        if wallet_data:
            # Извлечение нужных полей и конвертация значений
            referral_points = int(wallet_data.get("referralPoints", "0")) / 1e18
            reward_points = int(wallet_data.get("rewardPoints", "0")) / 1e18
            total_points = int(wallet_data.get("totalPoints", "0")) / 1e18
            leaderboard_position = wallet_data.get("leaderboardPosition", "Unknown")

            # Добавление данных в список
            data.append({
                'wallet': wallet,
                'referralPoints': referral_points,
                'rewardPoints': reward_points,
                'totalPoints': total_points,
                'leaderboardPosition': leaderboard_position
            })

            # Вывод данных в терминал
            print(f"Кошелек: {wallet}")
            print(f"Referral Points: {referral_points}")
            print(f"Reward Points: {reward_points}")
            print(f"Total Points: {total_points}")
            print(f"Leaderboard Position: {leaderboard_position}")
            print(f"Использован прокси: {current_proxy}")
            print("="*30)

    # Создание и сохранение Excel файла
    if data:
        df = pd.DataFrame(data)
        df.to_excel('usual_wallets_data.xlsx', index=False)
        print("Данные успешно сохранены в usual_wallets_data.xlsx")
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
