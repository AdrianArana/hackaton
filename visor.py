from flask import Flask, render_template, jsonify, request
import httpx

app = Flask(__name__)

# Memoria temporal
datos_memoria = {
    "estado": "En espera", 
    "info": "Iniciando captura de tráfico. A la espera de eventos de payment_processor.py..."
}

@app.route('/')
def panel_de_control():
    return render_template('index.html')

@app.route('/api/datos', methods=['GET'])
def obtener_datos():
    return jsonify(datos_memoria)

@app.route('/api/enviar', methods=['POST'])
def recibir_datos():
    global datos_memoria
    if request.is_json:
        datos_memoria = request.json
    return jsonify({"mensaje": "Datos recibidos correctamente"})

@app.route('/api/upload', methods=['POST'])
def upload_file():
    # Recogemos los tres archivos
    archivos_frontend = {
        'reglas': (request.files['reglas'].filename, request.files['reglas'].stream, request.files['reglas'].mimetype),
        'normativas': (request.files['normativas'].filename, request.files['normativas'].stream, request.files['normativas'].mimetype),
        'codigo': (request.files['codigo'].filename, request.files['codigo'].stream, request.files['codigo'].mimetype)
    }
    
    # Los enviamos de golpe a tu orquestador
    httpx.post("http://localhost:8001/api/modernize", files=archivos_frontend)
    return jsonify({"mensaje": "Archivos en proceso"})

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, port=5000)