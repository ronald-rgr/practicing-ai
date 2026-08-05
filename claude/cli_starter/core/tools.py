import json
from typing import Optional, Any, Literal
from mcp.types import CallToolResult, Tool, TextContent
from mcp_client import MCPClient


class ToolManager:
    @classmethod
    async def get_all_tools(cls, clients: dict[str, MCPClient]) -> list[Tool]:
        """Gets all tools from the provided clients."""
        tools = []
        for client in clients.values():
            tools += await client.list_tools()
        return tools

    @classmethod
    async def _find_client_with_tool(
        cls, clients: list[MCPClient], tool_name: str
    ) -> Optional[MCPClient]:
        """Finds the first client that has the specified tool."""
        for client in clients:
            tools = await client.list_tools()
            tool = next((t for t in tools if t.name == tool_name), None)
            if tool:
                return client
        return None

    @classmethod
    def _build_tool_result_part(
        cls,
        tool_use_id: str,
        text: str,
        status: Literal["success"] | Literal["error"],
    ):
        """Builds a tool result part dictionary."""
        return {
            "toolResult": {
                "toolUseId": tool_use_id,
                "content": [{"text": text}],
                "status": status,
            }
        }

    @classmethod
    async def execute_tool_requests(
        cls, clients: dict[str, MCPClient], parts: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """Executes a list of tool requests against the provided clients."""
        tool_requests = [part for part in parts if "toolUse" in part]
        tool_result_parts = []
        for tool_request in tool_requests:
            tool_use = tool_request.get("toolUse")
            if not tool_use:
                continue

            tool_use_id = tool_use.get("toolUseId")
            tool_name = tool_use.get("name")
            tool_input = tool_use.get("input", {})

            client = await cls._find_client_with_tool(
                list(clients.values()), tool_name
            )

            if not client:
                tool_result_part = cls._build_tool_result_part(
                    tool_use_id, "Could not find that tool", "error"
                )
                tool_result_parts.append(tool_result_part)
                continue

            try:
                tool_output: CallToolResult | None = await client.call_tool(
                    tool_name, tool_input
                )
                items = []
                if tool_output:
                    items = tool_output.content
                content_list = [
                    item.text for item in items if isinstance(item, TextContent)
                ]
                content_json = json.dumps(content_list)
                tool_result_part = cls._build_tool_result_part(
                    tool_use_id,
                    content_json,
                    "error"
                    if tool_output and tool_output.isError
                    else "success",
                )
            except Exception as e:
                error_message = f"Error executing tool '{tool_name}': {e}"
                print(error_message)
                tool_result_part = {
                    "toolResult": {
                        "toolUseId": tool_use_id,
                        "content": [
                            {"text": json.dumps({"error": error_message})}
                        ],
                        "status": "error",
                    }
                }

            tool_result_parts.append(tool_result_part)
        return tool_result_parts
