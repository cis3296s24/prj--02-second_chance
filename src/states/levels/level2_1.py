from src.objects.portal import Portal  # Import portal class
from .level import Level

#Create level 2 and set start game to direct to level 2

class Level2_1(Level):
    def __init__(self):
        imgArr = [f"plx-5.png"]
        super().__init__(
            level=2,
            music_file="levelmusic.mp3",
            imgArr=imgArr
        )

    def add_portal(self):
        # Add portal at specific coordinates
        self.portal = Portal(3500, 400, "assets/backgrounds/portal.png", 150, 150)
        self.portals.add(self.portal)
        self.objects.add(self.portals)
