// Sound URLs mapped to key codes
const sound = {
  65: "http://carolinegabriel.com/demo/js-keyboard/sounds/040.wav",
  87: "http://carolinegabriel.com/demo/js-keyboard/sounds/041.wav",
  83: "http://carolinegabriel.com/demo/js-keyboard/sounds/042.wav",
  69: "http://carolinegabriel.com/demo/js-keyboard/sounds/043.wav",
  68: "http://carolinegabriel.com/demo/js-keyboard/sounds/044.wav",
  70: "http://carolinegabriel.com/demo/js-keyboard/sounds/045.wav",
  84: "http://carolinegabriel.com/demo/js-keyboard/sounds/046.wav",
  71: "http://carolinegabriel.com/demo/js-keyboard/sounds/047.wav",
  89: "http://carolinegabriel.com/demo/js-keyboard/sounds/048.wav",
  72: "http://carolinegabriel.com/demo/js-keyboard/sounds/049.wav",
  85: "http://carolinegabriel.com/demo/js-keyboard/sounds/050.wav",
  74: "http://carolinegabriel.com/demo/js-keyboard/sounds/051.wav",
  75: "http://carolinegabriel.com/demo/js-keyboard/sounds/052.wav",
  79: "http://carolinegabriel.com/demo/js-keyboard/sounds/053.wav",
  76: "http://carolinegabriel.com/demo/js-keyboard/sounds/054.wav",
  80: "http://carolinegabriel.com/demo/js-keyboard/sounds/055.wav",
  186: "http://carolinegabriel.com/demo/js-keyboard/sounds/056.wav"
};

let keysPressed = '';
const sequence = 'weseeyou';

document.addEventListener('keydown', function(event) {
  const key = event.key.toLowerCase();
  keysPressed += key;
  
  // Keep only the last 8 characters to match the sequence
  keysPressed = keysPressed.substr(-8);
  
  if (keysPressed === sequence) {
      // Play creepy audio
      const audio = new Audio('/static/main/piano/audio/Creepy-piano-sound-effect.mp3');
      audio.play();
      awakenTheGreatOldOne();
  }
});

// Select the container that holds all keys
const keysContainer = document.querySelector('.keys');

// Add event listener for mouseover event on the keys container
keysContainer.addEventListener('mouseover', function() {
    // Select all labels and set their opacity to 1
    document.querySelectorAll('.key-label-black, .key-label-white').forEach(function(label) {
        label.style.opacity = '1';
    });
});

// Add event listener for mouseout event on the keys container
keysContainer.addEventListener('mouseout', function() {
    // Select all labels and set their opacity to 0
    document.querySelectorAll('.key-label-black, .key-label-white').forEach(function(label) {
        label.style.opacity = '0';
    });
});

// Function to apply the style change when a key is pressed
function pressPianoKey(keyElement) {
  keyElement.style.transform = 'scale(0.9)'; // Enlarge the key
  keyElement.style.boxShadow = '0px 0px 50px #666'; // Add a shadow effect
  setTimeout(function() {
    keyElement.style.transform = ''; // Reset the transform after a short delay
    keyElement.style.boxShadow = ''; // Reset the shadow effect
  }, 200); // Duration of the effect in milliseconds
}

// Add event listener to the whole document for the 'keydown' event
document.addEventListener('keydown', function(event) {
  // Convert the pressed key to lowercase
  const pressedKey = event.key.toLowerCase();

  // Check which key was pressed
  switch (pressedKey) {
    case 'a':
      pressPianoKey(document.getElementById('keyA'));
      break;
    case 's':
      pressPianoKey(document.getElementById('keyS'));
      break;
    case 'd':
      pressPianoKey(document.getElementById('keyD'));
      break;
    case 'f':
      pressPianoKey(document.getElementById('keyF'));
      break;
    case 'g':
      pressPianoKey(document.getElementById('keyG'));
      break;
    case 'h':
      pressPianoKey(document.getElementById('keyH'));
      break;
    case 'j':
      pressPianoKey(document.getElementById('keyJ'));
      break;
    case 'k':
      pressPianoKey(document.getElementById('keyK'));
      break;
    case 'l':
      pressPianoKey(document.getElementById('keyL'));
      break;
    case ';':
      pressPianoKey(document.getElementById('key;'));
      break;
    case 'w':
      pressPianoKey(document.getElementById('keyW'));
      break;
    case 'e':
      pressPianoKey(document.getElementById('keyE'));
      break;
    case 't':
      pressPianoKey(document.getElementById('keyT'));
      break;
    case 'y':
      pressPianoKey(document.getElementById('keyY'));
      break;
    case 'u':
      pressPianoKey(document.getElementById('keyU'));
      break;
    case 'o':
      pressPianoKey(document.getElementById('keyO'));
      break;
    case 'p':
      pressPianoKey(document.getElementById('keyP'));
      break;
  }
});

// Function to play sound
function playSound(url) {
  const audio = new Audio(url);
  audio.play();
}

// Event listener for keydown event
document.addEventListener('keydown', function(event) {
  // Get the keyCode of the pressed key
  const keyCode = event.keyCode;

  // Check if the keyCode exists in the sound object
  if (sound[keyCode]) {
      // Play the corresponding sound
      playSound(sound[keyCode]);
  }
});

function awakenTheGreatOldOne() {
  const pianoContainer = document.querySelector('.piano-container');
  const image = document.getElementById('greatOldOneImage');
  const title = document.getElementById('awokenTitle');
  
  // Start fade-out effect
  pianoContainer.style.opacity = '0';
  
  setTimeout(() => {
      // Wait for the fade-out to complete before hiding the container
      pianoContainer.style.display = 'none';

      // Prepare the image for fade-in
      title.style.display = 'block'; // Make the title visible in layout but still transparent
      image.style.display = 'block'; // Make the image visible in layout but still transparent
      setTimeout(() => {
        title.style.opacity = '1'; // Start the fade-in transition
        image.style.opacity = '1'; // Start the fade-in transition
      }, 10); // A minimal delay before starting the fade-in ensures the display change has taken effect
  }, 2000); // This delay should match the duration of the opacity transition
}
