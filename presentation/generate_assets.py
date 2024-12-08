import os
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import json
import colorsys

class AssetGenerator:
    """Base class for asset generation with modular design"""
    def __init__(self, output_dir):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def generate(self):
        """Abstract method to be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement generate method")

class DiagramGenerator(AssetGenerator):
    """Advanced diagram generation with configurable styles"""
    def __init__(self, output_dir, config_path=None):
        super().__init__(output_dir)
        self.config = self._load_config(config_path)
    
    def _load_config(self, config_path):
        """Load configuration from JSON file"""
        default_config = {
            "node_colors": ["#3498db", "#2ecc71", "#e74c3c", "#f39c12"],
            "node_sizes": [2000, 2500, 3000],
            "layout_algorithms": ["spring", "circular", "shell"]
        }
        
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                user_config = json.load(f)
            default_config.update(user_config)
        
        return default_config
    
    def generate_color_palette(self, num_colors):
        """Generate a visually pleasing color palette"""
        colors = []
        for i in range(num_colors):
            hue = i / num_colors
            saturation = 0.7
            lightness = 0.6
            rgb = colorsys.hls_to_rgb(hue, lightness, saturation)
            colors.append(tuple(max(0, min(1, x)) for x in rgb))  # Ensure 0-1 range
        return colors

class ClassDiagramGenerator(DiagramGenerator):
    def generate(self):
        """Generate an advanced, stylized class diagram"""
        G = nx.DiGraph()
        
        # More comprehensive class relationships
        classes = {
            'GameLogic': ['PlayerProfile', 'PuzzleGenerator'],
            'PlayerProfile': ['Achievement', 'GameState'],
            'UIManager': ['GameLogic', 'NetworkDiagnostics'],
            'NetworkDiagnostics': ['BananaAPI']
        }
        
        # Add nodes and edges
        for cls, dependencies in classes.items():
            G.add_node(cls)
            for dep in dependencies:
                G.add_edge(cls, dep)
        
        plt.figure(figsize=(12, 8), dpi=300)
        
        # Dynamic layout and color selection
        layout_algo = self.config['layout_algorithms'][0]
        node_colors = self.generate_color_palette(len(G.nodes))
        
        pos = {
            'spring': nx.spring_layout,
            'circular': nx.circular_layout,
            'shell': nx.shell_layout
        }[layout_algo](G, k=0.5)
        
        nx.draw_networkx_nodes(G, pos, 
                                node_color=node_colors, 
                                node_size=3000, 
                                alpha=0.8)
        nx.draw_networkx_edges(G, pos, 
                                edge_color='gray', 
                                arrows=True, 
                                connectionstyle='arc3,rad=0.1')
        nx.draw_networkx_labels(G, pos, 
                                 font_size=10, 
                                 font_weight="bold")
        
        plt.title("Banana Math Puzzle - Advanced Class Relationships", fontsize=16)
        plt.axis('off')
        plt.tight_layout()
        
        output_path = os.path.join(self.output_dir, 'advanced_class_diagram.png')
        plt.savefig(output_path, bbox_inches='tight')
        plt.close()
        
        return output_path

class StorytellingAssetGenerator(AssetGenerator):
    """Generate assets that tell a visual story"""
    def generate_journey_visualization(self):
        """Create a visual journey of game mechanics"""
        plt.figure(figsize=(15, 6))
        
        stages = [
            "Player Login", 
            "Puzzle Generation", 
            "Interactive Solving", 
            "Real-time Feedback", 
            "Achievement Unlock", 
            "Progress Tracking"
        ]
        
        # Create a journey-like path
        plt.plot(range(len(stages)), [1]*len(stages), 'o-', 
                 markersize=20, 
                 linewidth=3, 
                 color='#FFA500')  # Banana orange
        
        # Annotate each stage
        for i, stage in enumerate(stages):
            plt.text(i, 1.1, stage, 
                     horizontalalignment='center', 
                     verticalalignment='bottom',
                     fontsize=10,
                     color='#4A2C2A')  # Dark brown
        
        plt.title("Banana Math Puzzle - Learning Journey", fontsize=16)
        plt.xlabel("Game Progression", fontsize=12)
        plt.axis('off')
        plt.tight_layout()
        
        output_path = os.path.join(self.output_dir, 'learning_journey.png')
        plt.savefig(output_path, bbox_inches='tight', dpi=300)
        plt.close()
        
        return output_path

    def generate(self):
        return self.generate_journey_visualization()

class PresentationAssetManager:
    """Orchestrate asset generation with a unified interface"""
    def __init__(self, output_dir, config_path=None):
        self.output_dir = output_dir
        self.config_path = config_path
        self.generators = [
            ClassDiagramGenerator(output_dir, config_path),
            StorytellingAssetGenerator(output_dir)
        ]
    
    def generate_all_assets(self):
        """Generate all assets using registered generators"""
        generated_assets = {}
        for generator in self.generators:
            try:
                asset_path = generator.generate()
                generated_assets[generator.__class__.__name__] = asset_path
            except Exception as e:
                print(f"Error generating asset with {generator.__class__.__name__}: {e}")
        
        return generated_assets

def main():
    output_dir = '/Users/rupeshchaudhary/CascadeProjects/banana_math_puzzle/presentation/assets'
    config_path = '/Users/rupeshchaudhary/CascadeProjects/banana_math_puzzle/presentation/asset_config.json'
    
    asset_manager = PresentationAssetManager(output_dir, config_path)
    generated_assets = asset_manager.generate_all_assets()
    
    print("Generated Assets:")
    for generator, path in generated_assets.items():
        print(f"{generator}: {path}")

if __name__ == '__main__':
    main()
