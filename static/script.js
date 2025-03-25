document.addEventListener('DOMContentLoaded', function() {
    const audioPlayer = document.getElementById('audioPlayer');
    const playButton = document.getElementById('playButton');
    const statusText = document.getElementById('statusText');
    const equalizer = document.getElementById('equalizer');
    
    let isPlaying = false;
    let isLoading = false;
    
    playButton.addEventListener('click', togglePlay);
    
    function togglePlay() {
      if (isLoading) return;
      
      if (!isPlaying) {
        // Start playing
        isLoading = true;
        statusText.textContent = 'Carregando...';
        
        audioPlayer.play().then(() => {
          isPlaying = true;
          isLoading = false;
          playButton.innerHTML = '<i class="fas fa-stop"></i>';
          playButton.classList.add('playing');
          statusText.textContent = 'Tocando agora';
          equalizer.classList.remove('hidden');
          console.log('✅ Rádio está tocando!');
        }).catch(error => {
          isLoading = false;
          console.error('❌ Erro ao tocar rádio:', error);
          statusText.textContent = 'Erro ao carregar áudio';
          alert('Não foi possível tocar a rádio. Verifique a conexão ou o link do stream.');
        });
      } else {
        // Stop playing
        audioPlayer.pause();
        audioPlayer.currentTime = 0;
        isPlaying = false;
        playButton.innerHTML = '<i class="fas fa-play"></i>';
        playButton.classList.remove('playing');
        statusText.textContent = 'Pressione play';
        equalizer.classList.add('hidden');
        console.log('✅ Rádio parada');
      }
    }
    
    // Make equalizer bars animate randomly
    const equalizerBars = document.querySelectorAll('.equalizer-bar');
    
    function animateEqualizer() {
      if (isPlaying) {
        equalizerBars.forEach(bar => {
          const height = 5 + Math.random() * 15;
          bar.style.height = `${height}px`;
        });
      }
      
      requestAnimationFrame(animateEqualizer);
    }
    
    animateEqualizer();
    
    // Handle audio errors
    audioPlayer.addEventListener('error', function() {
      isPlaying = false;
      isLoading = false;
      playButton.innerHTML = '<i class="fas fa-play"></i>';
      playButton.classList.remove('playing');
      statusText.textContent = 'Erro no áudio';
      equalizer.classList.add('hidden');
      console.error('❌ Erro no elemento de áudio');
    });
  });