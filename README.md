# Trabalho-Desenvolvimento-WEB

<!DOCTYPE html>
<html lang="pt-BR">

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<form>
    <fieldset>
        <legend>Busca</legend>
        <label for="search">Termo de busca:</label>
        <input type="text" id="search" name="Q">
        <button type="submit">Pesquisar</button>
    </fieldset>
</form>

<form>
    <fieldset>
        <legend>Informações do Cliente</legend>

<label for="nome">Nome:</label><br>
    <input type="text" id="nome" name="nome" required><br><br>

<label for="cidade">Cidade:</label><br>
    <input type="text" id="cidade" name="cidade" required><br><br>

<label for="tel">Telefone:</label><br>
    <input type="text" id="tel" name="tel" required><br><br>

<label for="mail">E-mail:</label><br>
    <input type="email" id="mail" name="mail" required><br><br>

<label for="amb">Ambientes:</label><br>
    <input type="text" id="amb" name="amb" required><br><br>

<label for="ref">Referências:</label><br>
    <input type="text" id="ref" name="ref" required><br><br>

<label for="inv">Valor previsto de investimento:</label><br>
        <select id="inv" name="inv" required> <!– dropdown aqui –>
            <option value="">Selecione um valor</option>
            <option value="40-50k">De R$40.000 à R$50.000</option> 
            <option value="50-60k">De R$50.000 à R$60.000</option>
            <option value="70-80k">De R$70.000 à R$80.000</option>
            <option value="80-90k">De R$80.000 à R$90.000</option>
            <option value="100k-...">Acima de R$100.000</option>
        </select><br><br>

<button type="submit">Enviar</button>
    </fieldset>
</form>
