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

function setSearchVisibilityE(val) {
  let button = document.getElementById("search-button")
  let inside = button.getElementsByTagName("a")[0]
  let input = document.getElementById("search-input")
  if(val) {
    inside.style.visibility="collapse"
    inside.style.display="none"
    input.style.visibility="unset"
    input.style.display="unset"
    input.focus();
  } else {
    inside.style.visibility="unset"
    inside.style.display="flex"
    input.style.visibility="collapse"
    input.style.display="none"
  }
}

function initFeed() {
  sortPopupInit()
}
