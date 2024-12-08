# 🍌 Banana Math Puzzle 🧮

## Educational Math Game with Advanced Networking and Authentication

### 🌟 Project Overview

Banana Math Puzzle is an innovative educational game designed to make learning mathematics fun, engaging, and secure. Built with Python and Kivy, the game offers a robust, network-enabled platform for mathematical skill development.

### 🚀 Key Features

#### 1. Educational Gaming
- Adaptive math puzzle generation
- Multiple difficulty levels
- Engaging user interface
- Real-time scoring and feedback

#### 2. Advanced Networking
- Comprehensive network diagnostics
- Secure API communication
- Robust error handling
- Flexible connectivity management

#### 3. Authentication System
- Secure user registration
- Multi-factor login validation
- Account protection mechanisms
- Session management

### 🔧 Technical Architecture

#### Core Components
- **Game Logic**: Puzzle generation and scoring
- **Network API**: Secure communication layer
- **Authentication**: User management system
- **Diagnostics**: Network and system health monitoring

#### Technology Stack
- **Language**: Python 3.9+
- **UI Framework**: Kivy
- **Network**: aiohttp, requests
- **Authentication**: bcrypt
- **Testing**: pytest, pytest-asyncio

### 🛠️ System Requirements

#### Minimum Requirements
- Python 3.9+
- macOS 10.15+
- 2 GB RAM
- 100 MB disk space

#### Recommended
- Python 3.10+
- macOS 12+
- 4 GB RAM
- Stable internet connection

### 📦 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/banana-math-puzzle.git

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the game
python main.py
```

### 🧪 Testing

```bash
# Run network diagnostics
python -m pytest network_diagnostics.py

# Run full test suite
python -m pytest
```

### 🔐 Security Features

- Encrypted password storage
- Network connectivity validation
- Secure API communication
- Rate-limited authentication
- Comprehensive error logging

### 📊 Network Diagnostics

The game includes an advanced network diagnostic system that:
- Checks internet connectivity
- Validates local network interfaces
- Measures network performance
- Verifies API endpoint health
- Provides detailed system information

### 🌐 Connectivity Modes

1. **Full Online Mode**
   - Complete game features
   - Real-time synchronization
   - Leaderboard updates

2. **Offline Mode**
   - Puzzle generation
   - Local scoring
   - Limited features

### 📝 Logging

Comprehensive logging across:
- Network events
- Authentication attempts
- Game interactions
- System diagnostics

### 🚧 Known Limitations

- Initial beta release
- Limited platform support
- Ongoing feature development

### 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push and create Pull Request

### 📄 License

MIT License

### 🏆 Credits

Developed by Codeium Engineering Team

### Key Features and Software Engineering Themes

## 1. Software Design Principles
- **Object-Oriented Programming**: The game is built using a modular, class-based architecture
- **Low Coupling**: Each component (game logic, UI, API) operates independently
- **High Cohesion**: Each class has a single, well-defined responsibility
- **Clean Code**: Comprehensive documentation and consistent coding style

## 2. Event-Driven Programming
- **Event System**: Custom event system implementing the Observer pattern
- **UI Events**: Kivy-based event handling for user interactions
- **Game Events**: Decoupled communication between components through events
- **Asynchronous Operations**: Non-blocking API calls and game state updates

## 3. Interoperability
- **Banana API Integration**: Seamless interaction with external API services
- **RESTful Communication**: Standard HTTP methods for API requests
- **Data Exchange**: JSON-based data transfer between systems
- **Error Handling**: Robust error handling for API failures

## 4. Virtual Identity
- **User Authentication**: Secure local and API-based authentication
- **Profile Management**: Comprehensive user profile tracking
- **Session Handling**: Secure session management with expiration
- **Score Synchronization**: Bi-directional score syncing with Banana API

## Implementation Details

### Event System (`events.py`)
The event system implements the Observer pattern, allowing components to communicate without direct coupling:
```python
# Subscribe to events
event_system.subscribe(GameEvents.SCORE_UPDATED, on_score_update)

# Publish events
event_system.publish(GameEvents.SCORE_UPDATED, {'score': new_score})
```

### API Integration (`api_client.py`)
The Banana API client handles all external API communication:
```python
# Get puzzle from API
puzzle = api_client.get_puzzle(difficulty=5)

# Submit score to API
api_client.submit_score(user_id, score)
```

### Authentication Bridge (`auth_api_bridge.py`)
Bridges local authentication with the Banana API:
```python
# Login with API verification
profile, session = await auth_bridge.login(username, password)

# Sync scores with API
auth_bridge.sync_score(profile)
```

## Getting Started

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
BANANA_API_KEY=your_api_key
BANANA_API_URL=https://api.banana.dev/v1
```

3. Run the game:
```bash
python main.py
```
