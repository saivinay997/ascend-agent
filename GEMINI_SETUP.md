# Gemini Setup Guide for Ascend

This guide will help you configure the Ascend system to use Google's Gemini LLM instead of other providers.

## Prerequisites

1. **Google Cloud Account**: You need a Google Cloud account with billing enabled
2. **Google AI Studio API Key**: Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
3. **Python 3.9+**: Ensure you have Python 3.9 or higher installed

## Step 1: Get Your Google API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated API key (it starts with "AIza...")

## Step 2: Configure Environment Variables

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file and add your Google API key:
   ```env
   # LLM Configuration - Gemini
   GOOGLE_API_KEY=your_actual_api_key_here
   GEMINI_MODEL=gemini-2.0-flash-lite
   GEMINI_TEMPERATURE=0.7
   GEMINI_MAX_TOKENS=4000
   ```

## Step 3: Install Dependencies

Install the required packages:

```bash
pip install -r requirements.txt
```

The key dependencies for Gemini are:
- `langchain-google-genai>=0.1.0`
- `google-generativeai>=0.3.0`

## Step 4: Test the Integration

Run the test script to verify everything is working:

```bash
python test_gemini_integration.py
```

You should see output like:
```
Testing Gemini integration...
✅ Google API key configured
✅ Using model: gemini-2.0-flash-lite
✅ Test agent created successfully
Testing message processing...
✅ Message processing successful
Response: [Gemini's response here]
Execution time: 1.23s
Testing health check...
✅ Health check passed
🎉 All tests passed! Gemini integration is working correctly.
```

## Step 5: Run the Main Application

Once the test passes, you can run the main application:

```bash
# Run as server
python main.py --mode server

# Run CLI commands
python main.py --mode cli --command assess --student-id test123
```

## Configuration Options

### Available Gemini Models

You can change the model in your `.env` file:

```env
# Fast and efficient
GEMINI_MODEL=gemini-2.0-flash-lite

# More capable but slower
GEMINI_MODEL=google_genai:gemini-2.0-flash

# Most capable (requires different API access)
GEMINI_MODEL=google_genai:gemini-2.0-flash-exp
```

### Temperature and Token Settings

Adjust the creativity and response length:

```env
# Lower temperature = more focused responses
GEMINI_TEMPERATURE=0.3

# Higher temperature = more creative responses
GEMINI_TEMPERATURE=0.9

# Control response length
GEMINI_MAX_TOKENS=2000  # Shorter responses
GEMINI_MAX_TOKENS=8000  # Longer responses
```

## Troubleshooting

### Common Issues

1. **"No LLM configuration found"**
   - Make sure your `.env` file has the `GOOGLE_API_KEY` set
   - Verify the API key is valid and not empty

2. **"API key invalid"**
   - Check that your API key is correct
   - Ensure you have billing enabled on your Google Cloud account
   - Verify the API key has access to Gemini models

3. **"Model not found"**
   - Check that the model name is correct
   - Some models may require special access permissions

4. **Rate limiting errors**
   - Google has rate limits on API calls
   - Consider implementing retry logic or reducing concurrent requests

### Getting Help

- Check the [Google AI Studio documentation](https://ai.google.dev/docs)
- Review the [LangChain Google GenAI documentation](https://python.langchain.com/docs/integrations/llms/google_genai)
- Open an issue in the Ascend repository

## Migration from Other LLMs

If you're migrating from OpenAI or Anthropic:

1. **Update your `.env` file**: Replace the old API keys with `GOOGLE_API_KEY`
2. **Update model names**: Use the Gemini model format (`gemini-2.0-flash-lite`)
3. **Test thoroughly**: Run the test script to ensure everything works
4. **Update any custom prompts**: Gemini may respond differently to certain prompts

## Performance Considerations

- **Gemini 2.0 Flash Lite** is optimized for speed and efficiency
- **Response times** are typically 1-3 seconds for most queries
- **Token limits** are generous but monitor usage for cost control
- **Concurrent requests** are supported but respect rate limits

## Cost Optimization

- Monitor your API usage in the Google AI Studio dashboard
- Use appropriate model sizes for your use case
- Implement caching for repeated queries
- Consider batch processing for multiple requests
