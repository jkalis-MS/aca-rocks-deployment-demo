import http.server
import socketserver
from datetime import datetime
import sys
import time
import random
import threading

PORT = 8080

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/log':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            import json
            data = json.loads(post_data.decode('utf-8'))
            
            if data['type'] == 'caught':
                print(f"🎯 Score: {data['score']}, Missed: {data['missed']}", file=sys.stderr, flush=True)
            elif data['type'] == 'missed':
                print(f"❌ Score: {data['score']}, Missed: {data['missed']}", file=sys.stderr, flush=True)
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status": "ok"}')
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        html = """
        <html>
        <head>
            <title>ACA ROCKS! - Catch the Apps! (v2)</title>
            <style>
                body { 
                    margin: 0; 
                    overflow: hidden; 
                    background: linear-gradient(to bottom, #001429 0%, #0078d4 100%); 
                    font-family: 'Courier New', monospace; 
                    color: white;
                }
                #gameCanvas { 
                    display: block; 
                    margin: 0 auto; 
                    background: transparent;
                }
                #score { 
                    position: absolute; 
                    top: 20px; 
                    left: 20px; 
                    font-size: 24px; 
                    font-weight: bold;
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
                }
                #info {
                    position: absolute;
                    top: 60px;
                    left: 20px;
                    font-size: 14px;
                    opacity: 0.8;
                }
            </style>
        </head>
        <body>
            <div id="score">Score: 0</div>
            <div id="info">Use &larr; &rarr; arrow keys to catch the apps!</div>
            <canvas id="gameCanvas"></canvas>
            <script>
                const canvas = document.getElementById('gameCanvas');
                const ctx = canvas.getContext('2d');
                canvas.width = window.innerWidth;
                canvas.height = window.innerHeight;
                
                let score = 0;
                let missed = 0;
                let appCounter = 1;
                let playerX = canvas.width / 2 - 150;
                const playerY = canvas.height - 120;
                const playerWidth = 400;
                const playerHeight = 100;
                const moveSpeed = 15;
                
                const apps = [];
                const keys = {};
                
                // Console log
                console.log(`
   ___    ______ ___       ____   ____   ______ __ __ _____ __
  /   |  / ____//   |     / __ \\\\ / __ \\\\ / ____// //_// ___// /
 / /| | / /    / /| |    / /_/ // / / // /    / ,<   \\\\__ \\\\/ / 
/ ___ |/ /___ / ___ |   / _, _// /_/ // /___ / /| | ___/ /_/  
/_/  |_|\\\\____//_/  |_|  /_/ |_| \\\\____/ \\\\____//_/ |_|/____(_)   
                `);
                console.log('ACA ROCKS! Game started! 🎉');
                
                // Draw ACA ROCKS sign with ASCII art
                function drawPlayer() {
                    ctx.fillStyle = '#FFD700';
                    ctx.fillRect(playerX, playerY, playerWidth, playerHeight);
                    ctx.fillStyle = '#000';
                    ctx.font = 'bold 10px Courier New';
                    ctx.textAlign = 'left';
                    const art = [
                        '   ___    ______ ___       ____   ____   ______ __ __ _____ __',
                        '  /   |  / ____//   |     / __ \\\\ / __ \\\\ / ____// //_// ___// /',
                        ' / /| | / /    / /| |    / /_/ // / / // /    / ,<   \\\\__ \\\\/ /',
                        '/ ___ |/ /___ / ___ |   / _, _// /_/ // /___ / /| | ___/ /_/',
                        '/_/  |_|\\\\____//_/  |_|  /_/ |_| \\\\____/ \\\\____//_/ |_|/____(_)'
                    ];
                    art.forEach((line, i) => {
                        ctx.fillText(line, playerX + 5, playerY + 20 + (i * 12));
                    });
                }
                
                // Create falling app
                function createApp() {
                    apps.push({
                        x: Math.random() * (canvas.width - 80),
                        y: -50,
                        speed: 4 + Math.random() * 4,
                        label: `App${appCounter++}`
                    });
                }
                
                // Draw falling apps
                function drawApps() {
                    apps.forEach((app, index) => {
                        ctx.fillStyle = '#00D4FF';
                        ctx.fillRect(app.x, app.y, 80, 40);
                        ctx.fillStyle = '#000';
                        ctx.font = 'bold 14px Courier New';
                        ctx.textAlign = 'center';
                        ctx.fillText(app.label, app.x + 40, app.y + 25);
                        
                        app.y += app.speed;
                        
                        // Check collision
                        if (app.y + 40 >= playerY && 
                            app.y <= playerY + playerHeight &&
                            app.x + 80 >= playerX && 
                            app.x <= playerX + playerWidth) {
                            score++;
                            document.getElementById('score').textContent = `Score: ${score}`;
                            apps.splice(index, 1);
                            console.log(`Caught ${app.label}! Score: ${score}`);
                            // Send to server
                            fetch('/log', {
                                method: 'POST',
                                headers: {'Content-Type': 'application/json'},
                                body: JSON.stringify({type: 'caught', score: score, missed: missed})
                            });
                        }
                        
                        // Remove if off screen
                        if (app.y > canvas.height) {
                            missed++;
                            apps.splice(index, 1);
                            // Send to server
                            fetch('/log', {
                                method: 'POST',
                                headers: {'Content-Type': 'application/json'},
                                body: JSON.stringify({type: 'missed', score: score, missed: missed})
                            });
                        }
                    });
                }
                
                // Game loop
                function gameLoop() {
                    ctx.clearRect(0, 0, canvas.width, canvas.height);
                    
                    // Move player
                    if (keys['ArrowLeft'] && playerX > 0) {
                        playerX -= moveSpeed;
                    }
                    if (keys['ArrowRight'] && playerX < canvas.width - playerWidth) {
                        playerX += moveSpeed;
                    }
                    
                    drawPlayer();
                    drawApps();
                    requestAnimationFrame(gameLoop);
                }
                
                // Input handling
                window.addEventListener('keydown', (e) => {
                    keys[e.key] = true;
                    if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') {
                        e.preventDefault();
                    }
                });
                
                window.addEventListener('keyup', (e) => {
                    keys[e.key] = false;
                });
                
                // Spawn apps periodically
                setInterval(createApp, 1500);
                
                // Start game
                gameLoop();
            </script>
        </body>
        </html>
        """
        self.wfile.write(html.encode())

