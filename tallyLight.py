import network
import esp
import machine
import time
from machine import Pin

# Desativa as mensagens de debug do ESP
esp.osdebug(None)

# Configura os pinos (ESP12/NodeMCU)
ledSignal = Pin(15, Pin.OUT)
ledRed = Pin(12, Pin.OUT)
greenRed = Pin(14, Pin.OUT)

# Configurações do Web Menu
tallyName = "vMix Tally Lights"
backColor = "red"  # CSS da página
tallyCompany = "Smart Media"
tallyDescriptions = "Igreja Mover 2024"

# Configuração de IP e Rede
tallyIp = '192.168.48.15'  # Endereço IP do Web Menu
ssidTally = "vMix_Tally_Light_MOVER_%d"  # SSID da Tally
passwordTally = "vicksmedia"  # Senha da rede

# Configurações iniciais
statusOffTally = 0
ActiveTally = 1
previewTally = 2
currentState = -1
port = 8099

# Função para iniciar o ponto de acesso
def start_ap():
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid=ssidTally % 1, password=passwordTally)
    ap.ifconfig([tallyIp, '255.255.255.0', tallyIp, '8.8.8.8'])
    print('Acesso disponível no IP:', ap.ifconfig()[0])

# Função para desligar os LEDs
def ledSetOff():
    ledSignal.off()
    ledRed.off()
    greenRed.off()

# Função para sinalizar Tally ativo
def ledTallyActive():
    ledSetOff()
    ledRed.on()
    ledSignal.on()

# Função para sinalizar Preview
def ledSetPreview():
    ledSetOff()
    greenRed.on()
    ledSignal.on()

# Função para sinalizar Conectando
def ledSetConnecting():
    for _ in range(8):
        ledSignal.on()
        time.sleep(0.2)
        ledSignal.off()
        time.sleep(0.2)

# Função para conectar ao WiFi
def connect_wifi(ssid, password):
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(ssid, password)
    for _ in range(10):
        if sta_if.isconnected():
            break
        time.sleep(1)
    if sta_if.isconnected():
        print('Conectado ao WiFi, IP:', sta_if.ifconfig()[0])
    else:
        print('Falha ao conectar no WiFi')

# Função para configurar o WiFi e iniciar o AP
def start():
    ledSetConnecting()
    connect_wifi("Your_SSID", "Your_Password")  # Substitua pelo seu SSID e senha

    if not network.WLAN(network.STA_IF).isconnected():
        print("Iniciando ponto de acesso")
        start_ap()

# Configuração inicial
def setup():
    ledSetOff()
    start()

# Loop principal
def loop():
    while True:
        pass  # Adicione seu código principal aqui

# Chamada inicial
setup()
loop()
