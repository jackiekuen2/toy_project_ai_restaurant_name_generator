from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.exceptions import OutputParserException
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
azure_endpoint = os.getenv("ENDPOINT_URL")
azure_key = os.getenv("API_KEY")

openai_api_version = "2024-05-01-preview"
deployment_name = "gpt-4o-mini"

llm = AzureChatOpenAI(
    azure_endpoint=azure_endpoint,
    api_key=azure_key,
    azure_deployment=deployment_name,
    api_version=openai_api_version,
    max_tokens=200,
    temperature=0.7
)

# Define the desired output data structure
class Dishes(BaseModel):
    restaurant_name: str = Field(description="a fancy name of the restaurant")
    dishes: list = Field(description="a list of dishes names in string")
    ingredients: list = Field(description="a list of main ingredients in strng")

# output_parser = StrOutputParser()
output_parser = JsonOutputParser(pydantic_object=Dishes)

def generate_restaurant_name_and_items(cuisine):

    prompt_template_name = PromptTemplate(
        input_variable = ["cuisine"],
        template = "I want to open a restaurant for {cuisine} food. Give me one suggestion of a fnacy name for this.",
        partial_variables={"format_instructions": output_parser.get_format_instructions()}
    )

    prompt_template_item = PromptTemplate(
        input_variables=["restaurant_name"],
        template = """
        Suggest five menu items for {restaurant_name}.
        For each item, list at most four main ingredients.
        Format the output as JSON with the following keys: cuisine, restaurant_name, dishes, ingredients. 
        The dishes should be a list of strings
        The ingredients of each dish should be a list of strings
        """,
        partial_variables={"format_instructions": output_parser.get_format_instructions()}
    )

    composed_chain = prompt_template_name | prompt_template_item | llm | output_parser

    try:
        response = composed_chain.invoke({"cuisine": cuisine})
        # print(response)
        return response

    except OutputParserException as e:
        print(f"Invalid JSON output: {e}")
        print(e.llm_output)

if __name__ == "__main__":
    print(generate_restaurant_name_and_items("Mexican"))