from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/character', methods=['POST'])
def character():
    # Obtener los datos JSON del cuerpo de la solicitud
    data = request.get_json()

    # Verificar si se proporcionó un número de personaje
    if not data or 'character_number' not in data:
        return jsonify({"error": "El campo 'character_number' es requerido"}), 400

    # Obtener el número de personaje de los datos
    character_number = data['character_number']

    # Validar que el número sea un entero positivo
    if not isinstance(character_number, int) or character_number <= 0:
        return jsonify({"error": "El 'character_number' debe ser un entero positivo"}), 400

    # URL de la API de Rick and Morty para obtener el personaje
    url = f"https://rickandmortyapi.com/api/character/{character_number}"

    try:
        # Hacer la solicitud a la API de Rick and Morty
        response = requests.get(url)

        # Si la respuesta es 404, el personaje no existe
        if response.status_code == 404:
            return jsonify({"error": "Character not found"}), 404

        # Si hay un error diferente, devuelve un mensaje genérico
        response.raise_for_status()

        # Obtener los datos del personaje en formato JSON
        character_data = response.json()

        # Extraer el nombre y el estado del personaje
        name = character_data.get('name')
        status = character_data.get('status')

        # Devolver la respuesta con el nombre y el estado del personaje
        return jsonify({"name": name, "status": status}), 200

    except requests.exceptions.RequestException as e:
        # Manejar errores de la solicitud
        return jsonify({"error": f"Error al obtener los datos del personaje: {str(e)}"}), 500

if __name__ == '__main__':
    # Ejecutar la aplicación en el puerto 5000
    app.run(debug=True, host='0.0.0.0', port=5000)
