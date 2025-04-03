# from openai import OpenAI
# import user_config

# client = OpenAI(api_key=user_config.openai_key)

# # def send_request(query):
# #     completion = client.chat.completions.create(
# #         model="gpt-4o-mini",
# #         messages=[
# #             {
# #                 "role": "user",
# #                 "content": query
# #             }
# #         ]
# #     )

# #     return completion.choices[0].message.content

# def send_request(query):
#     completion = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=query
#     )

#     return completion.choices[0].message.content



import google.generativeai as genai
import user_config

genai.configure(api_key=user_config.gemini_key)

def send_request(query):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(query)
    return response.text if hasattr(response, "text") else "⚠️ No response from Gemini."


