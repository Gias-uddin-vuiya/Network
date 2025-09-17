
const editContentBtn = document.querySelectorAll(".edit-content-btn")
let likeBtn = document.querySelectorAll(".like-btn")

editContentBtn.forEach((btn) => {
  btn.addEventListener('click', (evt) => {
    evt.preventDefault()
    // console.log("edit button clicked");

    // Find the post container
    const post = evt.target.closest(".post"); 
    // console.log(post)
    const content = post.querySelector(".post-content");

    // Create textarea and set the value to current content
    const textarea = document.createElement("textarea");
    textarea.className = "post-content-edit form-control";
    textarea.value = content.innerText;

    // Replace the content with textarea
    content.replaceWith(textarea);

    

    // add save btn after click the edit btn
    const saveBtn = document.createElement("button");
    saveBtn.innerText = "Save";
    saveBtn.type = "submit"
    saveBtn.className = "save-btn btn btn-primary";
    textarea.insertAdjacentElement("afterend", saveBtn);

    saveBtn.addEventListener("click", async () => {
        const updatedText = textarea.value;
        const postId = btn.dataset.set; // we stored post.id in data-set

        const response = await fetch(`/edit-post/${postId}/`, {
          method: "POST",
          headers: {
            "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
            "Content-Type": "application/x-www-form-urlencoded",
          },
          body: new URLSearchParams({ content: updatedText }),
        });

        const data = await response.json();
        if (data.success) {
          const newContent = document.createElement("p");
          newContent.className = "post-content";
          newContent.innerText = data.updated_content;

          textarea.replaceWith(newContent);
          saveBtn.remove();
        } else {
          alert(data.error || "Failed to update post.");
        }
      });
  });
});


// let defaultLike = 1;
// let likeCount = document.querySelectorAll(".like-count")
// // showing value
// likeCount.innerText = defaultLike


// likeBtn.forEach((btn) => {
//   btn.addEventListener('click', (evt) => {
//     evt.preventDefault()
//     defaultLike++
//     likeCount.innerText = defaultLike
//     console.log('click like btn')
//   })
// })