"""
Small config file for endpoints and constants
"""

# The reviews rss api endpoint
API_BASE_URL = "https://itunes.apple.com/us/rss/customerreviews/id={app_id}/sortBy=mostRecent/page=1/json"

# Postgres connection string
# TODO: If this ever gets deployed, need to move this to an environment variable or a config file and gitignore it
POSTGRES_CONNECTION_STRING = "postgresql://austin:postgres@127.0.0.1/postgres" # IMPORTANT: change this connection string to your own local postgres credentials