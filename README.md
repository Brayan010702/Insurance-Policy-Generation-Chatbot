
# Insurance Chatbot Project

This chatbot assists users in the LATAM insurance market by answering queries, performing web searches, and optimizing policies based on user input.

## Project Structure

```
your_project/
├── main.py                            # Entry point of the project
├── config/
│   └── settings.py                    # Environment variables and database path configuration
├── prompts/
│   └── classification_prompt.py       # Classification prompt
│   └── conversation_prompt.py         # Conversation prompt
├── chains/
│   └── classification_chain.py        # Classification chain
│   └── conversation_chain.py          # Conversation chain
├── functions/
│   └── rag_chain.py                   # RAG chain for insurance queries
│   └── web_search_chain.py            # Web search chain
│   └── policy_optimizer_chain.py      # Policy optimizer
├── handlers/
│   └── router.py                      # Routes queries to the correct chain
├── requirements.txt                   # Project dependencies
```

## Setup

1. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

2. **Create a `.env` file** with the following content:

   ```plaintext
   DB_PATH= path-to-vector-db
   API_KEY=your-api-key-here
   ```

## Running the Chatbot

To start the chatbot, run:

```bash
chainlit main.py
```

The chatbot will respond to insurance-related queries, web searches, and policy optimizations based on user input.

## Best Practices for Framing Questions

For the best results, use clear, specific questions that align with the chatbot's capabilities:

1. **Be Direct and Specific**:
   - Good: *"¿Cuáles son las coberturas de un seguro de auto en Chile?"*
   - Avoid: *"Dime algo sobre seguros."*

2. **Ask One Question at a Time**:
   - Good: *"¿Cómo puedo optimizar mi póliza para reducir costos?"*
   - Avoid: *"¿Cómo optimizo mi póliza y qué coberturas tiene?"*

3. **Use Natural Language**: Frame questions as you would ask a human.
   - Good: *"¿Qué opciones de seguro de hogar me recomiendas?"*
   - Avoid: *"Opciones hogar seguro."*

4. **Clarify if Needed**: If the response isn’t what you expect, clarify or provide more context in the follow-up.

## Configuration

- **Database Path**: The path to the database storing embeddings can be updated in the `.env` file using the `DB_PATH` variable.
- **API Key**: Add the relevant API key for external tools in the `.env` file.

## License

This project is licensed under the MIT License.


