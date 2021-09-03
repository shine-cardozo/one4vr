from app.main import app

if __name__ == "__main__":
		app.secret_key = 'people'
		app.run(host="192.168.43.153", port="80")
		app.run(debug='true')
