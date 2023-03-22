
# Desafio do Labirinto Autômato Stone

Antes de rodar o projeto, verifique se você possui o interpretador Python na versão 3+, docker, docker-compose e verifique se possui todas as libs importadas no arquivo fase1_parte2.py

# Desafio do Labirinto Autômato Stone

Antes de rodar o projeto, verifique se você possui o interpretador Python na versão 3+, docker, docker-compose e verifique se possui todas as libs importadas no arquivo `main.py`

- Agora rode o docker-compose com o comando a seguir

`docker compose -f "docker-compose.yml" up -d --build` este comando irá executar o mongodb local. Ele será utilizado para guardar e buscar as matrizes.

Após o mongodb estar rodando, rode o comando

`python3 main.py``
este comando irá rodar o projeto, ao final, irá gerar um arquivo `solution` contendo o caminho que a partícula percorreu.
Essa solução é uma das milhares de soluções que podem ser encontradas com esse modelo.

outros arquivos serão gerados:
dentro da pasta `root/`encontrará quais caminhos a particula tentou percorrer até achar a solução.

(DICA: se preferir rodar no jupyter notebook, pode descomentar as linhas `259` e `160` que fazem a chamada à visualização `write_image`  que mostra uma image na tela a cada passo da partícula) 
