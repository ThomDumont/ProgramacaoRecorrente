import requests
from flask import Flask, request
import time
import threading


app = Flask(__name__)

solucao = 0
etoh = 0
glicerina = 0
solucaoLavagem = 0

@app.route('/decantador', method=['POST'])
def decantador():
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

@app.route('/decantador', method=['GET'])
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
                #response = requests.post(url='https://reator-url.herokuapp.com/reator', json=pedido, headers={"Content_Type": "application/json"}).json()

                solucao += (pedido['volume'])
                
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
                    
                    requests.post("https://concorrente.herokuapp.com/tanque_EtOH",json=requestEtoh, headers={"Content-Type:" "application/json"})
                    
                    #requests.post("",json=requestGlicerina, headers={"Content-Type:" "application/json"})
                    #requests.post("",json=requestSolLav, headers={"Content-Type:" "application/json"})

def create_app():
    global app
    iniciar = Decantador()
    iniciar.start()
    return app

#if __name__ == '__main__':
#    app.run()