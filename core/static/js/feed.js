function searchTagE() {
  let text = event.target.value.toLowerCase()
  let list = event.target.parentNode.getElementsByTagName("ul")[0]
  var counter = 0;
  for(let li of list.children) {
    if(!li.textContent.toLowerCase().includes(text) || counter>4) {
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
  let ul = document.getElementById("new-post-tag-list")
  let ulLis = ul.children
  ul.insertBefore(li, ulLis[ulLis.length-2])
}

function showTagSearch() {
  let li = document.getElementById("new-post-new-tag")
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
  let liList =  Array.from(document.getElementById("new-post-new-tag")
    .getElementsByClassName("search-hint")[0].getElementsByTagName("li"))
    .filter((x)=>getComputedStyle(x).visibility=="visible")
  for(let i=0;i<liList.length-1;i++) {
    liList[i].style.borderBottomColor = "var(--border-color)";
    liList[i].style.borderRadius = "0"
    initTag(liList[i])
  }
  if(liList.length>1)
    liList[liList.length-1].style.borderRadius = "0 0 var(--radius) var(--radius)"
}

function postCreateShow() {
  document.getElementById("new-post-container").style.visibility = "visible"
  document.getElementById("new-post-container").style.display = "block"
  popupSetState(true)
}
