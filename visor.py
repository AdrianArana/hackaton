from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Memoria temporal para simular los datos que enviará el procesador
datos_memoria = {
    "estado": "En espera", 
    "info": "Iniciando captura de tráfico. A la espera de eventos de payment_processor.py..."
}

# Ruta 1: Entrega la página web al usuario
@app.route('/')
def panel_de_control():
    return render_template('index.html')

# Ruta 2: Entrega los datos puros en JSON a la web (La API)
@app.route('/api/datos', methods=['GET'])
def obtener_datos():
    return jsonify(datos_memoria)

# Ruta 3: Recibe los datos reales desde el código de tus compañeros
@app.route('/api/enviar', methods=['POST'])
def recibir_datos():
    global datos_memoria
    # Sobrescribe la memoria con el JSON que le envíe el procesador
    if request.is_json:
        datos_memoria = request.json
    return jsonify({"mensaje": "Datos recibidos correctamente"})

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, port=5000)