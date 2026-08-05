from typing import Dict
from core.bedrock import Bedrock
from mcp_client import MCPClient
from core.tools import ToolManager


class Chat:
    def __init__(self, bedrock_service: Bedrock, clients: dict[str, MCPClient]):
        self.bedrock_service: Bedrock = bedrock_service
        self.clients: dict[str, MCPClient] = clients
        self.messages: list[Dict] = []

    async def _process_query(self, query: str):
        self.messages.append({"role": "user", "content": [{"text": query}]})

    async def run(
        self,
        query: str,
    ) -> str:
        final_text_response = ""

        await self._process_query(query)

        while True:
            response = self.bedrock_service.chat(
                messages=self.messages,
                tools=await ToolManager.get_all_tools(self.clients),
            )

            self.bedrock_service.add_assistant_message(
                self.messages, response["parts"]
            )

            if response["stop_reason"] == "tool_use":
                print(response["text"])
                tool_result_parts = await ToolManager.execute_tool_requests(
                    self.clients, response["parts"]
                )

                self.bedrock_service.add_user_message(
                    self.messages, tool_result_parts
                )
            else:
                final_text_response = response["text"]
                break

        return final_text_response
