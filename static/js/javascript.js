let langs = {
  New: "#a0a000",
  Hot: "#ff0000",
  Easy: "#00ff00",
  Medium: "#ffff00",
  Hard: "#ff0000",
  C: "#0000ff",
  Javascript: "#5E1DB8",
  Java: "#C5D5E9",
  Python: "#19125D",
  Cpp: "#07CE0B",
  Scheme: "#EAB738",
  Scala: "#2AE44A",
  Ruby: "#6305FD",
  Lua: "#684D53",
  Fortran: "#3F37C3",
  Matlab: "#7148F2",
  R: "#D994E9"
}

class Post {
  constructor(postId, upvoted) {
    this.postId = postId
    this.upvoted = upvoted
  }
}

posts = []

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

function setTagState(tag, state) {
  if (state) {
    tag.style.backgroundColor = langs[tag.textContent]
  } else {
    tag.style.backgroundColor = ""
  }
}

function selectTag(e) {
  let tag = e.target
  let input = tag.getElementsByTagName("input")[0];
  let status = input.checked
  if(input.getAttribute("type")==="radio") {
    radios = tag.parentNode.getElementsByTagName("li")
    for(li of radios) { setTagState(li, false) }
  }
  setTagState(tag, !status);
  tag.getElementsByTagName("input")[0].checked = !status
}

function ajax(f, type, url) {
  const xhttp = new XMLHttpRequest();
  xhttp.onload = f;
  xhttp.open(type, url, true);
  xhttp.send();
}

function upvoteEvent(postId, upvoted) {
  let counter = event.target.parentNode
    .getElementsByClassName("post-vote-count")[0];
  function UP() {
    index = posts.findIndex((x)=>x.postId==postId);
    if(index==-1) {
      change = upvoted;
      posts.push(new Post(postId,!upvoted));
    } else {
      change = posts[index].upvoted;
      posts[index].upvoted = !posts[index].upvoted;
    }
    counter.textContent = (change?-1:1)+Number(counter.textContent)
  }
  ajax(UP, "GET", "post/" + postId + "/vote");
}

function onLoad() {
  //Add listener for tag checkboxes
  for (let ul of document.getElementsByClassName("tag-list")) {
    for (let li of ul.getElementsByTagName("li"))
      li.style.borderColor = langs[li.textContent]
    if (ul.classList.contains("button-list")) {
      for (let li of ul.getElementsByTagName("li")) {
        if (li.firstChild instanceof HTMLInputElement) {
          li.addEventListener("click", selectTag)
        }
      }
    }
  }
  randomPalette()
}
