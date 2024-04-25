import os

import firebase_admin
import pygame
from firebase_admin import credentials
from firebase_admin import db


class LeaderboardManager:
    def __init__(self, game):
        # Initialize Pygame
        pygame.init()

        # Set up display
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        # Load font
        self.FONT = pygame.font.SysFont(None, 30)

        # Firebase initialization
        if not firebase_admin._apps:  # check that firebase has not been initialized
            json_file_path = os.path.join(game.resources_dir,
                                          "second-chance-64b66-firebase-adminsdk-etkn4-2927af9e64.json")
            cred = credentials.Certificate(json_file_path)
            firebase_admin.initialize_app(cred, {
                'databaseURL': 'https://second-chance-64b66-default-rtdb.firebaseio.com/'
            })

    def update_leaderboard(self, player_name, score):
        # Fetch existing leaderboard
        leaderboard = self.fetch_leaderboard()

        # Check if the player is already in the leaderboard
        if player_name in leaderboard:
            # Compare the new score with the existing score
            if score < leaderboard[player_name]:
                # Update the leaderboard only if the new score is better
                ref = db.reference('/leaderboard')
                ref.child(player_name).set(score)
        else:
            # Player is not in the leaderboard, so update the leaderboard with the new score
            ref = db.reference('/leaderboard')
            ref.child(player_name).set(score)

    def fetch_leaderboard(self, limit=10):
        ref = db.reference('/leaderboard')
        leaderboard = ref.get()

        if leaderboard:
            sorted_leaderboard = sorted(leaderboard.items(), key=lambda x: (x[1], x[0]), reverse=False)
            leaderboard = dict(sorted_leaderboard[:limit])

        return leaderboard

    def display_leaderboard(self, leaderboard):
        self.screen.fill((255, 255, 255))  # Fill screen with white
        if leaderboard:
            text_y = 50
            for i, (name, score) in enumerate(leaderboard.items(), start=1):
                text_surface = self.FONT.render(f"{i}. {name}: {score}", True, (0, 0, 0))
                self.screen.blit(text_surface, (50, text_y))
                text_y += 30

        pygame.display.flip()  # Update display
