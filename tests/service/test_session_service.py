import unittest
from unittest.mock import patch, Mock, AsyncMock

import asynctest

from src.service.session_service import SessionService


class SessionServiceTests(asynctest.TestCase):
    @patch('aiohttp.ClientSession')
    async def test_session_service_setup_creates_session(self, mock_session):
        service = SessionService()
        service.session = mock_session
        await service.__aenter__()
        mock_session.assert_called_once()

    @patch('aiohttp.ClientSession', new_callable=AsyncMock)
    async def test_session_service_terminate_closes_session(self, mock_session):
        service = SessionService()
        service.session = mock_session
        await service.__aexit__(None, None, None)
        mock_session.close.assert_called_once()

    @patch('aiohttp.ClientSession', new_callable=AsyncMock)
    async def test_session_service_get_makes_request(self, mock_session):
        service = SessionService()
        service.session = mock_session
        await service.get('https://test.com')
        mock_session.get.assert_called_once_with('https://test.com')


if __name__ == '__main__':
    unittest.main()
