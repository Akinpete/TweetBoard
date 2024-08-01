from hello import app, db
if __name__ == '__main__':
    
    # Ensure the application context is available to perform database operations
    with app.app_context():
        db.create_all()  # Ensure the database tables are created
    # app.run(debug=True)
