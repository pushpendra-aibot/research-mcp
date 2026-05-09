import os
from typing import Optional
from dotenv import load_dotenv
from fastmcp import FastMCP
from prefab_ui.app import PrefabApp
from prefab_ui.components import Column, Heading, Markdown, Card, Container

# Load environment variables explicitly from the script's directory
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
load_dotenv(env_path)

# Initialize the MCP Server
mcp = FastMCP("Research & UI Server")

@mcp.tool()
def search_internet(query: str) -> str:
    """
    Search the internet using Tavily to find information, facts, or data.
    
    Args:
        query: The search query to look up.
    Returns:
        A string containing the search results.
    """
    from tavily import TavilyClient
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return "Error: TAVILY_API_KEY environment variable is not set."
    
    try:
        client = TavilyClient(api_key=api_key)
        response = client.search(query=query, search_depth="basic")
        
        # Format the response into a readable string
        results = response.get("results", [])
        if not results:
            return f"No results found for: {query}"
            
        output = [f"Search Results for '{query}':\n"]
        for i, res in enumerate(results, 1):
            output.append(f"{i}. {res.get('title')}")
            output.append(f"   URL: {res.get('url')}")
            output.append(f"   Content: {res.get('content')}\n")
            
        return "\n".join(output)
    except Exception as e:
        return f"Error performing search: {str(e)}"

@mcp.tool()
def manage_local_file(action: str, filepath: str, content: str = "") -> str:
    """
    Perform CRUD operations on a local file.
    
    Args:
        action: The operation to perform ('read', 'create', 'update', 'delete').
        filepath: The path to the file.
        content: The content to write/append (only used for 'create' and 'update').
    Returns:
        A string indicating the result of the operation.
    """
    try:
        if action == "read":
            if not os.path.exists(filepath):
                return f"Error: File '{filepath}' does not exist."
            with open(filepath, "r", encoding="utf-8") as f:
                return f.read()
                
        elif action == "create":
            if os.path.exists(filepath):
                return f"Error: File '{filepath}' already exists. Use 'update' to modify."
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            return f"Successfully created file '{filepath}'."
            
        elif action == "update":
            if not os.path.exists(filepath):
                return f"Error: File '{filepath}' does not exist. Use 'create' first."
            with open(filepath, "a", encoding="utf-8") as f:
                # Add a newline before appending new content
                f.write(f"\n{content}")
            return f"Successfully updated file '{filepath}'."
            
        elif action == "delete":
            if not os.path.exists(filepath):
                return f"Error: File '{filepath}' does not exist."
            os.remove(filepath)
            return f"Successfully deleted file '{filepath}'."
            
        else:
            return f"Error: Invalid action '{action}'. Use 'read', 'create', 'update', or 'delete'."
            
    except Exception as e:
        return f"Error performing {action} on {filepath}: {str(e)}"

@mcp.tool(app=True)
def generate_custom_ui(python_code: str) -> PrefabApp:
    """
    Executes the provided python_code to generate a dynamic Prefab UI on the fly.
    The code MUST define and assign a valid PrefabApp object to a variable named `app`.
    
    Example python_code:
    ```python
    from prefab_ui.app import PrefabApp
    from prefab_ui.components import Column, Heading, Text
    
    with Column() as view:
        Heading("Dynamic Title")
        Text("Dynamic Content generated on the fly!")
    app = PrefabApp(view=view)
    ```
    
    Args:
        python_code: The Python code to execute that constructs the PrefabApp.
    """
    local_env = {}
    try:
        # Execute the agent's code in a restricted local environment
        exec(python_code, globals(), local_env)
        
        # Check if the code successfully assigned the app variable
        if 'app' in local_env and isinstance(local_env['app'], PrefabApp):
            return local_env['app']
        else:
            # Fallback if the app variable is missing or wrong type
            from prefab_ui.components import Container, Heading, Text
            with Container() as view:
                Heading("UI Generation Error", size="xl", css_class="text-red-600 mb-4")
                Text("The code executed successfully, but failed to assign a valid PrefabApp to the variable 'app'.")
            return PrefabApp(view=view)
            
    except Exception as e:
        # Catch syntax or runtime errors in the agent's code
        from prefab_ui.components import Container, Heading, Code
        with Container() as view:
            Heading("Error Executing UI Code", size="xl", css_class="text-red-600 mb-4")
            Code(str(e))
        return PrefabApp(view=view)

@mcp.prompt()
def deep_research(topic: str) -> str:
    """
    Triggers a massive 3-step research and dynamic UI generation workflow for any given topic.
    """
    return f"""You are an elite, autonomous AI Intelligence Agent operating through an MCP Server.
    
YOUR MISSION: Conduct a rigorous, multi-layered risk and financial assessment on the following topic/entity: '{topic}'

EXECUTE THE FOLLOWING WORKFLOW EXACTLY IN THIS ORDER:

### PHASE 1: INTELLIGENCE GATHERING (Multi-Hop Search)
Use the `search_internet` tool to uncover:
1. The latest financial data, valuation, or market position regarding {topic}.
2. A major public controversy, lawsuit, or security incident involving {topic} from the past 12 months.
3. The primary competitors of {topic}.

### PHASE 2: SYSTEM OF RECORD (Advanced File CRUD)
1. Initialize Audit: Use `manage_local_file` to `create` a file named `intelligence_audit.log` stating: "Audit started for {topic}."
2. Compile Report: Use `manage_local_file` to `create` a structured markdown report named `threat_matrix.md` containing all your findings.
3. Verify Integrity: Use `manage_local_file` to `read` `threat_matrix.md` to ensure the data was not corrupted.
4. Finalize Audit: Use `manage_local_file` to `update` `intelligence_audit.log` appending: "Data verified. Proceeding to UI Generation."

### PHASE 3: DYNAMIC DASHBOARD SYNTHESIS (Python UI Generation)
Translate your findings into a stunning, interactive dashboard. Use the `generate_custom_ui` tool to write a Python script that uses `prefab_ui.components` to construct the layout. You must assign the final `PrefabApp` object to a variable named `app`.

Your UI script MUST include the following complex layout requirements:
1. A top-level `Container` with a bold `Heading` (e.g., "{topic} Threat & Financial Matrix").
2. A `Grid` layout containing `Card` components for different aspects of the research (Financials, Competitors).
3. Inside the layout:
   - A `Table` structuring the financial or competitor data.
   - An `Accordion` component labeled "View Controversies". Inside the accordion, place a `Markdown` block detailing the controversy you found.
   - Use a `Badge` component (styled red or orange) to flag severe controversies.
4. At the very bottom, include a `Code` or `BlockQuote` component displaying the exact final line of your `intelligence_audit.log` to prove that the background tasks succeeded.

Execute this entire workflow autonomously right now!"""

if __name__ == "__main__":
    # Allows running the server directly via standard python if needed
    mcp.run()
