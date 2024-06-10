import unittest
from unittest.mock import patch, Mock, AsyncMock

import asynctest

from src.service.session_service import SessionService


class SessionServiceTests(asynctest.TestCase):
    @patch('aiohttp.ClientSession', new_callable=AsyncMock)
    async def test_session_service_setup_creates_session(self, mock_session):
        service = SessionService()
        await service.setup()
        mock_session.assert_called_once()

    @patch('aiohttp.ClientSession', new_callable=AsyncMock)
    async def test_session_service_terminate_closes_session(self, mock_session):
        service = SessionService()
        service.session = mock_session
        await service.terminate()
        mock_session.close.assert_called_once()

    @patch('aiohttp.ClientSession', new_callable=AsyncMock)
    async def test_session_service_get_makes_request(self, mock_session):
        service = SessionService()
        service.session = mock_session
        await service.get('http://test.com')
        mock_session.get.assert_called_once_with('http://test.com')


if __name__ == '__main__':
    unittest.main()
