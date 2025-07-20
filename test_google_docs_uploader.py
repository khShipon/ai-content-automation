import pytest
import os
import pickle
from unittest.mock import Mock, patch, mock_open, MagicMock
from google.auth.exceptions import RefreshError
from googleapiclient.errors import HttpError
import google_docs_uploader


class TestGoogleDocsUploader:
    
    def setup_method(self):
        """Setup method called before each test"""
        self.mock_creds = Mock()
        self.mock_creds.valid = True
        self.mock_creds.expired = False
        self.mock_creds.refresh_token = "refresh_token"
        
    @patch('google_docs_uploader.build')
    @patch('google_docs_uploader.pickle.load')
    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_get_google_docs_service_with_valid_token(self, mock_file, mock_exists, mock_pickle_load, mock_build):
        """Test getting Google Docs service with valid existing token"""
        mock_exists.return_value = True
        mock_pickle_load.return_value = self.mock_creds
        mock_service = Mock()
        mock_build.return_value = mock_service
        
        service = google_docs_uploader.get_google_docs_service()
        
        assert service == mock_service
        mock_exists.assert_called_with('token.pickle')
        mock_build.assert_called_once_with('docs', 'v1', credentials=self.mock_creds)
    
    @patch('google_docs_uploader.build')
    @patch('google_docs_uploader.pickle.dump')
    @patch('google_docs_uploader.pickle.load')
    @patch('google_docs_uploader.Request')
    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_get_google_docs_service_with_expired_token(self, mock_file, mock_exists, mock_request, mock_pickle_load, mock_pickle_dump, mock_build):
        """Test getting Google Docs service with expired token that can be refreshed"""
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
        
        service = google_docs_uploader.get_google_docs_service()
        
        assert service == mock_service
        expired_creds.refresh.assert_called_once()
        mock_pickle_dump.assert_called_once()
    
    @patch('google_docs_uploader.build')
    @patch('google_docs_uploader.pickle.dump')
    @patch('google_docs_uploader.pickle.load')
    @patch('google_docs_uploader.InstalledAppFlow.from_client_secrets_file')
    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_get_google_docs_service_refresh_error(self, mock_file, mock_exists, mock_flow_class, mock_pickle_load, mock_pickle_dump, mock_build):
        """Test getting Google Docs service when token refresh fails"""
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
        
        service = google_docs_uploader.get_google_docs_service()
        
        assert service == mock_service
        mock_flow.run_local_server.assert_called_once_with(port=0)
        mock_pickle_dump.assert_called_once()
    
    @patch('google_docs_uploader.build')
    @patch('google_docs_uploader.pickle.dump')
    @patch('google_docs_uploader.InstalledAppFlow.from_client_secrets_file')
    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_get_google_docs_service_no_token_file(self, mock_file, mock_exists, mock_flow_class, mock_pickle_dump, mock_build):
        """Test getting Google Docs service when no token file exists"""
        mock_exists.return_value = False
        
        # Mock the flow for new authentication
        mock_flow = Mock()
        new_creds = Mock()
        new_creds.valid = True
        mock_flow.run_local_server.return_value = new_creds
        mock_flow_class.return_value = mock_flow
        
        mock_service = Mock()
        mock_build.return_value = mock_service
        
        service = google_docs_uploader.get_google_docs_service()
        
        assert service == mock_service
        mock_flow_class.assert_called_once_with('credentials.json', google_docs_uploader.SCOPES)
        mock_flow.run_local_server.assert_called_once_with(port=0)
        mock_pickle_dump.assert_called_once()
    
    @patch('google_docs_uploader.build', side_effect=Exception("Build failed"))
    @patch('google_docs_uploader.pickle.load')
    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_get_google_docs_service_build_error(self, mock_file, mock_exists, mock_pickle_load, mock_build):
        """Test getting Google Docs service when build fails"""
        mock_exists.return_value = True
        mock_pickle_load.return_value = self.mock_creds
        
        with pytest.raises(Exception, match="Build failed"):
            google_docs_uploader.get_google_docs_service()
    
    @patch('google_docs_uploader.get_google_docs_service')
    def test_create_google_doc_success(self, mock_get_service):
        """Test successful Google Doc creation"""
        # Mock the service and its methods
        mock_service = Mock()
        mock_get_service.return_value = mock_service
        
        # Mock document creation
        mock_doc_response = {'documentId': 'test_doc_id_123'}
        mock_service.documents().create().execute.return_value = mock_doc_response
        
        # Mock batch update
        mock_service.documents().batchUpdate().execute.return_value = {}
        
        title = "Test Document"
        content = "This is test content"
        
        doc_id = google_docs_uploader.create_google_doc(title, content)
        
        assert doc_id == 'test_doc_id_123'
        
        # Verify document creation call
        mock_service.documents().create.assert_called_once_with(body={"title": title})
        
        # Verify batch update call
        expected_requests = [
            {
                'insertText': {
                    'location': {'index': 1},
                    'text': content
                }
            }
        ]
        mock_service.documents().batchUpdate.assert_called_once_with(
            documentId='test_doc_id_123',
            body={'requests': expected_requests}
        )
    
    @patch('google_docs_uploader.get_google_docs_service')
    def test_create_google_doc_http_error(self, mock_get_service):
        """Test Google Doc creation with HTTP error"""
        mock_service = Mock()
        mock_get_service.return_value = mock_service
        
        # Mock HTTP error during document creation
        http_error = HttpError(resp=Mock(status=403), content=b'Forbidden')
        mock_service.documents().create().execute.side_effect = http_error
        
        title = "Test Document"
        content = "This is test content"
        
        with pytest.raises(HttpError):
            google_docs_uploader.create_google_doc(title, content)
    
    @patch('google_docs_uploader.get_google_docs_service')
    def test_create_google_doc_general_error(self, mock_get_service):
        """Test Google Doc creation with general error"""
        mock_service = Mock()
        mock_get_service.return_value = mock_service
        
        # Mock general error during document creation
        mock_service.documents().create().execute.side_effect = Exception("General error")
        
        title = "Test Document"
        content = "This is test content"
        
        with pytest.raises(Exception, match="General error"):
            google_docs_uploader.create_google_doc(title, content)
    
    @patch('google_docs_uploader.get_google_docs_service')
    def test_create_google_doc_batch_update_error(self, mock_get_service):
        """Test Google Doc creation when batch update fails"""
        mock_service = Mock()
        mock_get_service.return_value = mock_service
        
        # Mock successful document creation
        mock_doc_response = {'documentId': 'test_doc_id_123'}
        mock_service.documents().create().execute.return_value = mock_doc_response
        
        # Mock batch update error
        mock_service.documents().batchUpdate().execute.side_effect = Exception("Batch update failed")
        
        title = "Test Document"
        content = "This is test content"
        
        with pytest.raises(Exception, match="Batch update failed"):
            google_docs_uploader.create_google_doc(title, content)


if __name__ == "__main__":
    pytest.main([__file__])
