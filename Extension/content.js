console.log('Content script starting');

function sendMessage(message) {
  return new Promise((resolve, reject) => {
    try {
      chrome.runtime.sendMessage(message, (response) => {
        if (chrome.runtime.lastError) {
          reject(new Error(chrome.runtime.lastError.message));
        } else {
          resolve(response);
        }
      });
    } catch (error) {
      reject(error);
    }
  });
}

sendMessage({ action: 'contentScriptInitialized' })
  .then((response) => {
    console.log('Initialization message sent. Response:', response);
  })
  .catch((error) => {
    console.warn('Failed to send initialization message:', error.message);
  });

function extractTweetId(element) {
  const article = element.closest('article');
  if (article) {
    const tweetIdMatch = article.innerHTML.match(/\/status\/(\d+)/);
    return tweetIdMatch ? tweetIdMatch[1] : null;
  }
  return null;
}

const observer = new MutationObserver((mutations) => {
  for (let mutation of mutations) {
    if (mutation.type === 'attributes' && mutation.target.getAttribute('data-testid') === 'removeBookmark') {
      console.log('Bookmark action detected');
      const tweetId = extractTweetId(mutation.target);
      if (tweetId) {
        console.log('Tweet ID found:', tweetId);
        sendMessage({ action: 'logTweetId', tweetId: tweetId })
          .then((response) => {
            if (response.success) {
              console.log('Tweet bookmarked successfully');
            } else {
              console.warn('Failed to bookmark tweet:', response.error);
              if (response.error === 'Not authenticated') {
                console.log('User needs to log in');
                // You might want to notify the user to log in here
                // For example, you could send a message to the popup to show a login prompt
                // chrome.runtime.sendMessage({ action: 'showLoginPrompt' });
              }
            }
          })
          .catch((error) => {
            console.warn('Error sending logTweetId message:', error.message);
          });
      } else {
        console.log('No tweet ID found');
      }
    }
  }
});

observer.observe(document.body, {
  attributes: true,
  subtree: true,
  attributeFilter: ['data-testid']
});

console.log('Content script setup complete');