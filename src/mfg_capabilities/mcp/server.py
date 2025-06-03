from dotenv import load_dotenv
from fastmcp import FastMCP
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_openai import ChatOpenAI

from mfg_capabilities.utils.databricks import get_sqlalchemy_engine


# Load environment variables
load_dotenv()

# Init database
engine = get_sqlalchemy_engine()
db = SQLDatabase(engine=engine, lazy_table_reflection=True)

# Init tools
llm = ChatOpenAI(model="gpt-4o")
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
tools = toolkit.get_tools()
list_tables_tool = next(tool for tool in tools if tool.name == "sql_db_list_tables")

# Create the MCP server
mcp = FastMCP("SQL")


@mcp.tool(
    name=list_tables_tool.name,
    description=list_tables_tool.description,
)
async def list_tables() -> list[str]:
    """
    Tool for getting table names.

    Returns:
        list[str]: A list of table names in the database.
    """
    return list_tables_tool.run(tool_input="")


if __name__ == "__main__":
    # Run the MCP server
    mcp.run()
