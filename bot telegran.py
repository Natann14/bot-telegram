from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import requests
import pandas as pd

def start(update: Update, context: CallbackContext) -> None:
    texto = """
    Olá, sou um bot secretário que coleta informações das atuais cotações de algumas moedas 😊\n\nDe qual moeda deseja ter informações? 
(ATUALIZAÇÕES A CADA 30 SEGUNDOS)

-CÓDIGOS DAS MOEDAS:

USD - Dólar Americano/Real
USDT - Dólar Americano/Real Turismo
CAD - Dólar Canadense/Real
EUR - Euro/Real
BTC - Bitcoin/Real 
GBP	- Libra Esterlina/Real Brasileiro	
ARS - Peso Argentino/Real Brasileiro
LTC	- Litecoin/Real Brasileiro		
JPY - Iene Japonês/Real Brasileiro	
CHF - Franco Suíço/Real Brasileiro	
AUD	- Dólar Australiano/Real Brasileiro	
CNY	- Yuan Chinês/Real Brasileiro	
ILS	- Novo Shekel Israelense/Real Brasileiro	
ETH	- Ethereum/Real Brasileiro
XRP	- XRP/Real Brasileiro	
DOGE - Dogecoin/Real Brasileiro

Use /info CÓDIGODOPAÍS para conseguir informações
"""
    
    update.message.reply_text(texto)


def informacao(update: Update, context: CallbackContext) -> None:
 
    lista_paises = ['USD', 'USDT', 'CAD', 'EUR', 'BTC', 'GBP', 'ARS', 'LTC', 'JPY', 'CHF', 'AUD', 'CNY', 'ILS', 'ETH', 'XRP', 'DOGE']
    try:
        due = context.args[0]
        if due not in lista_paises:
            update.message.reply_text('Código do país inválido.')
        else:
            #requisição da API das cotações de moedas
            cotacoes = requests.get('https://economia.awesomeapi.com.br/json/all')
            #essa função tranforma um dicionario json em um dicionario python
            cotacoes_dic = cotacoes.json() 

            df = pd.DataFrame.from_dict(cotacoes_dic, orient='index')
            df = df[['name', 'low', 'high', 'bid', 'ask', 'pctChange']]
            df.columns = ['Nome', 'Baixa', 'Alta', 'Compra', 'Venda', '% Variação']

            auxiliar = df.loc[[due]].to_dict()

            lista_de_informacoes = []

            for info, valor in auxiliar.items():
                for num in valor:
                    lista_de_informacoes.append(valor[num])
            
            nome, baixa, alta, compra, venda, variacao = lista_de_informacoes
            
            resposta = '''Resultado da pesquisa:\n\n Nome -  {}\n Baixa = R$ {}\n Alta = R$ {}\n Valor de Compra = R$ {}\n Valor de Venda = R$ {}
 Porcentagem de Variação = {} 
            '''.format(nome, baixa, alta, compra, venda, variacao)
            #enviando mensagem
            update.message.reply_text(resposta)

    except (IndexError, ValueError):
        update.message.reply_text('Formato incorreto.')

def main() -> None:
    """Run bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("5169989245:AAHmAFSf1dtRdGR5b2NEgbxRa7yTl4cW9l0")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", start))
    dispatcher.add_handler(CommandHandler("info", informacao))

    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()