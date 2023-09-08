from app.routes import app
from data_gen_module import generate_mock_data

if __name__ == '__main__':
    generate_mock_data()
    app.run(debug=True)