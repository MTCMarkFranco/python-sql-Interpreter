import os
import asyncio
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import ( AzureChatCompletion)
from semantic_kernel.orchestration.context_variables import ContextVariables
from semantic_kernel.planning.sequential_planner import SequentialPlanner

from dotenv import load_dotenv

useAzureOpenAI = True

async def main():
    kernel = sk.Kernel()

    originalPrompt = "which ppl live in San Diego and what are their phone numbers" # how many ppl live in san diego

    # Configure AI service used by the kernel. Load settings from the .env file.
    deployment, api_key, endpoint = sk.azure_openai_settings_from_dot_env()
    kernel.add_chat_service(
    "GPT35", AzureChatCompletion(deployment, endpoint, api_key))    

    # Point to the skills Directory
    skills_directory = "plugins"
        
    # Import Semantic Functions into the kernel
    sqlPLugins_SEM_Plugins = kernel.import_semantic_skill_from_directory(
        skills_directory, "sqlplugins"
    )

    #import Native Functions into the kernel
    sqlPLugins_NAT_Plugins = kernel.import_native_skill_from_directory(
        skills_directory + "\\sqlplugins\\","sqlQueryPlugin"
    )

    # 1. Create a Sequential Planner Object
    planner = SequentialPlanner(kernel)

    # 2. Describe The Plan
    ask ="Execute the following things in sequence: " \
        "Convert the prompt to a SQL statement" \
        "Execute the SQL statement" \
        "Returns natural language response to the prompt, reasoning over the sql records returned from the SQL Database"
    
    # 3. Generate The Plan using SKs Sequential Planner (Looks at function descriptions to build the plan)
    sequential_plan = await planner.create_plan_async(goal=ask)

    # 3. Execute The Plan    
    context = kernel.create_new_context(variables=ContextVariables(variables={"originalrequest": originalPrompt}));
    results = await sequential_plan.invoke_async(originalPrompt,context)
        
    # 4. Print the results
    print(results.result)

if __name__ == "__main__":
   asyncio.run(main())
