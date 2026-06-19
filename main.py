import os
import re
import sys
import time
import shutil
import colorama
import requests
from collections import Counter
from colorama import Fore, Back, Style

colorama.init(autoreset=True)

# ═══════════════════════════════════════════════════════════════
#  PALETA DE CORES (RED / WHITE / DARK)
# ═══════════════════════════════════════════════════════════════
R  = Fore.RED
LR = Fore.LIGHTRED_EX
W  = Fore.WHITE
DW = Fore.LIGHTBLACK_EX   # cinza escuro
RS = Style.RESET_ALL
BD = Style.BRIGHT

# Cores de destaque para substituir as antigas
PRIMARY   = R
SECONDARY = W
ACCENT    = LR
DIM       = DW

VERSION = "v9.9"
AUTHOR  = "Druca"

# CONFIGURAÇÃO GITHUB PARA UPDATE
GITHUB_USER = "Drucadb"
GITHUB_REPO = "stealercheker"

# ═══════════════════════════════════════════════════════════════
#  BANNER
# ═══════════════════════════════════════════════════════════════
BANNER_LINES = [
    f"{R}  ██████╗ ████████╗███████╗ █████╗ ██╗     ███████╗██████╗ ",
    f"{R}  ██╔════╝╚══██╔══╝██╔════╝██╔══██╗██║     ██╔════╝██╔══██╗",
    f"{LR}  ███████╗   ██║   █████╗  ███████║██║     █████╗  ██████╔╝",
    f"{LR}  ╚════██║   ██║   ██╔══╝  ██╔══██║██║     ██╔══╝  ██╔══██╗",
    f"{W}  ███████║   ██║   ███████╗██║  ██║███████╗███████╗██║  ██║",
    f"{W}  ╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝",
    f"",
    f"{DW}  ██████╗██╗  ██╗███████╗ ██████╗██╗  ██╗███████╗██████╗ ",
    f"{DW}  ██╔════╝██║  ██║██╔════╝██╔════╝██║ ██╔╝██╔════╝██╔══██╗",
    f"{W}  ██║     ███████║█████╗  ██║     █████╔╝ █████╗  ██████╔╝",
    f"{W}  ██║     ██╔══██║██╔══╝  ██║     ██╔═██╗ ██╔══╝  ██╔══██╗",
    f"{R}  ╚██████╗██║  ██║███████╗╚██████╗██║  ██╗███████╗██║  ██║",
    f"{R}   ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚══════╝",
]

# ═══════════════════════════════════════════════════════════════
#  SISTEMA DE AUTO-UPDATE COM BARRA DE PROGRESSO
# ═══════════════════════════════════════════════════════════════
def auto_update():
    if GITHUB_USER == "Drucadb": return
    url_ver = f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/main/version.txt"
    url_raw = f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/main/main.py"
    try:
        r = requests.get(url_ver, timeout=5)
        if r.status_code == 200 and r.text.strip() != VERSION:
            print(f"  {DW}[{R}!{DW}] Nova versão detectada: {LR}{r.text.strip()}{RS}")
            if input(f"  {DW}╰─{R}❯ {W}Atualizar agora? (s/n): {RS}").lower() == 's':
                print(f"  {DW}┌─{R} Baixando atualização...{RS}")
                
                # Download com barra de progresso visual
                response = requests.get(url_raw, stream=True)
                total_size = int(response.headers.get('content-length', 0))
                block_size = 1024
                wrote = 0
                
                new_code = b""
                for data in response.iter_content(block_size):
                    wrote = wrote + len(data)
                    new_code += data
                    if total_size > 0:
                        percent = int(50 * wrote / total_size)
                        sys.stdout.write(f"\r  {DW}│  {R}[{'█' * percent}{'░' * (50 - percent)}]{RS} {int(100 * wrote / total_size)}%")
                        sys.stdout.flush()
                
                print()
                with open(sys.argv[0], 'wb') as f:
                    f.write(new_code)
                
                print(f"  {DW}└─ {R}✔  Atualizado! Reiniciando...{RS}")
                time.sleep(2)
                os.execv(sys.executable, ['python'] + sys.argv)
    except Exception as e:
        print(f"  {DW}└─ {DW}✖ Erro no update: {e}{RS}")

def largura_terminal():
    try:
        return os.get_terminal_size().columns
    except:
        return 80

