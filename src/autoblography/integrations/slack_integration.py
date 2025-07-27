"""
Slack integration for fetching thread messages
"""

from urllib.parse import urlparse
from typing import List, Tuple, Optional
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from ..config.settings import settings


class SlackIntegration:
    """Slack integration for fetching thread messages"""
    
    def __init__(self, token: Optional[str] = None):
        """
        Initialize Slack integration
        
        Args:
            token: Slack API token. If not provided, uses SLACK_TOKEN from settings
        """
        self.token = token or settings.slack_token
        if not self.token:
            raise ValueError("Slack token is required. Set SLACK_TOKEN environment variable or pass token parameter.")
        
        self.client = WebClient(token=self.token)

    def _parse_permalink(self, thread_link: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Extracts channel ID and thread timestamp from a Slack permalink.
        
        Args:
            thread_link: Slack thread permalink URL
            
        Returns:
            Tuple of (channel_id, thread_timestamp) or (None, None) if parsing fails
        """
        try:
            path_parts = urlparse(thread_link).path.strip('/').split('/')
            # Expected path: ['archives', 'C1234567', 'p1234567890123456']
            if len(path_parts) == 3 and path_parts[0] == 'archives':
                channel_id = path_parts[1]
                ts_string = path_parts[2][1:]  # Remove the 'p'
                thread_ts = f"{ts_string[:-6]}.{ts_string[-6:]}"
                return channel_id, thread_ts
        except Exception as e:
            print(f"Error parsing permalink: {e}")

        return None, None

    def get_all_thread_messages(self, thread_link: str) -> List[dict]:
        """
        Fetches all messages from a Slack thread given its permalink.

        Args:
            thread_link: The URL of the thread's parent message.

        Returns:
            List of message objects from the thread, or an empty list if an error occurs.
        """
        all_messages = []
        channel_id, thread_ts = self._parse_permalink(thread_link)

        if not channel_id or not thread_ts:
            print(f"❌ Could not parse Channel ID and Timestamp from link: {thread_link}")
            return all_messages

        print(f"Fetching thread from Channel ID: {channel_id} and Timestamp: {thread_ts}")

        try:
            cursor = None
            while True:
                # Call the conversations.replies method using the WebClient
                result = self.client.conversations_replies(
                    channel=channel_id,
                    ts=thread_ts,
                    cursor=cursor,
                    limit=200  # Max limit is 1000, 200 is a safe default
                )

                all_messages.extend(result['messages'])

                # Check for more messages
                if not result['has_more']:
                    break

                cursor = result.get('response_metadata', {}).get('next_cursor')

        except SlackApiError as e:
            print(f"Error fetching thread replies: {e.response['error']}")
            return []

        print(f"✅ Successfully fetched {len(all_messages)} messages from the thread.")
        return all_messages 