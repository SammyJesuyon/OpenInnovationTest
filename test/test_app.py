import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    """Test the home page"""
    rv = client.get('/')
    assert b'Database initialized successfully!' in rv.data

def test_image_frames(client):
    """Test the image_frames endpoint with valid depth range"""
    rv = client.get('/image_frames?depth_min=9000&depth_max=9010')
    assert rv.status_code == 200

def test_image_frames_invalid(client):
    """Test the image_frames endpoint with invalid depth range"""
    rv = client.get('/image_frames?depth_min=0&depth_max=10')
    assert rv.status_code == 404
