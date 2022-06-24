from image_server.main import create_app

if __name__ == '__main__':
  app = create_app()
  app.run(debug=True, host=app.config["HOST"], port=app.config["PORT"])