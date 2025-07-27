import requests


def post_kapa_ai(query_text: str):
    """
    Sends a query to the Kapa AI API and returns the response object.
    """
    url = "https://api.kapa.ai/query/v1/projects/5e2862a7-aeac-4a87-8593-c1fd2842a7cd/chat/"
    api_key = "spFIXh5v.T7fslRgo6QV9PkRhfJIlj7jFYZgq1soc"

    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "query": query_text
    }

    response = requests.post(url, headers=headers, json=payload)
    return response


def get_relevant_existing_blogs(query_text: str):
    """
    Queries Kapa AI for relevant existing blogs based on the provided text.
    """

    response = post_kapa_ai(f"""
    I am writing a blog for below. Give existing documentation and blogs links only. It should be with key, value pair (value pair being link) only, on what resources would be helpful to link here. Don't add anything else.
    {query_text}
    """)

    if response.ok:
        response_json = response.json()
        sources = []
        for item in response_json.get('relevant_sources', []):
            try:
                sources.append((item['source_url'], item['title']))
            except Exception:
                continue  # Skip item if any error occurs
        return sources
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None
