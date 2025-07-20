import pytest
import os
from unittest.mock import Mock, patch, MagicMock
import main


class TestMain:
    
    def setup_method(self):
        """Setup method called before each test"""
        self.mock_generator = Mock()
        self.mock_topic = "Present Simple Tense"
        self.mock_content = "আজকে আমরা শিখবো Present Simple Tense. It is used for regular actions."
        self.mock_doc_id = "test_doc_id_123"
        self.mock_folder_id = "test_folder_id_456"
    
    @patch('main.move_doc_to_folder')
    @patch('main.create_google_doc')
    @patch('main.ContentGenerator')
    @patch.dict(os.environ, {'GOOGLE_DRIVE_FOLDER_ID': 'test_folder_id_456'}, clear=True)
    @patch('main.datetime')
    def test_main_success_with_folder_id(self, mock_datetime, mock_content_generator_class, mock_create_doc, mock_move_doc):
        """Test successful main execution with valid folder ID"""
        # Mock datetime
        mock_datetime.datetime.now().strftime.return_value = "2024-01-15"

        # Mock ContentGenerator
        mock_content_generator_class.return_value = self.mock_generator
        self.mock_generator.get_random_topic.return_value = self.mock_topic
        self.mock_generator.generate_content.return_value = self.mock_content

        # Mock Google Docs creation
        mock_create_doc.return_value = self.mock_doc_id

        # Mock Google Drive move
        mock_move_doc.return_value = True

        # Execute main function
        main.main()

        # Verify ContentGenerator was called correctly
        mock_content_generator_class.assert_called_once()
        self.mock_generator.get_random_topic.assert_called_once()
        self.mock_generator.generate_content.assert_called_once_with(self.mock_topic)

        # Verify Google Doc creation
        expected_title = f"2024-01-15 - {self.mock_topic}"
        mock_create_doc.assert_called_once_with(expected_title, self.mock_content)

        # Verify Google Drive move
        mock_move_doc.assert_called_once_with(self.mock_doc_id, 'test_folder_id_456')
    
    @patch('main.move_doc_to_folder')
    @patch('main.create_google_doc')
    @patch('main.ContentGenerator')
    @patch.dict(os.environ, {}, clear=True)  # Clear environment variables
    @patch('main.datetime')
    def test_main_success_without_folder_id(self, mock_datetime, mock_content_generator_class, mock_create_doc, mock_move_doc):
        """Test main execution without folder ID (should skip move step)"""
        # Mock datetime
        mock_datetime.datetime.now().strftime.return_value = "2024-01-15"
        
        # Mock ContentGenerator
        mock_content_generator_class.return_value = self.mock_generator
        self.mock_generator.get_random_topic.return_value = self.mock_topic
        self.mock_generator.generate_content.return_value = self.mock_content
        
        # Mock Google Docs creation
        mock_create_doc.return_value = self.mock_doc_id
        
        # Execute main function
        main.main()
        
        # Verify ContentGenerator was called correctly
        mock_content_generator_class.assert_called_once()
        self.mock_generator.get_random_topic.assert_called_once()
        self.mock_generator.generate_content.assert_called_once_with(self.mock_topic)
        
        # Verify Google Doc creation
        expected_title = f"2024-01-15 - {self.mock_topic}"
        mock_create_doc.assert_called_once_with(expected_title, self.mock_content)
        
        # Verify Google Drive move was NOT called
        mock_move_doc.assert_not_called()
    
    @patch('main.move_doc_to_folder')
    @patch('main.create_google_doc')
    @patch('main.ContentGenerator')
    @patch.dict(os.environ, {'GOOGLE_DRIVE_FOLDER_ID': 'your_folder_id_here'})
    @patch('main.datetime')
    def test_main_with_default_folder_id(self, mock_datetime, mock_content_generator_class, mock_create_doc, mock_move_doc):
        """Test main execution with default folder ID (should skip move step)"""
        # Mock datetime
        mock_datetime.datetime.now().strftime.return_value = "2024-01-15"
        
        # Mock ContentGenerator
        mock_content_generator_class.return_value = self.mock_generator
        self.mock_generator.get_random_topic.return_value = self.mock_topic
        self.mock_generator.generate_content.return_value = self.mock_content
        
        # Mock Google Docs creation
        mock_create_doc.return_value = self.mock_doc_id
        
        # Execute main function
        main.main()
        
        # Verify ContentGenerator was called correctly
        mock_content_generator_class.assert_called_once()
        self.mock_generator.get_random_topic.assert_called_once()
        self.mock_generator.generate_content.assert_called_once_with(self.mock_topic)
        
        # Verify Google Doc creation
        expected_title = f"2024-01-15 - {self.mock_topic}"
        mock_create_doc.assert_called_once_with(expected_title, self.mock_content)
        
        # Verify Google Drive move was NOT called (because of default folder ID)
        mock_move_doc.assert_not_called()
    
    @patch('main.ContentGenerator')
    def test_main_content_generation_error(self, mock_content_generator_class):
        """Test main execution when content generation fails"""
        # Mock ContentGenerator to raise an exception
        mock_content_generator_class.return_value = self.mock_generator
        self.mock_generator.get_random_topic.side_effect = Exception("Topic loading failed")
        
        # Execute main function (should not raise exception due to try-catch)
        main.main()
        
        # Verify ContentGenerator was called
        mock_content_generator_class.assert_called_once()
        self.mock_generator.get_random_topic.assert_called_once()
    
    @patch('main.move_doc_to_folder')
    @patch('main.create_google_doc')
    @patch('main.ContentGenerator')
    @patch.dict(os.environ, {'GOOGLE_DRIVE_FOLDER_ID': 'test_folder_id_456'})
    @patch('main.datetime')
    def test_main_google_doc_creation_error(self, mock_datetime, mock_content_generator_class, mock_create_doc, mock_move_doc):
        """Test main execution when Google Doc creation fails"""
        # Mock datetime
        mock_datetime.datetime.now().strftime.return_value = "2024-01-15"
        
        # Mock ContentGenerator
        mock_content_generator_class.return_value = self.mock_generator
        self.mock_generator.get_random_topic.return_value = self.mock_topic
        self.mock_generator.generate_content.return_value = self.mock_content
        
        # Mock Google Docs creation to fail
        mock_create_doc.side_effect = Exception("Google Doc creation failed")
        
        # Execute main function (should not raise exception due to try-catch)
        main.main()
        
        # Verify ContentGenerator was called correctly
        mock_content_generator_class.assert_called_once()
        self.mock_generator.get_random_topic.assert_called_once()
        self.mock_generator.generate_content.assert_called_once_with(self.mock_topic)
        
        # Verify Google Doc creation was attempted
        expected_title = f"2024-01-15 - {self.mock_topic}"
        mock_create_doc.assert_called_once_with(expected_title, self.mock_content)
        
        # Verify Google Drive move was NOT called (because doc creation failed)
        mock_move_doc.assert_not_called()
    
    @patch('main.move_doc_to_folder')
    @patch('main.create_google_doc')
    @patch('main.ContentGenerator')
    @patch.dict(os.environ, {'GOOGLE_DRIVE_FOLDER_ID': 'test_folder_id_456'})
    @patch('main.datetime')
    def test_main_google_drive_move_error(self, mock_datetime, mock_content_generator_class, mock_create_doc, mock_move_doc):
        """Test main execution when Google Drive move fails"""
        # Mock datetime
        mock_datetime.datetime.now().strftime.return_value = "2024-01-15"
        
        # Mock ContentGenerator
        mock_content_generator_class.return_value = self.mock_generator
        self.mock_generator.get_random_topic.return_value = self.mock_topic
        self.mock_generator.generate_content.return_value = self.mock_content
        
        # Mock Google Docs creation
        mock_create_doc.return_value = self.mock_doc_id
        
        # Mock Google Drive move to fail
        mock_move_doc.side_effect = Exception("Google Drive move failed")
        
        # Execute main function (should not raise exception due to try-catch)
        main.main()
        
        # Verify ContentGenerator was called correctly
        mock_content_generator_class.assert_called_once()
        self.mock_generator.get_random_topic.assert_called_once()
        self.mock_generator.generate_content.assert_called_once_with(self.mock_topic)
        
        # Verify Google Doc creation
        expected_title = f"2024-01-15 - {self.mock_topic}"
        mock_create_doc.assert_called_once_with(expected_title, self.mock_content)
        
        # Verify Google Drive move was attempted
        mock_move_doc.assert_called_once_with(self.mock_doc_id, 'test_folder_id_456')


if __name__ == "__main__":
    pytest.main([__file__])
