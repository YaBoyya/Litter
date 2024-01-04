let langs = new Map([ 
  ["New", "#a0a000"],
  ["Hot", "#ff0000"],
  ["Easy", "#00ff00"],
  ["Medium", "#ffff00"],
  ["Hard", "#ff0000"],
  ["E", "#00ff00"],
  ["M", "#ffff00"],
  ["H", "#ff0000"],
  ["C", "#0000ff"],
  ["JavaScript", "#5E1DB8"],
  ["Java", "#C5D5E9"],
  ["Python", "#19125D"],
  ["Cpp", "#07CE0B"],
  ["Scheme", "#EAB738"],
  ["Scala", "#2AE44A"],
  ["Ruby", "#6305FD"],
  ["Lua", "#684D53"],
  ["Fortran", "#3F37C3"],
  ["Matlab", "#7148F2"],
  ["R", "#D994E9"]])

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
      child.style.visibility = "collapse"
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

function removeElement() {
  let id = event.target.id;
  event.target.remove();
  input = document.getElementById(id)
  document.getElementById(id).checked = false;
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
  li.style.visibility="visible"
  li.style.display="block"
  li.getElementsByTagName("input")[0].focus()
  let counter = 0
  console.log(li)
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

function searchPickTagE() {
  let li = document.createElement("li");
  li.textContent = event.target.textContent;
  let input = event.target.getElementsByTagName('input')
  let id = input[0].id
  document.getElementById(id).checked = true;
  li.addEventListener("click", removeElement)
  initTag(li)
  li.id = id
  let ul = document.getElementsByClassName("selectable-tag-list")[0]
  let ulLis = ul.children
  ul.insertBefore(li, ulLis[ulLis.length-2])
}

function collapseTagSearchE() {
  li = event.target.parentNode
  li.style.visibility="collapse"
  li.style.display="none"
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
  setDarkMode(Math.floor(Math.random()*2));
  if(initFeed) initFeed()
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
