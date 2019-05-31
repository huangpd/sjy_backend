from app import create_app


__author__ = 'nb_info_tech'

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=3637)
