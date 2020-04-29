from flask import Flask, request
import time
import threading
import requests

app = Flask(__name__)


solucao = 0
decantador = {
    'etoh': 0,
    'glicerina': 0,
    'solucaoLavagem':0,
    'total':0
}


@app.route('/', methods=['POST'])
def decantadorPost():
    dados = request.get_json(force=True)
    
    decantador['etoh'] = decantador['solucao'] * 0.02
    decantador['glicerina'] = decantador['solucao'] * 0.08
    decantador['solucaoLavagem'] = decantador['solucao'] * 0.90
    
    resposta = {
            'etoh': decantador.etoh,
            'glicerina': decantador.glicerina,
            'solucaoLavagem': decantador.solucaoLavagem,
            'total': decantador[solucao]
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
            if(decantador['solucao'] != 500):
                time.sleep(5)
                pedido = {
                  'volume': 100
                  }
                
                #response = requests.post(url='https://reator-url.herokuapp.com/reator', json=pedido, headers={"Content_Type": "application/json"}).json()

                decantador['solucao'] += pedido['volume']
               
                
            if(decantador['solucao'] == 500):
                while(decantador['solucao'] > 0):
                    time.sleep(5)
                    decantador['glicerina'] = 100 * 0.02
                    decantador['etoh'] = 100 * 0.08
                    decantador['solucaoLavagem'] = 100 * 0.9
                    
                    requestGlicerina = {'glicerina': decantador.glicerina}
                    requestEtoh={'etoh': decantador.etoh}
                    requestSolLav={'solucaoLavagem': decantador.solucaoLavagem}
                    
                    decantador['solucao'] -= 100
                    
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