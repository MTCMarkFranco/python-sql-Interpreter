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

    # 1. First Call the NLP to SQL Plugin to get the SQL Query
    NLPToSqlPlugin_function = sqlPLugins_Plugins["nlpToSqlPlugin"]

    # The "input" variable in the prompt is set by "content" in the ContextVariables object.
    context_variables = ContextVariables(
        content=originalPrompt, variables={""}
    )
    
    sqlQuery = NLPToSqlPlugin_function(variables=context_variables)

    print(TQLQuery)

    # 2. Next Call the SQL Get records PLugin to get records from the database

    # Add the SQL Query to the context variables
    context_variables["content"] = sqlQuery
        
    sqlQueryPlugin_function = sqlPLugins_Plugins["get_sql_query_result"]

    # invoke the sqlQueryPlugin_function passing in the context variables
    context_variables = sqlQueryPlugin_function(variables=context_variables)

    returnedSqlRecords = context_variables["records"]

    # 3. call the semantic kernel chat completion service to return the answer to the user including the RecordsReturned
    NLPresponsewithRecords_function = sqlPLugins_Plugins["ReturnNLPresponsewithRecords"]
    # The "input" variable in the prompt is set by "content" in the ContextVariables object.
    context_variables = ContextVariables(
        content=originalPrompt, variables={"sqlRecords: " returnedSqlRecords}
    )
    
    returnedNLPResponse = NLPresponsewithRecords_function(variables=context_variables)
    print("Returned Records in NL" + returnedNLPResponse)

    )


if __name__ == "__main__":
    main()
