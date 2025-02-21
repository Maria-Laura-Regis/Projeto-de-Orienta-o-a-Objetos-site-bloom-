# Projeto Bookies

Este projeto é um site de histórias interativas onde os usuários podem explorar e se envolver com diferentes histórias. Para manter as informações organizadas e garantir que dados como usuários e histórias sejam facilmente acessados e gerenciados, utilizamos uma estrutura de **banco de dados** baseada em arquivos JSON.

## Estrutura do Projeto

### Pasta `app/controllers/db/`

Esta pasta contém os arquivos responsáveis por gerenciar o banco de dados do site. Existem duas classes principais que fazem a administração dos dados: **usuários** e **histórias**.

- **`db_users.py`**: Gerencia os dados dos usuários. Aqui, são armazenadas informações como o nome de usuário e a senha. É onde a classe `UserDatabase` se encontra, responsável por carregar, salvar e acessar dados dos usuários.
  
- **`db_historias.py`**: Gerencia as histórias interativas disponíveis no site. Cada história possui informações como título, autor, gênero, etc. A classe `DataStory` é responsável por organizar e acessar essas informações.

## Como Funciona

As classes `DataStory` e `HistoriaDatabase` são responsáveis por carregar e acessar os dados de seus respectivos arquivos JSON. Caso o arquivo JSON não exista, um valor padrão é inserido, garantindo que a aplicação sempre tenha dados válidos para trabalhar.

### Estrutura dos Arquivos

1. **`app/controllers/db/db_users.py`**
   - Responsável por gerenciar os dados dos usuários.
   - Utiliza o arquivo `user_accounts.json` para armazenar e acessar os dados dos usuários.

2. **`app/controllers/db/db_stories.py`**
   - Responsável por gerenciar as histórias.
   - Utiliza o arquivo `data_stories.json` para armazenar e acessar os dados das histórias.

