import requests
from flask import Flask, request
import time
import threading


app = Flask(__name__)


solucao = 0
decantador = {
    'etoh': 0,
    'glicerina': 0,
    'solucaoLavagem':0
}


@app.route('/', methods=['POST'])
def decantadorPost():
    global solucao
    dados = request.get_json(force=True)
    
    dados={'volume':50}
    
    solucao += (dados['volume'])
    
    decantador[etoh] = solucao * 0.02
    decantador[glicerina] = solucao * 0.08
    decantador[solucaoLavagem] = solucao * 0.90
    
    resposta = {
            'etoh': decantador.etoh,
            'glicerina': decantador.glicerina,
            'solucaoLavagem': decantador.solucaoLavagem,
            'total': solucao
            }
    
    return resposta


@app.route('/', methods=['GET'])
def decantadorGet():
    global decantador
    resposta = {
            'decantador': decantador
            }
    return resposta


class Decantador(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            if(solucao != 500):

               # pedido = {
               #    'volume': 50
               #    }
               # response = requests.post(url='https://reator-url.herokuapp.com/reator', json=pedido, headers={"Content_Type": "application/json"}).json()

               # solucao += (response['volume'])
               
                print('insert do paulo')
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
                    
                    #requests.post("https://tanque-glicerina.herokuapp.com/glicerina",json=requestGlicerina, headers={"Content-Type:" "application/json"})
                    
                    #requests.post("",json=requestSolLav, headers={"Content-Type:" "application/json"})
                    #milos
                    
                    return requestGlicerina, requestEtoh, requestSolLav

def create_app():
    global app
    print(Decantador)
    iniciar = Decantador()
    iniciar.start()
    return app

#if __name__ == '__main__':
#    app.run()