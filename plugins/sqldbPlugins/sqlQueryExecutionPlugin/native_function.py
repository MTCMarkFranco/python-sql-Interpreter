import os
from asyncio import exceptions
import pyodbc
from semantic_kernel.skill_definition import (
        sk_function,
        sk_function_context_parameter
)
from semantic_kernel.orchestration.sk_context import (
        SKContext
)

class sqlQueryExecutionPlugin:
    
    @sk_function(
        description="Get Result of SQL Query",
        name="sqlQueryExecutionPlugin",
        input_description="The SQL Query to be executed"
    )
    @sk_function_context_parameter(
        name="output",
        description="The result of the SQL Query",
    )
    def get_sql_result(self, context: SKContext) -> str:        
        
        query = context["input"]
        result = "No Records Found"

        server_name = os.getenv("SERVER_NAME")
        database_name = os.getenv("DATABASE_NAME")
        username = os.environ.get("SQLADMIN_USER")
        password = os.getenv("SQL_PASSWORD")
        conn = pyodbc.connect('DRIVER={driver};SERVER={server_name};DATABASE={database_name};UID={username};PWD={password}'.format(driver="ODBC Driver 17 for SQL Server",server_name=server_name, database_name=database_name, username=username, password=password))
        cursor = conn.cursor()
        try:
            cursor.execute(query)
            result = cursor.fetchall()
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:    
            cursor.close()
            conn.close()
        
        print("TSQL:" + str(query))
        print("originalrequest:" + str(context["originalrequest"]))
        
        print("Records:" + str(result))
        return str(result)