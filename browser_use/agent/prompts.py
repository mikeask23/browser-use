from langchain_core.messages import HumanMessage, SystemMessage

from browser_use.controller.views import ControllerPageState


class AgentSystemPrompt:
	def __init__(self, task: str, default_action_description: str):
		self.task = task
		self.default_action_description = default_action_description

	def get_system_message(self) -> SystemMessage:
		"""
		Get the system prompt for the agent.

		Returns:
		    str: Formatted system prompt
		"""
		# System prompts for the agent
		# 		output_format = """
		# {"valuation_previous_goal": "Success if completed, else short sentence of why not successful.", "goal": "short description what you want to achieve", "action": "action_name", "params": {"param_name": "param_value"}}
		#     """
		RESPONSE_FORMAT = """{{
			"current_state": {{
				"valuation_previous_goal": "String describing if previous action succeeded or failed",
				"memory": "String to store progress information",
				"next_goal": "String describing your next immediate goal"
			}},
			"action": {{
				// EXACTLY ONE of these actions must be specified
			}}
		}}"""

		AGENT_PROMPT = f"""
    
	You are an AI agent that helps users interact with websites. You receive a list of interactive elements from the current webpage and must respond with specific actions.

	INPUT FORMAT:
	- Clickable elements are numbered: "33: <button>Click me</button>"
	- Context elements are marked with underscore: "_: <div>Context text</div>"
	- Empty list means you're on a new page

	RESPONSE FORMAT valid JSON:
	{RESPONSE_FORMAT}

	AVAILABLE ACTIONS:
    {self.default_action_description}


	IMPORTANT RULES:
	1. Only use element IDs that exist in the input list
	2. Use extract_page_content to get more page information
	3. If stuck, try alternative approaches or go back
	4. Ask for human help only when completely stuck
	5. Use extract_page_content followed by done action to complete task
	6. If an image is provided, use it for context

	Remember: Choose EXACTLY ONE action per response. Invalid combinations or multiple actions will be rejected.
    """
		return SystemMessage(content=AGENT_PROMPT)


class AgentMessagePrompt:
	def __init__(self, state: ControllerPageState):
		self.state = state

	def get_user_message(self) -> HumanMessage:
		state_description = f"""
Current url: {self.state.url}
Available tabs:
{self.state.tabs}
Interactive elements:
{self.state.dom_items_to_string()}
        """

		if self.state.screenshot:
			# Format message for vision model
			return HumanMessage(
				content=[
					{'type': 'text', 'text': state_description},
					{
						'type': 'image_url',
						'image_url': {'url': f'data:image/png;base64,{self.state.screenshot}'},
					},
				]
			)

		return HumanMessage(content=state_description)

	def get_message_for_history(self) -> HumanMessage:
		return HumanMessage(content=f'Step url: {self.state.url}')