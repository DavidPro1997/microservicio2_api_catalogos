from app import app
from app.routes import * 

if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Ejecuta en modo de depuración