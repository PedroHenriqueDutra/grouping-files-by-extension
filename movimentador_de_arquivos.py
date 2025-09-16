'''ext = '.jpg .txt .xlsx .pdf .tar.gz'.split(' ') #transforma as estensõens em uma lista separando pelo espaço
for i in ext:
    with open(f'teste/teste_files/teste{i}','w+') as arch:
        arch.write('')
'''

# organize.py
"""
Organizador simples:
python organize.py /caminho/para/pasta         # faz dry-run (seguro)
python organize.py /caminho/para/pasta --run   # move de fato
"""
from pathlib import Path
import shutil
import argparse
import logging
import time
import re
import json

def organize(folder: Path, do_run: bool = False):
    if not folder.exists() or not folder.is_dir():
        raise ValueError(f"Pasta inválida: {folder}")

    # carrega log existente, se houver
    try:
        with open("moves.json", "r") as log:
            movimentos = json.load(log)
    except (FileNotFoundError, json.JSONDecodeError):
        movimentos = []

    for item in folder.iterdir():
        if not item.is_file():
            continue

        if re.search(r"temp_", item.name):
            continue

        ext = item.suffix.lower().lstrip('.') or "no_ext"
        target_dir = folder / ext
        target_dir.mkdir(exist_ok=True)
        dest = target_dir / item.name

        movimentos.append({
            "origem": str(item.resolve()),
            "destino": str(dest.resolve())
        })

        if do_run:
            if dest.exists():
                dest = target_dir / f"{item.stem}_{int(time.time())}{item.suffix}"
            shutil.move(str(item), str(dest))
            logging.info(f"MOVED: {item.name} -> {dest}")
        else:
            logging.info(f"[DRY] {item.name} -> {dest}")

    # salva todos os movimentos no final
    with open("moves.json", "w") as log:
        json.dump(movimentos, log, indent=4)


def undo(folder: Path):
    try:
        with open("moves.json", "r") as log:
            registros = json.load(log)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Nenhum movimento encontrado para desfazer.")
        return

    for i in registros:
        origem = Path(i['origem'])
        destino = Path(i['destino'])
        if destino.exists():
            shutil.move(str(destino), str(origem))
            print(f"UNDO: {destino} -> {origem}")


    '''if not folder.exists() or not folder.is_dir(): # Testa se a pasta é válida
        raise ValueError(f"Pasta inválida: {folder}")
    for item in folder.iterdir():# Itera dentro dos itens da pasta
        if item.is_dir():#Verifica se é um diretório
            for archive in item.iterdir():#Itera dentro do diretório
                if archive.is_file():#Verifica se é um arquivo
                    shutil.move(str(archive),str(folder) )# muda o arquivo para odiretório
'''

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("folder", help="pasta alvo")
    parser.add_argument("--run", action="store_true", help="executa a movimentação")
    parser.add_argument("--undo", action="store_true", help="Desfaz a última movimentação")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    if args.undo:
        undo(Path(args.folder))
    else:
        organize(Path(args.folder), do_run=args.run)
    
