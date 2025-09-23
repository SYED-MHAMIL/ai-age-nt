import os
from dotenv import load_dotenv
from agents import Agent,Runner,function_tool,ModelSettings,OpenAIChatCompletionsModel,AsyncOpenAI,set_tracing_disabled

# load env
load_dotenv()

# disabled to connect the openAI API tracing
set_tracing_disabled(disabled=True)
GIMINI_API_KEY = os.getenv("GOOGLE_API_KEY")  
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"

external_client: AsyncOpenAI = AsyncOpenAI(api_key=GIMINI_API_KEY,base_url=BASE_URL)
model:OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(model="gemini-2.5-flash" , openai_client=external_client)


@function_tool
def calculate_area(length:float,width: float) -> str:
    """Calcaulate the area of rectangle """
    area = length * area
    return f"Area= {length}x{width} = {area} square units"


def main():
    """ Learn model stting with simple examples"""
    print("\n Temperature Settings")
    print("-"*30)

    agent_cold = Agent(
        name= "Cold Agent" ,
        instructions="You are a helpfull assistant" ,
        model_settings=ModelSettings(temperature =0.1),
        model = model                     
    )
     
    agent_Hot = Agent(
        name= "Hot Agent" ,
        instructions="You are a helpfull assistant" ,
        model_settings=ModelSettings(temperature =1.9),
        model = model                     
    )
    
    question = "Tell me about AI  in 2 sentance"

    print("\nCold agent (temperature = 0.1):")
    result_cold = Runner.run_sync(agent_cold,question)
    print(result_cold.final_output)


    
    print("\nHot agent (temperature = 0.9):")
    result_cold = Runner.run_sync(agent_Hot,question)
    print(result_cold.final_output)





if __name__ == "__main__":
    main()