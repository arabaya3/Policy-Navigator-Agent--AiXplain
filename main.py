from aixplain.factories import AgentFactory, TeamAgentFactory, IndexFactory
from rich.console import Console
import requests
from dotenv import load_dotenv
load_dotenv()
def federal_register_tool(query):
    url = "https://www.federalregister.gov/api/v1/documents.json"
    params = {"per_page": 1, "order": "newest", "conditions[term]": query}
    try:
        resp = requests.get(url, params=params, timeout=10)
        data = resp.json()
        results = data.get("results", [])
        if results:
            doc = results[0]
            title = doc.get("title", "")
            summary = doc.get("abstract", "No summary available.")
            pub_date = doc.get("publication_date", "?")
            return f"{title} (Published: {pub_date}): {summary}"
        else:
            return "No relevant federal register documents found."
    except Exception as e:
        return f"Federal Register: Error fetching data: {e}"
def courtlistener_tool(query):
    import time
    url = "https://www.courtlistener.com/api/rest/v3/opinions/"
    params = {"search": query, "page_size": 1}
    headers = {'Authorization': 'Token b84fd8d15e3969573f5f1de7ced3f88288e70c95'}
    max_retries = 3
    for attempt in range(max_retries):
        try:
            resp = requests.get(url, params=params, headers=headers, timeout=30)
            data = resp.json()
            results = data.get('results', [])
            if results:
                opinion = results[0]
                case_name = (
                    opinion.get('caseName') or
                    opinion.get('case_name') or
                    opinion.get('name_abbreviation') or
                    "Unknown Case"
                )
                cite = (
                    opinion.get('cite') or
                    (opinion.get('citations') and opinion.get('citations')[0].get('cite')) or
                    "No citation"
                )
                summary = opinion.get('summary') or opinion.get('headnotes')
                if summary:
                    summary = summary.strip().replace('\n', ' ')
                else:
                    plain_text = opinion.get('plain_text', '').strip()
                    if plain_text:
                        paragraphs = [p.strip() for p in plain_text.split('\n') if p.strip()]
                        summary = None
                        for p in paragraphs:
                            if len(p) > 40 and not p.lower().startswith(('filed', 'court', 'state of', 'appeal', 'supreme', 'district', 'county', 'judge', 'panel', 'date', 'before', 'argued', 'decided', 'counsel', 'attorney', 'prosecutor', 'defendant', 'plaintiff', 'appellant', 'appellee', 'respondent', 'petitioner', 'brief', 'syllabus', 'headnote')):
                                summary = p
                                break
                        if not summary:
                            summary = paragraphs[0] if paragraphs else '[No summary available]'
                    else:
                        summary = '[No summary available]'
                return f"{case_name} ({cite}): {summary}"
            else:
                return "No relevant court opinions found."
        except requests.exceptions.Timeout:
            if attempt < max_retries - 1:
                time.sleep(2)
                continue
            else:
                return "CourtListener: Error fetching data: Request timed out after multiple attempts. Please try again later."
        except Exception as e:
            return f"CourtListener: Error fetching data: {e}"
def get_index_by_name(index_name, retries=5, delay=2):
    from time import sleep
    for attempt in range(retries):
        indexes = IndexFactory.list()
        for idx in indexes:
            if getattr(idx, 'name', None) == index_name:
                return idx
        if attempt < retries - 1:
            print(f"[INFO] Index '{index_name}' not found, retrying in {delay} seconds...")
            sleep(delay)
    print(f"[ERROR] Index '{index_name}' not found after {retries} retries.")
    return None
vehicle_code_index = get_index_by_name("Vehicle Code Index")
epa_index = get_index_by_name("EPA Index")
vehicle_code_agent = AgentFactory.create(
    name="Vehicle Code Agent",
    description="Answers queries about the Vehicle Code dataset.",
    instructions="You answer questions about the Vehicle Code.",
    tools=[vehicle_code_index] if vehicle_code_index else []
)
epa_agent = AgentFactory.create(
    name="EPA Agent",
    description="Answers queries about EPA regulations.",
    instructions="You answer questions about EPA regulations.",
    tools=[epa_index] if epa_index else []
)
team_agent = TeamAgentFactory.create(
    name="Policy Navigator Agent",
    description="Agentic RAG System for Government Regulation Search",
    instructions="Extract insights from regulations, policies, and public health guidelines.",
    agents=[vehicle_code_agent, epa_agent]
)
console = Console()
def main():
    console.print("[bold green]Welcome to the Agentic RAG System![/bold green]")
    while True:
        console.print("\n[bold yellow]Select query type:[/bold yellow]\n1. Vehicle Code\n2. EPA\n3. Federal Register\n4. CourtListener\n5. Exit")
        choice = console.input("[bold blue]Enter choice (1-5): [/bold blue]")
        if choice == "5" or choice.lower() == "exit":
            break
        query = console.input("[bold blue]Enter your query: [/bold blue]")
        try:
            if choice == "1":
                response = vehicle_code_agent.run(query)
                console.print(f"[green]Vehicle Code Agent response:[/green]\n{response['data']['output']}")
            elif choice == "2":
                response = epa_agent.run(query)
                console.print(f"[green]EPA Agent response:[/green]\n{response['data']['output']}")
            elif choice == "3":
                result = federal_register_tool(query)
                console.print(f"[green]Federal Register Tool response:[/green]\n{result}")
            elif choice == "4":
                result = courtlistener_tool(query)
                console.print(f"[green]CourtListener Tool response:[/green]\n{result}")
            else:
                console.print("[red]Invalid choice. Please select 1-5.[/red]")
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
if __name__ == "__main__":
    main() 