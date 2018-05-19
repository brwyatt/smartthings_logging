import json

from smartthings_cli import smartthings_cli

config = smartthings_cli.load_config()

access_token = config['access_token']
endpoint_base_url, endpoint_url = smartthings_cli.get_endpoint_url(access_token)

result = smartthings_cli.get_status(access_token, endpoint_base_url,
                                    endpoint_url, 'temperature')

print(json.dumps(result, sort_keys=True, indent=4))
