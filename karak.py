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
    url = f'https://restaking-backend.karak.network/getPortfolio,getActivity?batch=1&input={{"0":{{"wallet":"{wallet_address}"}},"1":{{"wallet":"{wallet_address}"}}}}'
    proxies = {
        'http': f'http://{proxy}',
        'https': f'http://{proxy}'
    }
    
    try:
        response = requests.get(url, proxies=proxies)
        
        if response.status_code == 200:
            try:
                json_response = response.json()
                # Проверка на наличие ошибки в ответе
                if "error" in json_response[0]:
                    error_info = json_response[0]["error"]
                    print(f"Ошибка для кошелька {wallet_address}: {error_info}")
                    return {"xp": 0}  # Устанавливаем XP в 0 при ошибке
                # Извлечение значения "xp" из ответа
                xp = json_response[0]["result"]["data"].get("xp", 0)
                return {"xp": xp}
            except ValueError as ve:
                print(f"Ошибка при разборе JSON ответа для кошелька {wallet_address}: {ve}")
                return {"xp": 0}  # Устанавливаем XP в 0 при ошибке разбора
        else:
            print(f"Ошибка при запросе для кошелька {wallet_address}: {response.status_code}")
            return {"xp": 0}  # Устанавливаем XP в 0 при ошибке запроса
    except Exception as e:
        print(f"Ошибка подключения для кошелька {wallet_address} с прокси {proxy}: {str(e)}")
        return {"xp": 0}  # Устанавливаем XP в 0 при ошибке подключения

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
            xp = wallet_data.get("xp", 0)

            data.append({
                'wallet': wallet,
                'xp': xp
            })

            print(f"Кошелек: {wallet}")
            print(f"XP: {xp}")
            print(f"Использован прокси: {current_proxy}")
            print("="*30)

    if data:
        df = pd.DataFrame(data)
        df.to_excel('karak_wallets_data.xlsx', index=False)
        print("Данные успешно сохранены в karak_wallets_data.xlsx")
    else:
        print("Не удалось получить данные ни для одного кошелька.")

if __name__ == "__main__":
    try:
        wallets = read_wallets('wallets.txt')
        proxies = read_proxies('proxy.txt')

        if not wallets:
            print("Файл wallets.txt пуст или не содержит валидных адресов.")
        else:
            process_data(wallets, proxies)
    
    except ValueError as ve:
        print(f"Ошибка: {ve}")
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {str(e)}")
