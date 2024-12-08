import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from matplotlib.animation import FuncAnimation
import matplotlib.patches as patches

class VisualStorytellingEngine:
    """Advanced visual storytelling for presentation"""
    
    def __init__(self, output_dir):
        self.output_dir = output_dir
    
    def create_interactive_learning_journey(self):
        """Create an animated visualization of learning progression"""
        fig, ax = plt.subplots(figsize=(15, 8), dpi=100)
        
        # Learning stages
        stages = [
            "Curiosity 🤔", 
            "Challenge 💡", 
            "Understanding 🧠", 
            "Mastery 🏆", 
            "Innovation 🚀"
        ]
        
        # Create a directed graph representing learning journey
        G = nx.DiGraph()
        G.add_edges_from(zip(stages[:-1], stages[1:]))
        
        pos = nx.spring_layout(G, k=0.5)
        
        def animate(frame):
            ax.clear()
            ax.set_title("Banana Math Puzzle: Learning Transformation", fontsize=16)
            
            # Draw nodes
            nx.draw_networkx_nodes(
                G, pos, 
                node_color=[plt.cm.viridis(frame/len(stages))] * len(G.nodes),
                node_size=1000, 
                alpha=0.8,
                ax=ax
            )
            
            # Draw edges
            nx.draw_networkx_edges(
                G, pos, 
                edge_color='gray', 
                arrows=True, 
                connectionstyle='arc3,rad=0.1',
                ax=ax
            )
            
            # Label nodes
            nx.draw_networkx_labels(
                G, pos, 
                font_size=10, 
                font_weight="bold",
                ax=ax
            )
            
            # Highlight current stage
            current_stage = stages[frame % len(stages)]
            highlighted_node = nx.draw_networkx_nodes(
                G, pos, 
                nodelist=[current_stage],
                node_color='gold', 
                node_size=1500, 
                alpha=1,
                ax=ax
            )
            
            # Add a pulsating effect
            highlighted_node.set_edgecolor('red')
            highlighted_node.set_linewidth(3)
            
            ax.set_axis_off()
        
        # Create animation
        anim = FuncAnimation(
            fig, 
            animate, 
            frames=len(stages), 
            interval=1000, 
            repeat_delay=2000
        )
        
        # Save animation
        anim.save(
            f'{self.output_dir}/learning_journey_animation.gif', 
            writer='pillow'
        )
        plt.close()
    
    def generate_narrative_flow_chart(self):
        """Create a flow chart representing game narrative"""
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Narrative elements
        narrative_stages = [
            "Player Enters Game",
            "Choose Difficulty",
            "Solve Puzzles",
            "Earn Achievements",
            "Track Progress",
            "Continuous Learning"
        ]
        
        # Create flow chart
        for i, stage in enumerate(narrative_stages):
            rect = patches.Rectangle(
                (0.2, 1 - (i+1)*0.15), 
                0.6, 0.1, 
                fill=True, 
                color=plt.cm.Pastel1(i/len(narrative_stages)),
                alpha=0.7
            )
            ax.add_patch(rect)
            
            ax.text(
                0.5, 
                1 - (i+0.5)*0.15, 
                stage, 
                horizontalalignment='center',
                verticalalignment='center',
                fontsize=10
            )
            
            # Add arrows between stages
            if i < len(narrative_stages) - 1:
                ax.arrow(
                    0.5, 1 - (i+1)*0.15, 
                    0, -0.05, 
                    head_width=0.03, 
                    head_length=0.02, 
                    fc='gray', 
                    ec='gray'
                )
        
        ax.set_title("Banana Math Puzzle: Learning Narrative", fontsize=16)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_axis_off()
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/narrative_flow_chart.png')
        plt.close()

def main():
    output_dir = '/Users/rupeshchaudhary/CascadeProjects/banana_math_puzzle/presentation/assets'
    storytelling_engine = VisualStorytellingEngine(output_dir)
    
    # Generate storytelling visualizations
    storytelling_engine.create_interactive_learning_journey()
    storytelling_engine.generate_narrative_flow_chart()

if __name__ == '__main__':
    main()
