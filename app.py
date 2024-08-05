from flask import Flask, render_template, request, redirect
from stories import Story
from flask_debugtoolbar import DebugToolbarExtension
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = "Orion"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

TEMPLATES = {"template1": "Once upon a time in a long-ago {place}, there lived a large {adjective} {noun}. It loved to {verb} {plural_noun}.",
             "template2": "Once upon a time there was a {occupation1} who wanted to {verb} a(n) {occupation2}; but she woul have to be a {adjective} {noun}.",
             "template3": "One evening a(n) {adjective} {noun1} came on; there was {noun2} and {noun3}, and the {noun4} poured down in torrents.",
             "template4": "In a village there once lived two {noun} who had the same {object}. They were both called {name}. One of them had four {animals}, but the other had only one.",
             "template5": "A long time ago, there lived an old {occupation}, a {adverb} {adjective} person. He really likes {fruit}."}
@app.route("/")
def test_home():
    return render_template("home_page.html", templates=TEMPLATES)

@app.route("/story-form")
def story_form():
    template_num = request.args["story-template"]
    template = TEMPLATES[template_num]
    prompts = get_prompts(template)
    return render_template("story_form.html", template=template, prompts=prompts, template_num=template_num)

@app.route("/read-story")
def read_story():
    story = Story(request.args.keys(), TEMPLATES[request.args["template"]])
    user_story = story.generate(request.args)
    return render_template("read_story.html", user_story=user_story)

def get_prompts(template):
    idx_start = [m.start() for m in re.finditer("{", template)]
    idx_stop = [m.start() for m in re.finditer("}", template)]
    prompts = [template[idx_start[i]+1:idx_stop[i]] for i in range(len(idx_start))]
    return prompts

@app.route("/add-story-form")
def add_story_form():
    return render_template("add_story_form.html")

@app.route("/add-story", methods=["POST"])
def add_story():
    story_text = request.form['story-text']
    TEMPLATES[f"template{len(TEMPLATES) + 1}"] = story_text
    return redirect('/')
