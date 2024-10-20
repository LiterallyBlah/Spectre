# Spectre

**Spectre** is a modular tool designed for web application reconnaissance and vulnerability analysis. It integrates browser-based interaction and link extraction capabilities to provide comprehensive coverage of web application security testing.

## Features

- **SpectreCore**: The foundational module for handling browser sessions and authentication using Playwright.
- **Dynamic Crawling**: Discover and extract links within web applications, both authenticated and unauthenticated.
- **Interactive Session Management**: Maintain and interact with browser sessions over extended periods.
- **LLM-Powered Link Extraction**: Utilise AI models to enhance link discovery and validation.
- **Configurable Task Management**: Customise tasks via an interactive command-line interface.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/LiterallyBlah/Spectre.git
   ```

2. Navigate to the project directory:
   ```bash
   cd spectre
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Install Playwright browser drivers:
   ```bash
   playwright install
   ```

5. Install Ollama and the required AI models (e.g., llama3.1, qwen2.5):
   ```bash
   # Install Ollama (follow instructions from https://ollama.ai/)
   # Pull the required models
   ollama pull llama3.1
   ollama pull qwen2.5
   ```

## Usage

You can run **Spectre** through the main entry point:

```bash
python main.py
```

This will launch the Spectre Command Centre, where you can interact with the tool using various commands:

- `help`: Show the help menu with available commands
- `options`: Show available options
- `start`: Start a new interactive session
- `exit`: Exit the programme

In an interactive session, you can use the following commands:
- `navigate`: Navigate to a new URL
- `extract`: Extract links from the current page
- `exit`: Exit the interactive session

## Checklist of Progress

### Completed:
- [x] **Browser Interaction**: Implemented functionality to start browser
- [x] **Navigation**: Implemented functionality to navigate to specified URLs
- [x] **Link Extraction**: Implemented functionality to extract links from the current page
- [x] **Core Folder Structure**: Set up basic folder structure and files for the `core` module.

### To Do:
- [ ] **Browser Session Management**: Implement setup for managing browser sessions using Playwright.
- [ ] **Authentication Handling**: Set up initial authentication and session maintenance with cookies/tokens.
- [ ] **Interactive Command Interface**: Implement a user-friendly command-line interface for tool interaction.
- [ ] **LLM Integration**: Integrate AI models (via Ollama) for enhanced link extraction and validation.
- [ ] **Session Continuity**: Implement functionality to maintain sessions over extended periods.
- [ ] **Advanced Fuzzing Modules**: Add optional fuzzing modules for headers, cookies, and custom parameters.
- [ ] **External Tool Integration**: Begin integrating tools like Nikto and SQLmap.
- [ ] **Response Analysis**: Implement more advanced response pattern analysis.
- [ ] **Reporting System**: Set up output for results in JSON and HTML format.
- [ ] **Test Suite**: Implement unit tests for all core functionalities.
- [ ] **Documentation**: Provide detailed user and developer documentation for configuration and usage.

## Folder Structure

- `core/`: The core functionality of **Spectre**, managing browser sessions and authentication.
- `crawl/`: Modules for dynamic crawling and link extraction.
- `llm/`: AI agents for link extraction and validation.
- `output/`: Output directory for generated reports and logs.

## Future Development

This project is under active development, with additional modules and functionality planned, including enhanced crawling, response pattern analysis, and deeper integrations with security tools.

## Contribution

Contributions are welcome! Feel free to submit pull requests or open issues for any bugs or feature requests. Please ensure that your code adheres to the existing coding standards and is thoroughly tested before submission.

## Licence

This project is licensed under the MIT Licence. See the `LICENCE` file for more details.
