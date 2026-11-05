from pathlib import Path

from flask import Flask, render_template, url_for


BASE_DIR = Path(__file__).resolve().parent
IMAGE_DIR = BASE_DIR / "static" / "images"
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
PHOTOS_PER_COLLAGE = 5

app = Flask(
    __name__,
    static_folder=str(BASE_DIR / "static"),
    static_url_path="/static",
    template_folder=str(BASE_DIR / "templates"),
)

MEMORIES = [
    {"from": "Sanvi", "message": "UHH MY FAV MEMORY IS DEFINITELY THE WAY WE USED TO SIT IN ALLEN CLASS AND JUDGE OTHER PEOPLES DOUBTS 😭 I COULD LITERALLY NEVER FORGET THOSE MOMENT", "tone": "yellow"},
    {"from": "Akriti", "message": "Girl I can't believe I am friends with such a diva like u 💃. Like literally everything about u amazes me. I miss ur random singing 🎤 and crashouts, the random deep conversations that never felt boring. I am so grateful for a friend like u who is so understanding and so fun 😘. And also stop looking so freaking cute all the time (leave some beauty for the rest of us 😜). Anyway I always love u bbg ❤️❤️❤️ Also a very very happy birthday always keep smiling 🥳", "tone": "rose"},
    {"from": "Reva", "message": "My fav memory with Riddhima i can't really point out just one she was such a light in my life with our gossip and her understanding me is such a deep level that i really can believe that i only know her for 2 yrs so, my fav memory with her is everyday i spent with her cause she just made it soo much better ✨", "tone": "mint"},
    {"from": "Sristi", "message": "And my fav memory of us is when we all were in the room and some guy was texting her very weirdly and we all were js making fun and texting him random shi and insulting him where we finally ended up blocking him , I think that was the funniest part 😭😂", "tone": "lavender"},
    {"from": "Harshithaa", "message": "Hhhheeeloo,call it fate or destiny ✨️ glad we ended up in the same class for 2 straight years! Instead of just picking 1 memory,id say every single time we chattered around in a gang of our own,during snacks ,ot just about playing hangman...they we're the best times with you💐keep slaying gurl 💅🥃", "tone": "peach"},
]


def discover_images():
    """Find every supported photo in static/images in a stable order."""
    if not IMAGE_DIR.exists():
        return []
    return sorted(
        (path.name for path in IMAGE_DIR.iterdir() if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS),
        key=str.casefold,
    )


@app.route("/")
def album():
    # Copy the constant so building a request never mutates the shared memory list.
    memories = list(MEMORIES)
    images = discover_images()
    slides = [{"kind": "cover"}]
    clusters = [images[i:i + PHOTOS_PER_COLLAGE] for i in range(0, len(images), PHOTOS_PER_COLLAGE)]
    note_after = {max(1, round(len(clusters) * (index + 1) / (len(memories) + 1))) for index in range(len(memories))}
    memory_index = 0

    for cluster_index, cluster in enumerate(clusters, start=1):
        slides.append({
            "kind": "collage",
            "number": cluster_index,
            "photos": [
                {"src": url_for("static", filename=f"images/{name}"), "name": name, "layout": photo_index}
                for photo_index, name in enumerate(cluster)
            ],
        })
        if cluster_index in note_after and memory_index < len(memories):
            slides.append({"kind": "note", **memories[memory_index]})
            memory_index += 1

    return render_template("index.html", slides=slides, photo_count=len(images))


if __name__ == "__main__":
    app.run(debug=True)
