import streamlit as st
import json
import os


with open("pages/posts.json", "r") as file:
    posts_data = json.load(file)
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.switch_page("Account.py")
st.title("Connectify+")
st.subheader("Connect. Share. Belong.")
st.write(f"What's on your mind today, {st.session_state.name}?")
if st.button("Log out"):
    st.session_state.logged_in = False
    st.switch_page("Account.py")
st.divider()
image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
if image:
    st.image(image)
post_content = st.text_area("Description")
if st.button("Upload"):
    if post_content:
        if image:
            image_path = "pages/images/" + image.name

            with open(image_path, "wb") as file:
                file.write(image.getbuffer())
        new_post = {
            "id": len(posts_data["posts"]) + 1,
            "content": post_content,
            "image": image.name if image else None,
            "user": st.session_state.name,
            "likes": [],
            "comments": []
        }
        posts_data["posts"].append(new_post)
        with open("pages/posts.json", "w") as file:
            json.dump(posts_data, file)
        st.success("Post successfully uploaded!")
        st.rerun()
    else:
        st.error("Please enter a description.")
st.divider()
st.subheader("Posts:")
st.divider()
for post in posts_data["posts"]:
    st.write("### Post Creator:")
    st.write(post["user"])
    st.write("### Image:")
    if post["image"]:
        image_path = "pages/images/" + post["image"]
        st.image(image_path)
    else:
        st.text("No Image Selected")
    st.write("### Description:")
    st.write(post["content"])
    number_of_likes = len(post["likes"])
    st.write(f"### Like(s): {number_of_likes}")
    if st.session_state.name not in post["likes"]:
        if st.button("👍", key=f"like_{post['id']}"):
            post["likes"].append(st.session_state.name)
            with open("pages/posts.json", "w") as file:
                json.dump(posts_data, file)
            st.rerun()
    else:
        if st.button("👎", key=f"unlike_{post['id']}"):
            post["likes"].remove(st.session_state.name)
            with open("pages/posts.json", "w") as file:
                json.dump(posts_data, file)
            st.rerun()
    st.write("### Comments💬:")
    number_of_comments = len(post["comments"])
    st.write(f"Comment(s): {number_of_comments}")
    with st.expander("Show Comments"):
        if number_of_comments > 0:
            for comment in post["comments"]:
                st.write(comment["user"] + ":")
                st.write(comment["text"])
                st.divider()
        else:
            st.write("No comments yet")
    comment = st.text_area("Write a comment")
    if st.button("Post Comment💬", key=f"comment_button_{post['id']}"):
        if comment:
            post["comments"].append({
                "user": st.session_state.name,
                "text": comment
            })
            with open("pages/posts.json", "w") as file:
                json.dump(posts_data, file)
            st.rerun()
        else:
            st.error("Please enter something in order to post the comment")
    st.divider()
