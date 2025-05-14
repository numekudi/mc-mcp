import asyncio

from dotenv import load_dotenv

from server.mcp_server import run_mcp_server

load_dotenv()


async def main():
    await run_mcp_server()


if __name__ == "__main__":
    asyncio.run(main())
