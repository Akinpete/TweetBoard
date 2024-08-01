// Select all video elements in the gallery

const videos = document.querySelectorAll('.bookmark-card video');

// Function to reset a video to preview mode
function resetToPreview(video) {
    video.currentTime = 0;
    video.muted = true;
    video.loop = true;
    video.play().catch(e => console.error("Preview play failed:", e));
    const container = video.closest('.bookmark-card');
    const playPauseBtn = container.querySelector('.play-pause');
    const stopBtn = container.querySelector('.stop');
    playPauseBtn.textContent = 'Play';
    playPauseBtn.setAttribute('aria-label', 'Play video');
    stopBtn.style.display = 'none';
    console.log('Reset to preview mode');
}

videos.forEach(video => {
    const container = video.closest('.bookmark-card');
    let isPreviewMode = true;

    // Create and append custom controls
    const controls = document.createElement('div');
    controls.className = 'custom-controls';
    controls.innerHTML = `
        <button class="play-pause" aria-label="Play video">Play</button>
        <button class="stop" aria-label="Stop video" style="display:none;">Stop</button>
    `;
    container.appendChild(controls);

    const playPauseBtn = controls.querySelector('.play-pause');
    const stopBtn = controls.querySelector('.stop');

    // Start preview on page load
    video.addEventListener('loadedmetadata', () => {
        resetToPreview(video);
    });

    // Show controls on hover or focus
    container.addEventListener('mouseenter', showControls);
    container.addEventListener('focus', showControls, true);

    container.addEventListener('mouseleave', hideControls);
    container.addEventListener('blur', hideControls, true);

    function showControls() {
        controls.style.display = 'flex';
        console.log('Controls visible');
    }

    function hideControls() {
        controls.style.display = 'none';
        if (isPreviewMode) {
            resetToPreview(video);
        }
    }

    // Play/Pause functionality
    playPauseBtn.addEventListener('click', togglePlayPause);

    function togglePlayPause() {
        console.log('Play button clicked. Video paused:', video.paused);
        if (isPreviewMode || video.paused) {
            // Reset all other videos to preview mode
            videos.forEach(otherVideo => {
                if (otherVideo !== video && !otherVideo.paused) {
                    resetToPreview(otherVideo);
                }
            });

            video.currentTime = 0; // Start from the beginning
            video.muted = false;
            video.loop = false;
            video.play().then(() => {
                console.log('Video started playing from the beginning');
                playPauseBtn.textContent = 'Pause';
                playPauseBtn.setAttribute('aria-label', 'Pause video');
                stopBtn.style.display = 'inline-block';
                isPreviewMode = false;
            }).catch(e => console.error("Play failed:", e));
        } else {
            video.pause();
            playPauseBtn.textContent = 'Play';
            playPauseBtn.setAttribute('aria-label', 'Play video');
            console.log('Video paused');
        }
    }

    // Stop functionality
    stopBtn.addEventListener('click', stopVideo);

    function stopVideo() {
        resetToPreview(video);
        isPreviewMode = true;
        console.log('Stop button clicked, returned to silent looping');
    }

    // Update button text when video ends
    video.addEventListener('ended', () => {
        playPauseBtn.textContent = 'Replay';
        playPauseBtn.setAttribute('aria-label', 'Replay video');
        stopBtn.style.display = 'none';
        isPreviewMode = true;
        resetToPreview(video);
    });

    // Keyboard accessibility
    container.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
            togglePlayPause();
            e.preventDefault();
        } else if (e.key === 'Escape') {
            stopVideo();
            e.preventDefault();
        }
    });

    // Make the video container focusable
    container.setAttribute('tabindex', '0');
});