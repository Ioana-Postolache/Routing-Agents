import os
from openai import OpenAI
from dotenv import load_dotenv

# Load config variables and initialize OpenAI client
import config 
client = OpenAI(
    base_url = "https://openai.vocareum.com/v1",
    api_key=config.api_key
    )

# --- Helper Function for API Calls ---
def call_openai(system_prompt, user_prompt, model="gpt-3.5-turbo"):
    """Simple wrapper for OpenAI API calls."""
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0
    )
    return response.choices[0].message.content


# --- Agents for Different Retail Tasks ---

def product_researcher_agent(query):
    """Product researcher agent gathers product information."""
    system_prompt = """You are a product research agent for a retail company. Your task is to provide 
    structured information about products, market trends, and competitor pricing."""
    
    user_prompt = f"Research this product thoroughly: {query}"
    return call_openai(system_prompt, user_prompt)


def customer_analyzer_agent(query):
    """Customer analyzer agent processes customer data and feedback."""
    system_prompt = """You are a customer analysis agent. Your task is to analyze customer feedback, 
    preferences, and purchasing patterns."""
    
    user_prompt = f"Analyze customer behavior for: {query}"
    return call_openai(system_prompt, user_prompt)


def pricing_strategist_agent(query, product_data=None, customer_data=None):
    """Pricing strategist agent recommends optimal pricing."""
    system_prompt = """You are a pricing strategist agent. Your task is to recommend optimal pricing 
    strategies based on product research and customer analysis."""
    
    user_prompt = f"""
        Original Pricing Query: {query}
        Product Research Data:
        {product_data}
        Customer Analysis Data:
        {customer_data}
        Based on all the above information, please provide a recommended pricing strategy, suggest an optimal price or price range, and explain your reasoning.
        """
    print(f"\nStarting pricing strategy analysis for {product_data} and {customer_data}...")
    return call_openai(system_prompt, user_prompt)

# --- Routing Agent with LLM-Based Task Determination ---
def routing_agent(query, context=None):
    """Routing agent that determines which agent to use based on the query."""
    
    classification_system_prompt = """You are a helpful AI assistant that categorizes retail-related user queries. Based on the user's query, determine if it is primarily about:
        * "product research" (e.g., asking for product specs, trends, competitor prices)
        * "customer analysis" (e.g., asking about customer feedback, preferences, purchase patterns)
        * "pricing strategy" (e.g., asking for optimal pricing for a product)
        Respond only with one of these exact phrases: "product research", "customer analysis", or "pricing strategy".

        Rules:
        - Return exactly one label
        - Do not add quotes
        - Do not add punctuation
        - Do not add explanations
        - Do not add extra words
        """

    classification_user_prompt = f"""Categorize this query: {query}
    """

    task_type = call_openai(classification_system_prompt, classification_user_prompt)

    print(f"\n\nFor {classification_user_prompt}, task type identified as: \"{task_type}\"")

    if task_type == "product research":
        print("Routing to Product Researcher Agent...")
        return product_researcher_agent(query)
    elif task_type == "customer analysis":
        print("Routing to Customer Analyzer Agent...")
        return customer_analyzer_agent(query)
    elif task_type == "pricing strategy": # This is the multi-step path. The original query likely contains the product name or context.
        print("Routing query to Pricing Strategist Agent...")
        
        # For pricing strategy, we might need additional information
        # First, get product information
        product_data = None
        if context and "product_data" in context:
            product_data = context["product_data"]
        else:
            print("Getting product information first...")
            product_data = product_researcher_agent(query)
        
        # Then, get customer insights
        customer_data = None
        if context and "customer_data" in context:
            customer_data = context["customer_data"]
        else:
            print("Getting customer insights...")
            customer_data = customer_analyzer_agent(query)
        
        # Finally, determine pricing strategy using both inputs
        return pricing_strategist_agent(query, product_data, customer_data)
    else: # (Unknown Task Type)
        print(f"Could not determine appropriate agent for query: {query}")
        return "Sorry, I could not understand how to route your request."



# --- Example Usage ---
if __name__ == "__main__":
    # Example queries
    queries = [
        "What are the specifications and current market trends for wireless earbuds?",
        "What do customers think about our premium coffee brand?",
        "What should be the optimal price for our new organic skincare line?"
    ]
    # Process each query
    for query in queries:
        print(f"\n\nProcessing Query: \"{query}\"")
        print("-" * 30)
        result = routing_agent(query)
        print("\n--- ROUTING AGENT FINAL RESULT ---")
        print(result)
        print("=" * 30)
