from math import ceil
from os import path, mkdir, system
from json import loads
from requests import get

dir = input('Qual o diretório de destino? (Padrão: ~/workspace): ')

if not dir:
    dir = path.join(path.expanduser("~"), 'workspace')

if not path.exists(dir):
    mkdir(path.join(path.expanduser("~"), dir))

user = input('Qual o nome do usuário: ')
token = input('Informe o personal token, caso não exista, crie um em https://github.com/settings/tokens/new com o escopo "repo" apenas: ')

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
        get(url=f'https://api.github.com/users/{user}/repos?per_page=10&page={i+1}',
            headers=headers).json()
    )

for i in range(len(repos)):
    clone_url = repos[i]['clone_url']
    folder_name = repos[i]['name']
    system(f'git clone {clone_url} {path.join(dir, folder_name)}')
