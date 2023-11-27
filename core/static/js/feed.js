function searchTagE() {
  let timer = 0
  function real(event) {
    clearTimeout(timer)
    let text = event.target.value.toLowerCase()
    let list = event.target.parentNode.getElementsByTagName("ul")[0]
    var counter = 0;
    for(let li of list.children) {
      if(!li.textContent.toLowerCase().trim().startsWith(text) || counter>4) {
        li.style.display = "none"
        li.style.visibility = "collapse"
      } else {
        li.style.display = "block"
        li.style.visibility = "visible"
        counter++;
      }
      styleTagSearch()
    }
  }
  timer = setTimeout(real.bind(this,event), 150)
}

function collapseTagSearchE() {
  li = event.target.parentNode
  li.style.visibility="collapse"
  li.style.display="none"
  li.getElementsByTagName("input")[0].value = ""
}

function searchPickTagE() {
  let li = document.createElement("li");
  li.textContent = event.target.textContent;
  let input = event.target.getElementsByTagName('input')
  let id = input[0].id
  document.getElementById(id).checked = true;
  li.addEventListener("click", removeElement)
  initTag(li)
  li.id = id
  let ul = document.getElementsByClassName("edit-post-tag-list")[0]
  let ulLis = ul.children
  ul.insertBefore(li, ulLis[ulLis.length-2])
}

function showTagSearch() {
  let li = document.getElementsByClassName("edit-post-new-tag")[0]
  li.style.visibility="visible"
  li.style.display="block"
  li.getElementsByTagName("input")[0].focus()
  let counter = 0
  for(li of li.getElementsByTagName("li")) {
    if(counter>4) break;
    li.style.visibility="visible"
    li.style.display="block"
    counter++;
  }
  styleTagSearch()
}

function styleTagSearch() {
  for(let i of document.getElementsByClassName("edit-post-new-tag")[0]
    .getElementsByClassName("popup-menu")) {
    refreshPopupMenu(i)
  }
}

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
