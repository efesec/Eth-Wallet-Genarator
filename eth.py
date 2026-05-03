import os
from mnemonic import Mnemonic
from bip_utils import Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes
from colorama import Fore, Style, init

# Terminal renklerini hazırla
init(autoreset=True)

def generate_eth_wallets():
    print(f"{Fore.CYAN}{Style.BRIGHT}=== ETHEREUM WALLET GENERATOR ==={Style.RESET_ALL}")
    
    try:
        user_input = input(f"{Fore.YELLOW}How many ETH wallets do you want to generate? {Fore.WHITE}")
        count = int(user_input)
    except ValueError:
        print(f"{Fore.RED}Error: Please enter a valid number.")
        return

    mnemo = Mnemonic("english")
    file_name = "ethwallet.txt"
    file_path = os.path.join(os.path.dirname(__file__), file_name)

    try:
        with open(file_path, "a", encoding="utf-8") as f:
            for i in range(1, count + 1):
                # 12 Kelimelik Seed (Mnemonic) Oluştur
                words = mnemo.generate(strength=128)
                
                # Seed'den Ethereum Adresi Üret (BIP-44)
                seed_bytes = Bip39SeedGenerator(words).Generate()
                bip44_mst_ctx = Bip44.FromSeed(seed_bytes, Bip44Coins.ETHEREUM)
                
                # Standart Ethereum yolu: m/44'/60'/0'/0/0
                address = bip44_mst_ctx.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0).PublicKey().ToAddress()
                
                # Terminale Yazdır (Renkli ve Okunaklı)
                header = f"{Fore.GREEN}{Style.BRIGHT}--- ETH Wallet #{i} ---"
                seed_text = f"{Fore.BLUE}{Style.BRIGHT}Seed Phrase: {Fore.WHITE}{words}"
                addr_text = f"{Fore.MAGENTA}{Style.BRIGHT}ETH Address: {Fore.YELLOW}{address}"
                
                print(f"\n{header}\n{seed_text}\n{addr_text}")
                
                # TXT Dosyasına Yaz
                f.write(f"Ethereum Wallet #{i}\nSeed: {words}\nAddress: {address}\n{'-'*50}\n")
                f.flush() # Dosyanın anında kaydedilmesini sağlar

        print(f"\n{Fore.CYAN}{Style.BRIGHT}Completed! Your wallets are saved here: {Fore.WHITE}{file_path}")
    
    except Exception as e:
        print(f"{Fore.RED}An error occurred: {e}")

if __name__ == "__main__":
    generate_eth_wallets()