import argparse
import sys
import pdpyras

def get_teams(session, comma_separated):
    if comma_separated:
        sys.stdout.write("Team ID, Team Name, User ID, User name, Team role\n")
    try:
        for team in session.iter_all('teams'):
            get_team_members(team['id'], team['name'], session, comma_separated)
    except pdpyras.PDClientError as e:
        raise e

def get_team_members(team_id, team_name, session, comma_separated):
    try:
        for member in session.iter_all(f'teams/{team_id}/members'):
            if comma_separated:
                sys.stdout.write(
                    f"{team_id}, {team_name}, {member['user']['id']}, {member['user']['summary']}, {member['role']}\n"
                )

            else:
                sys.stdout.write(f"Team ID: {team_id}\n")
                sys.stdout.write(f"Team Name: {team_name}\n")
                sys.stdout.write(f"User ID: {member['user']['id']}\n")
                sys.stdout.write(f"User name: {member['user']['summary']}\n")
                sys.stdout.write(f"Team role: {member['role']}\n")
                sys.stdout.write("-----\n")
    except pdpyras.PDClientError as e:
        print(f"Could not get team members for team {team_name} {team_id}")
        raise e



if __name__ == '__main__':
    ap = argparse.ArgumentParser(description="Retrieves team roles for"
        "users in a PagerDuty account")
    ap.add_argument('-k', '--api-key', required=True, help="REST API key")
    ap.add_argument('-c', '--comma-separated', required=False, default=False, action='store_true', help="Format output separated by commas")
    args = ap.parse_args()
    session = pdpyras.APISession(args.api_key)
    get_teams(session, args.comma_separated)