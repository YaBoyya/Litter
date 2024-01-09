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
      img.src = img.src.replace("upvote-clicked", "upvote");
    } else {
      img.src = img.src.replace("upvote", "upvote-clicked");
    }
  }
  ajax(UP, "GET", "/post/" + id + "/vote");
}

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

function showCommentCreate() {
  let cont =  document.getElementById("comment-create-container")
  if (cont != null) {
    cont.style.visibility = "visible"
    cont.style.display = "block"
    popupSetState(true)
  }
}
