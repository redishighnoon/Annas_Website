document.querySelectorAll('.painting-toggle').forEach(toggle => {
    let currentIndex = 0;
    const images = toggle.getElementsByClassName('toggle-image');

    toggle.querySelector('.prev').addEventListener('click', function() {
        changeImage(-1, images);
    });

    toggle.querySelector('.next').addEventListener('click', function() {
        changeImage(1, images);
    });

    function changeImage(step, images) {
        currentIndex += step;
        if (currentIndex >= images.length) {
            currentIndex = 0;
        } else if (currentIndex < 0) {
            currentIndex = images.length - 1;
        }
        updateImageDisplay(images);
    }

    function updateImageDisplay(images) {
        for (let img of images) {
            img.style.display = 'none';
        }
        images[currentIndex].style.display = 'block';
    }

    updateImageDisplay(images); // Initially set the correct image display
});
