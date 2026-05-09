![Research MCP Header](header.png)

# 🚀 Dynamic Prefab-UI FastMCP Server

Welcome to the **Research MCP**! This repository hosts an advanced **Model Context Protocol (MCP)** server built in Python using **FastMCP** and **Prefab-UI**. 

This server acts as a robust backend for AI Agents (like Claude Desktop), giving them the autonomous ability to perform multi-hop web research, conduct local file system management (CRUD), and most importantly, **generate dynamic, highly customized user interfaces on the fly**.

<div align="center">
  <h3>🔗 YouTube Demo: <a href="[Insert YouTube Link Here]">[Watch the Demo Here]</a></h3>
</div>

---

## ✨ Core Capabilities

The MCP server equips the AI with three powerful tools and one dynamic prompt:

### 🛠️ Tools
1. **`search_internet(query: str)`**: Leverages the [Tavily Search API](https://tavily.com/) to uncover real-time facts, financial data, and news across the web.
2. **`manage_local_file(action, filepath, content)`**: Provides full local CRUD capabilities, allowing the agent to automatically write markdown reports, parse data files, and maintain running audit logs.
3. **`generate_custom_ui(python_code: str)`**: Instead of using static UI templates, the agent writes pure Python scripts utilizing `prefab-ui` components. The server executes this code in a sandbox and renders interactive components (Tables, Accordions, Grids, Badges, etc.) dynamically directly inside the chat interface!

### 🎯 Prompts
- **`/deep_research`**: Users simply provide a single topic (e.g., "Tesla" or "OpenAI"). The server injects a massive set of instructions guiding the agent to perform an intelligence audit, write local threat matrices, and build a beautiful UI dashboard summarizing the findings.

---

## 🚀 Getting Started

### 1. Prerequisites
You will need a **Tavily API Key** to power the agent's web search capabilities.

### 2. Local Setup
```bash
# 1. Clone the repository
git clone https://github.com/pushpendra-aibot/research-mcp.git
cd research-mcp

# 2. Set up your environment variables
cp .env.example .env
# Edit .env and add your TAVILY_API_KEY

# 3. Create a virtual environment & install dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Connect to Claude Desktop
To integrate this server with the Claude Desktop app, edit your configuration file (typically located at `~/Library/Application Support/Claude/claude_desktop_config.json` on macOS) and add:

```json
{
  "mcpServers": {
    "research-server": {
      "command": "/absolute/path/to/your/research-mcp/venv/bin/fastmcp",
      "args": [
        "run",
        "/absolute/path/to/your/research-mcp/mcp_server.py"
      ]
    }
  }
}
```
*(Remember to replace the paths with the actual absolute paths on your machine!)*

Restart Claude Desktop for the changes to take effect.

---

## 🧠 How to Use It

1. Open Claude Desktop.
2. Click on the **Prompts** menu or type the slash command: `/deep_research`.
3. Enter any company or topic (e.g., "Anthropic" or "Tata Sons").
4. **Sit back and watch the magic:**
   - Claude will intelligently search Tavily for valuations and controversies.
   - Claude will write an audit log and a markdown report directly to your filesystem.
   - Claude will write Python code and generate a custom UI featuring Data Tables, Badges, and Accordions inside the chat!

---
*Built with ❤️ for advanced agentic workflows.*
