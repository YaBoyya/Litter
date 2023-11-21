function imgPopupE() {
  event.stopPropagation()
  var image = document.getElementById("popup-image")
  if(image === null) {
    image = document.createElement("img")
    let style = image.style
    image.id = "popup-image"
    style.position = "absolute"
    style.left = 0
    style.right = 0
    style.top = 0
    style.margin = "auto"
    style.width = "auto"
    style.height = "auto"
    style.maxHeight = "90vh"
    style.maxWidth = "90vw"
    document.getElementById("popup").appendChild(image)
  }
  image.src = event.target.src
  image.style.visibility = "visible"
  image.style.display = "block"
  popupSetState(true)
}
