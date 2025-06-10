from openai import OpenAI

client = OpenAI(api_key="#Your API Key")

def ask_dalle(prompt):
    response = client.images.generate(
        model = "dall-e-2",
        prompt = prompt,
        size = "1024x1024",
        quality = "standard",
        n=1
    )
    return response.data[0].url

prompt = input("Enter Prompt to generate image: ")
image_url = ask_dalle(prompt)
print("Generate Image URL:",image_url)