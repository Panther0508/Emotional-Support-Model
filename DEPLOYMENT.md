# Render Deployment Guide

## Emotional Support Chatbot - Deployment Instructions

### Prerequisites

1. **GitHub Repository**: Your code must be pushed to a GitHub repository
2. **Render Account**: Create an account at [render.com](https://render.com)
3. **API Keys**: If using external AI services, have your API tokens ready:
   - `HF_TOKEN`: HuggingFace API token (optional)
   - `GOOGLE_TOKEN`: Google AI API token (optional)

---

## Deployment Steps

### Option 1: Deploy via render.yaml (Recommended)

The repository includes `render.yaml` which defines the complete infrastructure.

1. **Push to GitHub**: Push all changes to your GitHub repository
2. **Connect to Render**:
   - Log in to Render Dashboard
   - Click "New +" and select "Blueprint"
   - Connect your GitHub repository
   - Select the `render.yaml` file
3. **Configure Secrets**:
   - After deployment, go to the service settings
   - Add the following environment variables:
     - `SECRET_KEY`: Auto-generated (or provide your own)
     - `HF_TOKEN`: Your HuggingFace token (optional)
     - `GOOGLE_TOKEN`: Your Google AI token (optional)
4. **Deploy**: Click "Create Blueprint" to deploy

### Option 2: Manual Deployment

1. **Create Web Service**:
   - In Render Dashboard, click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - Name: `emotional-support-chatbot`
     - Environment: `Python`
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `gunicorn wsgi:app --timeout 120 --workers 2 --bind 0.0.0.0:$PORT`

2. **Create PostgreSQL Database**:
   - Click "New +" → "PostgreSQL"
   - Configure:
     - Name: `emotional_support_db`
     - Database Name: `emotional_support`
     - User: `emotional_support`
   - Copy the "Internal Database URL"

3. **Configure Environment Variables**:
   - Go to your web service settings
   - Add environment variables:
     - `DATABASE_URL`: Paste the PostgreSQL internal URL
     - `FLASK_ENV`: `production`
     - `SECRET_KEY`: Generate a secure random string
     - `HF_TOKEN`: (optional) Your HuggingFace token
     - `GOOGLE_TOKEN`: (optional) Your Google AI token

4. **Deploy**: Click "Create Web Service"

---

## Environment Variables

| Variable       | Required | Description                  | Default        |
| -------------- | -------- | ---------------------------- | -------------- |
| `DATABASE_URL` | Yes      | PostgreSQL connection string | SQLite (dev)   |
| `SECRET_KEY`   | Yes      | Flask session secret key     | Auto-generated |
| `FLASK_ENV`    | No       | Environment mode             | `development`  |
| `HF_TOKEN`     | No       | HuggingFace API token        | None           |
| `GOOGLE_TOKEN` | No       | Google AI API token          | None           |
| `NLTK_DATA`    | No       | NLTK data directory          | `./nltk_data`  |
| `PORT`         | No       | Server port                  | `5000`         |

---

## Database Configuration

### PostgreSQL Setup

The app automatically detects the `DATABASE_URL` environment variable:

- If set: Uses PostgreSQL
- If not set: Falls back to SQLite (development only)

**Important**: For production, always use PostgreSQL!

---

## Post-Deployment Verification

1. **Health Check**: Visit `/health` endpoint
2. **Test Registration**: Create a new user account
3. **Test Chat**: Send a message to verify the chatbot works
4. **Check Logs**: Monitor the logs for any errors

---

## Troubleshooting

### Common Issues

1. **500 Error on First Load**:
   - Check if database tables are created
   - Verify `DATABASE_URL` is correct

2. **NLTK Errors**:
   - Ensure NLTK data is downloaded during build
   - Check build logs for download errors

3. **Static Files Not Loading**:
   - Verify the `static/` folder is in the root directory
   - Check that Flask can find templates

4. **Session Issues**:
   - Ensure `SECRET_KEY` is set
   - Check browser cookie settings

### View Logs

In Render Dashboard:

1. Select your web service
2. Click "Logs" tab
3. Filter by level (errors, warnings, etc.)

---

## Custom Domain (Optional)

1. **Add Domain**:
   - Go to service settings
   - Click "Custom Domains"
   - Add your domain name

2. **SSL Certificate**:
   - Render automatically provisions Let's Encrypt SSL
   - Certificate appears in "TLS/SSL" section

---

## Continuous Deployment

The `render.yaml` includes `autoDeploy: true`:

- Every push to the main branch triggers a new deployment
- Pull requests create preview deployments

---

## Security Recommendations

1. **Always use PostgreSQL in production**
2. **Keep API tokens as secrets** (not in code)
3. **Use strong, unique `SECRET_KEY`**
4. **Enable `SESSION_COOKIE_SECURE`** in production
5. **Regularly update dependencies**

---

## Local Production Testing

Test the production build locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export FLASK_ENV=production
export DATABASE_URL=postgresql://user:pass@localhost/dbname
export SECRET_KEY=your-secret-key

# Run with gunicorn
gunicorn wsgi:app --timeout 120 --workers 2 --bind 0.0.0.0:5000
```

---

## Support

For issues or questions:

- Check the application logs in Render Dashboard
- Review this documentation
- Check GitHub issues
