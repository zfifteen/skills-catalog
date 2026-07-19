#!/usr/bin/env python3
from __future__ import annotations

import argparse
import asyncio
import os
import sqlite3
from pathlib import Path
from typing import Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

DEFAULT_DB = "/Users/velocityworks/.agent_bus/agent_bus.sqlite"
DEFAULT_AGENT = "codex"
DEFAULT_COMMAND = "uvx"
DEFAULT_ARGS = ["--from", "agent-bus-mcp==0.5.0", "agent-bus"]


def server_params() -> StdioServerParameters:
    env = os.environ.copy()
    env.setdefault("AGENT_BUS_DB", DEFAULT_DB)
    return StdioServerParameters(command=DEFAULT_COMMAND, args=DEFAULT_ARGS, env=env)


async def call_tool(name: str, args: dict[str, Any]) -> Any:
    async with stdio_client(server_params()) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            return await session.call_tool(name, args)


def local_reclaim_token(topic_id: str, agent_name: str) -> str | None:
    db_path = os.environ.get("AGENT_BUS_DB", DEFAULT_DB)
    if not Path(db_path).exists():
        return None
    with sqlite3.connect(db_path) as conn:
        row = conn.execute(
            """
            select reclaim_token
            from agent_name_reservations
            where topic_id = ? and agent_name = ?
            """,
            (topic_id, agent_name),
        ).fetchone()
    return None if row is None else str(row[0])


async def joined_session(topic_name: str, agent_name: str, reclaim_token: str | None):
    params = server_params()
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            topic = await session.call_tool(
                "topic_create",
                {"name": topic_name, "mode": "reuse", "metadata": {"source": "codex-helper"}},
            )
            topic_id = topic.structuredContent["topic_id"]
            token = reclaim_token or local_reclaim_token(topic_id, agent_name)
            join_args: dict[str, Any] = {"agent_name": agent_name, "topic_id": topic_id}
            if token:
                join_args["reclaim_token"] = token
            joined = await session.call_tool("topic_join", join_args)
            yield session, joined.structuredContent["topic_id"]


async def cmd_ping(_: argparse.Namespace) -> None:
    result = await call_tool("ping", {})
    print(result.structuredContent)


async def cmd_topics(_: argparse.Namespace) -> None:
    result = await call_tool("topic_list", {"status": "open"})
    for topic in result.structuredContent["topics"]:
        print(f"{topic['topic_id']}\t{topic['name']}\t{topic['status']}")


async def cmd_history(args: argparse.Namespace) -> None:
    async for session, topic_id in joined_session(args.topic, args.agent, args.reclaim_token):
        await session.call_tool("cursor_reset", {"topic_id": topic_id, "last_seq": 0})
        result = await session.call_tool(
            "sync",
            {
                "topic_id": topic_id,
                "max_items": args.max_items,
                "include_self": True,
                "wait_seconds": 0,
            },
        )
        for message in result.structuredContent["received"]:
            print("---")
            print(
                f"seq={message['seq']} sender={message['sender']} "
                f"type={message['message_type']} id={message['message_id']}"
            )
            print(message["content_markdown"])


async def cmd_post(args: argparse.Namespace) -> None:
    body = Path(args.message_file).read_text(encoding="utf-8")
    async for session, topic_id in joined_session(args.topic, args.agent, args.reclaim_token):
        item: dict[str, Any] = {
            "content_markdown": body,
            "message_type": args.type,
            "metadata": {"sender_runtime": "codex-desktop"},
            "client_message_id": args.client_message_id,
        }
        if args.reply_to:
            item["reply_to"] = args.reply_to
        result = await session.call_tool(
            "sync",
            {
                "topic_id": topic_id,
                "outbox": [item],
                "include_self": True,
                "wait_seconds": 0,
            },
        )
        for sent in result.structuredContent["sent"]:
            message = sent["message"]
            print(
                f"sent seq={message['seq']} id={message['message_id']} "
                f"duplicate={sent['duplicate']}"
            )


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Agent Bus MCP helper for Codex/Grok collaboration.")
    sub = p.add_subparsers(dest="command", required=True)

    sub.add_parser("ping")
    sub.add_parser("topics")

    history = sub.add_parser("history")
    history.add_argument("topic")
    history.add_argument("--agent", default=DEFAULT_AGENT)
    history.add_argument("--reclaim-token")
    history.add_argument("--max-items", type=int, default=20)

    post = sub.add_parser("post")
    post.add_argument("topic")
    post.add_argument("message_file")
    post.add_argument("--agent", default=DEFAULT_AGENT)
    post.add_argument("--reclaim-token")
    post.add_argument("--type", default="message")
    post.add_argument("--reply-to")
    post.add_argument("--client-message-id")

    return p


async def main() -> None:
    args = parser().parse_args()
    if args.command == "ping":
        await cmd_ping(args)
    elif args.command == "topics":
        await cmd_topics(args)
    elif args.command == "history":
        await cmd_history(args)
    elif args.command == "post":
        await cmd_post(args)


if __name__ == "__main__":
    asyncio.run(main())
