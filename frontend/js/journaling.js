
const imageUpload = document.getElementById('imageUpload');
const imagePreview = document.getElementById('imagePreview');
const uploadForm = document.getElementById('uploadForm');

// Show image preview
imageUpload.addEventListener('change', function () {
    const file = this.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            imagePreview.src = e.target.result;
            imagePreview.style.display = 'block';
        }
        reader.readAsDataURL(file);
    }
});

// Handle form submission
uploadForm.addEventListener('submit', function (e) {
    e.preventDefault();
    const title = document.getElementById('title').value;
    const description = document.getElementById('description').value;
    const imgSrc = imagePreview.src;

    if (!title || !description || !imgSrc) return;

    alert(`Story Uploaded!\nTitle: ${title}\nDescription: ${description}`);
    uploadForm.reset();
    imagePreview.style.display = 'none';
});
