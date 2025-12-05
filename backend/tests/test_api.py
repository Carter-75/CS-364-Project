import unittest
from unittest.mock import patch, MagicMock
from app import create_app

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.testing = True

    def test_health_check(self):
        """Test the API health endpoint."""
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"status": "ok", "service": "api"})

    @patch('app.routes.ping_database')
    def test_db_ping_success(self, mock_ping):
        """Test DB ping when successful."""
        mock_ping.return_value = (True, None)
        response = self.client.get('/api/db/ping')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'ok')

    @patch('app.routes.ping_database')
    def test_db_ping_failure(self, mock_ping):
        """Test DB ping when database is down."""
        mock_ping.return_value = (False, "Connection refused")
        response = self.client.get('/api/db/ping')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'error')

    @patch('app.routes.create_full_media_entry')
    def test_create_media_entry_validation(self, mock_create):
        """Test validation for creating a media entry."""
        # Missing required fields
        payload = {"firstname": "John"}
        response = self.client.post('/api/media-entries', json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Missing field", response.json['error'])

    @patch('app.routes.create_full_media_entry')
    def test_create_media_entry_success(self, mock_create):
        """Test successful media entry creation."""
        mock_create.return_value = (True, None)
        payload = {
            "firstname": "John",
            "lastname": "Doe",
            "profilename": "jdoe",
            "mediatype": "Movie",
            "medianame": "Inception",
            "releaseyear": 2010,
            "genre": "Sci-Fi",
            "platform": "Netflix",
            "rating": 5,
            "status": "Completed"
        }
        response = self.client.post('/api/media-entries', json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['status'], 'ok')

if __name__ == '__main__':
    unittest.main()
