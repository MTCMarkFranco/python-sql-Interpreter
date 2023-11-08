# Microsoft Open Source Code Disclaimer
# -------------------------------------
# This source code is made available as a learning resource and is not meant to be representative of a production-ready application.
# The code is provided "as is" without warranty of any kind, either express or implied, including any implied warranties of fitness for a particular purpose, merchantability, or non-infringement.
# Microsoft does not guarantee the accuracy, completeness, efficacy, or timeliness of the information contained in this source code.
# Use of this source code is at your own risk. Microsoft is not responsible for any loss resulting from the use of this source code.
# This source code is not intended to be used for production purposes and is made available for learning purposes only.

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
    skills_root_directory = "plugins"
    skills_sqldbPlugins_directory = "sqldbPlugins"
        
    # Import Semantic Functions into the kernel
    sqldbPlugins_SEMANTIC_Plugins = kernel.import_semantic_skill_from_directory(
        skills_root_directory, skills_sqldbPlugins_directory
    )

    # Import the only native function into the kernel
    sqldbPlugins_NATIVE_Plugins = kernel.import_native_skill_from_directory(
        "{}\\{}".format(skills_root_directory,skills_sqldbPlugins_directory),
        "sqlQueryExecutionPlugin"
    )

    # 1. Create a Sequential Planner Object
    seqPlanner = SequentialPlanner(kernel)

    # 2. Describe The Plan
    planDirective = "Execute the following things in sequence: " \
                    "Convert the prompt to a SQL statement" \
                    "Execute the SQL statement" \
                    "Returns natural language response to the prompt, reasoning over the sql records returned from the SQL Database"
    
    # 3. Generate The Plan using SKs Sequential Planner (Looks at function descriptions to build the plan)
    seqPlan = await seqPlanner.create_plan_async(goal=planDirective)

    # 3. Execute The Plan    
    planContext = kernel.create_new_context(variables=ContextVariables(variables={"originalrequest": originalPrompt}));
    finalExecutedPlanResults = await seqPlan.invoke_async(originalPrompt,planContext)
        
    # 4. Print the results
    print(finalExecutedPlanResults.result)

if __name__ == "__main__":
   asyncio.run(main())
