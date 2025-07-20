import pytest
import os
import pickle
from unittest.mock import Mock, patch, mock_open
from google.auth.exceptions import RefreshError
from googleapiclient.errors import HttpError
import google_drive_uploader


class TestGoogleDriveUploader:
    
    def setup_method(self):
        """Setup method called before each test"""
        self.mock_creds = Mock()
        self.mock_creds.valid = True
        self.mock_creds.expired = False
        self.mock_creds.refresh_token = "refresh_token"
        
    @patch('google_drive_uploader.build')
    @patch('google_drive_uploader.pickle.load')
    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_get_drive_service_with_valid_token(self, mock_file, mock_exists, mock_pickle_load, mock_build):
        """Test getting Google Drive service with valid existing token"""
        mock_exists.return_value = True
        mock_pickle_load.return_value = self.mock_creds
        mock_service = Mock()
        mock_build.return_value = mock_service
        
        service = google_drive_uploader.get_drive_service()
        
        assert service == mock_service
        mock_exists.assert_called_with('token_drive.pickle')
        mock_build.assert_called_once_with('drive', 'v3', credentials=self.mock_creds)
    
    @patch('google_drive_uploader.build')
    @patch('google_drive_uploader.pickle.dump')
    @patch('google_drive_uploader.pickle.load')
    @patch('google_drive_uploader.Request')
    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_get_drive_service_with_expired_token(self, mock_file, mock_exists, mock_request, mock_pickle_load, mock_pickle_dump, mock_build):
        """Test getting Google Drive service with expired token that can be refreshed"""
        mock_exists.return_value = True
        expired_creds = Mock()
        expired_creds.valid = False
        expired_creds.expired = True
        expired_creds.refresh_token = "refresh_token"
        mock_pickle_load.return_value = expired_creds
        
        # After refresh, make it valid
        def refresh_side_effect(request):
            expired_creds.valid = True
        expired_creds.refresh.side_effect = refresh_side_effect
        
        mock_service = Mock()
        mock_build.return_value = mock_service
        
        service = google_drive_uploader.get_drive_service()
        
        assert service == mock_service
        expired_creds.refresh.assert_called_once()
        mock_pickle_dump.assert_called_once()
    
    @patch('google_drive_uploader.build')
    @patch('google_drive_uploader.pickle.dump')
    @patch('google_drive_uploader.pickle.load')
    @patch('google_drive_uploader.InstalledAppFlow.from_client_secrets_file')
    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_get_drive_service_refresh_error(self, mock_file, mock_exists, mock_flow_class, mock_pickle_load, mock_pickle_dump, mock_build):
        """Test getting Google Drive service when token refresh fails"""
        mock_exists.return_value = True
        expired_creds = Mock()
        expired_creds.valid = False
        expired_creds.expired = True
        expired_creds.refresh_token = "refresh_token"
        expired_creds.refresh.side_effect = RefreshError("Refresh failed")
        mock_pickle_load.return_value = expired_creds
        
        # Mock the flow for new authentication
        mock_flow = Mock()
        new_creds = Mock()
        new_creds.valid = True
        mock_flow.run_local_server.return_value = new_creds
        mock_flow_class.return_value = mock_flow
        
        mock_service = Mock()
        mock_build.return_value = mock_service
        
        service = google_drive_uploader.get_drive_service()
        
        assert service == mock_service
        mock_flow.run_local_server.assert_called_once_with(port=0)
        mock_pickle_dump.assert_called_once()
    
    @patch('google_drive_uploader.get_drive_service')
    def test_move_doc_to_folder_success(self, mock_get_service):
        """Test successful document move to folder"""
        # Mock the service and its methods
        mock_service = Mock()
        mock_get_service.return_value = mock_service
        
        # Mock file get response
        mock_file_get_response = {'parents': ['old_parent_id']}
        mock_service.files().get().execute.return_value = mock_file_get_response
        
        # Mock file update response
        mock_file_update_response = {'id': 'test_doc_id', 'parents': ['new_folder_id']}
        mock_service.files().update().execute.return_value = mock_file_update_response
        
        doc_id = "test_doc_id"
        folder_id = "new_folder_id"
        
        result = google_drive_uploader.move_doc_to_folder(doc_id, folder_id)
        
        assert result == mock_file_update_response
        
        # Verify file get call
        mock_service.files().get.assert_called_once_with(fileId=doc_id, fields='parents')
        
        # Verify file update call
        mock_service.files().update.assert_called_once_with(
            fileId=doc_id,
            addParents=folder_id,
            removeParents='old_parent_id',
            fields='id, parents'
        )
    
    @patch('google_drive_uploader.get_drive_service')
    def test_move_doc_to_folder_http_error(self, mock_get_service):
        """Test document move with HTTP error"""
        mock_service = Mock()
        mock_get_service.return_value = mock_service
        
        # Mock HTTP error during file get
        http_error = HttpError(resp=Mock(status=404), content=b'Not Found')
        mock_service.files().get().execute.side_effect = http_error
        
        doc_id = "test_doc_id"
        folder_id = "new_folder_id"
        
        with pytest.raises(HttpError):
            google_drive_uploader.move_doc_to_folder(doc_id, folder_id)
    
    @patch('google_drive_uploader.get_drive_service')
    def test_move_doc_to_folder_general_error(self, mock_get_service):
        """Test document move with general error"""
        mock_service = Mock()
        mock_get_service.return_value = mock_service
        
        # Mock general error during file get
        mock_service.files().get().execute.side_effect = Exception("General error")
        
        doc_id = "test_doc_id"
        folder_id = "new_folder_id"
        
        with pytest.raises(Exception, match="General error"):
            google_drive_uploader.move_doc_to_folder(doc_id, folder_id)
    
    @patch('google_drive_uploader.get_drive_service')
    def test_move_doc_to_folder_multiple_parents(self, mock_get_service):
        """Test document move when file has multiple parents"""
        mock_service = Mock()
        mock_get_service.return_value = mock_service
        
        # Mock file get response with multiple parents
        mock_file_get_response = {'parents': ['parent1', 'parent2', 'parent3']}
        mock_service.files().get().execute.return_value = mock_file_get_response
        
        # Mock file update response
        mock_file_update_response = {'id': 'test_doc_id', 'parents': ['new_folder_id']}
        mock_service.files().update().execute.return_value = mock_file_update_response
        
        doc_id = "test_doc_id"
        folder_id = "new_folder_id"
        
        result = google_drive_uploader.move_doc_to_folder(doc_id, folder_id)
        
        assert result == mock_file_update_response
        
        # Verify file update call with comma-separated parents
        mock_service.files().update.assert_called_once_with(
            fileId=doc_id,
            addParents=folder_id,
            removeParents='parent1,parent2,parent3',
            fields='id, parents'
        )
    
    @patch('google_drive_uploader.get_drive_service')
    def test_move_doc_to_folder_no_parents(self, mock_get_service):
        """Test document move when file has no parents"""
        mock_service = Mock()
        mock_get_service.return_value = mock_service
        
        # Mock file get response with no parents
        mock_file_get_response = {}
        mock_service.files().get().execute.return_value = mock_file_get_response
        
        # Mock file update response
        mock_file_update_response = {'id': 'test_doc_id', 'parents': ['new_folder_id']}
        mock_service.files().update().execute.return_value = mock_file_update_response
        
        doc_id = "test_doc_id"
        folder_id = "new_folder_id"
        
        result = google_drive_uploader.move_doc_to_folder(doc_id, folder_id)
        
        assert result == mock_file_update_response
        
        # Verify file update call with empty removeParents
        mock_service.files().update.assert_called_once_with(
            fileId=doc_id,
            addParents=folder_id,
            removeParents='',
            fields='id, parents'
        )


if __name__ == "__main__":
    pytest.main([__file__])
