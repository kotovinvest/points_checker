import sys
import pandas as pd
from colorama import init, Fore, Style
from fuel import process_data as process_fuel_data, read_wallets as read_fuel_wallets, read_proxies as read_fuel_proxies
from ethfi import process_data as process_ethfi_data, read_wallets as read_ethfi_wallets, read_proxies as read_ethfi_proxies
from karak import process_data as process_karak_data, read_wallets as read_karak_wallets, read_proxies as read_karak_proxies
from reya import process_data as process_reya_data, read_wallets as read_reya_wallets, read_proxies as read_reya_proxies
from usual import process_data as process_usual_data, read_wallets as read_usual_wallets, read_proxies as read_usual_proxies

# Инициализация colorama
init(autoreset=True)

def run_fuel():
    wallets = read_fuel_wallets('wallets.txt')
    proxies = read_fuel_proxies('proxy.txt')
    return process_fuel_data(wallets, proxies)

def run_ethfi():
    wallets = read_ethfi_wallets('wallets.txt')
    proxies = read_ethfi_proxies('proxy.txt')
    return process_ethfi_data(wallets, proxies)

def run_karak():
    wallets = read_karak_wallets('wallets.txt')
    proxies = read_karak_proxies('proxy.txt')
    return process_karak_data(wallets, proxies)

def run_reya():
    wallets = read_reya_wallets('wallets.txt')
    proxies = read_reya_proxies('proxy.txt')
    return process_reya_data(wallets, proxies)

def run_usual():
    wallets = read_usual_wallets('wallets.txt')
    proxies = read_usual_proxies('proxy.txt')
    return process_usual_data(wallets, proxies)

def run_all_protocols():
    # Запуск всех протоколов и сохранение результатов в один Excel файл
    protocols = {
        'Fuel': run_fuel(),
        'EtherFi': run_ethfi(),
        'Karak': run_karak(),
        'Reya': run_reya(),
        'Usual': run_usual()
    }

    with pd.ExcelWriter('all_protocols_stat.xlsx') as writer:
        for protocol, data in protocols.items():
            df = pd.DataFrame(data)
            df.to_excel(writer, sheet_name=protocol[:31], index=False)  # Лимит на длину имени листа в Excel

def main():
    print(f"{Fore.CYAN}Выберите протокол:{Style.RESET_ALL}")
    print(f"{Fore.GREEN}1. Fuel{Style.RESET_ALL}")
    print(f"{Fore.GREEN}2. EtherFi{Style.RESET_ALL}")
    print(f"{Fore.GREEN}3. Karak{Style.RESET_ALL}")
    print(f"{Fore.GREEN}4. Reya{Style.RESET_ALL}")
    print(f"{Fore.GREEN}5. Usual{Style.RESET_ALL}")
    print(f"{Fore.GREEN}6. Все протоколы{Style.RESET_ALL}")
    
    choice = input(f"{Fore.CYAN}Введите номер выбора (1, 2, 3, 4, 5 или 6): {Style.RESET_ALL}").strip()

    if choice == '1':
        run_fuel()
    elif choice == '2':
        run_ethfi()
    elif choice == '3':
        run_karak()
    elif choice == '4':
        run_reya()
    elif choice == '5':
        run_usual()
    elif choice == '6':
        run_all_protocols()
    else:
        print(f"{Fore.RED}Ошибка: Неверный выбор. Пожалуйста, введите 1, 2, 3, 4, 5 или 6.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
