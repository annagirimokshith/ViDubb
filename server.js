const express = require('express');
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.static('.'));
app.use(express.json());

// Serve the main page
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// Health check endpoint
app.get('/health', (req, res) => {
    res.json({ status: 'ok', message: 'ViDubb server is running' });
});

// Setup Python environment
app.post('/setup', (req, res) => {
    console.log('Setting up Python environment...');
    
    const setupProcess = spawn('python3', ['-m', 'pip', 'install', '--user', '--upgrade', 'pip'], {
        stdio: 'pipe'
    });
    
    let output = '';
    let errorOutput = '';
    
    setupProcess.stdout.on('data', (data) => {
        output += data.toString();
        console.log(data.toString());
    });
    
    setupProcess.stderr.on('data', (data) => {
        errorOutput += data.toString();
        console.error(data.toString());
    });
    
    setupProcess.on('close', (code) => {
        if (code === 0) {
            // Now install requirements
            const installProcess = spawn('python3', ['-m', 'pip', 'install', '--user', '-r', 'requirements.txt'], {
                stdio: 'pipe'
            });
            
            installProcess.stdout.on('data', (data) => {
                output += data.toString();
                console.log(data.toString());
            });
            
            installProcess.stderr.on('data', (data) => {
                errorOutput += data.toString();
                console.error(data.toString());
            });
            
            installProcess.on('close', (installCode) => {
                if (installCode === 0) {
                    res.json({ 
                        success: true, 
                        message: 'Python dependencies installed successfully',
                        output: output 
                    });
                } else {
                    res.status(500).json({ 
                        success: false, 
                        message: 'Failed to install Python dependencies',
                        error: errorOutput,
                        output: output 
                    });
                }
            });
        } else {
            res.status(500).json({ 
                success: false, 
                message: 'Failed to upgrade pip',
                error: errorOutput,
                output: output 
            });
        }
    });
});

// Start Gradio app
app.post('/start-gradio', (req, res) => {
    console.log('Starting Gradio app...');
    
    const gradioProcess = spawn('python3', ['app.py'], {
        stdio: 'pipe',
        env: { ...process.env, PYTHONPATH: process.env.HOME + '/.local/lib/python3.10/site-packages:' + (process.env.PYTHONPATH || '') }
    });
    
    let output = '';
    let errorOutput = '';
    
    gradioProcess.stdout.on('data', (data) => {
        output += data.toString();
        console.log(data.toString());
    });
    
    gradioProcess.stderr.on('data', (data) => {
        errorOutput += data.toString();
        console.error(data.toString());
    });
    
    gradioProcess.on('close', (code) => {
        if (code === 0) {
            res.json({ 
                success: true, 
                message: 'Gradio app started successfully',
                output: output 
            });
        } else {
            res.status(500).json({ 
                success: false, 
                message: 'Failed to start Gradio app',
                error: errorOutput,
                output: output 
            });
        }
    });
    
    // Send immediate response that startup is initiated
    setTimeout(() => {
        if (!res.headersSent) {
            res.json({ 
                success: true, 
                message: 'Gradio app startup initiated. Check logs for progress.',
                output: output 
            });
        }
    }, 2000);
});

app.listen(PORT, () => {
    console.log(`ViDubb server running on port ${PORT}`);
    console.log('Visit http://localhost:' + PORT + ' to access the application');
});