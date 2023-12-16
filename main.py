from package import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=4000)
    # coment for full 5 hours