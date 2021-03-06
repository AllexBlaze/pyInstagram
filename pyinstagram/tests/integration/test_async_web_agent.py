import asyncio
import random

import pytest

from pyinstagram.entities import (
    Account,
    Location,
    Media,
    Tag,
)
from .. import config


@pytest.mark.asyncio
async def test_update(async_web_agent):
    await async_web_agent.update()

    assert async_web_agent.rhx_gis is not None
    assert async_web_agent.csrf_token is not None


@pytest.mark.parametrize("username", config.accounts)
@pytest.mark.asyncio
async def test_update_account(async_web_agent, username):
    account = Account(username)
    data = await async_web_agent.update(account)

    assert data is not None
    assert account.id is not None
    assert account.full_name is not None
    assert account.profile_pic_url is not None
    assert account.profile_pic_url_hd is not None
    assert account.biography is not None
    assert account.follows_count is not None
    assert account.followers_count is not None
    assert account.media_count is not None
    assert account.is_private is not None
    assert account.is_verified is not None
    assert account.country_block is not None


@pytest.mark.parametrize("shortcode", [
    random.choice(config.photos + config.photo_sets + config.videos),
])
@pytest.mark.asyncio
async def test_update_media(async_web_agent, shortcode):
    media = Media(shortcode)
    data = await async_web_agent.update(media)

    assert data is not None
    assert media.id is not None
    assert media.code is not None
    assert media.date is not None
    assert media.likes_count is not None
    assert media.comments_count is not None
    assert media.comments_disabled is not None
    assert media.is_video is not None
    assert media.display_url is not None
    assert media.resources is not None
    assert media.is_album is not None


@pytest.mark.parametrize("id", config.locations)
@pytest.mark.asyncio
async def test_update_location(async_web_agent, id):
    location = Location(id)
    data = await async_web_agent.update(location)

    assert data is not None
    assert location.id is not None
    assert location.slug is not None
    assert location.name is not None
    assert location.has_public_page is not None
    assert location.coordinates is not None
    assert location.media_count is not None


@pytest.mark.parametrize("name", config.tags)
@pytest.mark.asyncio
async def test_update_tag(async_web_agent, name):
    tag = Tag(name)
    data = await async_web_agent.update(tag)

    assert data is not None
    assert tag.name is not None
    assert tag.media_count is not None
    assert tag.top_posts


@pytest.mark.parametrize("count, username", [(
    random.randint(100, 500),
    random.choice(config.accounts),
)])
@pytest.mark.asyncio
async def test_get_media_account(async_web_agent, delay, count, username):
    account = Account(username)
    data, pointer = await async_web_agent.get_media(
        account,
        count=count,
        delay=delay,
    )

    assert min(account.media_count, count) == len(data)
    assert (pointer is None) == (account.media_count <= count)


@pytest.mark.parametrize("count, id", [(
    random.randint(100, 500),
    random.choice(config.locations),
)])
@pytest.mark.asyncio
async def test_get_media_location(async_web_agent, delay, count, id):
    location = Location(id)
    data, pointer = await async_web_agent.get_media(
        location,
        count=count,
        delay=delay,
    )

    assert min(location.media_count, count) == len(data)
    assert (pointer is None) == (location.media_count <= count)


@pytest.mark.parametrize("count, name", [(
    random.randint(100, 500),
    random.choice(config.tags),
)])
@pytest.mark.asyncio
async def test_get_media_tag(async_web_agent, count, name):
    tag = Tag(name)
    data, pointer = await async_web_agent.get_media(tag, count=count, delay=delay)

    assert min(tag.media_count, count) == len(data)
    assert (pointer is None) == (tag.media_count <= count)


@pytest.mark.parametrize("shortcode", [
    random.choice(config.photos),
    random.choice(config.photo_sets),
    random.choice(config.videos),
])
@pytest.mark.asyncio
async def test_get_likes(async_web_agent, shortcode):
    media = Media(shortcode)
    data, _ = await async_web_agent.get_likes(media)

    assert media.likes_count >= len(data)


@pytest.mark.parametrize(
    "count, shortcode",
    [(random.randint(100, 500), shortcode) for shortcode in [
        random.choice(config.photos),
        random.choice(config.photo_sets),
        random.choice(config.videos),
    ]],
)
@pytest.mark.asyncio
async def test_get_comments(async_web_agent, delay, count, shortcode):
    media = Media(shortcode)
    data, pointer = await async_web_agent.get_comments(
        media,
        count=count,
        delay=delay,
    )

    assert min(media.comments_count, count) == len(data)
    assert (pointer is None) == (media.comments_count <= count)


@pytest.mark.parametrize("count, username", [(
    random.randint(1, 10),
    random.choice(config.accounts),
)])
@pytest.mark.asyncio
async def test_get_media_account_pointer(async_web_agent, delay, count, username):
    account = Account(username)
    pointer = None
    data = []

    for _ in range(count):
        tmp, pointer = await async_web_agent.get_media(account, pointer=pointer)
        await asyncio.sleep(delay)
        data.extend(tmp)

    assert (pointer is None) == (account.media_count == len(data))


@pytest.mark.parametrize("count, id", [(
    random.randint(1, 10),
    random.choice(config.locations),
)])
@pytest.mark.asyncio
async def test_get_media_location_pointer(async_web_agent, delay, count, id):
    location = Location(id)
    pointer = None
    data = []

    for _ in range(count):
        tmp, pointer = await async_web_agent.get_media(location, pointer=pointer)
        await asyncio.sleep(delay)
        data.extend(tmp)

    assert (pointer is None) == (location.media_count == len(data))


@pytest.mark.parametrize("count, name", [(
    random.randint(1, 10),
    random.choice(config.tags),
)])
@pytest.mark.asyncio
async def test_get_media_tag_pointer(async_web_agent, delay, count, name):
    tag = Tag(name)
    pointer = None
    data = []

    for _ in range(count):
        tmp, pointer = await async_web_agent.get_media(tag, pointer=pointer)
        await asyncio.sleep(delay)
        data.extend(tmp)

    assert (pointer is None) == (tag.media_count == len(data))


@pytest.mark.parametrize(
    "count, shortcode",
    [(random.randint(1, 10), shortcode) for shortcode in [
        random.choice(config.photos),
        random.choice(config.photo_sets),
        random.choice(config.videos),
    ]],
)
@pytest.mark.asyncio
async def test_get_comments_pointer(async_web_agent, delay, count, shortcode):
    media = Media(shortcode)
    pointer = None
    data = []

    for _ in range(count):
        tmp, pointer = await async_web_agent.get_comments(media, pointer=pointer)
        await asyncio.sleep(delay)
        data.extend(tmp)

    assert (pointer is None) == (media.likes_count == len(data))
