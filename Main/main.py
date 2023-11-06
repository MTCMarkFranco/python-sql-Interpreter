import os
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import (
    AzureTextCompletion,
    OpenAITextCompletion,
)
from semantic_kernel.orchestration.context_variables import ContextVariables

from dotenv import load_dotenv

useAzureOpenAI = True


def main():
    kernel = sk.Kernel()

    originalPrompt = "Initial Question and set of instructions"

    # Configure AI service used by the kernel. Load settings from the .env file.
    deployment, api_key, endpoint = sk.azure_openai_settings_from_dot_env()
    kernel.add_text_completion_service(
    "dv", AzureTextCompletion(deployment, endpoint, api_key)
    
    skills_directory = "plugins"
    
    sqlPLugins_Plugins = kernel.import_semantic_skill_from_directory(
        skills_directory, "sqlplugins"
    )

    # Create a sequential planner
    planner = SequentialPlanner(kernel)

    # Define the steps for the planner
    steps = [
        ("nlpToSqlPlugin", {"content": originalPrompt}),
        ("get_sql_query_result", {"content": "output"}),
        ("ReturnNLPresponsewithRecords", {"content": originalPrompt, "variables": {"sqlRecords": "output"}})
    ]

    # Generate the plan
    plan = planner.generate_plan(steps)

    # Execute the plan
    result = planner.execute_plan(plan)

    print("Returned Records in NL" + result)




if __name__ == "__main__":
    main()
