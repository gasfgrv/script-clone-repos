from math import ceil
from os import path, mkdir, system

from requests import get

diretorio = input('Qual o diretório de destino? (Padrão: ~/workspace): ')

if not diretorio:
    diretorio = path.join(path.expanduser("~"), 'workspace')

if not path.exists(diretorio):
    mkdir(path.join(path.expanduser("~"), diretorio))

user = input('Qual o nome do usuário: ')
token = input('Informe o token, se não existe, crie um em https://github.com/settings/tokens/new com o escopo "repo": ')

headers = {
    'Accept': 'application/vnd.github+json',
    'GitHub-Api-Version': '2022-11-28',
    'Authorization': f'token {token}'
}

url_repo_info = f'https://api.github.com/search/repositories?q=user:{user}&per_page=1&page=1'
repo_info = get(url=url_repo_info, headers=headers).json()
repo_count = repo_info['total_count']
page_count = ceil(repo_count / 10)

repos = []

for i in range(page_count):
    repos.extend(
        get(url=f'https://api.github.com/users/{user}/repos?per_page=10&page={i + 1}',
            headers=headers).json()
    )

for i in range(len(repos)):
    clone_url = repos[i]['ssh_url']
    folder_name = repos[i]['name']
    system(f'git clone {clone_url} {path.join(diretorio, folder_name)}')
