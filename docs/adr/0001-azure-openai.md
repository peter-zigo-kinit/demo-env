# Use Azure OpenAI for the Agent

This demo needs a hosted chat model behind the Query endpoint. We use **Azure OpenAI** (deployment `gpt-5.6-luna`) configured via `AZURE_OPENAI_*` env vars, rather than public OpenAI or Anthropic, because that matches the environment already available for this project and keeps credentials/endpoints in one place.
