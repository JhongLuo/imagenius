if __name__ == '__main__':
    from app.app import app
    app.run(debug=True, host='0.0.0.0', port=5000)