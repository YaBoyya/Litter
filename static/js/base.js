let langs = new Map([ 
["New",        "#f3f36e"],
["Hot",        "#f36e6e"],
["Easy",       "#6ef36e"],
["Medium",     "#f3f36e"],
["Hard",       "#f36e6e"],
["E",          "#6ef36e"],
["M",          "#f3f36e"],
["H",          "#f36e6e"],

["C",          "#3949ab"],
["Bash",       "#4da725"],
["JavaScript", "#f0db4f"],
["TypeScript", "#007bcd"],
["Java",       "#5382a1"],
["Python",     "#3871a0"],
["C++",        "#004482"],
["C#",         "#3a0095"],
["Scala",      "#de3423"],
["Ruby",       "#ef0e13"],
["Lua",        "#010080"],
["PHP",        "#7c8cc6"],
["HTML",       "#e44d26"],
["CSS",        "#264ee4"]])

class Post {
  constructor(id, upvoted) {
    this.id = id
    this.upvoted = upvoted
  }
}

function delay(fn, ms) {
  let timer = 0
  return function(...args) {
    clearTimeout(timer)
    timer = setTimeout(fn.bind(this, ...args), ms || 0)
  }
}

class Comment {
  constructor(id, upvoted) {
    this.id = id
    this.upvoted = upvoted
  }
}

posts = []
comments = []

function popupSetState(state) {
  if(state) {
    document.getElementById("popup-background").style.visibility = "unset"
    for(div of document.getElementsByClassName("blur-on-popup")) {
      div.style.filter = "blur(5px)";
    }
    document.getElementById("popup").style.visibility = "unset"
  } else {
    document.getElementById("popup-background").style.visibility = "collapse"
    for(div of document.getElementsByClassName("blur-on-popup")) {
      div.style.filter = "none";
    }
    document.getElementById("popup").style.visibility = "collapse"
   for(child of document.getElementById("popup").children) {
     child.style.visiblity = "collapse"
     child.style.display = "none"
   }
  }
}

function setTagState(tag, state) {
  if (state) {
    tag.style.backgroundColor = getComputedStyle(tag).borderColor;
  } else {
    tag.style.backgroundColor = ""
  }
}

function selectTagE() {
  event.preventDefault()
  let tag = event.currentTarget
  let input = tag.getElementsByTagName("input")[0];
  let status = input.checked;
  if(input.getAttribute("type")==="radio") {
    radios = tag.parentNode.children
    for(li of radios) { setTagState(li, false) }
  }
  setTagState(tag, !status);
  input.checked = !status
}

function ajax(f, type, url) {
  const xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function () {
    if(xhttp.readyState == 4) {
      if(xhttp.status == 200) {
        f();
      } else {
        console.log("Error in", xhttp)
      }
    }
  };
  xhttp.open(type, url, true);
  xhttp.send();
}

function removeTagE() {
  let target = event.target
  let li = document.createElement("li")
  while(target.tagName != "LI")
    target = target.parentNode
  for(let child of target.children) {
    li.appendChild(child);
  }
  li.addEventListener("mousedown", searchPickTagE)
  li.checked = false
  initTag(li)
  let ul = target.parentNode.getElementsByClassName("popup-menu")[0]
  //TODO: Correct order insert
  ul.insertBefore(li, ul.firstChild)
  target.remove();
 }

function initTag(tag) {
  tag.style.borderColor = langs.get(tag.textContent.trim())
}

function initTags() {
  for(let ul of document.getElementsByClassName("tag-list")) {
    for (let li of ul.children) {
      initTag(li)
    }
  }
}

function refreshPopupMenu(menu) {
  let liList = Array.from(menu.getElementsByTagName("li"))
  let visible = liList.filter((x)=>getComputedStyle(x).visibility=="visible")
  for(let i=0;i<visible.length-1;i++) {
    visible[i].style.borderBottomColor = "var(--border-color)";
    visible[i].style.borderRadius = "0"
  }
  if(visible.length>1)
    visible[visible.length-1].style.borderRadius = "0 0 var(--radius) var(--radius)"
}

