# Vercel Deployment Guide

## 🚀 Quick Deploy

### Option 1: GitHub Integration (Recommended)

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Setup Vercel deployment"
   git push origin main
   ```

2. **Connect to Vercel:**
   - Go to [vercel.com](https://vercel.com) and sign in/up
   - Click "New Project"
   - Import your GitHub repository
   - Vercel will automatically detect the configuration

3. **Deploy:**
   - Click "Deploy" - Vercel will handle the rest!
   - Your app will be available at `https://your-project-name.vercel.app`

### Option 2: Vercel CLI

1. **Install Vercel CLI:**
   ```bash
   npm i -g vercel
   ```

2. **Deploy:**
   ```bash
   cd "/Users/chrisbigler/D2 Loot Sim"
   vercel
   ```

3. **Follow the prompts:**
   - Link to existing project or create new one
   - Confirm settings
   - Deploy!

## 📁 Project Structure

Your project has been restructured for Vercel:

```
D2 Loot Sim/
├── api/
│   ├── index.py          # Main Flask serverless function
│   └── DropSim.py        # Simulation logic
├── index.html            # Static frontend (served by Vercel)
├── vercel.json          # Vercel configuration
├── requirements.txt     # Python dependencies
├── .vercelignore        # Files to exclude from deployment
└── DEPLOYMENT.md        # This guide
```

## ⚙️ Configuration Files

### `vercel.json`
- Configures Python serverless functions
- Sets up routing for API endpoints and static files
- Handles `/run_simulation` and `/compare_systems` routes

### `requirements.txt`
- Flask 2.3.3
- numpy 1.24.3 
- Werkzeug 2.3.7

### `.vercelignore`
- Excludes original `Core Files/` directory
- Excludes documentation and cache files

## 🔧 How It Works

1. **Static Frontend**: `index.html` is served directly by Vercel's CDN
2. **API Endpoints**: Python Flask functions in `/api/` handle simulation requests
3. **Serverless**: Each API call runs in an isolated serverless function
4. **Auto-scaling**: Vercel automatically handles traffic spikes

## 🧪 Local Testing

To test locally before deploying:

```bash
# Install Vercel CLI
npm i -g vercel

# Start development server
vercel dev
```

This will run your app at `http://localhost:3000` with the same serverless environment as production.

## 📊 Performance

- **Cold starts**: ~1-3 seconds for first request
- **Warm requests**: ~100-500ms response time
- **Timeout**: 30 seconds max (configured in vercel.json)
- **Memory**: Automatic allocation based on usage

## 🐛 Troubleshooting

### Common Issues:

1. **"Function Runtimes must have a valid version" Error**: 
   - This happens when using outdated runtime specifications like `"@vercel/python"`
   - **FIXED**: Removed runtime specification - Vercel auto-detects Python from .py files
   - Modern Vercel doesn't require explicit runtime for Python functions

2. **Import Errors**: 
   - Ensure `DropSim.py` is in the `/api/` directory
   - Check that all dependencies are in `requirements.txt`

3. **Build Failed During Deployment**:
   - Verify your `requirements.txt` only contains necessary packages
   - Make sure your Python code doesn't use any unsupported libraries
   - Check that all imports in `api/index.py` are available

4. **Timeout Errors**: 
   - Large simulations (1000+ trials) may timeout
   - Consider reducing trial count for complex analyses

5. **Static Files Not Loading**: 
   - Ensure `index.html` is in the root directory
   - Check `vercel.json` routing configuration

### Debug Tips:

- Check function logs in Vercel dashboard
- Use `vercel logs` CLI command for real-time logs
- Test locally with `vercel dev` first

## 🎯 Environment Variables

If needed, you can set environment variables in Vercel:

1. Go to Project Settings in Vercel dashboard
2. Navigate to "Environment Variables"
3. Add any configuration variables

## 📈 Monitoring

Vercel provides built-in analytics:
- Function invocations
- Response times
- Error rates
- Bandwidth usage

Access these in your Vercel project dashboard.

## 🔄 Updates

To deploy updates:

1. **With GitHub**: Just push to your main branch
2. **With CLI**: Run `vercel --prod` in your project directory

Vercel will automatically rebuild and deploy your changes.

## 🎉 Success!

Once deployed, your D2 Loot Simulator will be live and accessible worldwide with:
- ⚡ Fast global CDN
- 🔄 Automatic scaling  
- 🛡️ Built-in security
- 📊 Performance analytics
- 🆓 Generous free tier

Enjoy your deployed Destiny 2 Loot Simulator!
