
const editContentBtn = document.querySelectorAll(".edit-content-btn")


editContentBtn.forEach((btn) => {
  btn.addEventListener('click', (evt) => {
    evt.preventDefault()
    console.log("edit button clicked");

    // Find the post container
    const post = evt.target.closest(".post"); 
    console.log(post)
    const content = post.querySelector(".post-content");

    // Create textarea and set the value to current content
    const textarea = document.createElement("textarea");
    textarea.className = "post-content-edit form-control";
    textarea.value = content.innerText;

    // Replace the content with textarea
    content.replaceWith(textarea);

    

    // You can add a save button after editing
    const saveBtn = document.createElement("button");
    saveBtn.innerText = "Save";
    saveBtn.className = "save-btn btn btn-primary";
    textarea.insertAdjacentElement("afterend", saveBtn);

    saveBtn.addEventListener("click", () => {
      const newContent = document.createElement("p");
      newContent.className = "post-content";
      newContent.innerText = textarea.value;

      // Replace textarea back with updated content
      textarea.replaceWith(newContent);
      saveBtn.remove();
    });
  });
});



