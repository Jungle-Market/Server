const input = document.querySelector(".item-image");
const preview = document.querySelector(".preview");
const descBox = document.querySelector(".desc-box");

input.addEventListener("change", showImage);

function showImage() {
  //get input file
  const selectedFile = input.files[0];
  console.log(selectedFile);

  //reading file
  const reader = new FileReader();
  reader.readAsDataURL(selectedFile);

  //after load
  reader.onload = function(){
    descBox.innerHTML = "";
    preview.src = reader.result;
  }
}
