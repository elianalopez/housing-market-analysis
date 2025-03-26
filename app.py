from backend.data_loader import load_data
from frontend.dashboard import create_dashboard


data = load_data()

if data is not None:
    app = create_dashboard(data)
    app.run(debug=True)