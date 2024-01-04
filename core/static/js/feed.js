function postCreateShow() {
  document.getElementsByClassName("edit-post-container")[0].style.visibility = "visible"
  document.getElementsByClassName("edit-post-container")[0].style.display = "block"
  popupSetState(true)
}

function sortPopupE(state) {
  let parent = event.target.parentNode
  let menu = parent.getElementsByClassName("popup-menu")[0]
  let button = menu.parentNode.firstElementChild
  if(state) {
    menu.style.visibility = "visible"
    menu.style.display = "block"
    button.style.borderRadius = "var(--radius) var(--radius) 0 0"
  } else {
    menu.style.visibility = "collapse"
    menu.style.display = "none"
    button.style.borderRadius = "var(--radius)"
  }
}

function sortPopupInit() {
  let sort = document.getElementById("sort")
  let button = sort.firstElementChild
  let lis = sort.getElementsByClassName("popup-menu")[0].getElementsByTagName("li")
  button.textContent = button.textContent.charAt(0).toUpperCase() + button.textContent.slice(1)
  for(let li of lis) {
    if(li.textContent.trim()===button.textContent.trim()) {
      li.style.visibility = "collapse"
      li.style.display = "none"
    }
  }
}

function initFeed() {
  sortPopupInit()
}
