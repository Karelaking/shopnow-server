import logging
import pymongo
import unittest
from unittest.mock import patch, MagicMock
from pymongo.errors import ConnectionFailure, ConfigurationError, ServerSelectionTimeoutError

# Import the module to test
from database.connectDB import connectDB

class TestConnectDB(unittest.TestCase):
    """Test suite for MongoDB connection function"""
    
    @patch('database.connectDB.MongoClient')
    def test_successful_connection(self, mock_client):
        """Test successful MongoDB connection"""
        # Setup mock
        mock_instance = MagicMock()
        mock_client.return_value = mock_instance
        
        # Execute
        result = connectDB("mongodb://localhost:27017")
        
        # Assert
        mock_client.assert_called_once_with("mongodb://localhost:27017", serverSelectionTimeoutMS=5000)
        self.assertEqual(result, mock_instance)
        mock_instance.admin.command.assert_called_once_with('ping')
    
    @patch('database.connectDB.MongoClient')
    @patch('database.connectDB.logging')
    def test_connection_failure(self, mock_logging, mock_client):
        """Test handling of ConnectionFailure exception"""
        # Setup mock
        mock_client.side_effect = ConnectionFailure("Connection error")
        
        # Execute
        result = connectDB("mongodb://invalid:27017")
        
        # Assert
        self.assertIsNone(result)
        mock_logging.error.assert_called_once_with("MongoDB Connection Failed: Connection error")
    
    @patch('database.connectDB.MongoClient')
    @patch('database.connectDB.logging')
    def test_configuration_error(self, mock_logging, mock_client):
        """Test handling of ConfigurationError exception"""
        # Setup mock
        mock_client.side_effect = ConfigurationError("Invalid configuration")
        
        # Execute
        result = connectDB("invalid://url")
        
        # Assert
        self.assertIsNone(result)
        mock_logging.error.assert_called_once_with("MongoDB Configuration Error: Invalid configuration")
    
    @patch('database.connectDB.MongoClient')
    @patch('database.connectDB.logging')
    def test_server_selection_timeout(self, mock_logging, mock_client):
        """Test handling of ServerSelectionTimeoutError exception"""
        # Setup mock
        mock_client.side_effect = ServerSelectionTimeoutError("Server selection timeout")
        
        # Execute
        result = connectDB("mongodb://slowserver:27017")
        
        # Assert
        self.assertIsNone(result)
        mock_logging.error.assert_called_once_with("MongoDB Server Selection Timeout: Server selection timeout")
    
    @patch('database.connectDB.MongoClient')
    @patch('database.connectDB.logging')
    def test_generic_exception(self, mock_logging, mock_client):
        """Test handling of generic exceptions"""
        # Setup mock
        mock_client.side_effect = Exception("Unexpected error")
        
        # Execute
        result = connectDB("mongodb://localhost:27017")
        
        # Assert
        self.assertIsNone(result)
        mock_logging.error.assert_called_once_with("Unexpected error when connecting to MongoDB: Unexpected error")
    
    @patch('database.connectDB.MongoClient')
    def test_connection_with_custom_timeout(self, mock_client):
        """Test connection with custom timeout parameter"""
        # Setup mock
        mock_instance = MagicMock()
        mock_client.return_value = mock_instance
        
        # Execute
        result = connectDB("mongodb://localhost:27017", timeout=10000)
        
        # Assert
        mock_client.assert_called_once_with("mongodb://localhost:27017", serverSelectionTimeoutMS=10000)
        self.assertEqual(result, mock_instance)

    @patch('database.connectDB.MongoClient')
    @patch('database.connectDB.logging')
    def test_ping_failure(self, mock_logging, mock_client):
        """Test handling of ping command failure"""
        # Setup mock
        mock_instance = MagicMock()
        mock_client.return_value = mock_instance
        mock_instance.admin.command.side_effect = ConnectionFailure("Ping failed")
        
        # Execute
        result = connectDB("mongodb://localhost:27017")
        
        # Assert
        self.assertIsNone(result)
        mock_logging.error.assert_called_once_with("MongoDB Connection Failed: Ping failed")

if __name__ == '__main__':
    unittest.main()
