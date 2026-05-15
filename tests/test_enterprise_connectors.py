"""Enterprise connectors — Drive / Sheets / Slack / Teams.

These power enterprise delivery (data ingestion + notifications). With no
credentials configured they must degrade gracefully — never raise, never
make a live call — so CI and unconfigured environments stay safe.
"""
from __future__ import annotations

import pytest

from integrations.google_drive import DriveResult, GoogleDriveClient
from integrations.google_sheets import GoogleSheetsClient, SheetsResult
from integrations.slack import SlackClient, SlackResult
from integrations.teams import TeamsClient, TeamsResult


@pytest.mark.asyncio
async def test_slack_degrades_gracefully_when_unconfigured() -> None:
    client = SlackClient()
    assert client.configured is False
    result = await client.post_message("#general", "hello")
    assert isinstance(result, SlackResult)
    assert result.success is False
    assert result.error == "slack_not_configured"


@pytest.mark.asyncio
async def test_teams_degrades_gracefully_when_unconfigured() -> None:
    client = TeamsClient()
    assert client.configured is False
    result = await client.post_message("Alert", "build green")
    assert isinstance(result, TeamsResult)
    assert result.success is False
    assert result.error == "teams_not_configured"


@pytest.mark.asyncio
async def test_google_drive_degrades_gracefully_when_unconfigured() -> None:
    client = GoogleDriveClient()
    assert client.configured is False
    listed = await client.list_files()
    assert isinstance(listed, DriveResult)
    assert listed.success is False and listed.error == "google_drive_not_configured"
    fetched = await client.fetch_file_text("file123")
    assert fetched.success is False


@pytest.mark.asyncio
async def test_google_sheets_degrades_gracefully_when_unconfigured() -> None:
    client = GoogleSheetsClient()
    assert client.configured is False
    result = await client.read_range("sheet123", "A1:B10")
    assert isinstance(result, SheetsResult)
    assert result.success is False
    assert result.error == "google_sheets_not_configured"
    assert result.row_count == 0


def test_teams_card_shape() -> None:
    card = TeamsClient()._card("Title", "Body text")
    assert card["@type"] == "MessageCard"
    assert card["title"] == "Title"
    assert card["text"] == "Body text"
