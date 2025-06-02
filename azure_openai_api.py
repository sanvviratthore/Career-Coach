from openai import AzureOpenAI

endpoint = "https://sanvi-mbf58gtv-eastus2.cognitiveservices.azure.com/"
deployment = "gpt-35-turbo"  # Your deployment name here
subscription_key = "F8cvPQQ5iKHG8NUJY0GbhH4Zxhll5BJQUMOapCLVoDQ6xX9V70tYJQQJ99BFACHYHv6XJ3w3AAAAACOGaJVI"  # Replace this!
api_version = "2024-12-01-preview"  # or your supported version

client = AzureOpenAI(
    api_key=subscription_key,
    azure_endpoint=endpoint,
    api_version=api_version,
)

def ask_azure_openai(messages):
    try:
        response = client.chat.completions.create(
            model=deployment,
            messages=messages,
            max_tokens=500,
            temperature=1.0,
            top_p=1.0,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"



