from app.main import app

if __name__ == "__main__":
		app.secret_key = 'people'
		app.run(debug='true')
