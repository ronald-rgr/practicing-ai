import asyncio
import sys
import os
from dotenv import load_dotenv
from contextlib import AsyncExitStack

from mcp_client import MCPClient
from core.bedrock import Bedrock

from core.cli_chat import CliChat
from core.cli import CliApp

load_dotenv()

# Bedrock Config
bedrock_region = os.getenv("BEDROCK_REGION", "")
bedrock_model_id = os.getenv("BEDROCK_MODEL_ID", "")


assert bedrock_region, "Error: bedrock_region cannot be empty. Update .env"
assert bedrock_model_id, "Error: bedrock_model_id cannot be empty. Update .env"


async def main():
    bedrock_service = Bedrock(
        region_name=bedrock_region, model_id=bedrock_model_id
    )

    server_scripts = sys.argv[1:]
    clients = {}

    command, args = (
        ("uv", ["run", "mcp_server.py"])
        if os.getenv("USE_UV", "0") == "1"
        else ("python", ["mcp_server.py"])
    )

    async with AsyncExitStack() as stack:
        doc_client = await stack.enter_async_context(
            MCPClient(command=command, args=args)
        )
        clients["doc_client"] = doc_client

        for i, server_script in enumerate(server_scripts):
            client_id = f"client_{i}_{server_script}"
            client = await stack.enter_async_context(
                MCPClient(command="uv", args=["run", server_script])
            )
            clients[client_id] = client

        chat = CliChat(
            doc_client=doc_client,
            clients=clients,
            bedrock_service=bedrock_service,
        )

        cli = CliApp(chat)
        await cli.initialize()
        await cli.run()


if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    asyncio.run(main())
