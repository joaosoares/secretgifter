import os
from app import app

port = int(os.environ.get('PORT', 5000))
app.run(port=port, debug=True)
