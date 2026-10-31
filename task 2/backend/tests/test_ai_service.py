import pytest
from unittest.mock import AsyncMock, patch
from app.services.ai_service import AIService
from app.schemas.ai import AIRequest, AIResponse


@pytest.mark.asyncio
async def test_ai_service_no_api_key():
    """Test AI service when no API key is configured"""
    service = AIService()
    service.api_key = None
    
    request = AIRequest(glucose=100, haemoglobin=14, cholesterol=200)
    response = await service.analyze(request)
    
    assert response.status == "unavailable"
    assert response.remarks is None
    assert response.provider is None


@pytest.mark.asyncio
async def test_ai_service_timeout():
    """Test AI service timeout handling"""
    service = AIService()
    service.api_key = "test-key"
    
    request = AIRequest(glucose=100, haemoglobin=14, cholesterol=200)
    
    with patch('httpx.AsyncClient') as mock_client:
        mock_client_instance = AsyncMock()
        mock_client_instance.__aenter__.return_value = mock_client_instance
        mock_client_instance.post.side_effect = Exception("Timeout")
        mock_client.return_value = mock_client_instance
        
        response = await service.analyze(request)
        assert response.status == "failed"


@pytest.mark.asyncio
async def test_ai_service_successful_response():
    """Test successful AI service response"""
    service = AIService()
    service.api_key = "test-key"
    service.provider = "openai"
    
    request = AIRequest(glucose=100, haemoglobin=14, cholesterol=200)
    
    mock_response = AsyncMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "choices": [{
            "message": {
                "content": "Test AI remark about blood values."
            }
        }]
    }
    
    with patch('httpx.AsyncClient') as mock_client:
        mock_client_instance = AsyncMock()
        mock_client_instance.__aenter__.return_value = mock_client_instance
        mock_client_instance.post.return_value = mock_response
        mock_client.return_value = mock_client_instance
        
        response = await service.analyze(request)
        assert response.status == "completed"
        assert response.remarks == "Test AI remark about blood values."
        assert response.provider == "openai"


@pytest.mark.asyncio
async def test_ai_service_empty_response():
    """Test AI service with empty response"""
    service = AIService()
    service.api_key = "test-key"
    service.provider = "openai"
    
    request = AIRequest(glucose=100, haemoglobin=14, cholesterol=200)
    
    mock_response = AsyncMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "choices": [{
            "message": {
                "content": ""
            }
        }]
    }
    
    with patch('httpx.AsyncClient') as mock_client:
        mock_client_instance = AsyncMock()
        mock_client_instance.__aenter__.return_value = mock_client_instance
        mock_client_instance.post.return_value = mock_response
        mock_client.return_value = mock_client_instance
        
        response = await service.analyze(request)
        assert response.status == "failed"
