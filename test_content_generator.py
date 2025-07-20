import pytest
import os
import tempfile
from unittest.mock import Mock, patch, mock_open
from content_generator import ContentGenerator


class TestContentGenerator:
    
    def setup_method(self):
        """Setup method called before each test"""
        self.test_topics_content = "Present Simple Tense\nFuture Plans\nBangla Food Culture\n"
        
    @patch('content_generator.load_dotenv')
    @patch.dict(os.environ, {'OPENROUTER_API_KEY': 'test_api_key'})
    def test_init_with_default_topics_file(self, mock_load_dotenv):
        """Test ContentGenerator initialization with default topics file"""
        generator = ContentGenerator()
        assert generator.topics_file == 'topics.txt'
        assert generator.client is not None
        mock_load_dotenv.assert_called_once()
    
    @patch('content_generator.load_dotenv')
    @patch.dict(os.environ, {'OPENROUTER_API_KEY': 'test_api_key'})
    def test_init_with_custom_topics_file(self, mock_load_dotenv):
        """Test ContentGenerator initialization with custom topics file"""
        custom_file = 'custom_topics.txt'
        generator = ContentGenerator(topics_file=custom_file)
        assert generator.topics_file == custom_file
        mock_load_dotenv.assert_called_once()
    
    @patch('content_generator.load_dotenv')
    @patch.dict(os.environ, {'OPENROUTER_API_KEY': 'test_api_key'})
    @patch('builtins.open', new_callable=mock_open, read_data="Present Simple Tense\nFuture Plans\nBangla Food Culture\n")
    @patch('random.choice')
    def test_get_random_topic_success(self, mock_choice, mock_file, mock_load_dotenv):
        """Test successful topic selection"""
        mock_choice.return_value = "Present Simple Tense"
        
        generator = ContentGenerator()
        topic = generator.get_random_topic()
        
        assert topic == "Present Simple Tense"
        mock_file.assert_called_once_with('topics.txt', 'r', encoding='utf-8')
        mock_choice.assert_called_once_with(['Present Simple Tense', 'Future Plans', 'Bangla Food Culture'])
    
    @patch('content_generator.load_dotenv')
    @patch.dict(os.environ, {'OPENROUTER_API_KEY': 'test_api_key'})
    @patch('builtins.open', side_effect=FileNotFoundError("File not found"))
    def test_get_random_topic_file_not_found(self, mock_file, mock_load_dotenv):
        """Test topic selection when file is not found"""
        generator = ContentGenerator()
        
        with pytest.raises(FileNotFoundError):
            generator.get_random_topic()
    
    @patch('content_generator.load_dotenv')
    @patch.dict(os.environ, {'OPENROUTER_API_KEY': 'test_api_key'})
    @patch('builtins.open', new_callable=mock_open, read_data="")
    @patch('random.choice', side_effect=IndexError("list index out of range"))
    def test_get_random_topic_empty_file(self, mock_choice, mock_file, mock_load_dotenv):
        """Test topic selection when file is empty"""
        generator = ContentGenerator()
        
        with pytest.raises(IndexError):
            generator.get_random_topic()
    
    @patch('content_generator.load_dotenv')
    @patch.dict(os.environ, {'OPENROUTER_API_KEY': 'test_api_key'})
    def test_generate_content_success(self, mock_load_dotenv):
        """Test successful content generation"""
        # Mock the OpenAI client response
        mock_completion = Mock()
        mock_completion.choices = [Mock()]
        mock_completion.choices[0].message.content = "আজকে আমরা শিখবো Present Simple Tense. It is used for regular actions."
        
        generator = ContentGenerator()
        generator.client.chat.completions.create = Mock(return_value=mock_completion)
        
        topic = "Present Simple Tense"
        content = generator.generate_content(topic)
        
        assert content == "আজকে আমরা শিখবো Present Simple Tense. It is used for regular actions."
        generator.client.chat.completions.create.assert_called_once()
        
        # Verify the call arguments
        call_args = generator.client.chat.completions.create.call_args
        assert call_args[1]['model'] == "moonshotai/kimi-k2:free"
        assert len(call_args[1]['messages']) == 1
        assert call_args[1]['messages'][0]['role'] == 'user'
        assert topic in call_args[1]['messages'][0]['content']
    
    @patch('content_generator.load_dotenv')
    @patch.dict(os.environ, {'OPENROUTER_API_KEY': 'test_api_key'})
    def test_generate_content_api_error(self, mock_load_dotenv):
        """Test content generation when API call fails"""
        generator = ContentGenerator()
        generator.client.chat.completions.create = Mock(side_effect=Exception("API Error"))
        
        topic = "Present Simple Tense"
        
        with pytest.raises(Exception, match="API Error"):
            generator.generate_content(topic)
    
    @patch('content_generator.load_dotenv')
    @patch.dict(os.environ, {'OPENROUTER_API_KEY': 'test_api_key'})
    def test_generate_content_with_whitespace(self, mock_load_dotenv):
        """Test content generation with whitespace handling"""
        # Mock the OpenAI client response with extra whitespace
        mock_completion = Mock()
        mock_completion.choices = [Mock()]
        mock_completion.choices[0].message.content = "  \n  Content with whitespace  \n  "
        
        generator = ContentGenerator()
        generator.client.chat.completions.create = Mock(return_value=mock_completion)
        
        topic = "Test Topic"
        content = generator.generate_content(topic)
        
        assert content == "Content with whitespace"
    
    def test_integration_with_real_topics_file(self):
        """Integration test using the actual topics.txt file"""
        # This test requires the actual topics.txt file to exist
        if os.path.exists('topics.txt'):
            with patch.dict(os.environ, {'OPENROUTER_API_KEY': 'test_api_key'}):
                generator = ContentGenerator()
                
                # Mock the API call to avoid actual API usage
                mock_completion = Mock()
                mock_completion.choices = [Mock()]
                mock_completion.choices[0].message.content = "Test content"
                generator.client.chat.completions.create = Mock(return_value=mock_completion)
                
                topic = generator.get_random_topic()
                assert topic is not None
                assert len(topic.strip()) > 0
                
                content = generator.generate_content(topic)
                assert content == "Test content"
        else:
            pytest.skip("topics.txt file not found")


if __name__ == "__main__":
    pytest.main([__file__])