function initPopupMenus() {
  for(let m of document.getElementsByClassName("popup-menu")) {
    let liList = Array.from(m.getElementsByTagName("li"))
      .filter(x=>x.style.visibility!="collapse")
    for(let i=0;i<liList.length-1;i++) {
      liList[i].style.borderBottomColor = "var(--border-color)";
      liList[i].style.borderRadius = "0"
    }
    if(liList.length>1)
      liList[liList.length-1].style.borderRadius = "0 0 var(--radius) var(--radius)"
  }
  for(let ul of document.getElementsByClassName("popup-menu")) {
    for(let li of ul.getElementsByTagName("li")) {
      if(li.getElementsByTagName("input")[0].checked) {
        addTag(li)
      }
    }
  }
}

function styleTagSearch() {
  for(let n of document.getElementsByClassName("new-tag")) {
    for(let i of n.getElementsByClassName("popup-menu")) {
      refreshPopupMenu(i)
    }
  }
}

function showTagSearchE() {
  let li = event.target.parentNode.getElementsByClassName("new-tag")[0]
  let but = li.nextElementSibling
  li.style.visibility="visible"
  li.style.display="block"
  li.getElementsByTagName("input")[0].focus()
  let counter = 0
  but.style.visibility="collapse"
  but.style.display="none"
  for(li of li.getElementsByTagName("li")) {
    if(counter>4) {
      li.style.visibility="collapse"
      li.style.display="none"
    } else {
      li.style.visibility="visible"
      li.style.display="block"
      counter++;
    }
  }
  styleTagSearch()
}

function addTag(tag) {
  let li = document.createElement("li");
  for(let child of tag.children) {
    li.appendChild(child);
  }
  li.addEventListener("click", removeTagE)
  initTag(li)
  li.getElementsByTagName("input")[0].checked = true
  li.visibility = "visible"
  li.display = "block"
  let ul = tag.parentNode.parentNode.parentNode
  console.log(ul)
  let ulLis = ul.children
  ul.insertBefore(li, ulLis[ulLis.length-2])
  tag.remove()
}

function searchPickTagE() {
  let target = event.target
  while(target.tagName != "LI")
    target = target.parentNode
  addTag(target)
}

function collapseTagSearchE() {
  li = event.target.parentNode
  let but = li.nextElementSibling
  li.style.display="none"
  li.style.visibility="collapse"
  console.log(but)
  but.style.visibility="visible"
  but.style.display="block"
  li.getElementsByTagName("input")[0].value = ""
}

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

darkColors = [
  "#eeeeee", //border
  "#3e3ec3", //highlight
  "#ee0000", //important
  //base
  "#111111",
  "#333333",
  "#444444",
  "#555555",
  "#666666"
];

lightColors = [
  "#111111", //border
  "#9e9ef3", //highlight
  "#aa0000", //important
  //base
  "#eeeeee",
  "#bbbbbb",
  "#aaaaaa",
  "#999999",
  "#888888"
];

function setDarkMode(b) {
  var s = document.documentElement.style
  if(b) {
    for(let item of document.getElementsByClassName("dark-mode")) {
      item.style.filter = "invert()";
    }
    s.setProperty("--color-text", darkColors[0])
    s.setProperty("--color-border", darkColors[0])
    s.setProperty("--color-highlight", darkColors[1])
    s.setProperty("--color-important", darkColors[2])
    for(var i=0;i<5;i++) {
      s.setProperty("--color" + (i+1),
                                                 darkColors[i+3])
    }
  } else {
    for(let item of document.getElementsByClassName("dark-mode")) {
      item.style.filter = "unset";
    }
    s.setProperty("--color-text", lightColors[0])
    s.setProperty("--color-border", lightColors[0])
    s.setProperty("--color-highlight", lightColors[1])
    s.setProperty("--color-important", lightColors[2])
    for(var i=0;i<5;i++) {
      s.setProperty("--color" + (i+1),
                                                 lightColors[i+3])
    }
  }
}



function onLoad() {
  setDarkMode(false);
  if(typeof initFeed === "function") initFeed()
  initTags()
  initPopupMenus()
  for (let ul of document.getElementsByClassName("tag-list")) {
    if (ul.classList.contains("button-list")) {
      for (let li of ul.children) {
        if (li.firstElementChild instanceof HTMLInputElement) {
          li.addEventListener("click", selectTagE)
          if(li.firstElementChild.checked) {
            setTagState(li, true)
          }
        }
      }
    }
  }
}
