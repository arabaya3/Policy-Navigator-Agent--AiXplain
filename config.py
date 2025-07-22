import os
from dotenv import load_dotenv
load_dotenv()
AIXPLAIN_API_KEY = os.getenv('AIXPLAIN_API_KEY', '2de0b04cb2f0dc75f86bad241fc1af2b279c6f3410a45bb84bf00871caaed551')
COURTLISTENER_API_KEY = os.getenv('COURTLISTENER_API_KEY', 'b84fd8d15e3969573f5f1de7ced3f88288e70c95') 