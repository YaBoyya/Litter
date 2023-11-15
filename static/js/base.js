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
  ["Javascript", "#5E1DB8"],
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

class Comments {
  constructor(id, upvoted) {
    this.id = id
    this.upvoted = upvoted
  }
}

posts = []
comments = []

function getRandomColor() {
  var letters = '0123456789ABCDEF'
  var color = '#'
  for (var i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)]
  }
  return color
}

function randomPalette() {
  let compStyle = getComputedStyle(document.documentElement, null)
  var diff = Array(3).fill(0).map(x => Math.floor(Math.random() * 25 + 25))
  var colors = (new Array(5)).fill(0).map(x => (new Array(3)))
  colors[0] = diff;
  for (var i = 1; i < 5; i++) {
    colors[i][0] = colors[i - 1][0] + diff[0]
    colors[i][1] = colors[i - 1][1] + diff[1]
    colors[i][2] = colors[i - 1][2] + diff[2]
  }
  for (var i = 1; i < 6; i++) {
    document.documentElement.style.setProperty("--color" + i.toString(),
      "#" +
      colors[i - 1][0].toString(16) +
      colors[i - 1][1].toString(16) +
      colors[i - 1][2].toString(16))
  }
}

function popupSetState(state) {
  if(state) {
    document.getElementById("popup").style.visibility = "unset"
    document.getElementById("popup-background").style.visibility = "unset"
    for(div of document.getElementsByClassName("blur-on-popup")) {
      div.style.filter = "blur(5px)";
    }
  } else {
    document.getElementById("popup").style.visibility = "hidden"
    document.getElementById("popup-background").style.visibility = "hidden"
    for(div of document.getElementsByClassName("blur-on-popup")) {
      div.style.filter = "none";
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

function selectTagE(e) {
  e.preventDefault()
  let tag = e.currentTarget
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

function upvoteCommentE(id, upvoted) {
  event.preventDefault()
  event.stopPropagation()
  let counter = event.target.parentNode
    .getElementsByClassName("comment-vote-count")[0];
  function UP() {
    index = comments.findIndex((x)=>x.id==id);
    if(index==-1) {
      change = upvoted;
      comments.push(new Post(id,!upvoted));
    } else {
      change = comments[index].upvoted;
      comments[index].upvoted = !comments[index].upvoted;
    }
    counter.textContent = (change?-1:1)+Number(counter.textContent)
  }
  ajax(UP, "GET", "/comment/" + id + "/vote");
}

function upvotePostE(id, upvoted) {
  event.preventDefault()
  event.stopPropagation()
  let counter = event.target.parentNode
    .getElementsByClassName("post-vote-count")[0];
  function UP() {
    index = posts.findIndex((x)=>x.id==id);
    if(index==-1) {
      change = upvoted;
      posts.push(new Post(id,!upvoted));
    } else {
      change = posts[index].upvoted;
      posts[index].upvoted = !posts[index].upvoted;
    }
    counter.textContent = (change?-1:1)+Number(counter.textContent)
  }
  ajax(UP, "GET", "/post/" + id + "/vote");
}

function removeElement() {
  event.target.remove();
}

function initTag(tag) {
  tag.style.borderColor = langs.get(tag.textContent)
}

function initTags() {
  for(let ul of document.getElementsByClassName("tag-list")) {
    for (let li of ul.children) {
      initTag(li)
    }
  }
}

function onLoad() {
  randomPalette()
  initTags()
  for (let ul of document.getElementsByClassName("tag-list")) {
    if (ul.classList.contains("button-list")) {
      for (let li of ul.children) {
        if (li.firstChild instanceof HTMLInputElement) {
          li.addEventListener("click", selectTagE)
          if(li.firstChild.checked) {
            setTagState(li, true)
          }
        }
      }
    }
  }
}
