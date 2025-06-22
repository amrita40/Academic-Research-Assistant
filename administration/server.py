from fastapi import FastAPI, Query
import httpx
import xml.etree.ElementTree as ET

app = FastAPI()

@app.get("/search_arxiv")
async def search_arxiv(query: str = Query(...)):
    url = f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results=3"
    headers = {
        "User-Agent": "AcademicBot/0.1 (+mailto:your.email@example.com)"  # Replace with your email
    }

    async with httpx.AsyncClient(follow_redirects=True) as client:
        response = await client.get(url, headers=headers)

        if response.status_code != 200:
            return {"error": f"Failed to fetch from arXiv. Status code: {response.status_code}"}

        root = ET.fromstring(response.text)

        ns = {"atom": "http://www.w3.org/2005/Atom"}  # Define namespace

        entries = []
        for entry in root.findall("atom:entry", ns):
            title = entry.find("atom:title", ns).text.strip()
            summary = entry.find("atom:summary", ns).text.strip()
            link = entry.find("atom:link[@rel='alternate']", ns).attrib["href"]
            author = entry.find("atom:author/atom:name", ns).text.strip()

            entries.append({
                "title": title,
                "summary": summary,
                "author": author,
                "link": link
            })

        return {"papers": entries}
