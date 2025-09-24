
const editContentBtn = document.querySelectorAll(".edit-content-btn")
const likeBtns = document.querySelectorAll(".like-btn")
const navItem = document.querySelectorAll(".nav-item")




// A variable to keep track of the currently active item
let activeItem = null;

navItem.forEach((item) => {
  item.addEventListener("click", function(evt) {
    evt.preventDefault();

    // Reset the style of the previously active item, if one exists
    if (activeItem) {
      activeItem.style.color = ""; 
      activeItem.style.fontWeight = ""; 
    }

    // Apply new styles to the currently clicked item
    evt.target.style.color = "#000";
    evt.target.style.fontWeight = "800";

    // Update the activeItem variable to reference the newly clicked item
    activeItem = evt.target;

    console.log(evt.target);
  });
});

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




//  Fronted React System.
likeBtns.forEach((btn) => {
  btn.addEventListener("click", async () => {
    const postId = btn.closest(".like-container").dataset.postId; // get post.id
    const countSpan = btn.closest(".like-container").querySelector(".like-count");

    const response = await fetch(`/post/${postId}/like/`, {
      method: "POST",
      headers: {
        "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
        "Content-Type": "application/x-www-form-urlencoded",
      },
    });

    const data = await response.json();

    if (response.ok) {
      countSpan.innerText = data.likes;

      // Toggle icon style (like/unlike)
      if (data.liked) {
        btn.classList.remove("fa-regular");
        btn.classList.add("fa-solid", "text-danger");
      } else {
        btn.classList.remove("fa-solid", "text-danger");
        btn.classList.add("fa-regular");
      }
    } else {
      alert(data.error || "Failed to update like.");
    }
  });
});

