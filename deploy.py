from flask import Flask, request
import time
import threading
import requests

app = Flask(__name__)


solucao = 0

decantador = {
    'etoh':  0,
    'glicerina': 0,
    'solucaoLavagem':0,
    'SolucaoTotal': 0
}

def atualizaVolumes(volume):
    decantador['etoh'] += volume * 0.02
    decantador['glicerina'] += volume * 0.08
    decantador['solucaoLavagem'] += volume * 0.9
    decantador['SolucaoTotal'] += volume
    
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
            if(decantador['SolucaoTotal'] < 500):
                pedido = {
                  'volume': 50
                  }
                #response = requests.post(url='https://reator-url.herokuapp.com/reator', json=pedido, headers={"Content_Type": "application/json"}).json()
                #if (response.get('status_code', None) == 200):
                #    atualizaVolumes(pedido['volume'])
                atualizaVolumes(pedido['volume'])    
                
            if(decantador['SolucaoTotal'] == 500):
                while(decantador['SolucaoTotal'] > 0):
                    time.sleep(5)
                    glicerina = 100 * 0.02
                    decantador['glicerina'] -= glicerina
                    etoh = 100 * 0.08
                    decantador['etoh'] -= etoh
                    solucaoLavagem = 100 * 0.9
                    decantador['solucaoLavagem'] -= solucaoLavagem
                    
                    requestGlicerina = {'glicerina': glicerina}
                    requestEtoh={'etoh': etoh}
                    requestSolLav={'solucaoLavagem': solucaoLavagem}
                    
                    decantador['SolucaoTotal'] -= 100
                    
                    requests.post("https://concorrente.herokuapp.com/tanque_EtOH",json=requestEtoh, headers={"Content-Type:" "application/json"})
                    
                    #requests.post("https://tanque-glicerina.herokuapp.com/glicerina",json=requestGlicerina, headers={"Content-Type:" "application/json"})
                    
                    #requests.post("",json=requestSolLav, headers={"Content-Type:" "application/json"})
                    #milos
                    
                    return requestGlicerina, requestEtoh, requestSolLav

def create_app():
    global app
    iniciar = Decantador()
    iniciar.start()
    return app

#if __name__ == '__main__':
#    app.run()