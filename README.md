# Policy-Navigator-Agent--AiXplain

An Agentic RAG system that allows users to query and extract insights from complex government regulations, compliance policies, and public health guidelines.

---

## Project Overview
This project implements an Agentic Retrieval-Augmented Generation (RAG) system that allows users to query and extract insights from complex government regulations, compliance policies, and public health guidelines. The system leverages multiple agents, vector-based document retrieval, and integrates with external APIs and datasets.

## Features
- Multi-agent RAG pipeline (Retriever, Policy Checker, Case Law Summarizer)
- Vector indexing for efficient document retrieval
- Ingestion from both datasets and public websites
- Integration with at least three tool types (API, custom Python, CSV/SQL)
- Simple CLI interface for user interaction
- Extensible for future enhancements

## Data Sources
- **Dataset:** [California Vehicle Code - VEH](https://leginfo.legislature.ca.gov/faces/codesTOCSelected.xhtml?tocCode=VEH&tocTitle=+Vehicle+Code+-+VEH)
- **Website:** (e.g., EPA or WHO site, to be specified in implementation)

## Tool Integrations
- **Marketplace Tool:** aiXplain API
- **Custom Python Tool:** Document parser and vector indexer
- **CSV/SQL Tool:** Dataset ingestion and querying

## Setup Instructions
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Add your API keys to `config.py` or as environment variables
4. Run the main app: `python main.py`

## Example Queries
- "What is the latest update on vehicle emissions policy?"
- "Summarize case law related to Section 4000 of the Vehicle Code."
- "What are the compliance requirements for vehicle registration?"

## Future Improvements
- Add more agents (e.g., summarization, translation)
- Enhance UI/UX (web interface)
- Support more data sources
- Add caching and memory support
- Multilingual policy support

## Submission Instructions
- Make the repository public on GitHub
- Include this README and a demo video (2–3 minutes)
- Email the GitHub link to: `devrel@aixplain.com`

## References
- [aiXplain Documentation](https://docs.aixplain.com/)
- [California Vehicle Code](https://leginfo.legislature.ca.gov/faces/codesTOCSelected.xhtml?tocCode=VEH&tocTitle=+Vehicle+Code+-+VEH)
