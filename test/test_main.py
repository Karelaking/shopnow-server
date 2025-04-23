import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import io

# We need to mock modules before importing main
with patch.dict('sys.modules', {
	'uvicorn': MagicMock(),
	'app': MagicMock(),
	'dotenv': MagicMock(),
	'database.connetDB': MagicMock()  # Using the original typo for testing
}):
	# Mock environment variables
	with patch.dict(os.environ, {
		'DB_URL': 'mongodb://testdb:27017',
		'PORT': '9000'
	}):
		# Now import the main module
		from src import main


class TestMainApp(unittest.TestCase):
	"""Test suite for main application entry point"""
	
	@patch('main.connectDB')
	@patch('main.run')
	@patch('main.getenv')
	def test_successful_execution(self, mock_getenv, mock_run, mock_connectdb):
		"""Test successful application startup"""
		# Setup mocks
		mock_getenv.side_effect = lambda key, default=None: {
			'DB_URL': 'mongodb://testdb:27017',
			'PORT': '9000'
		}.get(key, default)
		
		mock_client = MagicMock()
		mock_connectdb.return_value = mock_client
		
		# Capture stdout
		captured_output = io.StringIO()
		sys.stdout = captured_output
		
		# Execute
		main.main()
		
		# Reset stdout
		sys.stdout = sys.__stdout__
		
		# Assert
		mock_connectdb.assert_called_once_with('mongodb://testdb:27017')
		mock_run.assert_called_once_with(main.app, host="0.0.0.0", port=9000)
		self.assertIn("Connected to MongoDB", captured_output.getvalue())
	
	@patch('main.connectDB')
	@patch('main.run')
	@patch('main.getenv')
	@patch('main.sys.exit')
	def test_failed_db_connection(self, mock_exit, mock_getenv, mock_run, mock_connectdb):
		"""Test handling of database connection failure"""
		# Setup mocks
		mock_getenv.side_effect = lambda key, default=None: {
			'DB_URL': 'mongodb://testdb:27017',
			'PORT': '9000'
		}.get(key, default)
		
		mock_connectdb.return_value = None
		
		# Capture stdout
		captured_output = io.StringIO()
		sys.stdout = captured_output
		
		# Execute
		main.main()
		
		# Reset stdout
		sys.stdout = sys.__stdout__
		
		# Assert
		mock_connectdb.assert_called_once_with('mongodb://testdb:27017')
		mock_exit.assert_called_once_with(1)
		mock_run.assert_not_called()
		self.assertIn("Failed to connect to MongoDB", captured_output.getvalue())
	
	@patch('main.connectDB')
	@patch('main.run')
	@patch('main.getenv')
	@patch('main.sys.exit')
	def test_missing_db_url(self, mock_exit, mock_getenv, mock_run, mock_connectdb):
		"""Test handling of missing DB_URL environment variable"""
		# Setup mocks
		mock_getenv.side_effect = lambda key, default=None: {
			'DB_URL': None,
			'PORT': '9000'
		}.get(key, default)
		
		# Capture stdout
		captured_output = io.StringIO()
		sys.stdout = captured_output
		
		# Execute
		main.main()
		
		# Reset stdout
		sys.stdout = sys.__stdout__
		
		# Assert
		mock_connectdb.assert_not_called()
		mock_exit.assert_called_once_with(1)
		mock_run.assert_not_called()
		self.assertIn("Error: DB_URL environment variable not set", captured_output.getvalue())
	
	@patch('main.connectDB')
	@patch('main.run')
	@patch('main.getenv')
	def test_default_port(self, mock_getenv, mock_run, mock_connectdb):
		"""Test using default port when PORT is not set"""
		# Setup mocks
		mock_getenv.side_effect = lambda key, default=None: {
			'DB_URL': 'mongodb://testdb:27017',
			'PORT': None
		}.get(key, default)
		
		mock_client = MagicMock()
		mock_connectdb.return_value = mock_client
		
		# Execute
		main.main()
		
		# Assert
		mock_run.assert_called_once_with(main.app, host="0.0.0.0", port=8000)
	
	@patch('main.connectDB')
	@patch('main.run')
	@patch('main.getenv')
	@patch('main.sys.exit')
	def test_db_connection_exception(self, mock_exit, mock_getenv, mock_run, mock_connectdb):
		"""Test handling of exception during database connection"""
		# Setup mocks
		mock_getenv.side_effect = lambda key, default=None: {
			'DB_URL': 'mongodb://testdb:27017',
			'PORT': '9000'
		}.get(key, default)
		
		mock_connectdb.side_effect = Exception("Test exception")
		
		# Capture stdout
		captured_output = io.StringIO()
		sys.stdout = captured_output
		
		# Execute
		main.main()
		
		# Reset stdout
		sys.stdout = sys.__stdout__
		
		# Assert
		mock_connectdb.assert_called_once_with('mongodb://testdb:27017')
		mock_exit.assert_called_once_with(1)
		mock_run.assert_not_called()
		self.assertIn("Error: Test exception", captured_output.getvalue())


if __name__ == '__main__':
	unittest.main()
