<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Minha segunda página com o BMVC</title>
</head>
<body>

    <h1>Minha página com interação de modelos :)</h1>

    % if transfered:
        <div>
            <h2>Dados do Usuário:</h2>
            <p>Username: {{ data.username }}</p>  <!-- Exibe o nome do usuário -->
            <p>Password: {{ data.password }}</p>  <!-- Exibe a senha -->
        </div>
    % else:
        <h2>Porém, desta vez não foram transferidas quaisquer informações ): </h2>

</body>
</html>
