# 🚀 Streamlit Cloud Deployment Guide

## 📋 Prerequisites

- ✅ GitHub repository with your code
- ✅ OpenAI API key
- ✅ Streamlit Cloud account

## 🌐 **Step 1: Sign Up for Streamlit Cloud**

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "Sign in" and authenticate with your GitHub account
3. Grant necessary permissions to Streamlit

## 🔑 **Step 2: Set Up Environment Variables**

1. In Streamlit Cloud dashboard, click "New app"
2. Select your `StockAnalyser` repository
3. Set the following environment variables:

```
OPENAI_API_KEY = your_openai_api_key_here
```

## ⚙️ **Step 3: Configure App Settings**

- **Main file path**: `streamlit_stock_analyser.py`
- **Python version**: 3.9 or higher
- **Branch**: `main`

## 🚀 **Step 4: Deploy**

1. Click "Deploy!" 
2. Wait for build to complete (usually 2-5 minutes)
3. Your app will be live at: `https://your-app-name.streamlit.app`

## 🔧 **Troubleshooting Common Issues**

### Build Failures
- Check that all dependencies are in `requirements.txt`
- Ensure Python version compatibility
- Verify file paths are correct

### Runtime Errors
- Check environment variables are set correctly
- Verify OpenAI API key is valid
- Check app logs in Streamlit Cloud dashboard

### Performance Issues
- Consider adding caching for expensive operations
- Optimize data fetching
- Use Streamlit's built-in performance features

## 📱 **Custom Domain (Optional)**

1. In Streamlit Cloud settings, go to "Custom domain"
2. Add your domain
3. Update DNS records as instructed

## 🔄 **Automatic Updates**

- Streamlit Cloud automatically redeploys when you push to main branch
- No manual intervention needed for updates
- Monitor deployment status in dashboard

## 💰 **Pricing**

- **Free tier**: Up to 3 apps, basic features
- **Pro tier**: $10/month, unlimited apps, custom domains
- **Enterprise**: Custom pricing for teams

## 🎯 **Best Practices**

- Keep dependencies minimal and specific
- Use environment variables for secrets
- Test locally before deploying
- Monitor app performance and usage
- Regular updates and maintenance

## 📞 **Support**

- [Streamlit Documentation](https://docs.streamlit.io)
- [Streamlit Community](https://discuss.streamlit.io)
- [GitHub Issues](https://github.com/streamlit/streamlit/issues) 