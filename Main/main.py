import asyncio
import os
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import (
    AzureTextCompletion,
    AzureChatCompletion,
    
)
from semantic_kernel.orchestration.context_variables import ContextVariables
from semantic_kernel.planning.sequential_planner import SequentialPlanner

from dotenv import load_dotenv

useAzureOpenAI = True


async def main():
    kernel = sk.Kernel()

    originalPrompt = "show me all the records in the database. include all columns."

    # Configure AI service used by the kernel. Load settings from the .env file.
    deployment, api_key, endpoint = sk.azure_openai_settings_from_dot_env()
    kernel.add_chat_service(
    "GPT35", AzureChatCompletion(deployment, endpoint, api_key))    

    skills_directory = "plugins"
        
    sqlPLugins_SEM_Plugins = kernel.import_semantic_skill_from_directory(
        skills_directory, "sqlplugins"
    )

    sqlPLugins_NAT_Plugins = kernel.import_native_skill_from_directory(
        skills_directory + "\\sqlplugins\\","sqlQueryPlugin"
    )

    # 1. Create a sequential planner
    planner = SequentialPlanner(kernel)

    # 2. Generate the plan
    ask ="Execute the following things in sequence: " \
        "1. Convert the prompt to a SQL query." \
        "2. Execute the SQL query." \
        "3. Return the records in a natural language response."
    sequential_plan = await planner.create_plan_async(goal=ask)

    # 3. Execute the plan    
    context = kernel.create_new_context(variables=ContextVariables(variables={"originalrequest": originalPrompt}));
    results = await sequential_plan.invoke_async(originalPrompt,context)
    
    # for step in sequential_plan._steps:
    #    print(step.description, ":", step._state.__dict__)

    print("AI Response: " + results.result)


if __name__ == "__main__":
   asyncio.run(main())
