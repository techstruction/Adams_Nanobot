<?php
/**
 * Nanobot System Architecture & Data Flow Overview
 * A premium, self-contained single-page dashboard for VPS deployment.
 */

// Define system constants for display
$version = "2.5.0-Stable";
$last_update = date("Y-m-d H:i:s");
$status = "Operational";

?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nanobot | System Architecture</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg: #0a0c10;
            --card-bg: rgba(23, 27, 33, 0.7);
            --border: rgba(255, 255, 255, 0.1);
            --accent-teal: #00f2ff;
            --accent-purple: #bc13fe;
            --text-main: #e6edf3;
            --text-dim: #848d97;
            --glow: 0 0 20px rgba(0, 242, 255, 0.2);
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            background-color: var(--bg);
            background-image: 
                radial-gradient(circle at 20% 20%, rgba(188, 19, 254, 0.05) 0%, transparent 40%),
                radial-gradient(circle at 80% 80%, rgba(0, 242, 255, 0.05) 0%, transparent 40%);
            color: var(--text-main);
            font-family: 'Inter', sans-serif;
            line-height: 1.6;
            overflow-x: hidden;
            padding: 40px 20px;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
        }

        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 60px;
            border-bottom: 1px solid var(--border);
            padding-bottom: 20px;
        }

        .logo {
            font-weight: 800;
            font-size: 24px;
            letter-spacing: -1px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .logo span {
            background: linear-gradient(90deg, var(--accent-teal), var(--accent-purple));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .status-badge {
            background: rgba(0, 242, 255, 0.1);
            border: 1px solid var(--accent-teal);
            color: var(--accent-teal);
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            box-shadow: var(--glow);
        }

        .grid {
            display: grid;
            grid-template-columns: repeat(12, 1fr);
            gap: 25px;
        }

        .card {
            background: var(--card-bg);
            backdrop-filter: blur(10px);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 30px;
            transition: all 0.3s ease;
        }

        .card:hover {
            border-color: rgba(255, 255, 255, 0.2);
            transform: translateY(-5px);
        }

        .card h2 {
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
            color: var(--accent-teal);
        }

        /* Hero Flow Section */
        .hero-flow {
            grid-column: span 12;
            text-align: center;
            padding: 60px 20px;
            background: linear-gradient(180deg, rgba(0, 242, 255, 0.03), transparent);
            border-radius: 24px;
            margin-bottom: 40px;
        }

        .flow-diagram {
            display: flex;
            justify-content: space-around;
            align-items: center;
            margin-top: 40px;
            position: relative;
        }

        .node {
            background: var(--card-bg);
            border: 1px solid var(--border);
            padding: 20px;
            border-radius: 12px;
            min-width: 150px;
            z-index: 2;
        }

        .node .label {
            font-size: 12px;
            color: var(--text-dim);
            margin-bottom: 5px;
            text-transform: uppercase;
        }

        .connector {
            flex-grow: 1;
            height: 2px;
            background: linear-gradient(90deg, var(--accent-teal), var(--accent-purple));
            position: relative;
            margin: 0 -10px;
            opacity: 0.5;
        }

        .connector::after {
            content: '';
            position: absolute;
            right: 0;
            top: -4px;
            border: 5px solid transparent;
            border-left-color: var(--accent-purple);
        }

        /* Specific Cards */
        .agent-core { grid-column: span 8; }
        .storage { grid-column: span 4; }
        .skills { grid-column: span 6; }
        .tools { grid-column: span 6; }

        ul {
            list-style: none;
        }

        li {
            margin-bottom: 12px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 14px;
        }

        .path {
            font-family: 'JetBrains Mono', monospace;
            color: var(--text-dim);
            font-size: 12px;
            background: rgba(0,0,0,0.3);
            padding: 2px 8px;
            border-radius: 4px;
        }

        .footer {
            margin-top: 60px;
            text-align: center;
            color: var(--text-dim);
            font-size: 12px;
        }

        @media (max-width: 900px) {
            .grid > div { grid-column: span 12 !important; }
            .flow-diagram { flex-direction: column; gap: 30px; }
            .connector { width: 2px; height: 30px; margin: 5px 0; }
            .connector::after { transform: rotate(90deg); bottom: -10px; right: -4px; top: auto; }
        }
    </style>
</head>
<body>

<div class="container">
    <header>
        <div class="logo">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="url(#paint0_linear)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M2 17L12 22L22 17" stroke="url(#paint0_linear)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M2 12L12 17L22 12" stroke="url(#paint0_linear)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <defs>
                    <linearGradient id="paint0_linear" x1="2" y1="2" x2="22" y2="22" gradientUnits="userSpaceOnUse">
                        <stop stop-color="#00f2ff"/>
                        <stop offset="1" stop-color="#bc13fe"/>
                    </linearGradient>
                </defs>
            </svg>
            Nanobot <span>System Overview</span>
        </div>
        <div class="status-badge">System: <?php echo $status; ?></div>
    </header>

    <div class="hero-flow">
        <h1>Architecture Flow</h1>
        <p style="color: var(--text-dim); margin-top: 10px;">The decoupled logic chain of the Nanobot Agent infrastructure.</p>
        
        <div class="flow-diagram">
            <div class="node">
                <div class="label">Input</div>
                <strong>Channels</strong>
                <div style="font-size: 10px; color: var(--text-dim); margin-top: 5px;">Telegram / CLI</div>
            </div>
            <div class="connector"></div>
            <div class="node" style="border-color: var(--accent-purple);">
                <div class="label">Middleware</div>
                <strong>Message Bus</strong>
                <div style="font-size: 10px; color: var(--text-dim); margin-top: 5px;">Async Asyncio.Queue</div>
            </div>
            <div class="connector"></div>
            <div class="node" style="background: rgba(0, 242, 255, 0.05); border-color: var(--accent-teal);">
                <div class="label">Core</div>
                <strong>Agent Brain</strong>
                <div style="font-size: 10px; color: var(--text-dim); margin-top: 5px;">Loop Logic & Context</div>
            </div>
            <div class="connector"></div>
            <div class="node">
                <div class="label">Output</div>
                <strong>Capabilites</strong>
                <div style="font-size: 10px; color: var(--text-dim); margin-top: 5px;">Tools & Skills</div>
            </div>
        </div>
    </div>

    <div class="grid">
        <!-- Agent Core Logic -->
        <div class="card agent-core">
            <h2>
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
                Core Engine Logic
            </h2>
            <ul>
                <li>
                    <span>Agent Iteration Loop</span>
                    <span class="path">nanobot/agent/loop.py</span>
                </li>
                <li>
                    <span>System Context Builder</span>
                    <span class="path">nanobot/agent/context.py</span>
                </li>
                <li>
                    <span>Skill Manifest Parsing</span>
                    <span class="path">nanobot/agent/skills.py</span>
                </li>
                <li>
                    <span>Subagent Management</span>
                    <span class="path">nanobot/agent/subagent.py</span>
                </li>
                <li>
                    <span>Async Message Dispatcher</span>
                    <span class="path">nanobot/bus/queue.py</span>
                </li>
            </ul>
        </div>

        <!-- Storage & Persistence -->
        <div class="card storage">
            <h2>
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/></svg>
                Persistence
            </h2>
            <ul>
                <li>
                    <span>Long-term Facts</span>
                    <span class="path">MEMORY.md</span>
                </li>
                <li>
                    <span>Event History</span>
                    <span class="path">HISTORY.md</span>
                </li>
                <li>
                    <span>Active Workspace</span>
                    <span class="path">~/.nanobot/</span>
                </li>
            </ul>
        </div>

        <!-- Skills Repository -->
        <div class="card skills">
            <h2>
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>
                Built-in Skills
            </h2>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 10px;">
                <div style="font-size: 13px; color: var(--text-dim);">• Apple Notes</div>
                <div style="font-size: 13px; color: var(--text-dim);">• Desktop Control</div>
                <div style="font-size: 13px; color: var(--text-dim);">• Gmail Manager</div>
                <div style="font-size: 13px; color: var(--text-dim);">• GitHub CLI</div>
                <div style="font-size: 13px; color: var(--text-dim);">• PDF Manager</div>
                <div style="font-size: 13px; color: var(--text-dim);">• Smart Summarizer</div>
                <div style="font-size: 13px; color: var(--text-dim);">• ClawHub Registry</div>
                <div style="font-size: 13px; color: var(--text-dim);">• Weather/Intel</div>
            </div>
        </div>

        <!-- Atomic Tools -->
        <div class="card tools">
            <h2>
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></svg>
                Atomic Toolset
            </h2>
            <div style="font-size: 14px; opacity: 0.8;">
                <code style="color: var(--accent-purple);">read_file()</code>, 
                <code style="color: var(--accent-purple);">write_file()</code>, 
                <code style="color: var(--accent-purple);">edit_file()</code>, 
                <code style="color: var(--accent-purple);">exec()</code>, 
                <code style="color: var(--accent-purple);">web_search()</code>, 
                <code style="color: var(--accent-purple);">spawn_subagent()</code>
            </div>
            <p style="font-size: 12px; color: var(--text-dim); margin-top: 15px;">
                These atomic tools provide the low-level hardware and OS access used by the higher-level skills.
            </p>
        </div>
    </div>

    <div class="footer">
        <p>Nanobot Engine v<?php echo $version; ?> | Configured for Nvidia NIM (Moonshot Kimi)</p>
        <p style="margin-top: 5px;">Status report generated at: <?php echo $last_update; ?></p>
    </div>
</div>

</body>
</html>
