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
      img.src = img.src.replace("upvote-clicked", "upvote");
    } else {
      img.src = img.src.replace("upvote", "upvote-clicked");
    }
  }
  ajax(UP, "GET", "/comment/" + id + "/vote");
}
