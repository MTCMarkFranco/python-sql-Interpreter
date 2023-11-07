import asyncio
import os
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import (
    AzureTextCompletion,
    OpenAITextCompletion,
)
from semantic_kernel.orchestration.context_variables import ContextVariables
from semantic_kernel.planning.sequential_planner import SequentialPlanner

from dotenv import load_dotenv

useAzureOpenAI = True


async def main():
    kernel = sk.Kernel()

    originalPrompt = "How many people in the database named mike?"

    # Configure AI service used by the kernel. Load settings from the .env file.
    deployment, api_key, endpoint = sk.azure_openai_settings_from_dot_env()
    kernel.add_text_completion_service(
    "GPT35", AzureTextCompletion(deployment, endpoint, api_key))
    
    skills_directory = "plugins"
    
    sqlPLugins_SEM_Plugins = kernel.import_semantic_skill_from_directory(
        skills_directory, "sqlplugins"
    )

    sqlPLugins_NAT_Plugins = kernel.import_native_skill_from_directory(
        skills_directory + "\\sqlplugins\\","sqlQueryPlugin"
    )

    # Create a sequential planner
    planner = SequentialPlanner(kernel)

    # Define the steps for the planner
    # steps = [
    #     (sqlPLugins_SEM_Plugins["nlpToSqlPlugin"], {"content": originalPrompt}),
    #     (sqlPLugins_NAT_Plugins["sqlQueryPlugin"], {"content": "output"}),
    #     (sqlPLugins_SEM_Plugins["ReturnNLPresponsewithRecords"], {"content": originalPrompt})
    # ]
    
    result = await kernel.run_async(sqlPLugins_SEM_Plugins["nlpToSqlPlugin"],input_str=originalPrompt)
    print(result.result.value)

    # Generate the plan
    ask ="Take in the prompt and do the following things in sequence: " \
        "1. Convert the prompt to a SQL query, and pass the output to the next steps as input. " \
        "2. Execute the SQL query " \
        "3. Return the result of the SQL query to the user"
    
    sequential_plan = await planner.create_plan_async(goal=ask)
    
    results = await sequential_plan.invoke_async()

    # for step in sequential_plan._steps:
    #     print(step.description, ":", step._state.__dict__)

    #print("Returned Records in NL" + results)




if __name__ == "__main__":
   asyncio.run(main())
