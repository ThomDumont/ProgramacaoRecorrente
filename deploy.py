from flask import Flask, request
import time
import json
import threading
import requests

app = Flask(__name__)

#----------------------------------------------------------------------------
#-------------------Dados-Decantador-----------------------------------------
#maximo de litros 500
#a cada 2 lancamentos o decantador para
#precisa repousar a cada 100 litros lancados por 5segundos
#----------------------------------------------------------------------------
#------------------Dados de Saida--------------------------------------------
#90% de solucao para lavagem
#2% de glicerina
#8% de EtOH
#-----------------------------------------------------------------------------
#-----------------Dados de entrada do outro módulo----------------------------
#solucao: 1 parte de NaOH, 4 partes de EtOH e 100 partes de oleo
#-----------------------------------------------------------------------------

#Tela apresentada
solucao = 0
etoh = 0
glicerina = 0
solucaoLavagem = 0

@app.route('/decantador', method=['POST'])
def decantadorPost():
    global solucao
    global etoh
    global glicerina
    global solucaoLavagem
    dados = request.get_json()
    
    etoh = solucao * 0.02
    glicerina = solucao * 0.08
    solucaoLavagem = solucaoLavagem * 0.90
    
    resposta = {
            'etoh': etoh,
            'glicerina': glicerina,
            'solucao': solucaoLavagem
            }
    
    return resposta

#aqui a gente pega os valores do módulo anterior Reator

@app.route('/decantadorGet', method=['GET'])
def decantadorGet():
    global solucao
    global etoh
    global glicerina
    global solucaoLavagem
    dados = request.get_json()
    
    resposta = {
            'etoh': etoh,
            'glicerina': glicerina,
            'solucao': solucaoLavagem
            }
    
    return resposta

class Decantador(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            if(solucao != 500):
                pedido = {
                'volume': 50
                }
                response = requests.post(url='https://reator-url.herokuapp.com/reator', json=pedido, headers={"Content_Type": "application/json"}).json()

                solucao += (response['volume'])
                
            if(solucao == 500):
                while(solucao > 0):
                    time.sleep(5)
                    glicerina = 100 * 0.02
                    etoh = 100 * 0.08
                    solucaoLavagem = 100 * 0.9
                    
                    requestGlicerina = {'glicerina': glicerina}
                    requestEtoh={'etoh': etoh}
                    requestSolLav={'solucaoLavagem': solucaoLavagem}
                    
                    solucao -= 100
                    
                    reqGlicerina = requests.post("",json=requestGlicerina, headers={"Content-Type:" "application/json"})
                    reqEtoh = requests.post("",json=requestEtoh, headers={"Content-Type:" "application/json"})
                    reqSolLav = requests.post("",json=requestSolLav, headers={"Content-Type:" "application/json"})

def create_app():
    global app
    iniciar = Decantador()
    iniciar.start()
    return app

#if __name__ == '__main__':
#    app.run()