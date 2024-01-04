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

function upvoteCommentE(id, upvoted) {
  event.preventDefault()
  event.stopPropagation()
  let counter = event.target.parentNode
    .getElementsByClassName("comment-vote-count")[0];
  let img = counter.previousElementSibling;
  function UP() {
    index = comments.findIndex((x)=>x.id==id);
    if(index==-1) {
      change = upvoted;
      comments.push(new Comment(id,!upvoted));
    } else {
      change = comments[index].upvoted;
      comments[index].upvoted = !comments[index].upvoted;
    }
    counter.textContent = (change?-1:1)+Number(counter.textContent)
    if(change == 1) {
      img.src = img.src.replace("down", "up");
    } else {
      img.src = img.src.replace("up", "down");
    }
  }
  ajax(UP, "GET", "/comment/" + id + "/vote");
}

function upvotePostE(id, upvoted) {
  event.preventDefault()
  event.stopPropagation()
  let counter = event.target.parentNode
    .getElementsByClassName("post-vote-count")[0];
  let img = counter.previousElementSibling;
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
    if(change == 1) {
      img.src = img.src.replace("down", "up");
    } else {
      img.src = img.src.replace("up", "down");
    }
  }
  ajax(UP, "GET", "/post/" + id + "/vote");
}