def linha_dupla(cor=R):
    w = largura_terminal()
    print(f"{cor}{'═' * w}{RS}")

def centralizar(texto, cor="", largura=None):
    if largura is None:
        largura = largura_terminal()
    limpo = re.sub(r'\x1b\[[0-9;]*m', '', texto)
    pad = max(0, (largura - len(limpo)) // 2)
    print(" " * pad + texto + RS)

def exibir_banner(path):
    os.system('cls' if os.name == 'nt' else 'clear')
    try:
        n_logs = len([d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))])
    except:
        n_logs = 0

    print()
    for linha_b in BANNER_LINES:
        centralizar(linha_b)

    print()
    linha_dupla(R)

    w = largura_terminal()
    info_left  = f"  {DW}[{R} {VERSION} {DW}]{W}  by {LR}{AUTHOR}{RS}"
    info_right = f"{DW}[{R} {n_logs} logs loaded {DW}]{RS}  "
    info_mid   = f"{DW}[{W} StealerChecker {DW}]{RS}"

    left_clean  = re.sub(r'\x1b\[[0-9;]*m', '', info_left)
    right_clean = re.sub(r'\x1b\[[0-9;]*m', '', info_right)
    mid_clean   = re.sub(r'\x1b\[[0-9;]*m', '', info_mid)

    total_clean = len(left_clean) + len(mid_clean) + len(right_clean)
    gap = max(1, (w - total_clean) // 2)

    print(info_left + " " * gap + info_mid + " " * gap + info_right)
    linha_dupla(R)
    print()

# ═══════════════════════════════════════════════════════════════
#  AUXILIARES
# ═══════════════════════════════════════════════════════════════
def salvar_lista(lista, nome_arquivo):
    if lista:
        lista = list(set(lista))
        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            f.write("\n".join(lista) + "\n")
        return len(lista)
    return 0

def limpar_campo(valor):
    return valor.strip() if valor else ""

def status_bar(atual, total, largura=40):
    if total == 0:
        return f"{DW}[{'─' * largura}]{RS}"
    preenchido = int(largura * atual / total)
    barra = f"{R}{'█' * preenchido}{DW}{'░' * (largura - preenchido)}"
    return f"{DW}[{barra}{DW}]{RS}"

def prompt_input(msg):
    return input(f"  {DW}╰─{R}❯ {W}{msg}{RS}")

def aguardar_enter(msg="Pressione Enter para voltar..."):
    print()
    input(f"  {DW}[ {LR}{msg} {DW}]{RS}")

def item_menu(num, texto, cor_num=LR, cor_texto=W):
    return f"  {DW}│  {cor_num}{num:>2}{DW} ─ {cor_texto}{texto}{RS}"

def separador_menu():
    w = largura_terminal() - 4
    print(f"  {DW}│{'─' * w}│{RS}")

def cabecalho_menu(titulo, cor=R):
    w = largura_terminal() - 4
    t_limpo = re.sub(r'\x1b\[[0-9;]*m', '', titulo)
    pad = (w - len(t_limpo)) // 2
    print(f"  {cor}╔{'═' * w}╗{RS}")
    print(f"  {cor}║{' ' * pad}{titulo}{' ' * (w - pad - len(t_limpo))}║{RS}")
    print(f"  {cor}╠{'═' * w}╣{RS}")

def rodape_menu(cor=R):
    w = largura_terminal() - 4
    print(f"  {cor}╚{'═' * w}╝{RS}")

# ═══════════════════════════════════════════════════════════════
#  EXTRAÇÃO (OPÇÃO 1)
# ═══════════════════════════════════════════════════════════════
def extrair_dados_get(path, tipo):
    encontrados = []
    print()
    print(f"  {DW}┌─{R} Extracting {LR}{tipo}{R} data...{RS}")
    regex_discord = r"[a-zA-Z0-9_-]{24}\.[a-zA-Z0-9_-]{6}\.[a-zA-Z0-9_-]{27}|mfa\.[a-zA-Z0-9_-]{84}"

    for raiz, dirs, arquivos in os.walk(path):
        for arquivo in arquivos:
            caminho_completo = os.path.join(raiz, arquivo)
            if tipo == "CC" and ("card" in arquivo.lower() or "cc" in arquivo.lower()):
                try:
                    with open(caminho_completo, 'r', encoding='utf-8', errors='ignore') as f:
                        blocos = re.split(r'\n\s*\n|={5,}', f.read())
                        for bloco in blocos:
                            if re.search(r'\d{13,16}', bloco) and "true" not in bloco.lower():
                                h = re.search(r"(?:Holder|Name):\s*(.*)", bloco, re.IGNORECASE)
                                n = re.search(r"(?:Number|Card):\s*(\d+.*)", bloco, re.IGNORECASE)
                                e = re.search(r"(?:Expiration|Exp|Date):\s*(.*)", bloco, re.IGNORECASE)
                                c = re.search(r"(?:CVC|CVV|Code):\s*(\d+)", bloco, re.IGNORECASE)
                                if n:
                                    res = (f"Holder: {limpar_campo(h.group(1) if h else '')}\n"
                                           f"Number: {limpar_campo(n.group(1))}\n"
                                           f"Exp: {limpar_campo(e.group(1) if e else '')}\n"
                                           f"CVC: {limpar_campo(c.group(1) if c else '')}\n")
                                    encontrados.append(res)
                except: continue
            elif tipo == "Discord":
                try:
                    with open(caminho_completo, 'r', encoding='utf-8', errors='ignore') as f:
                        encontrados.extend(re.findall(regex_discord, f.read()))
                except: continue

    total = salvar_lista(encontrados, f"{tipo.lower()}.txt")
    print(f"  {DW}└─ {R}✔  {total} items saved {DW}→ {W}{tipo.lower()}.txt{RS}")
    aguardar_enter()

# ═══════════════════════════════════════════════════════════════
#  BUSCA E ORGANIZAÇÃO DE TOKENS (NOVA FUNÇÃO)
# ═══════════════════════════════════════════════════════════════
def buscar_e_organizar_tokens(path):
    print()
    termo = prompt_input("Pesquisar Token/App (ex: steam): ").lower()
    if not termo: return
    
    output_dir = f"extracted_{termo}"
    if not os.path.exists(output_dir): os.makedirs(output_dir)
    
    print()
    print(f"  {DW}┌─{R} Buscando e organizando arquivos para {LR}\"{termo}\"{R}...{RS}")
    
    count = 0
    for raiz, dirs, arquivos in os.walk(path):
        if termo in raiz.lower() or any(termo in a.lower() for a in arquivos):
            for arquivo in arquivos:
                if any(ext in arquivo.lower() for ext in [".vdf", ".dat", ".txt", "ssfn", "config"]):
                    caminho_origem = os.path.join(raiz, arquivo)
                    log_folder_name = os.path.basename(os.path.dirname(raiz)) if os.path.dirname(raiz) != path else os.path.basename(raiz)
                    dest_subfolder = os.path.join(output_dir, log_folder_name)
                    if not os.path.exists(dest_subfolder): os.makedirs(dest_subfolder)
                    try:
                        shutil.copy2(caminho_origem, os.path.join(dest_subfolder, arquivo))
                        count += 1
                    except: continue

    if count > 0:
        print(f"  {DW}└─ {R}✔  {count} arquivos organizados em {W}{output_dir}/{RS}")
    else:
        print(f"  {DW}└─ {DW}✖  Nenhum arquivo encontrado para {LR}\"{termo}\"{RS}")
    aguardar_enter()

# ═══════════════════════════════════════════════════════════════
#  FILTRO DE COOKIES
# ═══════════════════════════════════════════════════════════════
def filtrar_cookies(path):
    print()
    keyword = prompt_input("Enter keyword to filter cookies (ex: netflix): ").lower()
    if not keyword: return
    
    output_dir = "filtered"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    found_cookie_sets = []
    
    print()
    print(f"  {DW}┌─{R} Filtering Netscape cookies for {LR}\"{keyword}\"{R}...{RS}")
    
    for raiz, dirs, arquivos in os.walk(path):
        if "cookie" in raiz.lower() or any("cookie" in a.lower() for a in arquivos):
            for arquivo in arquivos:
                if arquivo.endswith(".txt"):
                    caminho_completo = os.path.join(raiz, arquivo)
                    try:
                        with open(caminho_completo, 'r', encoding='utf-8', errors='ignore') as f:
                            lines = f.readlines()
                            relevant_lines = [l.strip() for l in lines if keyword in l.lower()]
                            
                            if relevant_lines:
                                cookie_content = "\n".join(relevant_lines)
                                found_cookie_sets.append(cookie_content)
                    except: continue

    if found_cookie_sets:
        count = 0
        for content in list(set(found_cookie_sets)):
            count += 1
            individual_file = os.path.join(output_dir, f"{keyword}_{count}.txt")
            with open(individual_file, 'w', encoding='utf-8') as f:
                f.write(content + "\n")
        
        print(f"  {DW}└─ {R}✔  {count} Netscape cookie files created in {W}{output_dir}/{RS}")
    else:
        print(f"  {DW}└─ {DW}✖  No cookies found for {LR}\"{keyword}\"{RS}")
    
    aguardar_enter()

# ═══════════════════════════════════════════════════════════════
#  BUSCA
# ═══════════════════════════════════════════════════════════════
def buscar_e_salvar(path):
    print()
    termo = prompt_input("Enter search query: ").lower()
    combos = []
    print()
    print(f"  {DW}┌─{R} Searching for {LR}\"{termo}\"{R}...{RS}")

    for raiz, dirs, arquivos in os.walk(path):
        for arquivo in arquivos:
            if "pass" in arquivo.lower():
                try:
                    with open(os.path.join(raiz, arquivo), 'r', encoding='utf-8', errors='ignore') as f:
                        for bloco in f.read().split('\n\n'):
                            if termo in bloco.lower():
                                u = re.search(r"(?:User|Login):\s*(.*)", bloco, re.IGNORECASE)
                                p = re.search(r"(?:Password|Pass):\s*(.*)", bloco, re.IGNORECASE)
                                if u and p:
                                    combos.append(f"{limpar_campo(u.group(1))}:{limpar_campo(p.group(1))}")
                except: continue

    total = salvar_lista(combos, "search.txt")
    print(f"  {DW}└─ {R}✔  {total} combos found {DW}→ {W}search.txt{RS}")
    aguardar_enter()

# ═══════════════════════════════════════════════════════════════
#  ANÁLISE
# ═══════════════════════════════════════════════════════════════
def menu_analysis(path):
    exibir_banner(path)
    cabecalho_menu(f"{W}  ANALYSIS  {RS}", cor=R)

    total_passwords, user_in_pass, user_equals_pass = 0, 0, 0
    urls = []
    stealer_types = Counter()

    print(f"  {DW}│  {R}Analyzing logs, please wait...{RS}")
    separador_menu()

    for raiz, dirs, arquivos in os.walk(path):
        for arquivo in arquivos:
            if "RedLine" in raiz:    stealer_types["RedLine"] += 1
            elif "Collector" in raiz: stealer_types["COLLECTOR"] += 1
            if "pass" in arquivo.lower() and arquivo.endswith(".txt"):
                try:
                    with open(os.path.join(raiz, arquivo), 'r', encoding='utf-8', errors='ignore') as f:
                        for bloco in f.read().split('\n\n'):
                            u   = re.search(r"(?:User|Login):\s*(.*)",    bloco, re.IGNORECASE)
                            p   = re.search(r"(?:Password|Pass):\s*(.*)", bloco, re.IGNORECASE)
                            url = re.search(r"(?:URL|Host):\s*(.*)",       bloco, re.IGNORECASE)
                            if p:
                                total_passwords += 1
                                pass_val = limpar_campo(p.group(1)).lower()
                                if u:
                                    user_val = limpar_campo(u.group(1)).lower()
                                    if user_val and user_val in pass_val: user_in_pass += 1
                                    if user_val == pass_val:              user_equals_pass += 1
                                if url: urls.append(limpar_campo(url.group(1)))
                except: continue

    perc_in = (user_in_pass / total_passwords * 100) if total_passwords > 0 else 0
    perc_eq = (user_equals_pass / total_passwords * 100) if total_passwords > 0 else 0

    print(f"  {DW}│  {LR}GENERAL STATS{RS}")
    print(f"  {DW}│")
    print(f"  {DW}│  {DW}Total Passwords   {DW}│ {W}{total_passwords:,}{RS}")
    print(f"  {DW}│  {DW}User in Password  {DW}│ {LR}~{perc_in:.2f}%{RS}")
    print(f"  {DW}│  {DW}User = Password   {DW}│ {R}~{perc_eq:.2f}%{RS}")
    separador_menu()

    print(f"  {DW}│  {LR}TOP URLS{RS}")
    print(f"  {DW}│")
    top_urls = Counter(urls).most_common(5)
    if top_urls:
        for i, (url, count) in enumerate(top_urls, 1):
            perc_url = (count / total_passwords * 100) if total_passwords > 0 else 0
            barra = status_bar(count, top_urls[0][1], largura=20)
            print(f"  {DW}│  {R}{i}.{W} {url[:45]:<45} {barra} {LR}{perc_url:.1f}%{DW} ({count}){RS}")
    else:
        print(f"  {DW}│  {DW}No URLs found.{RS}")
    
    rodape_menu(R)
    aguardar_enter()

# ═══════════════════════════════════════════════════════════════
#  MENUS DE NAVEGAÇÃO
# ═══════════════════════════════════════════════════════════════
def menu_getting(path):
    while True:
        exibir_banner(path)
        cabecalho_menu(f"{W}  GETTING  {RS}", cor=R)
        print(item_menu("1", "Search & Organize Tokens (Steam, etc)", cor_num=R))
        print(item_menu("2", "Get CC Cards",        cor_num=LR))
        print(item_menu("3", "Get Discord Tokens",  cor_num=LR))
        print(item_menu("4", "Get Telegrams",        cor_num=LR))
        print(item_menu("5", "Get Cold Wallets",     cor_num=LR))
        print(item_menu("6", "Filter Cookies (Netscape)", cor_num=R))
        separador_menu()
        print(item_menu("55", "Back  ←",             cor_num=DW, cor_texto=DW))
        rodape_menu(R)

        op = prompt_input("")
        if   op == "55": break
        elif op == "1":  buscar_e_organizar_tokens(path)
        elif op == "2":  extrair_dados_get(path, "CC")
        elif op == "3":  extrair_dados_get(path, "Discord")
        elif op == "6":  filtrar_cookies(path)
        else:
            print(f"\n  {R}⚠  Feature not yet implemented.{RS}")
            aguardar_enter()

def menu_search(path):
    while True:
        exibir_banner(path)
        cabecalho_menu(f"{W}  SEARCH  {RS}", cor=R)
        print(item_menu("1", "Search by URL",      cor_num=LR))
        print(item_menu("2", "Search by Password", cor_num=LR))
        print(item_menu("3", "Search by Username", cor_num=LR))
        print(item_menu("4", "Save All Combos",    cor_num=LR))
        separador_menu()
        print(item_menu("55", "Back  ←",            cor_num=DW, cor_texto=DW))
        rodape_menu(R)

        op = prompt_input("")
        if op == "55": break
        elif op in ["1", "2", "3", "4"]: buscar_e_salvar(path)

def menu_principal(path):
    verbose = False
    while True:
        exibir_banner(path)
        cabecalho_menu(f"{W}  MAIN MENU  {RS}", cor=R)
        print(item_menu("1", "Get / Filter / Organize", cor_num=R))
        print(item_menu("2", "Search",       cor_num=R))
        print(item_menu("3", "Check Update", cor_num=W))
        print(item_menu("4", "Analysis",     cor_num=R))
        separador_menu()
        verb_cor  = LR if verbose else DW
        verb_txt  = "ON" if verbose else "OFF"
        print(item_menu("88", f"Verbose: {verb_cor}{verb_txt}", cor_num=W, cor_texto=W))
        print(item_menu("99", "Exit",      cor_num=DW, cor_texto=DW))
        rodape_menu(R)

        opcao = prompt_input("")
        if   opcao == "99": break
        elif opcao == "1":  menu_getting(path)
        elif opcao == "2":  menu_search(path)
        elif opcao == "3":  auto_update()
        elif opcao == "4":  menu_analysis(path)
        elif opcao == "88": verbose = not verbose

if __name__ == "__main__":
    auto_update()
    os.system('cls' if os.name == 'nt' else 'clear')
    print()
    for linha_b in BANNER_LINES:
        centralizar(linha_b)
    print()
    linha_dupla(R)
    centralizar(f"{DW}[ {R}StealerChecker {VERSION} {DW}] [ {W}by {LR}{AUTHOR} {DW}]{RS}")
    linha_dupla(R)
    print()

    caminho = prompt_input("Enter path to logs folder: ")
    if os.path.exists(caminho):
        menu_principal(caminho)
    else:
        print(f"  {R}✖  Path not found: {W}{caminho}{RS}")
        sys.exit(1)