def terminal_game():
    """Simple terminal-based falling apps game"""
    try:
        import msvcrt  # Windows
        def get_key():
            if msvcrt.kbhit():
                key = msvcrt.getch()
                # Handle arrow keys (they send two bytes)
                if key == b'\xe0':  # Arrow key prefix
                    key = msvcrt.getch()
                    if key == b'K':  # Left arrow
                        return 'LEFT'
                    elif key == b'M':  # Right arrow
                        return 'RIGHT'
                return key
            return None
    except ImportError:
        import sys, tty, termios, select
        def get_key():
            if select.select([sys.stdin], [], [], 0)[0]:
                return sys.stdin.read(1)
            return None
    
    print("\n" + "="*80)
    print("   ___    ______ ___       ____   ____   ______ __ __ _____ __")
    print("  /   |  / ____//   |     / __ \\ / __ \\ / ____// //_// ___// /")
    print(" / /| | / /    / /| |    / /_/ // / / // /    / ,<   \\__ \\/ / ")
    print("/ ___ |/ /___ / ___ |   / _, _// /_/ // /___ / /| | ___/ /_/  ")
    print("/_/  |_|\\____//_/  |_|  /_/ |_| \\____/ \\____//_/ |_|/____(_)   ")
    print("="*80)
    print("Terminal Game Mode!")
    print("Use arrow keys (← →) to move left/right. Press 'q' to quit.")
    print("="*80 + "\n")
    
    width = 120
    height = 20
    player_pos = width // 2 - 30
    player_width = 66
    score = 0
    apps = []
    app_counter = 1
    frame = 0
    
    # ASCII art for player
    player_art = [
        "   ___    ______ ___       ____   ____   ______ __ __ _____ __",
        "  /   |  / ____//   |     / __ \\ / __ \\ / ____// //_// ___// /",
        " / /| | / /    / /| |    / /_/ // / / // /    / ,<   \\__ \\/ / ",
        "/ ___ |/ /___ / ___ |   / _, _// /_/ // /___ / /| | ___/ /_/  ",
        "/_/  |_|\\____//_/  |_|  /_/ |_| \\____/ \\____//_/ |_|/____(_)   "
    ]
    
    def render():
        grid = [[' ' for _ in range(width)] for _ in range(height)]
        
        # Draw player ASCII art at bottom
        start = max(0, min(player_pos, width - player_width))
        for row_offset, art_line in enumerate(player_art):
            row_idx = height - len(player_art) + row_offset
            if row_idx >= 0:
                for i, char in enumerate(art_line):
                    if start + i < width:
                        grid[row_idx][start + i] = char
        
        # Draw falling apps
        for app in apps:
            if 0 <= app['y'] < height and 0 <= app['x'] < width:
                label = app['label']
                for i, char in enumerate(label):
                    if app['x'] + i < width:
                        grid[app['y']][app['x'] + i] = char
        
        # Clear screen and print
        print('\033[H\033[J', end='')  # Clear screen
        print(f"Score: {score}  |  Apps Caught: {score}  |  Press 'q' to quit\n")
        print("+" + "-"*width + "+")
        for row in grid:
            print("|" + "".join(row) + "|")
        print("+" + "-"*width + "+")
    
    # Game loop
    running = True
    while running:
        frame += 1
        
        # Spawn new app every 20 frames
        if frame % 20 == 0:
            apps.append({
                'x': random.randint(0, width - 6),
                'y': 0,
                'label': f'App{app_counter}'
            })
            app_counter += 1
        
        # Move apps down
        for app in apps[:]:
            app['y'] += 1
            
            # Check collision with player (check if app hits any row of player ASCII art)
            if app['y'] >= height - len(player_art):
                app_x_end = app['x'] + len(app['label'])
                player_end = player_pos + player_width
                if not (app_x_end < player_pos or app['x'] > player_end):
                    score += 1
                    apps.remove(app)
                    continue
            
            # Remove if off screen
            if app['y'] >= height:
                apps.remove(app)
        
        # Handle input
        key = get_key()
        if key:
            if key == 'LEFT':
                player_pos = max(0, player_pos - 3)
            elif key == 'RIGHT':
                player_pos = min(width - player_width, player_pos + 3)
            elif isinstance(key, bytes):
                key_str = key.decode('utf-8', errors='ignore').lower()
                if key_str == 'q':
                    running = False
                elif key_str == 'a':
                    player_pos = max(0, player_pos - 3)
                elif key_str == 'd':
                    player_pos = min(width - player_width, player_pos + 3)
        
        render()
        time.sleep(0.1)
    
    print(f"\n\nGame Over! Final Score: {score}")
    print("Thanks for playing ACA ROCKS! 🚀\n")

def run_server():
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print(f"Server starting on port {PORT}")
        print("""
   ___    ______ ___       ____   ____   ______ __ __ _____ __
  /   |  / ____//   |     / __ \\ / __ \\ / ____// //_// ___// /
 / /| | / /    / /| |    / /_/ // / / // /    / ,<   \\__ \\/ / 
/ ___ |/ /___ / ___ |   / _, _// /_/ // /___ / /| | ___/ /_/  
/_/  |_|\\____//_/  |_|  /_/ |_| \\____/ \\____//_/ |_|/____(_)   
        """)
        print("ACA ROCKS! Game is running! 🎮")
        print(f"\nBrowser: http://localhost:{PORT}")
        print("Terminal: Run with --terminal flag\n")
        httpd.serve_forever()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--terminal":
        terminal_game()
    else:
        run_server()
