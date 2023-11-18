function searchTagE() {
  let text = event.target.value.toLowerCase()
  let list = event.target.parentNode.getElementsByTagName("ul")[0]
  for(let li of list.children) {
    if(!li.textContent.toLowerCase().includes(text)) {
      li.style.display = "none"
      li.style.visibility = "collapse"
    } else {
      li.style.display = "unset"
      li.style.visibility = "unset"
    }
    styleTagSearch()
  }
}

function collapseTagSearchE() {
  li = event.target.parentNode
  li.style.visibility="collapse"
  li.style.display="none"
  li.getElementsByTagName("input")[0].value = ""
  for(li of li.getElementsByTagName("li")) {
    li.style.visibility="unset"
    li.style.display="unset"
  }
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
  li.style.visibility="unset"
  li.style.display="unset"
  li.getElementsByTagName("input")[0].focus()
  styleTagSearch()
}

function styleTagSearch() {
  let liList =  Array.from(document.getElementById("new-post-new-tag")
           .getElementsByClassName("search-hint")[0].children)
           .filter(
             (x)=>x.style.visibility!="collapse" && x.style.visibility!="hidden")
  for(let i=0;i<liList.length-1;i++) {
    liList[i].style.borderBottomColor = "var(--border-color)";
    liList[i].style.borderRadius = "0"
    initTag(liList[i])
  }
  liList[liList.length-1].style.borderRadius = "0 0 var(--radius) var(--radius)"
}
