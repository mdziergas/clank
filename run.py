from clankapp import app
import os


if __name__ == '__main__':
    app.run(debug=os.environ.get("DEBUG"))