
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
// -------x---------x-----------x//
const titleInput = document.getElementById('title');
const descInput = document.getElementById('description');
const imgInput = document.getElementById('imageUpload');
const previewTitle = document.getElementById('previewTitle');
const previewDesc = document.getElementById('previewDescription');
const previewImg = document.getElementById('previewImage');

titleInput.addEventListener('input', function () {
    previewTitle.textContent = this.value;
});

descInput.addEventListener('input', function () {
    previewDesc.textContent = this.value;
});

imgInput.addEventListener('change', function () {
    const file = this.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            previewImg.src = e.target.result;
            previewImg.style.display = 'block';
        }
        reader.readAsDataURL(file);
    } else {
        previewImg.src = '';
        previewImg.style.display = 'none';
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



