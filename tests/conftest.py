import pytest
from app import app 

def setup_app():
    app.config['TESTING'] = True
    app.config['SERVER_NAME'] = 'localhost.localdomain'
    return app

app = setup_app()
client = app.test_client()

@pytest.fixture
def client():
    app.config.update({
        "TESTING": True,  # Enable testing mode
    })

    # Create a test client using the Flask application configured for testing
    with app.test_client() as testing_client:
        # Establish an application context before running the tests
        with app.app_context():
            yield testing_client