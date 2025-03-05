import json
from datetime import datetime
import os

class BadmintonTracker:
    def __init__(self, data_file="badminton_data.json"):
        self.data_file = data_file
        self.load_data()

    def load_data(self):
        """Load data from JSON file or initialize if it doesn't exist."""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                self.players = data['players']
                # Convert string dates back to datetime objects
                self.matches = []
                for match in data['matches']:
                    match['date'] = datetime.fromisoformat(match['date'])
                    self.matches.append(match)
        else:
            self.players = {}
            self.matches = []

    def save_data(self):
        """Save current state to JSON file."""
        data = {
            'players': self.players,
            'matches': []
        }
        # Convert datetime objects to strings for JSON serialization
        for match in self.matches:
            match_copy = match.copy()
            match_copy['date'] = match['date'].isoformat()
            data['matches'].append(match_copy)
            
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)

    def add_player(self, name: str):
        """Add a new player if they don't exist."""
        if name not in self.players:
            self.players[name] = {
                "rating": 1500,
                "matches": 0,
                "wins": 0
            }
            self.save_data()
            return True
        return False

    def record_match(self, team1_players, team2_players, team1_score, team2_score):
        """Record a match result and update stats."""
        for player in team1_players + team2_players:
            if player not in self.players:
                self.add_player(player)
        
        match = {
            "date": datetime.now(),
            "team1_players": team1_players,
            "team2_players": team2_players,
            "team1_score": team1_score,
            "team2_score": team2_score
        }
        self.matches.append(match)
        
        team1_won = team1_score > team2_score
        
        # Update match counts
        for player in team1_players + team2_players:
            self.players[player]["matches"] += 1
        
        # Update wins
        winning_team = team1_players if team1_won else team2_players
        for player in winning_team:
            self.players[player]["wins"] += 1
        
        self.update_ratings(team1_players, team2_players, team1_won)
        self.save_data()

    def update_ratings(self, team1_players, team2_players, team1_won):
        """Update player ratings using Elo system."""
        K = 32
        team1_rating = sum(self.players[p]["rating"] for p in team1_players) / 2
        team2_rating = sum(self.players[p]["rating"] for p in team2_players) / 2
        
        expected_team1 = 1 / (1 + 10 ** ((team2_rating - team1_rating) / 400))
        actual_score = 1 if team1_won else 0
        
        rating_change = K * (actual_score - expected_team1)
        
        for player in team1_players:
            self.players[player]["rating"] += rating_change
        for player in team2_players:
            self.players[player]["rating"] -= rating_change

def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    tracker = BadmintonTracker()
    
    while True:
        clear_screen()
        print("\n=== Badminton Match Tracker ===")
        print("1. Add Player")
        print("2. Record Match")
        print("3. View Player Stats")
        print("4. View All Players")
        print("5. View Match History")
        print("0. Exit")
        print("==============================")
        
        choice = input("\nEnter your choice (0-5): ")
        
        if choice == "1":
            clear_screen()
            print("=== Add New Player ===")
            name = input("Enter player name: ").strip()
            if name:
                if tracker.add_player(name):
                    print(f"\nPlayer '{name}' added successfully!")
                else:
                    print(f"\nPlayer '{name}' already exists!")
                    
        elif choice == "2":
            clear_screen()
            print("=== Record Match ===")
            
            if len(tracker.players) < 4:
                print("\nNot enough players! Please add more players first.")
            else:
                print("\nAvailable players:")
                for player in sorted(tracker.players.keys()):
                    print(f"- {player}")
                
                print("\nTeam 1:")
                player1 = input("Enter first player name: ").strip()
                player2 = input("Enter second player name: ").strip()
                
                print("\nTeam 2:")
                player3 = input("Enter first player name: ").strip()
                player4 = input("Enter second player name: ").strip()
                
                if all(p in tracker.players for p in [player1, player2, player3, player4]):
                    try:
                        print("\nEnter scores:")
                        score1 = int(input("Team 1 score: "))
                        score2 = int(input("Team 2 score: "))
                        
                        tracker.record_match(
                            (player1, player2),
                            (player3, player4),
                            score1,
                            score2
                        )
                        print("\nMatch recorded successfully!")
                    except ValueError:
                        print("\nInvalid scores! Please enter numbers.")
                else:
                    print("\nOne or more players not found!")
                    
        elif choice == "3":
            clear_screen()
            print("=== Player Statistics ===")
            name = input("\nEnter player name: ").strip()
            
            if name in tracker.players:
                player = tracker.players[name]
                win_rate = (player["wins"] / player["matches"] * 100) if player["matches"] > 0 else 0
                print(f"\nStatistics for {name}:")
                print(f"Rating: {player['rating']:.1f}")
                print(f"Matches played: {player['matches']}")
                print(f"Wins: {player['wins']}")
                print(f"Win rate: {win_rate:.1f}%")
            else:
                print(f"\nPlayer '{name}' not found!")
                
        elif choice == "4":
            clear_screen()
            print("=== All Players ===")
            
            if tracker.players:
                # Sort players by rating
                sorted_players = sorted(
                    tracker.players.items(),
                    key=lambda x: x[1]["rating"],
                    reverse=True
                )
                
                print("\nName           Rating  Matches  Wins  Win Rate")
                print("=" * 50)
                
                for name, data in sorted_players:
                    win_rate = (data["wins"] / data["matches"] * 100) if data["matches"] > 0 else 0
                    print(f"{name:<14} {data['rating']:>6.1f} {data['matches']:>8} {data['wins']:>5} {win_rate:>8.1f}%")
            else:
                print("\nNo players registered yet!")
                
        elif choice == "5":
            clear_screen()
            print("=== Match History ===")
            
            if tracker.matches:
                for i, match in enumerate(reversed(tracker.matches), 1):
                    print(f"\nMatch {i}:")
                    print(f"Date: {match['date'].strftime('%Y-%m-%d %H:%M')}")
                    print(f"Team 1: {match['team1_players'][0]} & {match['team1_players'][1]}")
                    print(f"Team 2: {match['team2_players'][0]} & {match['team2_players'][1]}")
                    print(f"Score: {match['team1_score']} - {match['team2_score']}")
            else:
                print("\nNo matches recorded yet!")
                
        elif choice == "0":
            print("\nThank you for using Badminton Match Tracker!")
            break
            
        else:
            print("\nInvalid choice! Please try again.")
            
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()