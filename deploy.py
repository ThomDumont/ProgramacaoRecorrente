from flask import Flask, request
import time
import threading
import requests

app = Flask(__name__)


solucao = 0

decantador = {
    'etoh':  0.0,
    'glicerina': 0.0,
    'solucaolavagem':0.0,
    'solucaototal': 0.0
}

print('Total Recebido :', decantador)

def atualizaVolumes(volume):
    decantador['glicerina'] += volume * 0.02
    decantador['etoh'] += volume * 0.08 
    decantador['solucaolavagem'] += volume * 0.9
    decantador['solucaototal'] += volume
    
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
            if(decantador['solucaototal'] < 500):
                time.sleep(1)
                
                pedido = {
                  "volume": 50
                  }
                
                response = requests.post("https://reator-url.herokuapp.com/reator", json=pedido, headers={"Content_Type": "application/json"}).json()
                
                if (response.get('status_code', None) == 200):
                    atualizaVolumes(response['volume'])
                #atualizaVolumes(pedido['volume'])    
                print(decantador)
            if(decantador['solucaototal'] == 500):
                while(decantador['solucaototal'] > 0):
                    time.sleep(5)
                    glicerina = 100 * 0.02
                    decantador['glicerina'] = decantador['glicerina'] - glicerina
                    
                    etoh = 100 * 0.08
                    decantador['etoh'] = decantador['etoh'] - etoh
                    
                    solucaoLavagem = 100 * 0.9
                    decantador['solucaolavagem'] = decantador['solucaolavagem'] - solucaoLavagem
                    
                    requestEtoh={'etoh': etoh}
                    requestGlicerina = {"glicerina": glicerina}
                    requestSolLav={'solucaolavagem': solucaoLavagem}
                    
                    decantador['solucaototal'] = decantador['solucaototal'] - 100
                    
                    reqLav = requests.post("https://sistemas-distribuido.herokuapp.com/lavagem", json=requestSolLav, headers={"Content_Type": "application/json"}).json()
                    
                    reqetoh = requests.post("https://concorrente-tanque-etoh.herokuapp.com/",json=requestEtoh, headers={"Content-Type": "application/json"}).json()
                        
                    reqGli = requests.post("https://tanque-glicerina.herokuapp.com/glicerina", json=requestGlicerina, headers={"Content-Type": "application/json"})
                    
                    print('Envio da Lavagem:',reqLav, 'Envio de EtOH:' , reqetoh, 'Envio de Glicerina:',reqGli)
                    
                    
def create_app():
    global app
    decantadorThread = Decantador()
    decantadorThread.start()
    return app

#if __name__ == '__main__':
#   decantadorThread = Decantador()
#   decantadorThread.start()
#   app.run() 