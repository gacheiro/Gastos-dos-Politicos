![GitHub](https://img.shields.io/github/license/thiagojobson/Gastos-dos-Politicos)

# Gastos dos Políticos

Acompanhe os gastos dos políticos com a [Cota Parlamentar](https://www.camara.leg.br/transparencia/gastos-parlamentares).

## Instalação

Para instalar e rodar o app é preciso ter o python 3 no seu computador.

```
# Clone o repositório no seu computador
git clone https://github.com/thiagojobson/Gastos-dos-Politicos

# Crie um ambiente virtual
cd Gastos-dos-Politicos/
python -m venv venv

# Ative o ambiente virtual
source venv/bin/activate   # linux
venv\Scripts\activate      # windows

# Instale o app e as depêndencias
pip install -e .
```

```bash
sudo locale-gen pt_BR.UTF-8
```

Agora é preciso configurar o app. Copie o conteúdo do arquivo `env.example` para um arquivo `.env`.
Em seguida rode os testes para ver se está tudo funcionando:

```
pytest gastos_politicos/tests
```

Agora é só rodar o app localmente e acessar em [http://localhost:5000/]:

```
flask run
```
