const dropZone = document.querySelector(".file-dropzone");
const dropText = dropZone.querySelector("header"),
button = document.querySelector(".browseBtn"),
input = dropZone.querySelector("input");
let file; 
console.log("HELLO");
button.onclick = () => {
    input.click();
}

input.addEventListener("change", function() {
    file = this.files[0];
    dropZone.classList.add("active");
    showFile();
})

// when file is over the drop zone
dropZone.addEventListener("dragover", (event) => {
    event.preventDefault();
    dropZone.classList.add("active");
    dropText.textContent = "Release to Upload File.";
})

// when file leaves the drop zone
dropZone.addEventListener("dragleave", () => {
    dropZone.classList.remove("active");
    dropText.textContent = "Drag & Drop to Uplaod File";
})

// when file is dropped on the drop zone
dropZone.addEventListener("drop", (event) => {
    event.preventDefault();
    file = event.dataTransfer.files[0];
    showFile();
})

function showFile() {
    let fileType = file.type;
    let validExtensions = ['image/jpeg', 'image/png', 'image/jpg'];
    if(validExtensions.includes(fileType)){
        let fileReader = new FileReader();
        fileReader.onload = () => {
            let fileURL = fileReader.result;
            let imgTag = `<img src="${fileURL}" alt="">`;
            dropZone.innerHTML = imgTag;
        }
        fileReader.readAsDataURL(file);
    } else {
        alert("File extension not supported\nValid extensions include: JPG/JPEG/PNG");
        dropeZone.classList.remove("active");
    }
}