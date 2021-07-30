import os
from data_service.main import create_app
app = create_app()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8081)))
