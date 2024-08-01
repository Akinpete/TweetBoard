console.log('Background script loaded');

let accessToken = null;
let refreshToken = null;

// Function to store tokens
function storeTokens(access, refresh) {
  accessToken = access;
  refreshToken = refresh;
  console.log('Tokens updated:', { accessToken, refreshToken });
}

// Function to get tokens
function getTokens() {
  return { accessToken, refreshToken };
}

// Function to refresh the access token
async function refreshAccessToken() {
  console.log('Attempting to refresh access token');
  const tokens = getTokens();
  if (!tokens.refreshToken) {
    console.error('No refresh token available');
    throw new Error('No refresh token available');
  }
  
  try {
    const response = await fetch('http://localhost:5000/refresh', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${tokens.refreshToken}`
      }
    });

    if (response.ok) {
      const data = await response.json();
      console.log('Access token refreshed successfully');
      storeTokens(data.access_token, tokens.refreshToken);
    } else {
      console.error('Failed to refresh access token');
      throw new Error('Failed to refresh access token');
    }
  } catch (error) {
    console.error('Error refreshing access token:', error);
    throw error;
  }
}

// Function to send authenticated requests
async function sendAuthenticatedRequest(url, method, data) {
  console.log(`Preparing authenticated request to ${url}`);
  console.log('Current access token:', accessToken);

  if (!accessToken) {
    console.error('No access token available. User needs to log in.');
    throw new Error('Not authenticated');
  }

  const requestOptions = {
    method: method,
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${accessToken}`
    },
    body: JSON.stringify(data)
  };

  console.log('Request options:', JSON.stringify(requestOptions, null, 2));

  try {
    let response = await fetch(url, requestOptions);
    console.log(`Response status: ${response.status}`);

    if (response.status === 401) {
      console.log('Access token expired, attempting to refresh');
      await refreshAccessToken();
      requestOptions.headers['Authorization'] = `Bearer ${accessToken}`;
      response = await fetch(url, requestOptions);
      console.log(`Response status after token refresh: ${response.status}`);
    }

    if (!response.ok) {
      const text = await response.text();
      console.error(`HTTP error! status: ${response.status}, body: ${text}`);
      throw new Error(`HTTP error! status: ${response.status}, body: ${text}`);
    }

    const data = await response.json();
    console.log('Response data:', data);
    return data;
  } catch (error) {
    console.error('Fetch error:', error);
    throw error;
  }
}

// New function to check if a URL is a Twitter/X URL
function isTwitterUrl(url) {
  return url.includes('twitter.com') || url.includes('x.com');
}

// New function to inject the content script
function injectContentScript(tabId) {
  chrome.scripting.executeScript({
    target: { tabId: tabId },
    files: ['content.js']
  }, () => {
    if (chrome.runtime.lastError) {
      console.error('Error injecting content script:', chrome.runtime.lastError);
    } else {
      console.log('Content script injected successfully');
    }
  });
}

// Listen for tab activation
chrome.tabs.onActivated.addListener((activeInfo) => {
  chrome.tabs.get(activeInfo.tabId, (tab) => {
    if (tab.url && isTwitterUrl(tab.url)) {
      console.log('Twitter tab activated. Injecting content script.');
      injectContentScript(activeInfo.tabId);
    }
  });
});

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  console.log('Message received:', message);

  if (message.action === 'contentScriptInitialized') {
    console.log('Content script initialized in tab:', sender.tab.id);
    sendResponse({received: true});
  } 
  else if (message.action === 'login') {
    const { username, password } = message;
    console.log(`Attempting login for username: ${username}`);

    fetch('http://localhost:5000/login/extension', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username, password }),
    })
    .then(response => {
      console.log(`Login response status: ${response.status}`);
      if (!response.ok) {
        return response.text().then(text => {
          console.error(`Login HTTP error! status: ${response.status}, body: ${text}`);
          throw new Error(`Login HTTP error! status: ${response.status}, body: ${text}`);
        });
      }
      return response.json();
    })
    .then(data => {
      console.log('Login response data:', data);
      if (data.access_token && data.refresh_token) {
        storeTokens(data.access_token, data.refresh_token);
        console.log('Access and refresh tokens received and stored');
        sendResponse({success: true});
      } else {
        console.log('Login failed', data);
        sendResponse({success: false, error: data.msg || 'Unknown error'});
      }
    })
    .catch(error => {
      console.error('Login error:', error);
      sendResponse({success: false, error: 'An error occurred during login: ' + error.message});
    });
    return true;  // Indicates that the response is sent asynchronously
  } 
  else if (message.action === 'logTweetId') {
    console.log(`Attempting to log tweet ID: ${message.tweetId}`);
    if (!accessToken) {
      console.error('No access token available. User needs to log in.');
      sendResponse({success: false, error: 'Not authenticated'});
      return true;
    }

    sendAuthenticatedRequest('http://localhost:5000/bookmark', 'POST', { tweet_id: message.tweetId })
      .then(data => {
        console.log('Bookmark added:', data);
        sendResponse({success: true});
      })
      .catch(error => {
        console.error('Error adding bookmark:', error);
        sendResponse({success: false, error: error.message});
      });
    return true;  // Indicates that the response is sent asynchronously
  }
});

console.log('Background script setup complete');