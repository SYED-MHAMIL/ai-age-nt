import asyncio
from dataclasses import dataclass
import os

from agents import Agent,AsyncOpenAI,OpenAIChatCompletionsModel,RunContextWrapper, Runner,set_tracing_disabled, function_tool
from dotenv import load_dotenv, find_dotenv


def main():
    load_dotenv(find_dotenv())
    gemini_api_key: str | None = os.environ.get("GOOGLE_API_KEY")

    set_tracing_disabled(disabled=True)
    external_client: AsyncOpenAI = AsyncOpenAI(api_key=gemini_api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
    llm_provider : OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(model='gemini-2.5-flash', openai_client=external_client) 

    @dataclass
    class UserInfo:  
        name: str
        uid: int

    user_info = UserInfo("zain",1) 
    
  # 🎯 Example 1: Basic Dynamic Instructions
    print("\n🎭 Example 1: Basic Dynamic Instructions")
    print("-" * 40)

    def basic_dynamic(context: RunContextWrapper[UserInfo], agent: Agent) -> str:
        """Basic dynamic instructions function."""
        return f"You are {agent.name}. Be helpful and friendly."
    
    agent_basic = Agent(
        name="Dynamic Agent",
        instructions=basic_dynamic,
        model=llm_provider
    )
    
    result = Runner.run_sync(agent_basic, "Hello!", context=user_info)
    print("Basic Dynamic Agent:")
    print(result.final_output)


    
    # 🎯 Example 2: Context-Aware Instructions
    print("\n🎭 Example 2: dynamic_instructions  Instructions")
    print("-" * 40)

    def dynamic_instructions(context: RunContextWrapper[UserInfo], agent: Agent) -> str:
        return f"You are {agent.name}. Adapt to the user's needs. The user's name is {context.context.name}. Help them with their questions."


    agent = Agent(
        name="Smart Assistant",
        instructions=dynamic_instructions , # ✅ Changes based on context
        model=llm_provider
    )

    user_info = UserInfo("zain",1)

    output = Runner.run_sync(agent,input= "what is user name",context=user_info)
    print(output.final_output)


    # 🎯 Example 3: Context-Aware Instructions
    print("\n🎭 Example 3: Context-Aware Instructions")
    print("-" * 40)


    def context_aware(context:RunContextWrapper[UserInfo],agent:Agent):
        """Context-aware instructions based on message count."""
        message_count = len(getattr(context, 'messages', []))
        
        if message_count == 0:
            return "You are a welcoming assistant. Introduce yourself!"
        elif message_count < 3:
            return "You are a helpful assistant. Be encouraging and detailed."
        else:
            return "You are an experienced assistant. Be concise but thorough."
    
    agent_context = Agent(
        name="Context Aware Agent",
        instructions=context_aware,
        model=llm_provider
    )    

    result1= Runner.run_sync(agent_context,"hello",context=user_info)
    print("First message:")
    print(result1.final_output)
    
    result2 = Runner.run_sync(agent_context, "Tell me about Python",context=user_info)
    print("\nSecond message:")
    print(result2.final_output)
    
    
    # 🎯 Example 3: Time-Based Instructions
    print("\n🎭 Example 4: Time-Based Instructions")
    print("-" * 40)
    
    import datetime
    
    def time_based(context: RunContextWrapper[UserInfo], agent: Agent) -> str:
        """Time-based instructions based on current hour."""
        current_hour = datetime.datetime.now().hour
        if 6<=current_hour < 12:
            return f"You are {agent.name}. Good morning! Be energetic and positive."
        elif 12 <= current_hour < 17:
            return f"You are {agent.name}. Good afternoon! Be focused and productive."
        else:
            return f"You are {agent.name}. Good evening! Be calm and helpful."
    
    agent_time_based = Agent(
        name="Context Aware Agent",
        instructions=time_based,
        model=llm_provider
    )    

    result1= Runner.run_sync(agent_time_based,"hello",context=user_info)
    print("First message:")
    print(result1.final_output)
    


if __name__  == "__main__":
    main()