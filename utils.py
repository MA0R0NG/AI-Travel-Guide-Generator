from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.utilities import WikipediaAPIWrapper

def generate_travel_guide(location, duration, budget, special_preferences, api_key):
    # Crafting the prompt for the travel guide
    days_itinerary = "\n".join([f"Day {i + 1}:" for i in range(duration)])

    guide_template = ChatPromptTemplate.from_messages(
        [
            ("human", f"Create a detailed {duration}-day travel guide for the location: {location}. "
                      f"Budget considerations: ${budget}. Special preferences: {special_preferences}. "
                      f"Include a day-by-day plan with practical tips, top attractions, "
                      "accommodation suggestions, local customs and cuisines to try. "
                      "Additionally, provide detailed local transportation information, "
                      "including best ways to arrive and depart, guide on using local transit "
                      "(such as buses, subways, taxis), costs, and ticketing information. "
                      "Recommend accommodations based on budget and preferences, including booking links, "
                      "price ranges, and reviews. Offer a dining guide highlighting local delicacies, "
                      "recommended restaurants, street food areas, and options for special dietary needs. "
                      "Explain cultural background, festivals, customs, and etiquette for engaging with locals. "
                      "Include emergency contact information, tips on language basics, safety advice, "
                      "shopping recommendations, and unique local experiences or activities. "
                      f"Here's the expected itinerary breakdown:\n{days_itinerary}")
        ]
    )

    # Initialize the OpenAI model with the provided API key
    model = ChatOpenAI(openai_api_key=api_key, temperature=0.5)

    # Create the chain with the template and model
    guide_chain = guide_template | model

    # Invoke the chain to generate the travel guide, providing the necessary input
    travel_guide_response = guide_chain.invoke({
        "location": location,
        "time_of_travel": duration,
        "budget": budget,
        "special_preferences": special_preferences
    }).content

    # Initialize the Wikipedia API wrapper
    wikipedia_api = WikipediaAPIWrapper(lang="en")
    wikipedia_search_result = wikipedia_api.run(location)

    cleaned_wikipedia_info = wikipedia_search_result.replace('Page: ', '')

    # Return the travel guide response and Wikipedia search result separately
    return travel_guide_response, cleaned_wikipedia_info




#print(generate_script("sora模型", 1, 0.7, os.getenv("OPENAI_API_KEY")))
