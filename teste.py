import requests

def verificar_cnpj(cnpj):
    url = f"https://www.receitaws.com.br/v1/cnpj/{cnpj}"
    response = requests.get(url)
    if response.status_code == 200:
        dados = response.json()
        if dados.get('status') == 'OK':
            print(f"Nome: {dados['nome']}")
            print(f"Situação: {dados['situacao']}")
            print(f"Endereço: {dados['logradouro']}, {dados['bairro']}, {dados['municipio']}-{dados['uf']}")
            print(f"email:{dados['email']}")
        else:
            print("CNPJ inválido ou não encontrado.")
    else:
        print("Erro na consulta.")

# Exemplo de uso:
verificar_cnpj("13660696000124")
