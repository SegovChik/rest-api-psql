from core import create_app
# from app.core import create_app

def myconnect():
    while True:
        try:
            return create_app()
        except:
            print("api isn't connected to database yet")


app = myconnect()

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=4000)

