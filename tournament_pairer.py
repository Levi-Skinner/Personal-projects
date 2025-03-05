import json
import os
from typing import List, Tuple

class TournamentPairer:
    def __init__(self, data_file="badminton_data.json"):
        self.data_file = data_file
        self.load_data()

    def load_data(self):
        """Load player data from the tracker's JSON file."""
        if not os.path.exists(self.data_file):
            raise FileNotFoundError(f"Data file '{self.data_file}' not found! Please run the tracker first.")
            
        with open(self.data_file, 'r') as f:
            data = json.load(f)
            self.players = data['players']

    def generate_pairings(self, num_matches: int) -> List[Tuple]:
        """Generate balanced tournament pairings based on player ratings."""
        if len(self.players) < num_matches * 4:
            raise ValueError(f"Not enough players for {num_matches} matches! Need at least {num_matches * 4} players.")

        # Sort players by rating
        sorted_players = sorted(
            self.players.items(),
            key=lambda x: x[1]["rating"],
            reverse=True
        )
        
        teams = []
        players_pool = list(sorted_players)
        
        for _ in range(num_matches):
            # Select 4 players for 2 teams
            team_players = []
            for _ in range(4):
                if len(players_pool) % 2 == 0:
                    # Take from top
                    player = players_pool.pop(0)
                else:
                    # Take from bottom
                    player = players_pool.pop()
                team_players.append(player[0])
            
            # Create balanced teams
            team1 = (team_players[0], team_players[3])  # Highest + Lowest
            team2 = (team_players[1], team_players[2])  # Middle two
            teams.append((team1, team2))

        return teams

def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    try:
        pairer = TournamentPairer()
        
        while True:
            clear_screen()
            print("\n=== Tournament Pairing Generator ===")
            print("1. Generate Pairings")
            print("2. View All Players")
            print("0. Exit")
            print("=================================")
            
            choice = input("\nEnter your choice (0-2): ")
            
            if choice == "1":
                clear_screen()
                print("=== Generate Pairings ===")
                
                try:
                    num_matches = int(input("\nHow many matches to generate? "))
                    pairings = pairer.generate_pairings(num_matches)
                    
                    print("\nGenerated pairings:")
                    print("===================")
                    
                    for i, (team1, team2) in enumerate(pairings, 1):
                        print(f"\nMatch {i}:")
                        team1_ratings = [pairer.players[p]["rating"] for p in team1]
                        team2_ratings = [pairer.players[p]["rating"] for p in team2]
                        team1_avg = sum(team1_ratings) / 2
                        team2_avg = sum(team2_ratings) / 2
                        
                        print(f"Team 1: {team1[0]} ({pairer.players[team1[0]]['rating']:.1f}) & "
                              f"{team1[1]} ({pairer.players[team1[1]]['rating']:.1f})")
                        print(f"       Average rating: {team1_avg:.1f}")
                        
                        print(f"Team 2: {team2[0]} ({pairer.players[team2[0]]['rating']:.1f}) & "
                              f"{team2[1]} ({pairer.players[team2[1]]['rating']:.1f})")
                        print(f"       Average rating: {team2_avg:.1f}")
                        
                except ValueError as e:
                    print(f"\nError: {e}")
                    
            elif choice == "2":
                clear_screen()
                print("=== All Players ===")
                
                # Sort players by rating
                sorted_players = sorted(
                    pairer.players.items(),
                    key=lambda x: x[1]["rating"],
                    reverse=True
                )
                
                print("\nName           Rating  Matches  Wins  Win Rate")
                print("=" * 50)
                
                for name, data in sorted_players:
                    win_rate = (data["wins"] / data["matches"] * 100) if data["matches"] > 0 else 0
                    print(f"{name:<14} {data['rating']:>6.1f} {data['matches']:>8} {data['wins']:>5} {win_rate:>8.1f}%")
                    
            elif choice == "0":
                print("\nThank you for using Tournament Pairing Generator!")
                break
                
            else:
                print("\nInvalid choice! Please try again.")
                
            input("\nPress Enter to continue...")
            
    except FileNotFoundError as e:
        print(f"\nError: {e}")
        input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()